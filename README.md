# Virtual Kubelet Web Provider Python Mock Implementation
This project is a sample API implementation for the [Virtual Kubelet](https://github.com/virtual-kubelet/virtual-kubelet) [web provider](https://github.com/virtual-kubelet/virtual-kubelet/tree/master/providers/web) written in Python

This API simply stores the a list of the pods that it has been requested to create, marks them as started and serves up their status

```
+----------------+         +---------------------------+          +------------------------------+
|                |         |                           |   HTTP   |                              |
|   Kubernetes   | <-----> |   Virtual Kubelet: Web    | <------> |   This sample/mock API       |
|                |         |                           |          |                              |
+----------------+         +---------------------------+          +------------------------------+
```

## Running locally for development

To run the API locally, run `flask run --host 0.0.0.0 --port 3000`

## Connecting the API with Virtual Kubelet locally

To connect Virtual Kubelet to the API, set the `WEB_ENDPOINT_URL` environment variable to `http://localhost:3000/` (or whatever you have exposed the API as)

```bash
export WEB_ENDPOINT_URL=http://localhost:3000/
```

Then run `virtual-kubelet` with the `--provider web` switch. This will run Virtual Kubelet on your local machine. It will connect to Kubernetes based on the kubectl config, and connect to the API defined in the `WEB_ENDPOINT_URL` environment variable

## Visualising the API state

You can use `kubectl` commands to query running pods, but you can also run [Virtual Kubelet Web UI](https://github.com/stuartleeks/virtual-kubelet-web-ui) to connect to the API directly and show details of the running pods and their status.
