#!/bin/bash

kubectl apply -f k8s/deployments/streamlit-deployment.yaml
kubectl apply -f k8s/services/streamlit-service.yaml
kubectl apply -f k8s/ingress/ingress.yaml
