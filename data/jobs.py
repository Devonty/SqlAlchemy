import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"),
                                    nullable=True)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.datetime.now)
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)

    leader = orm.relation('User')

    def __repr__(self):
        return f"<Job> {self.job}"
