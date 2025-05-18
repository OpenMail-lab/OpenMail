import os
import requests

GITHUB_REPO = "https://api.github.com/repos/openmail-lab/OpenMail/releases/latest"

def check_for_updates():
    print("🔹 Checking for updates...")
    response = requests.get(GITHUB_REPO)
    latest_version = response.json()["tag_name"]

    current_version = "1.0.0"  # Replace with actual version tracking
    if latest_version > current_version:
        print(f"🚀 New version {latest_version} available! Updating...")
        download_update(response.json()["zipball_url"])
    else:
        print("✅ OpenMail is up to date.")

def download_update(url):
    os.system(f"curl -L {url} -o update.zip")
    os.system("unzip update.zip -d OpenMail")
    os.system("rm update.zip")
    print("🔄 Update installed! Restarting OpenMail...")
    restart_app()

def restart_app():
    os.system("python3 main.py")
    os.system("python3 -m webbrowser -t 'http://localhost:8080/changelog.html'")  # 🔥 Auto-open changelog!

if __name__ == "__main__":
    check_for_updates()
