# Cross-Platform Compatibility Guide

## 🌍 Supported Platforms

The Network Mapper is designed to work seamlessly across multiple operating systems:

### ✅ Fully Supported
- **macOS** (10.14+)
- **Linux** (Ubuntu 18.04+, CentOS 7+, RHEL 7+, Arch Linux)
- **Windows** (10, 11)

### 🔧 Platform-Specific Features

#### macOS
- **Installation**: Automated via `./install.sh`
- **Package Manager**: Homebrew for nmap and libpcap
- **Commands**: Native Unix commands (ping, arp, netstat)
- **Permissions**: May require sudo for certain operations

#### Linux
- **Installation**: Automated via `./install.sh`
- **Package Managers**: apt, yum, dnf, pacman
- **Commands**: Native Unix commands (ping, arp, netstat)
- **Permissions**: May require sudo for certain operations

#### Windows
- **Installation**: Automated via `install.bat` or `install.ps1`
- **Package Manager**: Manual download or Chocolatey/Scoop
- **Commands**: Windows-specific commands (ping, arp, netstat)
- **Permissions**: May require admin privileges

## 📦 Installation Methods

### macOS/Linux
```bash
# Automated installation
./install.sh

# Manual installation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```cmd
# Command Prompt
install.bat

# PowerShell
.\install.ps1

# Manual installation
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🔍 Platform-Specific Commands

### Ping Commands
```bash
# macOS/Linux
ping -c 1 -W 1 192.168.1.1

# Windows
ping -n 1 -w 1000 192.168.1.1
```

### ARP Commands
```bash
# macOS/Linux
arp -n 192.168.1.1

# Windows
arp -a 192.168.1.1
```

### Network Statistics
```bash
# All platforms
netstat -an
```

## 🛠️ Platform-Specific Dependencies

### macOS
- **Python**: 3.8+ (via Homebrew or python.org)
- **nmap**: `brew install nmap`
- **libpcap**: `brew install libpcap` (optional)

### Linux
- **Python**: 3.8+ (via package manager)
- **nmap**: `sudo apt-get install nmap` (Ubuntu/Debian)
- **nmap**: `sudo yum install nmap` (CentOS/RHEL)
- **nmap**: `sudo pacman -S nmap` (Arch)

### Windows
- **Python**: 3.8+ (from python.org)
- **nmap**: Download from https://nmap.org/download.html
- **Alternative**: `choco install nmap` (Chocolatey)
- **Alternative**: `scoop install nmap` (Scoop)

## 🔧 Configuration Differences

### File Paths
```python
# Cross-platform path handling
from pathlib import Path

# Works on all platforms
config_path = Path("config.yaml")
reports_dir = Path("reports")
```

### Command Execution
```python
import platform
import subprocess

system = platform.system().lower()

if system == "windows":
    # Windows-specific commands
    subprocess.run(['ping', '-n', '1', ip])
else:
    # Unix-specific commands
    subprocess.run(['ping', '-c', '1', ip])
```

### Environment Variables
```python
# Cross-platform environment handling
import os

# Virtual environment activation
if platform.system() == "Windows":
    activate_script = "venv\\Scripts\\activate"
else:
    activate_script = "venv/bin/activate"
```

## 🧪 Testing Cross-Platform Compatibility

Run the compatibility test:
```bash
# macOS/Linux
python test_cross_platform.py

# Windows
python test_cross_platform.py
```

This will test:
- ✅ Platform detection
- ✅ Command availability
- ✅ Python modules
- ✅ File paths
- ✅ Network utilities

## 🚨 Common Platform Issues

### macOS
- **Permission Issues**: May need to grant network access
- **Homebrew**: Ensure Homebrew is installed for automated setup
- **Firewall**: macOS firewall may block some scans

### Linux
- **SELinux**: May block network operations
- **Firewall**: Check iptables/ufw settings
- **Permissions**: Some operations require root privileges

### Windows
- **Antivirus**: May flag network scanning as suspicious
- **Firewall**: Windows Defender may block scans
- **UAC**: Some operations require admin privileges
- **nmap**: Manual installation required

## 🔧 Troubleshooting by Platform

### macOS Issues
```bash
# Fix Homebrew permissions
sudo chown -R $(whoami) /opt/homebrew

# Grant network access
sudo chmod +a "everyone allow read,write,execute" /usr/bin/ping

# Check firewall
sudo pfctl -s all
```

### Linux Issues
```bash
# Fix SELinux
sudo setsebool -P network_connect 1

# Check firewall
sudo ufw status
sudo iptables -L

# Fix permissions
sudo chmod +s /bin/ping
```

### Windows Issues
```cmd
# Run as administrator
# Right-click Command Prompt/PowerShell -> Run as administrator

# Check Windows Defender
# Windows Security -> Virus & threat protection -> Manage settings

# Add to PATH
# System Properties -> Environment Variables -> Path
```

## 📊 Performance by Platform

### macOS
- **Performance**: Excellent
- **Network Stack**: BSD-based, very stable
- **Python**: Native support, fast execution

### Linux
- **Performance**: Excellent
- **Network Stack**: Native, highly configurable
- **Python**: Native support, fast execution

### Windows
- **Performance**: Good (slightly slower due to abstraction)
- **Network Stack**: Windows-specific, may have limitations
- **Python**: Good support, slightly slower startup

## 🎯 Best Practices

### Cross-Platform Development
1. **Use pathlib**: Handles path differences automatically
2. **Platform detection**: Check platform before executing commands
3. **Error handling**: Graceful fallbacks for missing commands
4. **Testing**: Test on all target platforms

### Installation
1. **Automated scripts**: Use platform-specific installers
2. **Dependencies**: Document platform-specific requirements
3. **Fallbacks**: Provide manual installation instructions

### Usage
1. **Permissions**: Document required privileges
2. **Firewall**: Explain potential firewall issues
3. **Antivirus**: Warn about potential false positives

## 📝 Platform-Specific Notes

### macOS
- Most Unix-like experience
- Excellent Python support
- Homebrew provides easy package management
- May require granting permissions to terminal apps

### Linux
- Native Unix environment
- Excellent performance
- Multiple package managers supported
- SELinux may require configuration

### Windows
- Requires manual nmap installation
- May need admin privileges
- Antivirus software may interfere
- PowerShell provides better experience than CMD

## 🔄 Migration Between Platforms

### From macOS to Linux
- Most commands work identically
- Package manager syntax differs
- SELinux may require additional configuration

### From macOS/Linux to Windows
- Command syntax differs significantly
- Manual nmap installation required
- May need admin privileges
- Antivirus software considerations

### From Windows to macOS/Linux
- Commands become more powerful
- Automated installation available
- Better performance expected
- More granular control over network operations

The Network Mapper is designed to provide a consistent experience across all supported platforms while leveraging platform-specific optimizations where available. 