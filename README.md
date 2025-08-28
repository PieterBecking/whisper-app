# 🎤 Global Voice Transcriber for macOS

A system-wide voice transcription app that lets you record audio with a keyboard shortcut and automatically paste the OpenAI Whisper transcription wherever your cursor is.

## ✨ Features

- **Global hotkey**: Press `Cmd+Shift+Space` from anywhere to start/stop recording
- **Smart pasting**: Automatically pastes transcription at your cursor location
- **Real-time feedback**: Visual notifications during recording and processing
- **OpenAI Whisper**: High-quality transcription using OpenAI's Whisper API
- **Background operation**: Runs invisibly in the background

## 🔧 Prerequisites

- macOS (tested on macOS Sonoma 14+)
- Python 3.8 or later
- OpenAI API key
- Microphone access
- Accessibility permissions

## 🚀 Installation

### 1. Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Install system audio dependencies (if needed)
# On some systems, you may need to install PortAudio:
# brew install portaudio
```

### 2. Configure API Key

Set your OpenAI API key using one of these methods:

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: Edit config.py**
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 3. Grant Permissions

The app requires several macOS permissions:

#### Microphone Access
- Run the app once, and macOS will prompt for microphone access
- Or go to: **System Preferences → Privacy & Security → Microphone**
- Add Terminal (or your Python executable) to the allowed apps

#### Accessibility Access (Required for global shortcuts and pasting)
- Go to: **System Preferences → Privacy & Security → Accessibility**
- Click the lock icon and enter your password
- Click "+" and add Terminal (or your Python executable)
- Ensure the checkbox is enabled

#### Input Monitoring (May be required)
- Go to: **System Preferences → Privacy & Security → Input Monitoring**
- Add Terminal (or your Python executable) if prompted

## 🎯 Usage

### Running the App

```bash
python3 main.py
```

The app will run in the background and show:
```
🎤 Voice Transcriber initialized
📋 Shortcut: cmd+shift+space
🔄 Press the shortcut to start recording...
🚀 Voice Transcriber is running...
```

### Recording and Transcribing

1. **Start Recording**: Press `Cmd+Shift+Space` anywhere on your system
   - You'll see a notification: "🔴 Recording started..."

2. **Stop Recording**: Press `Cmd+Shift+Space` again
   - The app will process the audio and show: "⏹️ Processing transcription..."

3. **Auto-Paste**: The transcription will be automatically pasted wherever your cursor was when you first pressed the shortcut

### Example Workflow

1. Open any text editor, email, or chat app
2. Click where you want the transcription to appear
3. Press `Cmd+Shift+Space` to start recording
4. Speak your message
5. Press `Cmd+Shift+Space` to stop
6. The transcription appears automatically at your cursor

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Keyboard shortcut (default: Cmd+Shift+Space)
TOGGLE_SHORTCUT = {'cmd', 'shift', 'space'}

# Audio settings
SAMPLE_RATE = 16000  # Best for Whisper
CHANNELS = 1         # Mono recording

# Notifications
SHOW_NOTIFICATIONS = True  # Set to False to disable popups
```

## 🔧 Troubleshooting

### Permission Issues
- **"AccessibilityNotEnabled"**: Grant Accessibility permissions as described above
- **"Microphone access denied"**: Check Privacy & Security → Microphone settings

### Audio Issues
- **"No audio input device"**: Check your microphone is connected and working
- **"Poor transcription quality"**: Ensure you're in a quiet environment and speak clearly

### API Issues
- **"Invalid API key"**: Check your OpenAI API key is correct and has credits
- **"Rate limited"**: Wait a moment between requests if you hit rate limits

### Installation Issues
- **"Module not found"**: Make sure all requirements are installed: `pip3 install -r requirements.txt`
- **"Permission denied"**: You may need to install packages with `sudo` or use a virtual environment

## 🛠️ Running as Background Service

To run the app automatically on startup:

### Option 1: Add to Login Items
1. Open **System Preferences → Users & Groups → Login Items**
2. Add a script that runs: `cd /path/to/whisper && python3 main.py`

### Option 2: Create Launch Agent (Advanced)
Create `~/Library/LaunchAgents/com.voicetranscriber.plist` with appropriate plist configuration.

## 📝 Technical Details

- **Audio Format**: 16kHz mono WAV (optimal for Whisper)
- **Shortcut System**: Uses `pynput` for global hotkeys
- **Pasting Method**: Clipboard + AppleScript for system-wide pasting
- **API**: OpenAI Whisper-1 model via REST API
- **Notifications**: Native macOS notifications via `plyer`

## 🔒 Privacy & Security

- Audio is recorded temporarily and immediately deleted after transcription
- No audio data is stored permanently on your device
- Audio is sent to OpenAI's servers for transcription (see OpenAI's privacy policy)
- The app only activates when you press the keyboard shortcut

## 📄 License

This project is provided as-is for educational purposes. Check OpenAI's terms of service for API usage compliance.

## 🆘 Support

For issues:
1. Check the troubleshooting section above
2. Verify all permissions are granted
3. Test with `python3 -c "import pyaudio, pynput, openai; print('All modules imported successfully')"`