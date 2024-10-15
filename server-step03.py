


from flask import Flask, abort
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

task_db =  [
  {'id': 0, 'name': 'Sleep'},
  {'id': 1, 'name': 'Eat'},
  {'id': 2, 'name': 'Work'},
  {'id': 3, 'name': 'Play'}
]

class Task(Resource):
  def get(self, task_id):
    if task_id < 0 or task_id >= len(task_db):
      abort(404, description="404 Task not found")
    return task_db[task_id]


class Tasks(Resource):
  def get(self):
    return task_db

api.add_resource(Tasks, '/')
api.add_resource(Task, '/<int:task_id>')
