from datetime import datetime
import os
import json
from src.utils.get_datafields import get_datafields

data_field=get_datafields(dataset_id='fundamental6')
data_field=data_field['id'].values

alpha_list = []


print(data_field)

for x in data_field:
    print(f"正在将如下Alpha表达式与setting封装")
    for y in data_field:
        if x == y:
            continue
    alpha_expression = f"group_rank({x}/{y}, subindustry)"
    print(alpha_expression)
    simulation_data = {
        'type': 'REGULAR',
        'settings': {
            'instrumentType': 'EQUITY',
            'region': 'USA',
            'universe': 'TOP3000',
            'delay': 1,
            'decay': 0,
            'neutralization': 'SUBINDUSTRY',
            'truncation': 0.08,
            'pasteurization': 'ON',
            'unitHandling': 'VERIFY',
            'nanHandling': 'ON',
            'language': 'FASTEXPR',
            'visualization': False,
        },
        'regular': alpha_expression
    }

    alpha_list.append(simulation_data)

    # 写入 simulation_data 到 ./simulation/{timeStamp}.json

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    directory = './simulation'
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, f"{timestamp}.json")

    with open(file_path, 'w') as f:
        json.dump(alpha_list, f)