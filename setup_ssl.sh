#!/bin/bash

echo "🔹 Installing Certbot for automatic SSL..."
sudo apt update && sudo apt install -y certbot

echo "🔹 Generating an SSL certificate..."
sudo certbot certonly --standalone --preferred-challenges http --agree-tos --email admin@openmail.com -d openmail.example.com

echo "🔹 Configuring automatic renewal..."
echo "0 0 * * * root certbot renew --quiet" | sudo tee -a /etc/crontab
