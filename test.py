import requests
import datetime
import json

url = 'http://localhost:5000/api/'
GET = False
POST = True
DELETE = False
# GET
if GET:
    get_all_ = requests.get(url + "jobs")
    print(*get_all_)
    get_one_ = requests.get(url + "jobs/1")
    print(*get_one_)
    get_error_id_ = requests.get(url + "jobs/-1")
    print(*get_error_id_)
    get_error_string_ = requests.get(url + "jobs/string")
    print(*get_error_string_)
# POST
if POST:
    params = json.dumps({
        'team_leader': 1,
        'job': "job",
        'work_size': 5,
        'collaborators': "2,3",
        'is_finished': False,
    })
    post_correct = requests.post(url + "jobs", json=params)
    print(post_correct.url)
    print(*post_correct)