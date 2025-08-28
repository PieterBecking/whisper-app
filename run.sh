#!/bin/bash

# Voice Transcriber Launcher Script
# This script launches the Voice Transcriber app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎤 Starting Voice Transcriber...${NC}"

# Check if API key is set
if [[ -z "${OPENAI_API_KEY}" ]] && ! grep -q "OPENAI_API_KEY.*=" config.py | grep -v "YOUR_OPENAI_API_KEY"; then
    echo -e "${RED}❌ OpenAI API key not found!${NC}"
    echo "Please set your API key using one of these methods:"
    echo "1. Environment variable: export OPENAI_API_KEY='your-key'"
    echo "2. Edit config.py and set OPENAI_API_KEY = 'your-key'"
    echo ""
    exit 1
fi

# Check Python dependencies
if ! python3 -c "import pyaudio, pynput, openai, pyperclip, plyer" 2>/dev/null; then
    echo -e "${RED}❌ Missing Python dependencies!${NC}"
    echo "Please run: pip3 install -r requirements.txt"
    echo "Or run the setup script: ./setup.sh"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Starting Voice Transcriber${NC}"
echo -e "${BLUE}Press Ctrl+C to quit${NC}"
echo ""

# Run the main application
python3 main.py