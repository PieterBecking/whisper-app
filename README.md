# 🎤 Cross-Platform Global Voice Transcriber

A cross-platform system-wide voice transcription app that lets you record audio with a keyboard shortcut and automatically paste the OpenAI Whisper transcription wherever your cursor is.

**Supported Platforms:** macOS and Linux

## ✨ Features

- **Cross-platform**: Works on both macOS and Linux with platform-specific optimizations
- **Global hotkey**: Press `Cmd+Shift+Space` (macOS) or `Ctrl+Shift+Space` (Linux) to start/stop recording
- **Smart pasting**: Automatically pastes transcription at your cursor location
- **Real-time feedback**: Native notifications during recording and processing
- **OpenAI Whisper**: High-quality transcription using OpenAI's Whisper API
- **Background operation**: Runs invisibly in the background

## 🔧 Prerequisites

### Universal Requirements
- Python 3.8 or later
- OpenAI API key
- Microphone access

### Platform-Specific Requirements

#### macOS
- macOS Sonoma 14+ (tested)
- Accessibility permissions
- Input Monitoring permissions

#### Linux
- X11 or Wayland desktop environment
- Audio system (PulseAudio/ALSA)
- One of: `xdotool` (X11) or `ydotool` (Wayland) for key simulation
- `libnotify-bin` for notifications (optional)

## 🚀 Installation

### 1. Install Dependencies

#### Python Dependencies (All Platforms)
```bash
pip3 install -r requirements.txt
```

#### Platform-Specific System Dependencies

**macOS:**
```bash
# Install PortAudio if needed
brew install portaudio
```

**Linux (Ubuntu/Debian):**
```bash
# Required packages
sudo apt update
sudo apt install python3-dev portaudio19-dev libnotify-bin

# For X11 environments (most common)
sudo apt install xdotool

# OR for Wayland environments
sudo apt install ydotool
# Note: ydotool may require additional setup
```

**Linux (Fedora/RHEL):**
```bash
# Required packages
sudo dnf install python3-devel portaudio-devel libnotify

# For X11
sudo dnf install xdotool

# OR for Wayland
sudo dnf install ydotool
```

**Linux (Arch):**
```bash
# Required packages
sudo pacman -S python portaudio libnotify

# For X11
sudo pacman -S xdotool

# OR for Wayland
sudo pacman -S ydotool
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

#### macOS Permissions

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

#### Linux Permissions

Linux typically doesn't require explicit permission grants, but you may need:

**Audio Access:**
- Your user should be in the `audio` group: `sudo usermod -a -G audio $USER`
- Restart your session after adding to the group

**Wayland + ydotool Setup (if using Wayland):**
```bash
# Start ydotool daemon (required for ydotool to work)
sudo systemctl enable --now ydotool

# Or run manually:
sudo ydotoold
```

**Notification Access:**
- Most Linux distributions enable notifications by default
- If notifications don't work, the app will fall back to console output

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

1. **Start Recording**: Press the platform shortcut anywhere on your system:
   - **macOS**: `Cmd+Shift+Space`
   - **Linux**: `Ctrl+Shift+Space`
   - You'll see a notification: "🔴 Recording started..."

2. **Stop Recording**: Press the same shortcut again
   - The app will process the audio and show: "⏹️ Processing transcription..."

3. **Auto-Paste**: The transcription will be automatically pasted wherever your cursor was when you first pressed the shortcut

### Example Workflow

1. Open any text editor, email, or chat app
2. Click where you want the transcription to appear
3. Press the shortcut (`Cmd+Shift+Space` on macOS, `Ctrl+Shift+Space` on Linux) to start recording
4. Speak your message
5. Press the shortcut again to stop
6. The transcription appears automatically at your cursor

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# Keyboard shortcuts are automatically configured based on platform:
# - macOS: Cmd+Shift+Space
# - Linux: Ctrl+Shift+Space

# Audio settings
SAMPLE_RATE = 16000  # Best for Whisper
CHANNELS = 1         # Mono recording

# Notifications
SHOW_NOTIFICATIONS = True  # Set to False to disable popups
```

