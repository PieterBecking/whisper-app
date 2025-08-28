#!/bin/bash

# Voice Transcriber Setup Script for macOS
# This script helps set up the Global Voice Transcriber app

set -e  # Exit on any error

echo "🎤 Voice Transcriber Setup Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo -e "${RED}❌ This script is designed for macOS only${NC}"
    exit 1
fi

echo -e "${BLUE}🔍 Checking system requirements...${NC}"

# Check Python version
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python 3 found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    echo "Please install Python 3.8+ from https://python.org or using Homebrew:"
    echo "brew install python"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✅ pip3 found${NC}"
else
    echo -e "${RED}❌ pip3 is required but not found${NC}"
    exit 1
fi

# Check for Homebrew (optional but recommended for PortAudio)
if command -v brew &> /dev/null; then
    echo -e "${GREEN}✅ Homebrew found${NC}"
    
    # Check if PortAudio is installed
    if brew list portaudio &> /dev/null; then
        echo -e "${GREEN}✅ PortAudio already installed${NC}"
    else
        echo -e "${YELLOW}⚠️  PortAudio not found, installing...${NC}"
        brew install portaudio
        echo -e "${GREEN}✅ PortAudio installed${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Homebrew not found. You may need to install PortAudio manually if you encounter audio issues${NC}"
fi

echo ""
echo -e "${BLUE}📦 Installing Python dependencies...${NC}"

# Install Python packages
pip3 install -r requirements.txt

echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
echo ""

# API Key setup
echo -e "${BLUE}🔑 OpenAI API Key Setup${NC}"
echo "You need an OpenAI API key to use the transcription service."
echo ""

if [[ -n "${OPENAI_API_KEY}" ]]; then
    echo -e "${GREEN}✅ OPENAI_API_KEY environment variable is already set${NC}"
else
    echo -e "${YELLOW}⚠️  OPENAI_API_KEY environment variable not found${NC}"
    echo ""
    echo "You can set it in one of these ways:"
    echo ""
    echo "1. Add to your shell profile (.zshrc, .bash_profile, etc.):"
    echo "   export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    echo "2. Or edit config.py in this directory and set:"
    echo "   OPENAI_API_KEY = 'your-api-key-here'"
    echo ""
    
    read -p "Do you want to set the API key now? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -s -p "Enter your OpenAI API key: " api_key
        echo ""
        
        # Add to .zshrc (assuming zsh, which is default on modern macOS)
        if [[ -f "$HOME/.zshrc" ]]; then
            echo "export OPENAI_API_KEY='$api_key'" >> ~/.zshrc
            echo -e "${GREEN}✅ API key added to ~/.zshrc${NC}"
            echo "Please run: source ~/.zshrc or restart your terminal"
        else
            echo -e "${YELLOW}⚠️  ~/.zshrc not found. Please set the environment variable manually${NC}"
        fi
    fi
fi

echo ""
echo -e "${BLUE}🔐 macOS Permissions Setup${NC}"
echo "The app requires the following permissions:"
echo ""
echo -e "${YELLOW}📋 Required Permissions:${NC}"
echo "1. 🎤 Microphone Access"
echo "2. ♿ Accessibility (for global shortcuts and pasting)"
echo "3. 👀 Input Monitoring (may be requested)"
echo ""

echo -e "${BLUE}To grant these permissions:${NC}"
echo "1. Go to: System Preferences → Privacy & Security"
echo "2. Add Terminal (or your Python executable) to:"
echo "   • Microphone"
echo "   • Accessibility" 
echo "   • Input Monitoring (if prompted)"
echo ""

# Test installation
echo -e "${BLUE}🧪 Testing installation...${NC}"

if python3 -c "import pyaudio, pynput, openai, pyperclip, plyer; print('All modules imported successfully')" 2>/dev/null; then
    echo -e "${GREEN}✅ All Python modules imported successfully${NC}"
else
    echo -e "${RED}❌ Some Python modules failed to import${NC}"
    echo "Please check the error messages above and resolve any issues."
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo -e "${BLUE}🚀 To start the Voice Transcriber:${NC}"
echo "   python3 main.py"
echo ""
echo -e "${BLUE}🎯 Usage:${NC}"
echo "   Press Cmd+Shift+Space to start/stop recording"
echo "   Transcription will be pasted wherever your cursor is"
echo ""
echo -e "${YELLOW}📝 Important:${NC}"
echo "• Grant the required permissions when prompted"
echo "• Make sure your OpenAI API key is set and has credits"
echo "• The app needs to run in the foreground to receive global shortcuts"
echo ""
echo -e "${BLUE}📚 For detailed instructions, see README.md${NC}"