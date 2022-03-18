from flask_restful import reqparse, abort, Api, Resource, reqparse
from flask import Flask, render_template, redirect, make_response, jsonify, request, abort
from data import db_session
from data.jobs import Jobs

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('is_published', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)


def abort_if_news_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"News {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        return jsonify({'news': job.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, job_id):
        abort_if_news_not_found(job_id)
        session = db_session.create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = Jobs(
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
            is_published=args['is_published'],
            is_private=args['is_private']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})
