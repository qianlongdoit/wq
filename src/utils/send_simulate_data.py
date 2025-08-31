from __future__ import annotations

import asyncio
import logging

import aiohttp
import re
import time
from typing import Callable, Optional, Tuple, Any
from src.utils.write_file import write_file


def send_simulation_data(sess, data, success=None, fail=None):
    """
    发送模拟数据并获取结果
    :param sess: 会话对象
    :param data: 模拟数据
    :param success: 成功回调函数
    :param fail: 失败回调函数
    """

    regular = data.get('regular')
    try:
        response = sess.post(
            'https://api.worldquantbrain.com/simulations',
            json=data
        )

        location = response.headers.get('Location')

        if not location:
            fail(regular)
            logging.warning(f'任务失败: 未在响应头中找到Location信息，当前任务为 {regular}')
            return None

        match = re.search(r'simulations/(.*)', location)

        if not match:
            fail(regular)
            logging.warning(f'任务失败: 未在 Location 中找到 alpha id，当前任务为 {regular}')
            return None

        location_id = match.group(1)

        progress_url = f'https://api.worldquantbrain.com/simulations/{location_id}'
        timeout_seconds = 240  # 4分钟超时
        start_time = time.time()

        while True:
            # 检查是否超时
            if time.time() - start_time > timeout_seconds:
                fail(regular)
                logging.warning(f'任务超时: 超过{timeout_seconds}秒未完成，当前任务为 {regular}')
                return None

            cur_progress_res = sess.get(progress_url)
            cur_progress_data = cur_progress_res.json()

            status = cur_progress_data.get('status')

            if status == 'COMPLETE':
                # 成功跳出循环
                break

            # 运行日志
            print(f"任务进度 {cur_progress_res.json().get('progress')}, 任务状态 status 是 {status}，任务是{regular}")
            time.sleep(4.5)

        alpha = cur_progress_res.json().get('alpha')

        if success:
            success(alpha, regular)
        print(f'任务成功, regular: {regular}，location_id: {location_id}')
        return alpha, regular

    except Exception as e:
        logging.warning(f'任务失败: regular:{regular}，error is{e}')
        if fail:
            fail(regular)
        return None


async def send_simulation_data_sync(
        sess: aiohttp.ClientSession,
        data: dict,
        success: Optional[Callable] = None,
        fail: Optional[Callable] = None
) -> Tuple[Any, Any] | None:
    regular = data.get('regular')

    try:
        # 异步发送POST请求
        async with sess.post(
                'https://api.worldquantbrain.com/simulations',
                json=data
        ) as response:
            if response.status == 429:
                time.sleep(90)  # 429, message='Too Many Requests 等待90秒
            location = response.headers.get('Location')

            if not location:
                logging.warning("未在响应头中找到 Location 信息")
                write_file(config={
                    'directory': './simulation',
                    'data': f'{regular}\n',
                    'file_name': 'progress.text',
                })
                return


            # 提取simulation ID
            match = re.search(r'simulations/(.*)', location)
            if not match:
                raise ValueError(f"无法从Location提取ID: {location}")
            location_id = match.group(1)

        # 轮询获取进度（带超时控制）
        progress_url = f'https://api.worldquantbrain.com/simulations/{location_id}'
        timeout_seconds = 240  # 4分钟超时
        start_time = time.time()

        while True:
            # 检查是否超时
            if time.time() - start_time > timeout_seconds:
                logging.warning(f"请求超时，超过{timeout_seconds}秒未完成")
                fail(data.get('regular'), f"请求超时，超过{timeout_seconds}秒未完成")
                return

            # 异步获取进度
            async with sess.get(progress_url) as progress_res:
                # progress_res.raise_for_status()  # 检查HTTP错误
                progress_data = await progress_res.json()  # 异步解析JSON

            status = progress_data.get('status')
            if status == 'COMPLETE':
                break

            print(f"progress is {progress_data.get('progress')}, regular is {regular}")
            # 等待4秒后重试（使用异步sleep）
            await asyncio.sleep(6)

        alpha = progress_data.get('alpha')

        if success:
            success(regular, alpha)
        print(f'任务成功, regular: {regular}')
        return alpha, regular

    except Exception as e:
        print(f'任务失败, regular is {regular}, error is {str(e)}')
        if fail:
            fail(regular, e)
        await sess.close()
        return None
