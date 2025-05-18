import os
import update
import auto_update
# Ensure dependencies are installed
try:
    import flask
    import kubernetes
except ImportError:
    print("🔹 Installing missing dependencies...")
    os.system("pip install flask kubernetes")

print("✅ All dependencies installed. Starting OpenMail...")
print("🔹 Starting OpenMail...")
update.check_for_updates()
print("🔹 Starting OpenMail...")
auto_update.check_for_updates()