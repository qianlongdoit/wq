import requests
from requests.auth import HTTPBasicAuth

def read_config(file_path="../src/env.txt"):
    """
    读取配置文件的第一行和第二行内容。
    :param file_path: 配置文件路径，默认为 env.txt
    :return: 包含第一行和第二行内容的元组 (line1, line2)
    """
    try:
        with open(file_path, 'r') as file:
            line1 = file.readline().strip()
            line2 = file.readline().strip()
            return line1, line2
    except FileNotFoundError:
        raise FileNotFoundError(f"文件 {file_path} 不存在")
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
