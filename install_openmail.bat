@echo off
echo 🔹 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is missing, installing now...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo ❌ Python installation failed!
        exit /b 2
    )
    echo ✅ Python installed!
)

echo 🔹 Verifying pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pip missing, installing now...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
    echo ✅ Pip installed!
)

echo 🔹 Running OpenMail installer...
python "%~dp0universal-installer.py"
if %errorlevel% neq 0 (
    echo ❌ OpenMail installation failed!
    exit /b 2
)

echo ✅ OpenMail installed successfully!
pause
