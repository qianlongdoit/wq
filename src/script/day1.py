import asyncio
import json
import logging
import os
from src.utils.get_datafields import get_data_fields
from src.utils.sign_in import sign_in
from src.utils.write_file import write_file
from src.utils.sign_in import get_sync_session
from src.utils.execute_req import execute_requests
from src.config.simulation_setting_config import gen_simulation_config
from src.utils.send_simulate_data import send_simulation_data_sync

# 策略模板 rank(factor1/factor2)

STRATEGY_TEMPLATE_NAME = 'RANK(A_DIVIDE_B)'
template = []
data_base_id = 'fundamental6'

STORAGE_PATH = f'../simulation/{STRATEGY_TEMPLATE_NAME}'


def get_template_data(database_id):
    """
    检查模板文件是否存在，如果不存在，则生成模板
    :param file_name: 文件名
    :param database_id: 数据库ID
    :return: 模板
    """
    res = []

    file_name = 'template.json'

    if not os.path.isfile(f'{STORAGE_PATH}/{file_name}'):
        data_field = get_data_fields(dataset_id=database_id)
        data_field = data_field['id'].values
        for factor1 in data_field:
            for factor2 in data_field:
                if factor1 == factor2:
                    continue
                res.append(f'rank({factor1}/{factor2})')

        write_file(config={
            'directory': STORAGE_PATH,
            'data': res,
            'file_name': file_name
        })
    else:
        res = json.load(open(f'{STORAGE_PATH}/{file_name}'))

    return res


template = get_template_data(database_id=data_base_id)

sess = sign_in()


def restore_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.normpath(os.path.join(current_dir, f'{STORAGE_PATH}/progress.text'))
    path2 = os.path.normpath(os.path.join(current_dir, f'{STORAGE_PATH}/res.text'))

    progress = ''

    if os.path.isfile(path2):
        with open(path2, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            progress = lines[-1].rstrip('\n') if lines else None

    if os.path.isfile(path1):
        with open(path1, 'r', encoding='utf-8') as f:
            content = f.read()
            progress = content.rstrip('\n') if content else None

    # print(f'progress is {progress}')
    return progress[1:-1]


async def main():
    rest_data = template.copy()
    progress = template.index(restore_data()) if restore_data() in template else 0

    if progress:
        rest_data = template[int(progress) + 1]
        logging.log(logging.INFO, f'上次完成的进度是{progress}')
    else:
        rest_data = template

    logging.log(logging.INFO, f'当前进度{len(rest_data)}， 剩余{len(template) - progress}，总共{len(template)}')

    def on_success(regular):
        write_file(config={
            'directory': STORAGE_PATH,
            'data': regular,
            'file_name': 'progress.text',
            'is_append': False
        })

    def on_fail(regular):
        write_file(config={
            'directory': f'./simulation/{STRATEGY_TEMPLATE_NAME}',
            'data': regular,
            'file_name': 'fail.text',
        })

    async def req(alpha):
        config = gen_simulation_config(alpha)
        sync_session = await get_sync_session(sess)
        await send_simulation_data_sync(data=config, sess=sync_session, success=on_success, fail=on_fail)

    await execute_requests(req=req, data_list=rest_data, concurrency=3)


asyncio.run(main())