## 🔧 Troubleshooting

### macOS-Specific Issues
- **"AccessibilityNotEnabled"**: Grant Accessibility permissions as described above
- **"Microphone access denied"**: Check Privacy & Security → Microphone settings

### Linux-Specific Issues
- **"No paste tool available"**: Install `xdotool` (X11) or `ydotool` (Wayland)
- **"Paste failed"**: 
  - For X11: Ensure `xdotool` is installed and you're in an X11 session
  - For Wayland: Ensure `ydotool` daemon is running: `sudo ydotoold`
- **"Audio device not found"**: Add your user to audio group: `sudo usermod -a -G audio $USER`
- **No notifications**: Install `libnotify-bin` or check if notification service is running

### Universal Issues
- **"No audio input device"**: Check your microphone is connected and working
- **"Poor transcription quality"**: Ensure you're in a quiet environment and speak clearly
- **"Invalid API key"**: Check your OpenAI API key is correct and has credits
- **"Rate limited"**: Wait a moment between requests if you hit rate limits
- **"Module not found"**: Make sure all requirements are installed: `pip3 install -r requirements.txt`
- **"Permission denied"**: You may need to install packages with `sudo` or use a virtual environment

### Platform Detection Issues
If the app doesn't detect your platform correctly:
```bash
python3 -c "import platform; print(f'System: {platform.system()}, Release: {platform.release()}')"
```

## 🛠️ Running as Background Service

To run the app automatically on startup:

### macOS Options

**Option 1: Add to Login Items**
1. Open **System Preferences → Users & Groups → Login Items**
2. Add a script that runs: `cd /path/to/whisper && python3 main.py`

**Option 2: Create Launch Agent (Advanced)**
Create `~/Library/LaunchAgents/com.voicetranscriber.plist` with appropriate plist configuration.

### Linux Options

**Option 1: Systemd User Service**
Create `~/.config/systemd/user/voice-transcriber.service`:
```ini
[Unit]
Description=Voice Transcriber
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/whisper/main.py
Restart=always
Environment=DISPLAY=:0

[Install]
WantedBy=default.target
```

Then enable:
```bash
systemctl --user enable voice-transcriber.service
systemctl --user start voice-transcriber.service
```

**Option 2: Desktop Autostart**
Create `~/.config/autostart/voice-transcriber.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=Voice Transcriber
Exec=python3 /path/to/whisper/main.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
```

## 📝 Technical Details

- **Audio Format**: 16kHz mono WAV (optimal for Whisper)
- **Shortcut System**: Uses `pynput` for global hotkeys with platform-specific key mappings
- **Pasting Method**: 
  - **macOS**: Clipboard + AppleScript for system-wide pasting
  - **Linux**: Clipboard + xdotool/ydotool for key simulation
- **API**: OpenAI Whisper-1 model via REST API
- **Notifications**: 
  - **macOS**: Native notifications via `osascript`
  - **Linux**: `notify-send` with fallback to console output
- **Platform Detection**: Automatic detection using Python's `platform` module

## 🔒 Privacy & Security

- Audio is recorded temporarily and immediately deleted after transcription
- No audio data is stored permanently on your device
- Audio is sent to OpenAI's servers for transcription (see OpenAI's privacy policy)
- The app only activates when you press the keyboard shortcut

## 📄 License

This project is provided as-is for educational purposes. Check OpenAI's terms of service for API usage compliance.

## 🆘 Support

For issues:
1. Check the platform-specific troubleshooting sections above
2. Verify all permissions are granted (macOS) or dependencies installed (Linux)
3. Test module imports: `python3 -c "import pyaudio, pynput, openai, platform_utils; print('All modules imported successfully')"`
4. Check platform detection: `python3 -c "from platform_utils import get_platform_info; print(get_platform_info())"`