#!/usr/bin/env python3
"""
Test MAC address lookup functionality
"""

import asyncio
import sys
from src.config import Config
from src.mac_lookup import MACLookup

async def test_mac_lookup():
    """Test MAC address lookup with various MAC addresses"""
    
    print("🧪 Testing MAC Address Lookup...")
    
    # Load configuration
    config = Config()
    mac_lookup = MACLookup(config)
    
    # Test MAC addresses
    test_macs = [
        "00:0C:29:12:34:56",  # VMware
        "00:1B:63:45:67:89",  # Apple
        "00:0C:41:23:45:67",  # Cisco
        "00:0D:0B:78:9A:BC",  # Cisco
        "00:1C:58:AB:CD:EF",  # Apple
        "00:23:DF:12:34:56",  # Apple
        "00:0C:29:AB:CD:EF",  # VMware
        "00:1B:63:78:9A:BC",  # Apple
        "00:0C:41:45:67:89",  # Cisco
        "00:0D:0B:23:45:67",  # Cisco
        "AA:BB:CC:DD:EE:FF",  # Unknown
        "12:34:56:78:9A:BC",  # Unknown
    ]
    
    print(f"\n📋 Testing {len(test_macs)} MAC addresses...")
    print("=" * 60)
    
    for i, mac in enumerate(test_macs, 1):
        manufacturer = await mac_lookup.get_manufacturer(mac)
        status = "✅" if manufacturer and manufacturer != "Unknown" else "❌"
        print(f"{i:2d}. {status} {mac} -> {manufacturer or 'Unknown'}")
    
    print("=" * 60)
    
    # Test cache functionality
    print(f"\n🔍 Testing cache functionality...")
    start_time = asyncio.get_event_loop().time()
    for _ in range(5):
        await mac_lookup.get_manufacturer("00:0C:29:12:34:56")
    end_time = asyncio.get_event_loop().time()
    
    print(f"Cache test completed in {end_time - start_time:.3f} seconds")
    
    print(f"\n🎉 MAC lookup test completed!")
    print(f"Cache size: {len(mac_lookup.cache)} entries")

if __name__ == "__main__":
    try:
        asyncio.run(test_mac_lookup())
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1) 