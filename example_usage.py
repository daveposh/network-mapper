#!/usr/bin/env python3
"""
Example usage of Network Mapper
"""

import asyncio
import sys
from network_mapper import NetworkMapper
from src.config import Config

async def example_scan():
    """Example network scan"""
    
    print("🔍 Running example network scan...")
    
    # Load configuration
    config = Config()
    
    # Initialize network mapper
    mapper = NetworkMapper(config)
    
    # Run a discovery scan on localhost
    print("Scanning localhost for demonstration...")
    results = await mapper.scan_network("127.0.0.1", "discovery")
    
    print(f"\n📊 Scan Results:")
    print(f"Found {len(results)} devices")
    
    for result in results:
        print(f"\nDevice: {result.ip_address}")
        print(f"  MAC: {result.mac_address or 'Unknown'}")
        print(f"  Manufacturer: {result.manufacturer or 'Unknown'}")
        print(f"  Device Type: {result.device_type or 'Unknown'}")
        print(f"  Open Ports: {result.open_ports}")
        print(f"  Protocols: {result.protocols}")

if __name__ == "__main__":
    try:
        asyncio.run(example_scan())
    except Exception as e:
        print(f"❌ Example failed: {e}")
        sys.exit(1) 