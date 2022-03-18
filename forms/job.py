from flask_wtf import FlaskForm
from wtforms import PasswordField, IntegerField, BooleanField, StringField, TextAreaField, \
    SubmitField, EmailField, DateTimeField
from wtforms.validators import DataRequired


class AddJob(FlaskForm):
    team_leader = IntegerField('TeamLeader', validators=[DataRequired()])
    job = StringField('Job', validators=[DataRequired()])
    work_size = IntegerField('Work_size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    end_date = DateTimeField('End time', validators=[DataRequired()])
    is_finished = BooleanField('Is finished')

    submit = SubmitField('Добавить')

class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    is_private = BooleanField("Личное")
    submit = SubmitField('Применить')