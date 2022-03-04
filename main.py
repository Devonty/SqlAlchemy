from flask import Flask, render_template, redirect, make_response
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    jobs = db_sess.query(Jobs).all()
    names = {user.id: [user.name, user.surname] for user in users}
    return render_template("index.html", names=names, jobs=jobs)

def main():
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()

    # очистка
    db_sess.query(User).delete()
    db_sess.query(Jobs).delete()
    db_sess.commit()
    # лидер
    user = User()
    user.name = "Ridley"
    user.surname = "Scott"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    db_sess.add(user)
    db_sess.commit()

    # остальные
    for i in range(1, 3 + 1):
        user = User()
        user.name = "name" + str(i)
        user.surname = "surname" + str(i)
        user.age = 21 + i
        user.position = "captain" + str(i)
        user.speciality = "research engineer" + str(i)
        user.address = "module_1" + str(i)
        user.email = "mail" + str(i) + "@mars.org"
        db_sess.add(user)
        db_sess.commit()
    # работы
    job = Jobs()
    job.team_leader = 1
    job.job = 'deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now
    job.is_finished = False

    db_sess.add(job)
    db_sess.commit()

    app.run()


if __name__ == '__main__':
    main()
