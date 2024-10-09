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

# Create data base
with app.app_context():
    db.create_all()

# Run app
app.run(debug=True)