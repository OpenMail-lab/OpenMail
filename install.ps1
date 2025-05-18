Write-Host "🔹 Installing OpenMail..."
winget install -e --id Docker.DockerDesktop
Start-Sleep -s 10  # Wait for Docker installation
podman build -t openmail .
podman run -p 5001:5001 --name openmail_container openmail

Write-Host "✅ OpenMail is now running at http://localhost:5001/"
