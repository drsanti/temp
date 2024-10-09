from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

# Create app and config db.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"

# Create db and initialize
db = SQLAlchemy(app)

# Data model
class TaskModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable=False)

  def __init__(self, name):
      self.name = name
      

# Create data base (run this code to create db, then comment it out)
# with app.app_context():
#     db.create_all()

# ------------------------------------------------------

# API
api = Api(app)

class Task(Resource):
    def get(self, task_id):
        task = TaskModel.query.get(task_id)
        if task:
            return task.name
        else:
            return {"error": "not found!"}
        
    def post(self):
        task = TaskModel("Eat")
        # to be continue....

# Run app
app.run(debug=True)
api.add_resource(Task, "/<int:task_id>")