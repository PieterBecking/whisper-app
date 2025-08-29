#!/usr/bin/env python3
"""
Cross-platform utilities for the Voice Transcriber app
Handles platform-specific functionality for macOS and Linux
"""

import os
import platform
import subprocess
from typing import Optional, Dict, Set
from abc import ABC, abstractmethod


class PlatformHandler(ABC):
    """Abstract base class for platform-specific operations"""
    
    @abstractmethod
    def show_notification(self, title: str, message: str) -> None:
        """Show system notification"""
        pass
    
    @abstractmethod
    def paste_text(self) -> None:
        """Simulate paste keystroke (Cmd+V or Ctrl+V)"""
        pass
    
    @abstractmethod
    def get_shortcut_keys(self) -> Dict[str, str]:
        """Get platform-specific keyboard shortcut mapping"""
        pass


class MacOSHandler(PlatformHandler):
    """macOS-specific implementation"""
    
    def show_notification(self, title: str, message: str) -> None:
        """Show native macOS notification using osascript"""
        try:
            escaped_message = message.replace('"', '\\"').replace("'", "\\'")
            escaped_title = title.replace('"', '\\"').replace("'", "\\'")
            os.system(f'osascript -e "display notification \\"{escaped_message}\\" with title \\"{escaped_title}\\""')
        except Exception:
            pass  # Fail silently if notifications don't work
    
    def paste_text(self) -> None:
        """Use AppleScript to paste (Cmd+V)"""
        try:
            os.system('osascript -e "tell application \\"System Events\\" to keystroke \\"v\\" using command down"')
        except Exception as e:
            print(f"❌ Error pasting on macOS: {e}")
    
    def get_shortcut_keys(self) -> Dict[str, str]:
        """Return macOS shortcut mapping"""
        return {
            'modifier': 'cmd',
            'secondary': 'shift',
            'key': 'space',
            'display': 'Cmd+Shift+Space'
        }


class LinuxHandler(PlatformHandler):
    """Linux-specific implementation"""
    
    def __init__(self):
        self.paste_tool = self._detect_paste_tool()
    
    def _detect_paste_tool(self) -> Optional[str]:
        """Detect available tools for key simulation on Linux"""
        tools = ['xdotool', 'ydotool']
        for tool in tools:
            if subprocess.run(['which', tool], capture_output=True).returncode == 0:
                return tool
        return None
    
    def show_notification(self, title: str, message: str) -> None:
        """Show Linux notification using notify-send"""
        try:
            # Check if notify-send is available
            if subprocess.run(['which', 'notify-send'], capture_output=True).returncode == 0:
                subprocess.run([
                    'notify-send', 
                    '--app-name=Voice Transcriber',
                    '--urgency=normal',
                    title, 
                    message
                ], capture_output=True)
            else:
                # Fallback to console output
                print(f"🔔 {title}: {message}")
        except Exception:
            print(f"🔔 {title}: {message}")  # Fallback to console
    
    def paste_text(self) -> None:
        """Simulate Ctrl+V keystroke on Linux"""
        try:
            if self.paste_tool == 'xdotool':
                # Use xdotool for X11
                subprocess.run(['xdotool', 'key', 'ctrl+v'], check=True)
            elif self.paste_tool == 'ydotool':
                # Use ydotool for Wayland (requires ydotool daemon)
                subprocess.run(['ydotool', 'key', 'ctrl+v'], check=True)
            else:
                print("❌ No paste tool available. Please install xdotool or ydotool")
                print("   sudo apt install xdotool  # For X11")
                print("   sudo apt install ydotool   # For Wayland")
        except Exception as e:
            print(f"❌ Error pasting on Linux: {e}")
            print("💡 Make sure xdotool or ydotool is installed and you have the necessary permissions")
    
    def get_shortcut_keys(self) -> Dict[str, str]:
        """Return Linux shortcut mapping"""
        return {
            'modifier': 'ctrl',
            'secondary': 'shift', 
            'key': 'space',
            'display': 'Ctrl+Shift+Space'
        }


def get_platform_handler() -> PlatformHandler:
    """Factory function to get the appropriate platform handler"""
    system = platform.system().lower()
    
    if system == 'darwin':  # macOS
        return MacOSHandler()
    elif system == 'linux':
        return LinuxHandler()
    else:
        raise NotImplementedError(f"Platform '{system}' is not supported. Only macOS and Linux are supported.")


def get_platform_info() -> Dict[str, str]:
    """Get platform information for display"""
    system = platform.system()
    release = platform.release()
    
    if system == 'Darwin':
        return {
            'name': 'macOS',
            'system': system,
            'version': release
        }
    elif system == 'Linux':
        # Try to get Linux distribution info
        try:
            with open('/etc/os-release') as f:
                lines = f.readlines()
                distro_info = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        distro_info[key] = value.strip('"')
                
                name = distro_info.get('PRETTY_NAME', distro_info.get('NAME', 'Linux'))
                return {
                    'name': name,
                    'system': system,
                    'version': release
                }
        except:
            pass
        
        return {
            'name': 'Linux',
            'system': system, 
            'version': release
        }
    else:
        return {
            'name': system,
            'system': system,
            'version': release
        }


def check_linux_dependencies() -> Dict[str, bool]:
    """Check if required Linux dependencies are available"""
    if platform.system().lower() != 'linux':
        return {}
    
    dependencies = {
        'notify-send': False,
        'xdotool': False,
        'ydotool': False
    }
    
    for tool in dependencies:
        try:
            result = subprocess.run(['which', tool], capture_output=True)
            dependencies[tool] = result.returncode == 0
        except:
            dependencies[tool] = False
    
    return dependencies