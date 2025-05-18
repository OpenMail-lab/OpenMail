#!/bin/bash
echo "🔹 Setting up DevOps tools inside OpenMail..."
#!/bin/bash
echo "🔹 Setting up DevOps tools inside OpenMail..."
python3 ui/turtle-graphics.py &

# Start DevOps containers inside OpenMail
podman run -d --name kiali -p 31001:20001 kiali/kiali
podman run -d --name terraform -p 31002:20002 hashicorp/terraform
podman run -d --name argocd -p 31003:20003 argoproj/argocd
podman run -d --name helm -p 31004:20004 bitnami/helm
podman run -d --name ansible -p 31005:20005 ansible/ansible
podman run -d --name docker -p 31006:20006 docker

echo "🚀 All DevOps services are running inside OpenMail!"
