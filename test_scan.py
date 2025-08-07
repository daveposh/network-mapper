#!/usr/bin/env python3
"""
Test script for Network Mapper
"""

import asyncio
import sys
from src.config import Config
from src.scanner import NetworkScanner
from src.mac_lookup import MACLookup

async def test_basic_functionality():
    """Test basic network mapper functionality"""
    
    print("🧪 Testing Network Mapper functionality...")
    
    # Load configuration
    config = Config()
    
    # Test scanner
    print("📡 Testing network scanner...")
    scanner = NetworkScanner(config)
    
    # Test MAC lookup
    print("🔍 Testing MAC address lookup...")
    mac_lookup = MACLookup(config)
    
    # Test with a known MAC address (Cisco)
    test_mac = "00:0C:29:12:34:56"
    manufacturer = await mac_lookup.get_manufacturer(test_mac)
    print(f"MAC {test_mac} -> Manufacturer: {manufacturer}")
    
    print("✅ Basic functionality tests completed!")

if __name__ == "__main__":
    try:
        asyncio.run(test_basic_functionality())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1) 