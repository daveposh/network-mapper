#!/bin/bash

# Network Mapper Installation Script

set -e

echo "🚀 Installing Network Mapper..."

# Detect operating system
OS=$(uname -s)
case "$OS" in
    Linux*)     PLATFORM="linux" ;;
    Darwin*)    PLATFORM="macos" ;;
    CYGWIN*|MINGW*|MSYS*) PLATFORM="windows" ;;
    *)          PLATFORM="unknown" ;;
esac

echo "🔍 Detected platform: $PLATFORM"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or higher and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Check for nmap
echo "🔍 Checking for nmap..."
if ! command -v nmap &> /dev/null; then
    echo "⚠️  nmap not found. Installing..."
    
    # Install nmap based on platform
    case "$PLATFORM" in
        "linux")
            if command -v apt-get &> /dev/null; then
                echo "📦 Installing nmap via apt-get..."
                sudo apt-get update && sudo apt-get install -y nmap
            elif command -v yum &> /dev/null; then
                echo "📦 Installing nmap via yum..."
                sudo yum install -y nmap
            elif command -v dnf &> /dev/null; then
                echo "📦 Installing nmap via dnf..."
                sudo dnf install -y nmap
            elif command -v pacman &> /dev/null; then
                echo "📦 Installing nmap via pacman..."
                sudo pacman -S nmap
            else
                echo "❌ Could not install nmap automatically. Please install nmap manually."
                echo "For Ubuntu/Debian: sudo apt-get install nmap"
                echo "For CentOS/RHEL: sudo yum install nmap"
                echo "For Arch Linux: sudo pacman -S nmap"
            fi
            ;;
        "macos")
            if command -v brew &> /dev/null; then
                echo "📦 Installing nmap via Homebrew..."
                brew install nmap
            else
                echo "❌ Homebrew not found. Please install Homebrew and nmap manually."
                echo "Install Homebrew: https://brew.sh/"
                echo "Then run: brew install nmap"
            fi
            ;;
        "windows")
            echo "⚠️  nmap installation on Windows requires manual setup."
            echo "Please download and install nmap from: https://nmap.org/download.html"
            echo "Or use Chocolatey: choco install nmap"
            echo "Or use Scoop: scoop install nmap"
            ;;
        *)
            echo "❌ Unsupported platform. Please install nmap manually."
            ;;
    esac
else
    echo "✅ nmap found"
fi

# Install libpcap on macOS if needed
if [[ "$PLATFORM" == "macos" ]]; then
    echo "🔧 Checking for libpcap..."
    if ! brew list libpcap &> /dev/null 2>&1; then
        echo "📦 Installing libpcap..."
        brew install libpcap
    else
        echo "✅ libpcap found"
    fi
fi

# Create reports directory
echo "📁 Creating reports directory..."
mkdir -p reports

# Make the main script executable
echo "🔧 Making network_mapper.py executable..."
chmod +x network_mapper.py

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To use Network Mapper:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run a scan: python network_mapper.py --mode discovery --target 192.168.1.0/24"
echo ""
echo "Example commands:"
echo "  # Discovery scan"
echo "  python network_mapper.py --mode discovery --target 192.168.1.0/24"
echo ""
echo "  # Detailed local scan"
echo "  python network_mapper.py --mode local --target 192.168.1.0/24 --detailed"
echo ""
echo "  # Generate HTML report"
echo "  python network_mapper.py --mode discovery --target 192.168.1.0/24 --output html"
echo "" 