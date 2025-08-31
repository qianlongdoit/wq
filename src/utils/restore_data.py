import os


def restore_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path1 = os.path.normpath(os.path.join(current_dir, '../simulation/progress.text'))
    path2 = os.path.normpath(os.path.join(current_dir, '../simulation/res.text'))

    progress = None

    if os.path.isfile(path1):
        with open(path1, 'r', encoding='utf-8') as f:
            content = f.read()
            progress = content.rstrip('\n') if content else None
            # print(f'progress.text is {progress}')

    if progress is None:
        with open(path2, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            progress = lines[-1].rstrip('\n') if lines else None

    # print(f'progress is {progress}')
    return progress[1:-1]
