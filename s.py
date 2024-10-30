
from flask import Flask, abort, request
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)
 
task_db =  [
  {'id': 0, 'name': 'Sleep'},
  {'id': 1, 'name': 'Eat'},
  {'id': 2, 'name': 'Work'},
  {'id': 3, 'name': 'Play'},
]


class TaskModel():
  id = 99999
  name = 'hello'

  def __init__(self, id, name):
    self.id = id
    self.name = name

class Task(Resource):
  def get(self, task_id):
    if task_id < 0 or task_id >= len(task_db):
      abort(404, description="404 Task not found")
    return task_db[task_id]


  def delete(self, task_id):
    # Check if task_id is valid
    if task_id < 0 or task_id >= len(task_db):
        abort(404, description="404 Task not found")
    
    # Remove the task
    deleted_task = task_db.pop(task_id)
    
    # Return success message
    return {'message': f"Task '{deleted_task['name']}' deleted successfully"}, 200

  def put(self, task_id):
    if task_id < 0 or task_id >= len(task_db):
        abort(404, description="404 Task not found")
    
    # The new task data is sent as JSON format in the request body
    data = request.get_json()

    # Update the task in task_db
    task_db[task_id]['name'] = data.get('name', task_db[task_id]['name'])

    return {'message': f"Task '{task_db[task_id]['name']}' updated successfully"}, 200


class Tasks(Resource):
  def get(self):
    return task_db
  
  def post(self):
    data = request.get_json()

    if not data or 'name' not in data:
        abort(400, description="Invalid task data")

    new_task = {
        'id': task_db[-1]['id'] + 1 if task_db else 1, 
        'name': data['name']
    }

    task_db.append(new_task)

    return new_task, 201


api.add_resource(Tasks, '/')
api.add_resource(Task, '/<int:task_id>')