@echo off
echo 🔹 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is missing, installing now...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    if %errorlevel% neq 0 (
        echo ❌ Failed to download Python installer!
        exit /b 1
    )
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    if %errorlevel% neq 0 (
        echo ❌ Python installation failed!
        exit /b 1
    )
    echo ✅ Python installed!
    :: Refresh environment variables
    set "PATH=%PATH%;C:\Program Files\Python312\Scripts;C:\Program Files\Python312"
)

echo 🔹 Verifying pip installation...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Pip missing, installing now...
    python -m ensurepip --default-pip
    if %errorlevel% neq 0 (
        echo ❌ Failed to install ensurepip!
        exit /b 1
    )
    python -m pip install --upgrade pip
    if %errorlevel% neq 0 (
        echo ❌ Failed to upgrade pip!
        exit /b 1
    )
    echo ✅ Pip installed!
)

echo 🔹 Installing dependencies from requirements.txt...
python -m pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies!
    exit /b 1
)

echo ✅ Setup completed successfully! Run universal-installer.py to continue.
pause