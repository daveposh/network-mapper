"""
Device classification and OS detection
"""

import asyncio
import re
import socket
import platform
import sys
from typing import Dict, List, Any, Optional
import nmap

from .config import Config

class DeviceClassifier:
    """Classify devices and detect operating systems"""
    
    def __init__(self, config: Config):
        self.config = config
        self.nm = nmap.PortScanner()
        self.device_patterns = self._load_device_patterns()
        self.os_patterns = self._load_os_patterns()
    
    def _load_device_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load device classification patterns"""
        return {
            'router': {
                'ports': [80, 443, 22, 23],
                'services': ['http', 'https', 'ssh', 'telnet'],
                'patterns': ['router', 'gateway', 'cisco', 'juniper', 'fortinet'],
                'priority': 1
            },
            'switch': {
                'ports': [22, 23, 80, 443],
                'services': ['ssh', 'telnet', 'http', 'https'],
                'patterns': ['switch', 'catalyst', 'nexus'],
                'priority': 2
            },
            'server': {
                'ports': [22, 80, 443, 3306, 5432, 27017],
                'services': ['ssh', 'http', 'https', 'mysql', 'postgresql', 'mongodb'],
                'patterns': ['server', 'apache', 'nginx', 'mysql', 'postgresql'],
                'priority': 3
            },
            'printer': {
                'ports': [80, 443, 631, 9100],
                'services': ['http', 'https', 'ipp', 'printer'],
                'patterns': ['printer', 'hp', 'canon', 'epson', 'brother'],
                'priority': 4
            },
            'camera': {
                'ports': [80, 443, 554, 8000],
                'services': ['http', 'https', 'rtsp'],
                'patterns': ['camera', 'ipcam', 'dvr', 'nvr'],
                'priority': 5
            },
            'iot': {
                'ports': [80, 443, 1883, 8883],
                'services': ['http', 'https', 'mqtt'],
                'patterns': ['iot', 'smart', 'home', 'automation'],
                'priority': 6
            },
            'mobile': {
                'ports': [80, 443],
                'services': ['http', 'https'],
                'patterns': ['mobile', 'android', 'ios', 'phone'],
                'priority': 7
            },
            'workstation': {
                'ports': [22, 80, 443, 3389],
                'services': ['ssh', 'http', 'https', 'rdp'],
                'patterns': ['windows', 'linux', 'mac', 'desktop'],
                'priority': 8
            }
        }
    
    def _load_os_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load OS detection patterns"""
        return {
            'windows': {
                'ports': [135, 139, 445, 3389],
                'services': ['msrpc', 'netbios-ssn', 'microsoft-ds', 'rdp'],
                'patterns': ['windows', 'microsoft', 'nt', 'win'],
                'ttl_range': (128, 128)
            },
            'linux': {
                'ports': [22, 80, 443],
                'services': ['ssh', 'http', 'https'],
                'patterns': ['linux', 'ubuntu', 'debian', 'centos', 'redhat'],
                'ttl_range': (64, 64)
            },
            'macos': {
                'ports': [22, 80, 443, 548],
                'services': ['ssh', 'http', 'https', 'afp'],
                'patterns': ['mac', 'darwin', 'apple'],
                'ttl_range': (64, 64)
            },
            'ios': {
                'ports': [22, 23, 80, 443],
                'services': ['ssh', 'telnet', 'http', 'https'],
                'patterns': ['cisco', 'ios', 'router'],
                'ttl_range': (255, 255)
            },
            'android': {
                'ports': [80, 443],
                'services': ['http', 'https'],
                'patterns': ['android', 'mobile'],
                'ttl_range': (64, 64)
            }
        }
    
    async def classify_device(self, device: Dict[str, Any]) -> Optional[str]:
        """Classify device type based on characteristics"""
        
        device_score = {}
        ip = device['ip']
        
        # Get open ports and services
        open_ports = await self._get_open_ports(ip)
        services = await self._get_services(ip)
        
        # Score each device type
        for device_type, pattern in self.device_patterns.items():
            score = 0
            
            # Port matching
            for port in open_ports:
                if port in pattern['ports']:
                    score += 2
            
            # Service matching
            for service in services:
                if service in pattern['services']:
                    score += 3
            
            # Pattern matching in hostname/banner
            hostname = device.get('hostname', '').lower()
            for pattern_str in pattern['patterns']:
                if pattern_str in hostname:
                    score += 5
            
            device_score[device_type] = score
        
        # Return device type with highest score
        if device_score:
            best_match = max(device_score.items(), key=lambda x: x[1])
            if best_match[1] > 0:
                return best_match[0]
        
        return 'unknown'
    
    async def quick_classify(self, device: Dict[str, Any]) -> Optional[str]:
        """Quick device classification for discovery mode"""
        
        ip = device['ip']
        
        # Quick port scan for common ports
        common_ports = [22, 23, 80, 443, 3389, 9100]
        open_ports = await self._quick_port_check(ip, common_ports)
        
        # Simple classification based on ports
        if 9100 in open_ports:
            return 'printer'
        elif 3389 in open_ports:
            return 'workstation'
        elif 22 in open_ports and 80 in open_ports:
            return 'server'
        elif 80 in open_ports or 443 in open_ports:
            return 'device'
        else:
            return 'unknown'
    
    async def detect_os(self, device: Dict[str, Any]) -> Optional[str]:
        """Detect operating system"""
        
        ip = device['ip']
        
        try:
            # Use nmap for OS detection
            scan_args = f"-O --osscan-guess {ip}"
            self.nm.scan(hosts=ip, arguments=scan_args)
            
            if ip in self.nm.all_hosts():
                os_info = self.nm[ip].get('osmatch', [])
                if os_info:
                    return os_info[0]['name']
        
        except Exception:
            pass
        
        # Fallback to TTL-based detection
        return await self._detect_os_by_ttl(ip)
    
    async def _detect_os_by_ttl(self, ip: str) -> Optional[str]:
        """Detect OS using TTL values"""
        
        try:
            system = platform.system().lower()
            
            if system == "windows":
                # Windows ping command
                proc = await asyncio.create_subprocess_exec(
                    'ping', '-n', '1', ip,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            else:
                # Linux/macOS ping command
                proc = await asyncio.create_subprocess_exec(
                    'ping', '-c', '1', ip,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
            
            stdout, stderr = await proc.communicate()
            
            if proc.returncode == 0:
                # Extract TTL from ping output
                output = stdout.decode()
                
                # Handle different TTL patterns for different platforms
                ttl_patterns = [
                    r'ttl=(\d+)',  # Linux/macOS
                    r'TTL=(\d+)',  # Windows
                    r'Time to live=(\d+)'  # Alternative Windows format
                ]
                
                for pattern in ttl_patterns:
                    ttl_match = re.search(pattern, output, re.IGNORECASE)
                    if ttl_match:
                        ttl = int(ttl_match.group(1))
                        
                        # Classify based on TTL
                        if ttl <= 64:
                            return 'Linux/macOS'
                        elif ttl <= 128:
                            return 'Windows'
                        elif ttl <= 255:
                            return 'Network Device'
                        else:
                            return 'Unknown'
        
        except Exception:
            pass
        
        return None
    
    async def _get_open_ports(self, ip: str) -> List[int]:
        """Get open ports for a device"""
        
        open_ports = []
        
        try:
            # Quick port scan
            scan_args = f"-sS -F {ip}"
            self.nm.scan(hosts=ip, arguments=scan_args)
            
            if ip in self.nm.all_hosts():
                for proto in self.nm[ip].all_protocols():
                    ports = self.nm[ip][proto].keys()
                    open_ports.extend(ports)
        
        except Exception:
            # Fallback to basic port checking
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            open_ports = await self._quick_port_check(ip, common_ports)
        
        return open_ports
    
    async def _get_services(self, ip: str) -> List[str]:
        """Get services running on a device"""
        
        services = []
        
        try:
            # Service detection scan
            scan_args = f"-sV --version-intensity 3 {ip}"
            self.nm.scan(hosts=ip, arguments=scan_args)
            
            if ip in self.nm.all_hosts():
                for proto in self.nm[ip].all_protocols():
                    ports = self.nm[ip][proto].keys()
                    for port in ports:
                        service_info = self.nm[ip][proto][port]
                        service_name = service_info.get('name', 'unknown')
                        services.append(service_name)
        
        except Exception:
            pass
        
        return services
    
    async def _quick_port_check(self, ip: str, ports: List[int]) -> List[int]:
        """Quick port availability check"""
        
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