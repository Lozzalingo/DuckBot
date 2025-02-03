#!/bin/bash

# This script automates the installation of Ollama, Llama 3.2 model, Python (if necessary),
# setting up a virtual environment, and installing Python dependencies from requirements.txt.

echo "Starting installation..."

# Step 1: Check OS type
OS=$(uname -s)

# Step 2: Install Python (if not already installed)
echo "Checking for Python installation..."
if ! command -v python3 &>/dev/null; then
    echo "Python 3 not found! Installing Python..."
    if [[ "$OS" == "Darwin" ]]; then
        # For macOS
        brew install python3
    elif [[ "$OS" == "Linux" ]]; then
        # For Linux
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif [[ "$OS" == "MINGW"* || "$OS" == "CYGWIN"* ]]; then
        # For Windows
        echo "For Windows, please download and install Python from https://www.python.org/downloads/."
        exit 1
    else
        echo "Unsupported OS. Please install Python manually."
        exit 1
    fi
else
    echo "Python 3 is already installed."
fi

# Step 3: Create Virtual Environment if not already created
echo "Checking for existing virtual environment..."
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Step 4: Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For macOS/Linux
# For Windows, uncomment the following line:
# source venv/Scripts/activate

# Step 5: Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 6: Install Ollama
echo "Installing Ollama..."
if ! command -v ollama &>/dev/null; then
    if [[ "$OS" == "Darwin" || "$OS" == "Linux" ]]; then
        # Install Ollama for macOS/Linux
        curl -sSL https://ollama.com/install.sh | bash
    elif [[ "$OS" == "MINGW"* || "$OS" == "CYGWIN"* ]]; then
        # For Windows, download Ollama manually from https://ollama.com
        echo "For Windows, please follow the installation instructions at https://ollama.com."
        exit 1
    else
        echo "Unsupported OS for Ollama installation. Please follow the installation instructions from https://ollama.com."
        exit 1
    fi
else
    echo "Ollama is already installed."
fi

# Step 7: Pull Llama 3.2:latest Model
echo "Downloading Llama 3.2 model..."
ollama pull llama3.2:latest

echo "Installation complete! You can now run DuckBot."
