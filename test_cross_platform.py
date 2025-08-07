#!/usr/bin/env python3
"""
Cross-platform compatibility test for Network Mapper
"""

import platform
import sys
import os
import subprocess
from pathlib import Path

def test_platform_compatibility():
    """Test cross-platform compatibility"""
    
    print("🧪 Testing Cross-Platform Compatibility...")
    print(f"Platform: {platform.system()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Python Executable: {sys.executable}")
    
    # Test platform-specific commands
    system = platform.system().lower()
    
    print(f"\n🔍 Testing platform-specific commands...")
    
    # Test ping command
    try:
        if system == "windows":
            result = subprocess.run(['ping', '-n', '1', '127.0.0.1'], 
                                  capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['ping', '-c', '1', '127.0.0.1'], 
                                  capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Ping command working")
        else:
            print("⚠️  Ping command failed")
    except Exception as e:
        print(f"❌ Ping command error: {e}")
    
    # Test ARP command
    try:
        if system == "windows":
            result = subprocess.run(['arp', '-a'], 
                                  capture_output=True, text=True, timeout=5)
        else:
            result = subprocess.run(['arp', '-n'], 
                                  capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ ARP command working")
        else:
            print("⚠️  ARP command failed")
    except Exception as e:
        print(f"❌ ARP command error: {e}")
    
    # Test nmap
    try:
        result = subprocess.run(['nmap', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Nmap found and working")
        else:
            print("⚠️  Nmap not working properly")
    except FileNotFoundError:
        print("❌ Nmap not found - please install nmap")
    except Exception as e:
        print(f"❌ Nmap error: {e}")
    
    # Test Python modules
    print(f"\n📦 Testing Python modules...")
    
    required_modules = [
        'asyncio', 'aiohttp', 'click', 'rich', 'jinja2', 
        'yaml', 'nmap', 'scapy', 'requests'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - not installed")
    
    # Test file paths
    print(f"\n📁 Testing file paths...")
    
    paths_to_check = [
        'network_mapper.py',
        'requirements.txt',
        'config.yaml',
        'src/',
        'src/__init__.py',
        'src/config.py',
        'src/scanner.py'
    ]
    
    for path in paths_to_check:
        if Path(path).exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path} - missing")
    
    print(f"\n🎉 Cross-platform compatibility test completed!")
    print(f"Platform: {platform.system()}")
    print(f"Ready for network scanning!")

if __name__ == "__main__":
    test_platform_compatibility() 