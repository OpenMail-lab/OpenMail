#!/bin/bash
echo "🔹 Checking Python installation..."
if ! command -v python3 &> /dev/null
then
    echo "❌ Python missing, detecting system architecture..."
    
    ARCH=$(uname -m)
    if [[ "$ARCH" == "x86_64" ]]; then
        PYTHON_URL="https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.pkg"
    elif [[ "$ARCH" == "arm64" ]]; then
        PYTHON_URL="https://www.python.org/ftp/python/3.12.0/python-3.12.0-arm64.pkg"
    else
        PYTHON_URL="https://www.python.org/ftp/python/3.12.0/python-3.12.0.pkg"
    fi

    curl -O $PYTHON_URL
    sudo installer -pkg $(basename $PYTHON_URL) -target /
    echo "✅ Python installed!"
fi

echo "🔹 Running OpenMail installer..."
python3 universal-installer.py
