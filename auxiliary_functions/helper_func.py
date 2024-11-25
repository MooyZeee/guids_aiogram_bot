import json

admins_list_data = '/Users/mansur/Desktop/bot_checked_subscribes_andyes_send_video/database/admin_list.txt'
ansar_player_data = '/Users/mansur/Desktop/bot_checked_subscribes_andyes_send_video/database/players_list_db.txt'


def get_anonim(id):
    try:
        with open(f'{ansar_player_data}', 'r', encoding='utf-8') as file:
            # Читаем все строки и убираем пробелы
            data_id = {line.strip() for line in file if line.strip()}  # Используем множество
        return str(id) in data_id
    except FileNotFoundError:
        print(f"Файл {ansar_player_data} не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def write_user_id(id):
    with open(f'{ansar_player_data}', 'a', encoding='utf-8') as file:
        file.write(f'{id}\n')


def add_new_admin_db(add_admin_id):
    with open(f'{admins_list_data}', 'r', encoding='utf-8') as file:
        read_file = file.read()
        split_file = read_file.split('\n')
        if add_admin_id not in split_file:
            with open(f'{admins_list_data}', 'a', encoding='utf-8') as file2:
                file2.write(f'\n{add_admin_id}')
                return True

        elif add_admin_id in split_file:
            print('Такой пользователь уже существует!')
            return False

        else:
            # print('Возможно пользователь уже существует или введены некоректные данные.')
            print('Ошибка! 5534-235')
            return False


def remove_admin_from_db(admin_id):
    try:
        with open(f'{admins_list_data}', 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]

        if str(admin_id) in lines:
            lines.remove(str(admin_id))
            with open(f'{admins_list_data}', 'w', encoding='utf-8') as file:
                file.write('\n'.join(lines))
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Файл '{admins_list_data}' не найден.")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def checked_admin_list():
    with open(f'{admins_list_data}', 'r', encoding='utf-8') as file2:
        file_read = file2.readlines()
        file_split = [int(line.strip()) for line in file_read if line.strip()]

        return file_split


def _writer_group_to_json(data, filename='groups.json'):
    try:
        # Читаем существующие данные
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # Проверяем, существует ли группа с таким же username
    for group in existing_data:
        if group['username'] == data['username']:
            return False  # Возвращаем False, если дубликат найден

    # Добавляем новые данные
    existing_data.append(data)

    # Сохраняем обновленные данные
    with open(filename, 'w', encoding='utf-8') as g:
        json.dump(existing_data, g, indent=4)

    return True


def _remove_group_from_json(username, filename='groups.json'):
    try:
        # Читаем json файл
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        return False  # Файл не найден, возвращаем False

    # Ищем группу с указанным username
    for group in existing_data:
        if group['username'] == username:
            existing_data.remove(group)  # Удаляем группу
            # Сохраняем обновленные данные
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=4)
            return True  # Возвращаем True, если группа была успешно удалена

    return False  # Возвращаем False, если группа с таким username не найдена


def load_from_json(filename='groups.json'):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_all_user():
    with open(f'{ansar_player_data}', 'r', encoding='utf-8') as file:
        get_all_player = file.readlines()
        split_player = [line.strip() for line in get_all_player if line.strip()]
        return split_player



# def checked_groups_db():
#     with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#         file_read = file.read()
#         file_split = file_read.split('\n')
#
#         return file_split
#
#
# def add_group_db(group_name):
#     with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#         file_read = file.read()
#         file_split = file_read.split('\n')
#         if group_name not in file_split:
#             with open(f'{database_groups_file}', 'a', encoding='utf-8') as file2:
#                 file2.write(f'\n{group_name}')
#                 return True
#
#         elif group_name in file_split:
#             return False
#
#         else:
#             print('Ошибка 77356-211')
#             return False
#
#
# def remove_group_db(group_name):
#     try:
#         with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#             lines = [line.strip() for line in file.readlines()]
#
#         if group_name in lines:
#             lines.remove(group_name)
#             with open(f'{database_groups_file}', 'w', encoding='utf-8') as file:
#                 file.write('\n'.join(lines))
#             return True
#         else:
#             return False
#     except FileNotFoundError:
#         print(f"Файл '{database_groups_file}' не найден.")
#         return False
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return False
#
#
# def read_group_file():
#     try:
#         keyboard = []
#         with open(f'{database_groups_file}', 'r', encoding='utf-8') as file:
#             file_read = file.read()
#             file_split = file_read.split('\n')
#             for i in file_split:
#                 keyboard.append([InlineKeyboardButton(text=f'{i}', url=f'https://t.me/{i}')])
#
#             keyboard_list = InlineKeyboardMarkup(inline_keyboard=keyboard)
#             return keyboard_list
#
#     except Exception as e:
#         print(f'Ошибка типа: {e} - (9990-0001)')
