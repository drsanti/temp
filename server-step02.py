from flask import Flask, abort
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

class Task(Resource):
  def get(self, task_id):
    if task_id is 0:
      return {'id': 0, 'name': 'Sleep'}
    elif task_id is 1:
      return {'id': 1, 'name': 'Eat'}
    else:
      abort(404, description="404 Task not found")


class Tasks(Resource):
  def get(self):
    return [{'id': 0, 'name': 'Sleep'},{'id': 1, 'name': 'Eat'}]

api.add_resource(Tasks, '/')
api.add_resource(Task, '/<int:task_id>')
