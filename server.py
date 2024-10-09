from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self, arg):
        return {'x': arg}

api.add_resource(HelloWorld, '/<string:arg>')


app.run(debug=True)