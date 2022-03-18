import requests
import datetime
import json

url = 'http://localhost:5000/api/v2/'
user_id = -1
email = 'email@email'

POST = True
GET = True
DELETE = True

# POST
if POST:
    params = {
        'surname': 'surname',
        'name': "name",
        'age': 5,
        'position': "position",
        'speciality': 'speciality',
        'address': 'address',
        'email': email,
        'hashed_password': 'hashed_password',
    }
    print('Параметры:', params)
    post_correct = requests.post(url + "users", params=params)
    print('Ссылка: ', post_correct.url)
    print('Ответ: ', post_correct.json())

# GET
if GET:
    # Инфа обо всех
    get_all_ = requests.get(url + "users").json()
    print('Люди:', get_all_)

    # Ищу id добавленного в POST
    for user in get_all_['users']:
        if user['email'] == email:
            user_id = user['id']
    # ----------------

    # Информация о добавленном пользователе
    get_one_ = requests.get(url + f"users/{user_id}").json()
    print('Наш чел:', get_one_)

# DELETE
if DELETE:
    # удаляю пользователя
    get_one_ = requests.delete(url + f"users/{user_id}").json()
    print("Удаление:", get_one_)
