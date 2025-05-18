from flask import Flask, request, jsonify
import pygame

app = Flask(__name__)
pygame.init()

# Define sound effects
sounds = {
    "success": "sounds/success.mp3",
    "error": "sounds/error.mp3",
    "warning": "sounds/warning.mp3"
}

@app.route('/api/play-sound', methods=['POST'])
def play_sound():
    event_type = request.json.get("type", "success")  # Default to success
    sound_file = sounds.get(event_type, sounds["success"])  # Use appropriate sound

    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    
    return jsonify({"status": f"🔊 Playing {event_type} sound!"})

if __name__ == '__main__':
    app.run(port=5006, debug=True)
