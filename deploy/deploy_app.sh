#!/bin/bash
echo "Building docker image.\n" 
echo ""
echo ""
echo ""

cd ../
docker build -t app_deploy .

cd deploy/
echo "Create kubernetes deployment.\n" 
echo ""
echo ""
echo ""
kubectl apply -f deploy_msg_service.yaml
kubectl apply -f deploy_arango_service.yaml