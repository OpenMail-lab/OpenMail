#!/bin/bash
echo "🔹 Installing OpenMail..."
sudo apt update && sudo apt install -y docker.io
docker build -t openmail .
docker run -d -p 5001:5001 --name openmail_container openmail
echo "✅ OpenMail is now running at http://localhost:5001/"
#!/bin/bash
echo "🔹 Setting up OpenMail..."
pip install --upgrade flask kubernetes pygame requests
kubectl apply -f microservices/
python3 api/recovery_service.py &
python3 api/sound_service.py &
echo "✅ Installation complete! OpenMail is now running."
