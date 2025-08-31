import os
import json


def write_file(config):
    directory = config['directory']
    file_name = config['file_name']
    data = config['data']
    is_append = config.get('is_append', True)

    # 检查目录是否存在
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"{file_name}")

    with open(file_path, 'w' if not is_append else 'a') as f:
        json.dump(data, f)
        f.write('\n')
