import json

PATH = 'todos.json'


def load_data_from_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def cut_title(title: str):
    if len(title) <= 50:
        return title
    else:
        return title[:50] + '...'


def get_users_id(tasks_list):
    tasks_by_users_id = {}
    for task in tasks_list:
        try:
            user_id = task['userId']
        except KeyError:
            print('Ошибка обработки задачи, не указан User Id')
        else:
            if user_id not in tasks_by_users_id.keys():
                tasks_by_users_id[user_id] = {'completed': [], 'uncompleted': []}

            title = cut_title(task['title'])
            if task['completed']:
                tasks_by_users_id[user_id]['completed'].append(title)
            else:
                tasks_by_users_id[user_id]['uncompleted'].append(title)
    return tasks_by_users_id


if __name__ == '__main__':
    data = load_data_from_file(PATH)
    # print(data)
    users_id_dict = get_users_id(data)
    print(users_id_dict)
