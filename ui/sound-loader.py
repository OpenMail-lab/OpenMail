import pygame
import time

pygame.init()

# Define sound effects for different steps
sounds = {
    "start": "sounds/start.mp3",
    "installing": "sounds/installing.mp3",
    "done": "sounds/done.mp3"
}

def play_sound(event):
    pygame.mixer.music.load(sounds[event])
    pygame.mixer.music.play()
    time.sleep(2)  # Wait for sound to play

def install_with_sound():
    play_sound("start")
    print("🔹 Installation started...")

    # Simulating different installation steps
    for step in ["Installing dependencies...", "Setting up Kubernetes...", "Deploying services...", "Finalizing setup..."]:
        print(f"✅ {step}")
        play_sound("installing")
        time.sleep(2)  # Simulate process time

    play_sound("done")
    print("🎉 Installation complete!")

if __name__ == "__main__":
    install_with_sound()
