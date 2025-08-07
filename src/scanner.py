"""
Core network scanning functionality
"""

import asyncio
import nmap
import socket
import subprocess
import ipaddress
import platform
import sys
import re
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import time
import struct

from .config import Config

class NetworkScanner:
    """Core network scanning functionality"""
    
    def __init__(self, config: Config):
        self.config = config
        self.nm = nmap.PortScanner()
        self.executor = ThreadPoolExecutor(max_workers=config.max_concurrent_scans)
    
    async def discover_devices(self, target: str) -> List[Dict[str, Any]]:
        """Discover devices in the target network"""
        
        devices = []
        
        try:
            # Use nmap for initial discovery
            scan_args = f"-sn -n {target}"
            self.nm.scan(hosts=target, arguments=scan_args)
            
            # Get all MAC addresses from ARP table at once
            mac_addresses = self._get_all_mac_addresses()
            
            for host in self.nm.all_hosts():
                if self.nm[host].state() == 'up':
                    device_info = {
                        'ip': host,
                        'mac': mac_addresses.get(host),
                        'hostname': self._get_hostname(host),
                        'state': 'up'
                    }
                    devices.append(device_info)
        
        except Exception as e:
            # Fallback to ping-based discovery
            devices = await self._ping_discovery(target)
        
        return devices
    
    def _get_mac_address(self, ip: str) -> Optional[str]:
        """Get MAC address for an IP"""
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Windows ARP command
                result = subprocess.run(
                    ['arp', '-a', ip], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if ip in line:
                            parts = line.split()
                            if len(parts) >= 2:
                                mac = parts[1].replace('-', ':')
                                if len(mac) == 17:  # Valid MAC length
                                    return mac
                                    
            else:
                # For macOS/Linux, first try to get from existing ARP table
                try:
                    arp_result = subprocess.run(
                        ['arp', '-a'], 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    
                    if arp_result.returncode == 0:
                        lines = arp_result.stdout.strip().split('\n')
                        for line in lines:
                            if ip in line:
                                # Extract MAC address using regex
                                mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
                                if mac_match:
                                    return mac_match.group(0).replace('-', ':').upper()
                except Exception:
                    pass
                
                # If not found in ARP table, try to ping and then check again
                try:
                    # Ping the IP to populate ARP cache
                    ping_cmd = ['ping', '-c', '1', '-W', '1', ip] if system != "windows" else ['ping', '-n', '1', '-w', '1000', ip]
                    subprocess.run(ping_cmd, capture_output=True, timeout=3)
                    
                    # Now check ARP table again
                    arp_result = subprocess.run(
                        ['arp', '-a'], 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    
                    if arp_result.returncode == 0:
                        lines = arp_result.stdout.strip().split('\n')
                        for line in lines:
                            if ip in line:
                                # Extract MAC address using regex
                                mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
                                if mac_match:
                                    return mac_match.group(0).replace('-', ':').upper()
                except Exception:
                    pass
        
        except Exception:
            pass
        
        # Fallback: Try using nmap for MAC address detection
        try:
            nmap_result = self.nm.scan(hosts=ip, arguments='-sn')
            if ip in nmap_result.all_hosts():
                host_info = nmap_result[ip]
                if 'addresses' in host_info and 'mac' in host_info['addresses']:
                    return host_info['addresses']['mac']
        except Exception:
            pass
        
        return None
    
    def _get_all_mac_addresses(self) -> Dict[str, str]:
        """Get all MAC addresses from ARP table at once"""
        
        mac_addresses = {}
        
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Windows ARP command
                result = subprocess.run(
                    ['arp', '-a'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        # Parse Windows ARP output
                        if 'dynamic' in line.lower() or 'static' in line.lower():
                            parts = line.split()
                            if len(parts) >= 2:
                                ip = parts[0]
                                mac = parts[1].replace('-', ':')
                                if len(mac) == 17:  # Valid MAC length
                                    mac_addresses[ip] = mac.upper()
                                    
            else:
                # macOS/Linux ARP command
                result = subprocess.run(
                    ['arp', '-a'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        # Extract IP and MAC using regex
                        ip_match = re.search(r'\(([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\)', line)
                        mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', line)
                        
                        if ip_match and mac_match:
                            ip = ip_match.group(1)
                            mac = mac_match.group(0).replace('-', ':').upper()
                            mac_addresses[ip] = mac
        
        except Exception:
            pass
        
        return mac_addresses
    
    def _get_hostname(self, ip: str) -> Optional[str]:
        """Get hostname for an IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except Exception:
            return None
    
    async def _ping_discovery(self, target: str) -> List[Dict[str, Any]]:
        """Fallback ping-based discovery"""
        
        devices = []
        network = ipaddress.ip_network(target, strict=False)
        
        async def ping_host(ip):
            try:
                system = platform.system().lower()
                
                if system == "windows":
                    # Windows ping command
                    proc = await asyncio.create_subprocess_exec(
                        'ping', '-n', '1', '-w', '1000', str(ip),
                        stdout=asyncio.subprocess.DEVNULL,
                        stderr=asyncio.subprocess.DEVNULL
                    )
                else:
                    # Linux/macOS ping command
                    proc = await asyncio.create_subprocess_exec(
                        'ping', '-c', '1', '-W', '1', str(ip),
                        stdout=asyncio.subprocess.DEVNULL,
                        stderr=asyncio.subprocess.DEVNULL
                    )
                
                await proc.wait()
                
                if proc.returncode == 0:
                    return {
                        'ip': str(ip),
                        'mac': None,
                        'hostname': None,
                        'state': 'up'
                    }
            
            except Exception:
                pass
            
            return None
        
        # Scan network concurrently
        tasks = [ping_host(ip) for ip in network.hosts()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result and isinstance(result, dict):
                devices.append(result)
        
        return devices
    
    async def scan_services(self, ip: str) -> Dict[int, str]:
        """Scan for open ports and services"""
        
        services = {}
        
        try:
            # Use nmap for service detection
            scan_args = f"-sS -sV -O --version-intensity 5 -p- {ip}"
            self.nm.scan(hosts=ip, arguments=scan_args)
            
            if ip in self.nm.all_hosts():
                for proto in self.nm[ip].all_protocols():
                    ports = self.nm[ip][proto].keys()
                    for port in ports:
                        service_info = self.nm[ip][proto][port]
                        service_name = service_info.get('name', 'unknown')
                        services[port] = service_name
        
        except Exception as e:
            # Fallback to basic port scanning
            services = await self._basic_port_scan(ip)
        
        return services
    
    async def _basic_port_scan(self, ip: str) -> Dict[int, str]:
        """Basic port scanning fallback"""
        
        services = {}
        common_services = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
            80: 'http', 110: 'pop3', 143: 'imap', 443: 'https', 
            993: 'imaps', 995: 'pop3s', 3306: 'mysql', 3389: 'rdp',
            5432: 'postgresql', 8080: 'http-proxy', 8443: 'https-alt'
        }
        
        async def check_port(port):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=self.config.async_timeout
                )
                writer.close()
                await writer.wait_closed()
                return port, common_services.get(port, 'unknown')
            except Exception:
                return None
        
        # Check common ports concurrently
        tasks = [check_port(port) for port in common_services.keys()]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result and isinstance(result, tuple):
                port, service = result
                services[port] = service
        
        return services
    
    async def quick_port_scan(self, ip: str, ports: List[int]) -> List[int]:
        """Quick port scan for discovery mode"""
        
        open_ports = []
        
        async def check_port(port):
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=2
                )
                writer.close()
                await writer.wait_closed()
                return port
            except Exception:
                return None
        
        # Check ports concurrently
        tasks = [check_port(port) for port in ports]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result and isinstance(result, int):
                open_ports.append(result)
        
        return open_ports
    
    async def analyze_connections(self, ip: str) -> Dict[str, Any]:
        """Analyze network connections for detailed local scan"""
        
        connections = {
            'response_time': None,
            'tcp_connections': [],
            'udp_connections': [],
            'established_connections': []
        }
        
        try:
            # Measure response time
            start_time = time.time()
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, 80),
                timeout=self.config.async_timeout
            )
            writer.close()
            await writer.wait_closed()
            response_time = time.time() - start_time
            connections['response_time'] = response_time
        
        except Exception:
            pass
        
        # Get established connections (requires root/admin)
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Windows netstat command
                result = subprocess.run(
                    ['netstat', '-an'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
            else:
                # Linux/macOS netstat command
                result = subprocess.run(
                    ['netstat', '-an'], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if ip in line:
                        connections['established_connections'].append(line.strip())
        
        except Exception:
            pass
        
        return connections 