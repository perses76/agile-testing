import os
from urllib import request
import json


URL = 'https://test.com/new_user'


def save_new_user():
    # input
    body = request.urlopen(url=URL).read().decode('utf-8')
    user_data = json.loads(body)

    # transformation
    user_data['username'] = user_data['username'].capitalize()

    # output
    path = os.path.join('db', 'users.txt')
    with open(path, 'a') as f:
        f.write('"{}", "{}"\n'.format(
            user_data['username'], user_data['email'])
        )

    return True
