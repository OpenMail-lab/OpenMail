import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.welcome_screen import WelcomeScreen


def main():
    app = WelcomeScreen()
    app.run()


if __name__ == "__main__":
    main()