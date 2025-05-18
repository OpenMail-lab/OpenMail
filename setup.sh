#!/bin/bash
echo "🔹 Installing OpenMail & all DevOps tools..."

# ✅ Automatically setup Podman, Minikube, Helm, ArgoCD
mkdir /app/devops-tools
curl -LO https://github.com/redhat-developer/podman/releases/latest/podman-linux.tar.gz
curl -LO https://github.com/kubernetes/minikube/releases/latest/minikube-linux.tar.gz
curl -LO https://get.helm.sh/helm-latest-linux-amd64.tar.gz
curl -LO https://github.com/argoproj/argo-cd/releases/latest/argo-cd-linux.tar.gz

tar -xzf podman-linux.tar.gz -C /app/devops-tools
tar -xzf minikube-linux.tar.gz -C /app/devops-tools
tar -xzf helm-latest-linux-amd64.tar.gz -C /app/devops-tools
tar -xzf argo-cd-linux.tar.gz -C /app/devops-tools

# ✅ Start everything automatically
export PATH="/app/devops-tools:$PATH"
podman machine start
minikube start --network-plugin=cni --disable-driver-mounts
helm repo add openmail https://openmail-lab.github.io/OpenMail/charts/
kubectl apply -f openmail-service.yaml
