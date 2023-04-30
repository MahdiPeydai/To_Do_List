import json


def get_username(user_id):
    with open('../To_Do_List/To_Do_List/data/users_information.json', 'r+') as information_file:
        information = json.load(information_file)

    for user_info in information:
        if user_info['user_id'] == user_id:
            user_name = user_info['user_name']
            break
    return user_name
