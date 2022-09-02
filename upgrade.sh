#! /usr/bin/bash
docker build . -t local/discover-service:0.0.1
helm upgrade discover-service -f deploy/kubernetes/discover/values.yaml deploy/kubernetes/discover/
export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=discover,app.kubernetes.io/instance=discover-service" -o jsonpath="{.items[0].metadata.name}")
kubectl --namespace default port-forward $POD_NAME 3000:3000
