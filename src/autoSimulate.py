import json
import os
import random
from time import sleep
from src.utils.get_datafields import get_data_fields
from src.utils.gen_template import gen_template
from src.utils.sign_in import sign_in
from src.utils.write_file import write_file

from src.utils.send_template import send_template

template = []

data_base_id = 'analyst4'



if not os.path.isfile(f'./simulation/{data_base_id}_template.json'):
    data_field = get_data_fields(dataset_id=data_base_id)
    data_field = data_field['id'].values
    template = gen_template(fields=data_field)
    print('write template')
    write_file(config={
        'directory': './simulation',
        'data': template,
        'file_name': f'{data_base_id}_template.json'
    })
else:
    template = json.load(open(f'./simulation/f{data_base_id}_template.json'))


progress = 0

if os.path.isfile(f'./simulation/{data_base_id}_progress.text'):
    print('read progress')
    with open(f'./simulation/{data_base_id}_progress.text', 'r', encoding='utf-8') as f:
        progress = f.read()
        print(f'progress.text is {progress}')

def write_progress(progress, alpha):
    write_file(config={
        'directory': './simulation',
        'data': progress,
        'file_name': f'{data_base_id}_progress.text',
        'is_append': False
    })
    print(f'now progress is {progress}, alpha is {alpha}')


def success(index, alpha):
    write_file(config={
        'directory': './simulation',
        'data': alpha,
        'file_name': f'{data_base_id}_res.text'
    })
    write_progress(progress=index, alpha=alpha)


def fail(index, alpha):
    write_progress(index, alpha=alpha)

sess = sign_in()


send_template(
    alpha_list=template,
    start=int(progress),
    sess=sess,
    success=success,
    fail=fail
)
