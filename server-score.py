from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///score.db'
db = SQLAlchemy(app)

class TaskModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float, nullable=False)

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return f"<Task(id={self.id}, name={self.name}, score={self.score})>"

# Handles multiple tasks (e.g., GET / for all tasks)
class Tasks(Resource):
    def get(self):
        tasks = TaskModel.query.all()
        return [{'id': task.id, 'name': task.name, 'score': task.score} for task in tasks]  # Include 'score'

    def post(self):
        data = request.json
        task = TaskModel(name=data['name'], score=data['score'])
        db.session.add(task)
        db.session.commit()
        tasks = TaskModel.query.all()
        return [{'id': task.id, 'name': task.name, 'score': task.score} for task in tasks]  # Include 'score'

# Handles a single task (e.g., GET /<task_id> for one task)
class Task(Resource):
    def get(self, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            return {'id': task.id, 'name': task.name, 'score': task.score}
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
            task.score = data['score']  # Update score as well
            db.session.commit()
            return {'id': task.id, 'name': task.name, 'score': task.score}
        else:
            return {'message': 'Task not found'}, 404

def init_database():
    with app.app_context():
        db.create_all()

init_database()
api.add_resource(Tasks, '/')
api.add_resource(Task, '/<int:task_id>')
app.run(debug=True)
