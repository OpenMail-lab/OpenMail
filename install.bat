@echo off
echo Installing OpenMail...

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found, installing embedded Python...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip -OutFile python.zip"
    powershell -Command "Expand-Archive python.zip -DestinationPath .\python"
    del python.zip
)

:: Set up Python path
set PATH=%~dp0python;%PATH%

:: Install dependencies
.\python\python.exe -m pip install -r requirements.txt

:: Run the application
start OpenMail-Installer.exe
