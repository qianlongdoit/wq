import os
import aiohttp
import requests
from requests.auth import HTTPBasicAuth
from aiohttp import BasicAuth


def read_config(file_path="../env.text"):
    """
    读取配置文件的第一行和第二行内容。
    :param file_path: 配置文件路径，默认为 env.txt
    :return: 包含第一行和第二行内容的元组 (line1, line2)
    """
    # 获取当前脚本所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 计算配置文件的绝对路径（拼接当前目录和相对路径）
    abs_file_path = os.path.normpath(os.path.join(current_dir, file_path))
    try:
        with open(abs_file_path, 'r') as file:
            line1 = file.readline().strip()
            line2 = file.readline().strip()
            return line1, line2
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {abs_file_path} 不存在")
    except Exception as e:
        raise Exception(f"读取文件时发生错误: {e}")


def sign_in():
    # Load credentials # 加载凭证
    credentials = read_config()

    # Extract username and password from the list # 从列表中提取用户名和密码
    username, password = credentials
    # print(username, password)
    # Create a session object # 创建会话对象
    sess = requests.Session()

    # Set up basic authentication # 设置基本身份验证
    sess.auth = HTTPBasicAuth(username, password)

    # Send a POST request to the API for authentication # 向API发送POST请求进行身份验证
    response = sess.post('https://api.worldquantbrain.com/authentication')

    # Print response status and content for debugging # 打印响应状态和内容以调试
    # print(response.status_code)
    # print(response.json())
    return sess


async def get_sync_session(sess: requests.Session):
    cookie_jar = aiohttp.CookieJar()
    header = None
    auth = None

    if sess.cookies:
        for cookie in sess.cookies:
            cookie_jar.update_cookies({cookie.name: cookie.value})

    if sess.headers:
        header = sess.headers

    if hasattr(sess, 'auth') and sess.auth:
        # 处理HTTPBasicAuth类型的认证
        if isinstance(sess.auth, HTTPBasicAuth):
            username = sess.auth.username
            password = sess.auth.password
            auth = BasicAuth(username, password)

    sync_sess = aiohttp.ClientSession(
        cookie_jar=cookie_jar,
        headers=header,
        auth=auth
    )

    return sync_sess
