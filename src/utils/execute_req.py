import asyncio
from typing import List, Callable, Any, Awaitable


async def execute_requests(
        req: Callable[[Any, Callable, Callable], Awaitable],
        data_list: List[Any],
        concurrency: int = 3,
) -> None:
    """
    并发处理请求队列，适配带会话的请求函数

    参数:
        req: 请求处理函数（如send_simulation_data）
        data_list: 待请求的数据列表
        concurrency: 最大并发数量
    """
    semaphore = asyncio.Semaphore(concurrency)

    async def progress_data(data):
        async with semaphore:
            try:
                await req(data)
            except Exception as e:
                print(f'execute_requests error: {e}')
                raise
    tasks = [progress_data(data) for data in data_list]
    await asyncio.gather(*tasks)

