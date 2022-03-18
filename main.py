'''make_samlple_db - на создание капитана, 3-участнков и работы'''
from flask_restful import reqparse, abort, Api, Resource, reqparse
from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from data import db_session, jobs_api
from data.jobs_resource import JobsListResource, JobsResource
from data.users_resource import UsersResource, UsersListResource
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm, LoginForm
from forms.job import AddJob
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

# для списка объектов
api.add_resource(JobsListResource, '/api/v2/jobs')

# для одного объекта
api.add_resource(JobsResource, '/api/v2/jobs/<int:job_id>')

# для списка объектов
api.add_resource(UsersListResource, '/api/v2/users')

# для одного объекта
api.add_resource(UsersResource, '/api/v2/users/<int:user_id>')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    jobs = db_sess.query(Jobs).all()
    names = {user.id: [user.name, user.surname] for user in users}
    return render_template("index.html", names=names, jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/index")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJob()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # Проверка на существование лидера
        leader = db_sess.query(User).filter(User.id == form.team_leader.data).first()
        if not leader:
            return render_template('add_job.html',
                                   message="Обозначен несуществующий лидер.",
                                   form=form)

        # Проверка на существование участников
        members_id = list(map(int, form.collaborators.data.split(',')))
        members = db_sess.query(User).filter(User.id.in_(members_id)).all()
        if len(members) != len(members_id):
            return render_template('add_job.html',
                                   message="Обозначены несуществующие участники.",
                                   form=form)
        # Все хорошо
        job = Jobs(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            end_date=form.end_date.data,
            is_finished=form.is_finished.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = AddJob()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.team_leader == current_user.id
                                          ).first()
        if jobs:
            form.title.data = jobs.title
            form.content.data = jobs.content
            form.is_private.data = jobs.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(jobs).filter(jobs.id == id,
                                          jobs.user == current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_samlple_db(db_sess):
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


def main():
    db_session.global_init("db/with_jobs.db")
    db_sess = db_session.create_session()
    app.register_blueprint(jobs_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
