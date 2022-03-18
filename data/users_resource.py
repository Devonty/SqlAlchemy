from flask_restful import reqparse, abort, Api, Resource, reqparse
from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from data import db_session
from data.jobs import Jobs
from data.users import User
from data.user_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict(
            only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'hashed_password'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'modified_date')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            name=args['name'],
            surname=args['surname'],
            email=args['email'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            hashed_password=args['hashed_password'],
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
