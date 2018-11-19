import flask
from flask import Flask, request, jsonify

import flask_cors
from flask_cors import CORS

import datetime
from datetime import datetime

def getutcnow():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


app = flask.Flask(__name__)
CORS(app)
# app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return jsonify(
        {
            'message': 'Welcome to the Python mock web api for Virtual Kubelet',
            'links': [
                { 'text': 'capacity',       'link': '/capacity'},
                { 'text': 'nodeConditions', 'link': '/nodeConditions'},
                { 'text': 'nodeAddresses',  'link': '/nodeAddresses'},
                { 'text': 'getPods',        'link': '/getPods'},
            ]
        }
    )

@app.route('/capacity', methods=['GET'])
def capacity():
    return jsonify(
        { 'cpu': '20', 'memory': '100Gi', 'pods': '20' }
    )

@app.route('/nodeConditions', methods=['GET'])
def nodeConditions():
    utcnow = getutcnow()
    return jsonify([
        { 
            'type': 'Ready',
            'status': 'True',
            'lastHeartbeatTime': utcnow,
            'lastTransitionTime': utcnow,
            'reason': 'KubeletReady',
            'message': 'At your service'
        }
        # TODO add more conditions
    ])

@app.route('/nodeAddresses', methods=['GET'])
def nodeAddresses():
    return jsonify([])

@app.route('/getPods', methods=['GET'])
def getPods():
    return jsonify([])

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='3000')

