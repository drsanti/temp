from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/HELLO')
def hello():
    return 'Hello, World'
