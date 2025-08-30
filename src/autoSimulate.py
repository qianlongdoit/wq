import json
import os
import random
from time import sleep
from src.utils.get_datafields import get_datafields
from src.utils.gen_template import gen_template
from src.utils.sign_in import sign_in
from src.utils.write_file import write_file

from src.utils.send_template import send_template

template = []



if not os.path.isfile('./simulation/fundamental6_template.json'):
    data_field = get_datafields(dataset_id='fundamental6')
    data_field = data_field['id'].values
    template = gen_template(fields=data_field)
    print('write template')
    write_file(config={
        'directory': './simulation',
        'data': template,
        'file_name': 'fundamental6_template.json'
    })
else:
    template = json.load(open('./simulation/fundamental6_template.json'))


progress = 0

if os.path.isfile('./simulation/progress.text'):
    print('read progress')
    with open('./simulation/progress.text', 'r', encoding='utf-8') as f:
        progress = f.read()
        print(f'progress.text is {progress}')

def write_progress(progress, alpha):
    write_file(config={
        'directory': './simulation',
        'data': progress,
        'file_name': 'progress.text',
        'is_append': False
    })
    print(f'now progress is {progress}, alpha is {alpha}')


def success(index, alpha):
    write_file(config={
        'directory': './simulation',
        'data': alpha,
        'file_name': 'res.text'
    })
    write_progress(progress=index, alpha=alpha)


def fail(index, alpha):
    write_progress(index, alpha=alpha)

#
# def send_template(alpha_list, sess, success, fail, start=0):
#     alpha_fail_attempt_tolerance = 3  # 每个alpha允许的最大失败尝试次数
#
#     print('begin send template')
#     if success is None:
#         def default_success(data):
#             print(data)
#             return
#
#         success = default_success
#     if fail is None:
#         def default_success(data):
#             print(data)
#             return
#
#         fail = default_success
#
#     print(f'{len(alpha_list)}, start{start}')
#     for index, alpha in enumerate(alpha_list, start=start):
#         keep_trying = True  # 控制while循环继续的标志
#         failure_count = 0  # 记录失败尝试次数的计数器
#
#         while keep_trying:
#             num = random.random()
#
#             if num > 0.8:
#                 keep_trying = False  # 成功获取位置，退出while循环
#                 # print(f'Alpha is: {alpha}')  # 打印位置
#                 print(f'{num}, Alpha is: {alpha}')  # 打印位置
#                 success(index, alpha)
#
#             else:
#                 sleep(1.2)
#                 failure_count += 1  # 增加失败尝试次数
#
#                 # 检查失败尝试次数是否达到容忍上限
#                 if failure_count >= alpha_fail_attempt_tolerance:
#                     fail(index, alpha)
#                     failure_count = 0  # 重置失败尝试次数
#                     print(
#                         f"{alpha} no location for too many times, move to next alpha {alpha}")  # 打印信息
#                     break  # 退出while循环，移动到for循环中的下一个alpha



sess = sign_in()


send_template(
    alpha_list=template,
    start=int(progress),
    sess=sess,
    success=success,
    fail=fail
)
