from time import sleep
import logging
import os
import json
from src.utils.sign_in import sign_in


# 从 ../simulation 目录下读取全部文件，文件格式为[{},{} ]，其中{}为一个alpha表达式，打印每个alpha表达式
def read_alpha_files():
    alpha_list = []
    pathname_str = '../simulation'
    for file in os.listdir(pathname_str):
        if file.endswith('.json'):
            with open(os.path.join(pathname_str, file), 'r') as f:
                alphas = json.load(f)
                # 换行打印每个alpha表达式
                for alpha in alphas:
                    alpha_list.append(alpha)
    return alpha_list


alpha_list = read_alpha_files()


# 从 ../simulationRes/index.text 读取文件
def read_simulation_res_files():
    res_list = []
    pathname_str = '../simulationRes/index.text'
    try:
        with open(pathname_str, 'r') as res:
            for r in res:
                res_list.append(r)
    except Exception as e:
        logging.error(f"Error reading simulation results: {str(e)}")
        print(f"Error reading simulation results: {str(e)}")
    return res_list


res_list = read_simulation_res_files()


# 在 ../simulationRes/index.text append 当前alpha的
def append_simulation_res_files(alpha):
    pathname_str = '../simulationRes/index.text'
    try:
        with open(pathname_str, 'a') as f:
            json.dump(alpha, f)
            f.write('\n')
        logging.info(f"Wrote alpha to results: {alpha['regular']}")
        print(f"Wrote alpha to results: {alpha['regular']}")
    except Exception as e:
        logging.error(f"Error writing simulation result: {str(e)}")
        print(f"Error writing simulation result: {str(e)}")

alpha_fail_attempt_tolerance = 15  # 每个alpha允许的最大失败尝试次数

sess = sign_in()

for alpha in alpha_list:
    keep_trying = True  # 控制while循环继续的标志
    failure_count = 0  # 记录失败尝试次数的计数器
    # 检查是否已经存在结果
    if any(alpha['regular'] in res for res in res_list):
        logging.info(f"Alpha already exists in results: {alpha['regular']}")
        continue

    while keep_trying:
        try:
            # 尝试发送POST请求
            sim_resp = sess.post(
                'https://api.worldquantbrain.com/simulations',
                json=alpha  # 将当前alpha（一个JSON）发送到服务器
            )

            # 从响应头中获取位置
            sim_progress_url = sim_resp.headers['Location']
            logging.info(f'Alpha location is: {sim_progress_url}')  # 记录位置
            print(f'Alpha location is: {sim_progress_url}')  # 打印位置
            append_simulation_res_files(alpha)
            keep_trying = False  # 成功获取位置，退出while循环

        except Exception as e:
            logging.error(f"No Location, sleep 15 and retry, error message: {str(e)}")
            print("No Location, sleep 15 and retry")
            sleep(10)
            failure_count += 1  # 增加失败尝试次数

            # 检查失败尝试次数是否达到容忍上限
            if failure_count >= alpha_fail_attempt_tolerance:
                sess = sign_in()  # 重新登录会话
                failure_count = 0  # 重置失败尝试次数
                logging.error(f"No location for too many times, move to next alpha {alpha['regular']}")  # 记录错误
                print(f"No location for too many times, move to next alpha {alpha['regular']}")  # 打印信息
                append_simulation_res_files(alpha)
                break  # 退出while循环，移动到for循环中的下一个alpha
