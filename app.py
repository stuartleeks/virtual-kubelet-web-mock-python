import flask
from flask import Flask, request, jsonify

import flask_cors
from flask_cors import CORS

import datetime
from datetime import datetime

import os

def getutcnow():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

pods = []
def getPod(namespace, name):
    for pod in pods:
        if pod['metadata']['namespace'] == namespace and \
           pod['metadata']['name'] == name:
            return pod
    return None

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
        },
        { 
            'type': 'OutOfDisk',
            'status': 'False',
            'lastHeartbeatTime': utcnow,
            'lastTransitionTime': utcnow,
            'reason': 'KubeletHasSufficientDisk',
            'message': 'Plenty of disk space here'
        },
        { 
            'type': 'MemoryPressure',
            'status': 'False',
            'lastHeartbeatTime': utcnow,
            'lastTransitionTime': utcnow,
            'reason': 'KubeletHasSufficientMemory',
            'message': 'Plenty of memory here'
        },
        { 
            'type': 'DiskPressure',
            'status': 'False',
            'lastHeartbeatTime': utcnow,
            'lastTransitionTime': utcnow,
            'reason': 'KubeletHasNoDiskPressure',
            'message': 'At your service'
        },
        { 
            'type': 'NetworkUnavailable',
            'status': 'False',
            'lastHeartbeatTime': utcnow,
            'lastTransitionTime': utcnow,
            'reason': 'RouteCreated',
            'message': 'Cables all intact'
        },
    ])

@app.route('/nodeAddresses', methods=['GET'])
def nodeAddresses():
    kubelet_port = os.environ.get('KUBELET_PORT')
    kubelet_pod_ip = os.environ.get('VKUBELET_POD_IP')
    if kubelet_pod_ip == None:
        print ('NodeAddresses - returning emtpy list')
        return jsonify([])
    else:
        print('NodeAddresses - returning InternalIP ' + kubelet_pod_ip)
        return jsonify([
            {
                'type': 'InternalIP',
                'address': kubelet_pod_ip
            }
        ])

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
    pod = getPod(namespace, name)
    if pod != None:
        return jsonify(pod['status'])
    return ('', 404)

@app.route('/deletePod', methods=['DELETE'])
def deletePod():
    pod = request.json
    namespace = pod['metadata']['namespace']
    name = pod['metadata']['name']
    matchingPod = getPod(namespace, name)
    if matchingPod != None:
        pods.remove(matchingPod)
        return ('', 200)
    return ('', 404)

@app.route('/getContainerLogs', methods=['GET'])
def getContainerLogs():
    namespace = request.args.get('namespace')
    pod_name = request.args.get('podName')
    container_name = request.args.get('containerName')

    pod = getPod(namespace, pod_name)

    if pod == None:
        return ('No such pod', 404)

    for container in pod['spec']['containers']:
        if container['name'] == container_name:
            return "Simulated log content for {}, {}, {}\nIf this provider actually ran the containers then the logs would appear here ;-)\n".format(namespace, pod_name, container_name)

    return ('No such container', 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port='3000')

