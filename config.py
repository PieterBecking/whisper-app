import os
from platform_utils import get_platform_handler

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY")

# Get platform-specific handler for dynamic configuration
_platform_handler = get_platform_handler()
_shortcut_info = _platform_handler.get_shortcut_keys()

# Keyboard shortcut configuration (platform-specific)
TOGGLE_SHORTCUT = {_shortcut_info['modifier'], _shortcut_info['secondary'], _shortcut_info['key']}
SHORTCUT_DISPLAY = _shortcut_info['display']

# Audio recording settings
SAMPLE_RATE = 16000  # OpenAI Whisper works best with 16kHz
CHANNELS = 1  # Mono
CHUNK_SIZE = 1024
FORMAT = 'wav'

# File settings
TEMP_AUDIO_FILE = "/tmp/whisper_recording.wav"

# Notification settings
SHOW_NOTIFICATIONS = True