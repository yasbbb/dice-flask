import flask
import random
from dieroll import roll, evaluate
from flask import request, jsonify
from flask_cors import CORS


app  = flask.Flask(__name__)
app.config['DEBUG'] = False
cors = CORS(app)

@app.route('/', methods=['GET'])
def home():
    return flask.render_template('layout.html')

@app.route('/roll', methods=['GET', 'POST'])
def roll():
    if request.method == 'GET':
        rollequation = ''
        if 'eq' in request.args:
            rollequation = str(request.args['eq'])

        res = evaluate(rollequation)
        return jsonify(res)
    
    req = request.get_json()
    rollequation = req['equation']
    res = evaluate(rollequation)

    return jsonify(res)

@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'

# app.run()