import asyncio
import json

from src.utils.sign_in import sign_in, get_sync_session
from src.config.simulation_setting_config import gen_simulation_config
from src.utils.send_simulate_data import send_simulation_data_sync
from src.utils.execute_req import execute_requests
from src.utils.write_file import write_file
from src.utils.restore_data import restore_data

sess = sign_in()
print(f'login success, session is {sess}')


data = json.load(open('./simulation/fundamental6_template.json', 'r'))


async def main():
    sync_session = await get_sync_session(sess)
    progress = data.index(restore_data())
    rest_data = []

    if progress:
        rest_data = data[int(progress):]
        print(f'rest data is {progress}')
    else:
        rest_data = data

    print(f'total data is {len(data)}, last index is {len(data) - len(rest_data)}')

    def on_success(index, alpha):
        write_file(config={
            'directory': './simulation',
            'data': alpha,
            'file_name': 'res.text'
        })
        write_file(config={
            'directory': './simulation',
            'data': alpha,
            'file_name': 'progress.text',
            'is_append': False
        })

    def on_fail(index, alpha):
        write_file(config={
            'directory': './simulation',
            'data': alpha,
            'file_name': 'progress.text',
            'is_append': False
        })

    async def req(alpha):
        config = gen_simulation_config(alpha)
        await send_simulation_data_sync(data=config, sess=sync_session, success=on_success, fail=on_fail)

    await execute_requests(req=req, data_list=rest_data, concurrency=3)


asyncio.run(main())
