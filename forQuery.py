from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime


def global_init(argmt):
    return db_session.global_init(argmt)


def create_session():
    return db_session.create_session()


def main():
    global_init(input())
    db_sess = create_session()
    users = db_sess.query(User).filter(User.age < 21, User.address == 'module_1').all()

    for user in users:
        user.address = 'module_3'
    db_sess.commit()


if __name__ == '__main__':
    main()
