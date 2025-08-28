import os

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# Keyboard shortcut configuration
TOGGLE_SHORTCUT = {'cmd', 'shift', 'space'}  # Cmd+Shift+Space

# Audio recording settings
SAMPLE_RATE = 16000  # OpenAI Whisper works best with 16kHz
CHANNELS = 1  # Mono
CHUNK_SIZE = 1024
FORMAT = 'wav'

# File settings
TEMP_AUDIO_FILE = "/tmp/whisper_recording.wav"

# Notification settings
SHOW_NOTIFICATIONS = True