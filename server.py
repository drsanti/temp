
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task.db'
db = SQLAlchemy(app)

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name):
        self.name = name

# Handles multiple tasks (e.g., GET / for all tasks)
class Tasks(Resource):
    def get(self):
        tasks = TaskModel.query.all()
        return [{'id': task.id, 'name': task.name} for task in tasks]  # Serialize tasks as a list of dicts

    def post(self):
        data = request.json
        task = TaskModel(name=data['name'])
        db.session.add(task)
        db.session.commit()
        tasks = TaskModel.query.all()
        return [{'id': task.id, 'name': task.name} for task in tasks]  # Serialize tasks as a list of dicts

# Handles a single task (e.g., GET /<task_id> for one task)
class Task(Resource):
    def get(self, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            return {'id': task.id, 'name': task.name}
        else:
            return {'message': 'Task not found'}, 404

    def delete(self, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': 'Task deleted successfully'}
        else:
            return {'message': 'Task not found'}, 404

    def put(self, task_id):
        data = request.json
        task = TaskModel.query.get(task_id)
        if task:
            task.name = data['name']
            db.session.commit()
            return {'id': task.id, 'name': task.name}
        else:
            return {'message': 'Task not found'}, 404

def init_database():
    with app.app_context():
        db.create_all()

# if __name__ == '__main__':
#     init_database()
#     api.add_resource(Tasks, '/')
#     api.add_resource(Task, '/<int:task_id>')
#     app.run(debug=True)

init_database()
api.add_resource(Tasks, '/')
api.add_resource(Task, '/<int:task_id>')
app.run(debug=True)