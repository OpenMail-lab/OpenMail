#!/bin/bash
echo "🔹 Starting OpenMail microservices..."

python3 microservices/turtle-graphics/turtle_service.py &
python3 microservices/kiali-service/kiali_service.py &
python3 microservices/terraform-service/terraform_service.py &
python3 microservices/argocd-service/argocd_service.py &
python3 microservices/helm-service/helm_service.py &
python3 microservices/ansible-service/ansible_service.py &
python3 microservices/docker-service/docker_service.py &

echo "✅ All services running! Every user has full control."
