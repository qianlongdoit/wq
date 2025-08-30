import os
from src.utils.sign_in import sign_in

sess = sign_in()
print(sess)

if os.path.isfile('./simulation/progress.text'):
    print('isfile')
else:
    print('not file')