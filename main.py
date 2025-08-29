#!/usr/bin/env python3
"""
Cross-Platform Global Voice Transcription App
Supports macOS and Linux - automatically detects platform and uses appropriate shortcuts
"""

import os
import sys
import threading
import time
import tempfile
import wave
from typing import Optional

import pyaudio
import pyperclip
from openai import OpenAI
from pynput import keyboard

import config
from platform_utils import get_platform_handler, get_platform_info, check_linux_dependencies


class VoiceTranscriber:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.is_recording = False
        self.audio_stream: Optional[pyaudio.Stream] = None
        self.audio_data = []
        self.pyaudio_instance = pyaudio.PyAudio()
        
        # Get platform handler
        self.platform_handler = get_platform_handler()
        
        # Display platform info
        platform_info = get_platform_info()
        print(f"🖥️  Platform: {platform_info['name']}")
        
        # Check Linux dependencies if on Linux
        if platform_info['system'].lower() == 'linux':
            self._check_linux_setup()
        
        # Setup keyboard listener
        self.setup_keyboard_listener()
        
        print("🎤 Voice Transcriber initialized")
        print(f"📋 Shortcut: {config.SHORTCUT_DISPLAY}")
        print("🔄 Press the shortcut to start recording...")

    def _check_linux_setup(self):
        """Check Linux dependencies and provide setup guidance"""
        deps = check_linux_dependencies()
        
        if not any(deps.values()):
            print("⚠️  Warning: No Linux dependencies detected")
            print("   Install required packages:")
            print("   sudo apt install libnotify-bin xdotool  # For X11")
            print("   sudo apt install libnotify-bin ydotool  # For Wayland")
        else:
            available = [tool for tool, avail in deps.items() if avail]
            print(f"✅ Linux tools available: {', '.join(available)}")
    
    def setup_keyboard_listener(self):
        """Setup global keyboard shortcut listener with platform-specific keys"""
        shortcut_info = self.platform_handler.get_shortcut_keys()
        modifier = shortcut_info['modifier']
        secondary = shortcut_info['secondary']
        key = shortcut_info['key']
        
        shortcut_string = f'<{modifier}>+<{secondary}>+<{key}>'
        
        self.keyboard_listener = keyboard.GlobalHotKeys({
            shortcut_string: self.toggle_recording
        })
        self.keyboard_listener.start()

    def toggle_recording(self):
        """Toggle between start and stop recording"""
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.audio_data = []
        
        self.platform_handler.show_notification("Voice Transcriber", "🔴 Recording started...")
        
        print("🔴 Recording started...")
        
        try:
            self.audio_stream = self.pyaudio_instance.open(
                format=pyaudio.paInt16,
                channels=config.CHANNELS,
                rate=config.SAMPLE_RATE,
                input=True,
                frames_per_buffer=config.CHUNK_SIZE,
                stream_callback=self.audio_callback
            )
            self.audio_stream.start_stream()
        except Exception as e:
            print(f"❌ Error starting recording: {e}")
            self.is_recording = False
            self.platform_handler.show_notification("Voice Transcriber", "❌ Failed to start recording")

    def audio_callback(self, in_data, frame_count, time_info, status):
        """Callback function for audio stream"""
        if self.is_recording:
            self.audio_data.append(in_data)
        return (in_data, pyaudio.paContinue)

    def stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        print("⏹️ Recording stopped, processing...")
        
        self.platform_handler.show_notification("Voice Transcriber", "⏹️ Processing transcription...")
        
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_stream = None
        
        # Process the recording in a separate thread
        threading.Thread(target=self.process_recording, daemon=True).start()

    def process_recording(self):
        """Process the recorded audio and transcribe it"""
        if not self.audio_data:
            print("❌ No audio data recorded")
            return
        
        try:
            # Save audio data to temporary file
            temp_file_path = self.save_audio_to_file()
            
            # Transcribe with OpenAI
            transcription = self.transcribe_audio(temp_file_path)
            
            if transcription:
                # Copy to clipboard and paste
                self.paste_transcription(transcription)
                print(f"✅ Transcribed: {transcription}")
            else:
                print("❌ No transcription received")
                
        except Exception as e:
            print(f"❌ Error processing recording: {e}")
            self.platform_handler.show_notification("Voice Transcriber", f"❌ Error: {str(e)}")
        finally:
            # Cleanup
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def save_audio_to_file(self) -> str:
        """Save recorded audio data to a temporary WAV file"""
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file_path = temp_file.name
        temp_file.close()
        
        with wave.open(temp_file_path, 'wb') as wav_file:
            wav_file.setnchannels(config.CHANNELS)
            wav_file.setsampwidth(self.pyaudio_instance.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(config.SAMPLE_RATE)
            wav_file.writeframes(b''.join(self.audio_data))
        
        return temp_file_path

    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio using OpenAI Whisper API"""
        try:
            with open(audio_file_path, 'rb') as audio_file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                return response.text.strip()
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None

    def paste_transcription(self, text: str):
        """Copy text to clipboard and simulate paste"""
        try:
            # Copy to clipboard
            pyperclip.copy(text)
            
            # Small delay to ensure clipboard is ready
            time.sleep(0.1)
            
            # Use platform-specific paste method
            self.platform_handler.paste_text()
            
            # Show success notification
            preview = text[:50] + '...' if len(text) > 50 else text
            self.platform_handler.show_notification("Voice Transcriber", f"✅ Pasted: {preview}")
                
        except Exception as e:
            print(f"❌ Error pasting text: {e}")
            self.platform_handler.show_notification("Voice Transcriber", f"❌ Paste failed: {str(e)}")

    def cleanup(self):
        """Clean up resources"""
        self.is_recording = False
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
        self.pyaudio_instance.terminate()
        self.keyboard_listener.stop()

    def run(self):
        """Run the application"""
        try:
            print("🚀 Voice Transcriber is running...")
            print("Press Ctrl+C to quit")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.cleanup()
            sys.exit(0)


def main():
    """Main entry point"""
    if config.OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        print("❌ Please set your OpenAI API key in config.py or as an environment variable OPENAI_API_KEY")
        sys.exit(1)
    
    app = VoiceTranscriber()
    app.run()


if __name__ == "__main__":
    main()