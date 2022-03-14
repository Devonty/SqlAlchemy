from data import db_session
from data.users import User
from data.jobs import Jobs
from data.department import Department
import datetime


def global_init(argmt):
    return db_session.global_init(argmt)


def create_session():
    return db_session.create_session()


def main():
    global_init(input())
    db_sess = create_session()
    department = db_sess.query(Department).filter(Department.id == 1).first()
    members_id_list = list(map(int, department.members.split(',')))

    members = db_sess.query(User).filter(User.id.in_(members_id_list)).all()

    for user in members:
        jobs = db_sess.query(Jobs).filter((Jobs.id == user.id) | (Jobs.collaborators.like(
            f'% {user.id},%')) | (Jobs.collaborators.like(f'% {user.id}'))).all()

        job_size = 0
        for job in jobs:
            job_size += job.work_size

        if job_size > 25:
            print(user.surname, user.name)


if __name__ == '__main__':
    main()
