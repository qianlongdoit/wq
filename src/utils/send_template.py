from time import sleep
from src.utils.sign_in import sign_in
from src.config.simulation_config import gen_simulation_config

def send_template(alpha_list, sess, success, fail, start=0):
    alpha_fail_attempt_tolerance = 15  # 每个alpha允许的最大失败尝试次数

    if success is None:
        def default_success(data):
            print(data)
            return
        success = default_success
    if fail is None:
        def default_success(data):
            print(data)
            return
        fail = default_success


    for index, alpha in enumerate(alpha_list, start=start):
        keep_trying = True  # 控制while循环继续的标志
        failure_count = 0  # 记录失败尝试次数的计数器

        while keep_trying:
            try:
                sim_resp = sess.post(
                    'https://api.worldquantbrain.com/simulations',
                    json=gen_simulation_config(alpha)  # 将当前alpha（一个JSON）发送到服务器
                )

                # 从响应头中获取位置
                sim_progress_url = sim_resp.headers['Location']
                print(f'Alpha location is: {sim_progress_url}')  # 打印位置
                keep_trying = False  # 成功获取位置，退出while循环
                success(index, alpha)

            except Exception as e:
                # 处理异常：记录错误，让程序休眠15秒后重试
                print(f"{alpha} is no Location, sleep 10 and retry")
                sleep(10)  # 休眠15秒后重试
                failure_count += 1  # 增加失败尝试次数

                # 检查失败尝试次数是否达到容忍上限
                if failure_count >= alpha_fail_attempt_tolerance:
                    fail(index, alpha)
                    sess = sign_in()  # 重新登录会话c
                    failure_count = 0  # 重置失败尝试次数
                    print(f"{alpha} no location for too many times, move to next alpha {alpha}")  # 打印信息
                    break  # 退出while循环，移动到for循环中的下一个alpha