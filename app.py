import flask
from flask import Flask, request, jsonify

import flask_cors
from flask_cors import CORS

import datetime
from datetime import datetime

def getutcnow():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

pods = []

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
    return jsonify(pods)

@app.route('/createPod', methods=['POST'])
def createPod():
    pod = request.json
    
    pod['status']['phase'] = 'Running'
    pod['status']['conditions'] = [
        { 'type': 'PodScheduled', 'status': 'True'},
        { 'type': 'Initialized', 'status': 'True'},
        { 'type': 'Ready', 'status': 'True'},
    ]
    container_statuses = []
    for container in pod['spec']['containers']:
        container_statuses.append({
            'name': container['name'],
            'image': container['image'],
            'ready': True,
            'state': {
                'running': {
                    'startedAt': getutcnow()
                }
            }
        })
    pod['status']['containerStatuses'] = container_statuses

    pods.append(pod)
    return ('', 200)

@app.route('/getPodStatus', methods=['GET'])
def getPodStatus():
    namespace = request.args.get('namespace')
    name = request.args.get('name')
    for pod in pods:
        if pod['metadata']['namespace'] == namespace and \
           pod['metadata']['name'] == name:
            return jsonify(pod['status'])
    return ('', 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port='3000')

