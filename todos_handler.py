import json
import os
from datetime import datetime
from typing import List


def get_filename() -> str:
    file: str = 'todos.json'
    while not os.path.exists(file):
        file = os.path.abspath(input(f'Файла {file} не существует. '
                                     f'Введите имя фала или путь к нему: '))
    return file


def load_data_from_file(path: str) -> List[dict]:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def cut_title(title: str) -> str:
    return title if len(title) <= 50 else title[:50] + '...'


def get_tasks_by_users_id(tasks_list: List[dict]) -> dict:
    tasks_by_users_id = {}
    for task in tasks_list:
        try:
            user_id = task['userId']
            title = cut_title(task['title'])
            is_task_completed = task['completed']
        except KeyError as e:
            print(f'Ошибка, в задаче не указаны некоторые поля: {e}')
        else:
            if user_id not in tasks_by_users_id.keys():
                tasks_by_users_id[user_id] = {'completed': [],
                                              'uncompleted': []}

            if is_task_completed:
                tasks_by_users_id[user_id]['completed'].append(title)
            else:
                tasks_by_users_id[user_id]['uncompleted'].append(title)
    return tasks_by_users_id


def write_tasks_in_files(users_task: dict):
    for key, value in users_task.items():
        user_filename: str = f'{key}_{datetime.now().strftime("%Y-%m-%dT%H-%M")}.txt'
        with open(user_filename, 'w') as file:
            file.write(f'# Сотрудник №{key}\n'
                       f'{datetime.now().strftime("%d.%m.%Y %H:%M")}\n')
            file.write('\n## Завершённые задачи:\n')
            file.writelines("%s\n" % line for line in value['completed'])
            file.write('\n## Оставшиеся задачи:\n')
            file.writelines("%s\n" % line for line in value['uncompleted'])


if __name__ == '__main__':
    filename = get_filename()
    data = load_data_from_file(filename)
    tasks = get_tasks_by_users_id(data)
    write_tasks_in_files(tasks)
