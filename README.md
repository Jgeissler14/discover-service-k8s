# discover-service-k8s
An implementation of the discover web service on k8s

# Developer Setup and Workflow
When working within k8s this is how you can assure you have the proper developer environment set up for contribution to this repository.

## Prerequisites
1. Rancher Desktop installed (https://docs.rancherdesktop.io/getting-started/installation/)
2. kubectl CLI Tool installed (https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/)
3. helm CLI Tool installed (https://helm.sh/docs/intro/install/)


### Using Rancher Distribution as OS

    Use the cli command `docker info` to check the operating system of docker daemon. For this project we want to have the OS be `Operating System: Rancher Desktop WSL Distribution`

If this is not the OS, then:
    
        1. Open Rancher Desktop
        2. Select Kubernetes Settings
        3. Select `dockerd` bullet

## Build the Docker Image

        1. docker build . -t discover-service:0.0.1
        2. docker run -it -p 127.0.0.1:3000:3000 discover-service:0.0.1


## Install helm chart for local container deployment

 > helm install -f deploy/kubernetes/discover/Chart.yaml discover-service ./deploy/kubernetes/discover/

 To update helm chart after code changes

 > helm upgrade discover-service -f deploy/kubernetes/discover/values.yaml deploy/kubernetes/discover/

## Check if pods are running in kubernetes environment

 > kubectl get pods -A

## Port Forward the pod with the discover service for UI
 > 1. export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=discover,app.kubernetes.io/instance=discover-service" -o jsonpath="{.items[0].metadata.name}")
 >
 > 2. export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
 >
 > 3. kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
