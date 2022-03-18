import requests
import datetime
import json

url = 'http://localhost:5000/api/v2/'

# Константы. Вкл/Выкл проверки ресурсов работы и пользователей.
JOBS = True
USERS = True

if JOBS:
    POST = True
    GET = True
    DELETE = True

    job_id = -1
    params = {
        'team_leader': 1,
        'job': "name_job",
        'work_size': 5,
        'collaborators': "2, 3",
        'is_finished': True
    }

    # POST
    if POST:
        print('Параметры:', params)
        post_correct = requests.post(url + "jobs", params=params)
        print('Ссылка: ', post_correct.url)
        print('Ответ: ', post_correct.json())

        # НЕККОРЕКТНЫЕ
        post_uncorrect = requests.post(url + "jobs")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.post(url + "jobs", params={'job': 'lol'})
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)

    # GET
    if GET:
        # Инфа обо всех
        get_all_ = requests.get(url + "jobs").json()
        print('Работы:', get_all_)

        # Ищу id добавленного в POST
        for job in get_all_['jobs']:
            # Ищу
            for param in params:
                if job[param] != params[param]:
                    break
            else:
                # Нашел
                job_id = job['id']

        # ----------------

        # Информация о добавленной работе
        get_one_ = requests.get(url + f"jobs/{job_id}").json()
        print('Наша работа:', get_one_)

        # НЕККОРЕКТНЫЕ
        post_uncorrect = requests.get(url + "jobs/-1")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.get(url + "jobs/12312321")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.get(url + "jobs/aboba")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)

        # DELETE
        if DELETE:
            # Удаляю работу
            get_one_ = requests.delete(url + f"jobs/{job_id}").json()
            print("Удаление:", get_one_)

            # НЕККОРЕКТНЫЕ
            post_uncorrect = requests.delete(url + "jobs/-1")
            print('НЕККОРЕКТНЫЙ', *post_uncorrect)
print()

# USERS
if USERS:
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

        # НЕККОРЕКТНЫЕ
        post_uncorrect = requests.post(url + "users")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.post(url + "users", params={'name': 'lol'})
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
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

        # НЕККОРЕКТНЫЕ
        post_uncorrect = requests.get(url + "users/-1")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.get(url + "users/12312321")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
        post_uncorrect = requests.get(url + "users/aboba")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)

    # DELETE
    if DELETE:
        # удаляю пользователя
        get_one_ = requests.delete(url + f"users/{user_id}").json()
        print("Удаление:", get_one_)

        # НЕККОРЕКТНЫЕ
        post_uncorrect = requests.delete(url + "users/-1")
        print('НЕККОРЕКТНЫЙ', *post_uncorrect)
