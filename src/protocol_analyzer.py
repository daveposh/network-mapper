"""
Protocol analysis and deep packet inspection
"""

import asyncio
import socket
import struct
from typing import List, Dict, Any, Optional
import aiohttp
import json

from .config import Config

class ProtocolAnalyzer:
    """Analyze network protocols and application layer data"""
    
    def __init__(self, config: Config):
        self.config = config
        self.protocol_patterns = self._load_protocol_patterns()
    
    def _load_protocol_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Load protocol detection patterns"""
        return {
            'http': {
                'ports': [80, 8080, 8443],
                'patterns': [b'GET ', b'POST ', b'HTTP/'],
                'name': 'HTTP'
            },
            'https': {
                'ports': [443, 8443],
                'patterns': [b'\x16\x03', b'\x17\x03'],  # TLS handshake
                'name': 'HTTPS'
            },
            'ssh': {
                'ports': [22],
                'patterns': [b'SSH-'],
                'name': 'SSH'
            },
            'ftp': {
                'ports': [21],
                'patterns': [b'220 ', b'FTP'],
                'name': 'FTP'
            },
            'smtp': {
                'ports': [25, 587],
                'patterns': [b'220 ', b'SMTP'],
                'name': 'SMTP'
            },
            'pop3': {
                'ports': [110, 995],
                'patterns': [b'+OK ', b'POP3'],
                'name': 'POP3'
            },
            'imap': {
                'ports': [143, 993],
                'patterns': [b'* OK ', b'IMAP'],
                'name': 'IMAP'
            },
            'dns': {
                'ports': [53],
                'patterns': [b'\x00\x01', b'\x00\x02'],  # DNS query patterns
                'name': 'DNS'
            },
            'mysql': {
                'ports': [3306],
                'patterns': [b'\x0a'],  # MySQL protocol version
                'name': 'MySQL'
            },
            'postgresql': {
                'ports': [5432],
                'patterns': [b'\x00\x00\x00\x08'],  # PostgreSQL startup message
                'name': 'PostgreSQL'
            },
            'rdp': {
                'ports': [3389],
                'patterns': [b'\x03\x00'],  # RDP protocol
                'name': 'RDP'
            }
        }
    
    async def analyze_device(self, ip: str) -> List[str]:
        """Analyze protocols used by a device"""
        
        protocols = []
        
        # Test common protocols
        for protocol, info in self.protocol_patterns.items():
            if await self._test_protocol(ip, protocol, info):
                protocols.append(info['name'])
        
        # Additional protocol detection
        additional_protocols = await self._detect_additional_protocols(ip)
        protocols.extend(additional_protocols)
        
        return list(set(protocols))  # Remove duplicates
    
    async def _test_protocol(self, ip: str, protocol: str, info: Dict[str, Any]) -> bool:
        """Test if a specific protocol is supported"""
        
        for port in info['ports']:
            try:
                # Try to connect and send a probe
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=self.config.async_timeout
                )
                
                # Send a basic probe based on protocol
                probe = self._get_protocol_probe(protocol)
                if probe:
                    writer.write(probe)
                    await writer.drain()
                
                # Read response
                try:
                    response = await asyncio.wait_for(
                        reader.read(1024),
                        timeout=2
                    )
                    
                    # Check for protocol patterns
                    for pattern in info['patterns']:
                        if pattern in response:
                            writer.close()
                            await writer.wait_closed()
                            return True
                
                except asyncio.TimeoutError:
                    pass
                
                writer.close()
                await writer.wait_closed()
            
            except Exception:
                continue
        
        return False
    
    def _get_protocol_probe(self, protocol: str) -> Optional[bytes]:
        """Get appropriate probe for protocol detection"""
        
        probes = {
            'http': b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n',
            'https': b'\x16\x03\x01\x00\x01\x01',  # TLS ClientHello
            'ssh': b'SSH-2.0-OpenSSH_8.1\r\n',
            'ftp': b'USER anonymous\r\n',
            'smtp': b'EHLO localhost\r\n',
            'pop3': b'USER test\r\n',
            'imap': b'a001 CAPABILITY\r\n',
            'dns': b'\x00\x01\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01',
            'mysql': b'\x0a',  # MySQL protocol version
            'postgresql': b'\x00\x00\x00\x08\x04\xd2\x16\x2f',  # PostgreSQL startup
            'rdp': b'\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00'  # RDP connection request
        }
        
        return probes.get(protocol)
    
    async def _detect_additional_protocols(self, ip: str) -> List[str]:
        """Detect additional protocols not in standard patterns"""
        
        additional_protocols = []
        
        # Test for common application protocols
        app_protocols = [
            (8080, 'HTTP-Proxy'),
            (8443, 'HTTPS-Alt'),
            (8888, 'HTTP-Alt'),
            (9000, 'Jenkins'),
            (9090, 'HTTP-Alt'),
            (27017, 'MongoDB'),
            (6379, 'Redis'),
            (11211, 'Memcached'),
            (5672, 'AMQP'),
            (1883, 'MQTT'),
            (8883, 'MQTT-SSL')
        ]
        
        for port, protocol_name in app_protocols:
            try:
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(ip, port),
                    timeout=2
                )
                writer.close()
                await writer.wait_closed()
                additional_protocols.append(protocol_name)
            except Exception:
                continue
        
        return additional_protocols
    
    async def analyze_application_layer(self, ip: str, port: int) -> Dict[str, Any]:
        """Deep analysis of application layer protocols"""
        
        analysis = {
            'protocol': 'unknown',
            'version': None,
            'banner': None,
            'capabilities': []
        }
        
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port),
                timeout=self.config.async_timeout
            )
            
            # Send generic probe
            probe = b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'
            writer.write(probe)
            await writer.drain()
            
            # Read response
            try:
                response = await asyncio.wait_for(
                    reader.read(1024),
                    timeout=3
                )
                
                # Analyze response
                analysis['banner'] = response.decode('utf-8', errors='ignore')[:200]
                analysis['protocol'] = self._identify_protocol_from_response(response)
                analysis['version'] = self._extract_version_from_response(response)
                analysis['capabilities'] = self._extract_capabilities_from_response(response)
            
            except asyncio.TimeoutError:
                pass
            
            writer.close()
            await writer.wait_closed()
        
        except Exception:
            pass
        
        return analysis
    
    def _identify_protocol_from_response(self, response: bytes) -> str:
        """Identify protocol from response data"""
        
        response_str = response.decode('utf-8', errors='ignore').lower()
        
        if b'HTTP/' in response:
            return 'HTTP'
        elif b'SSH-' in response:
            return 'SSH'
        elif b'FTP' in response:
            return 'FTP'
        elif b'SMTP' in response:
            return 'SMTP'
        elif b'POP3' in response:
            return 'POP3'
        elif b'IMAP' in response:
            return 'IMAP'
        elif b'MySQL' in response:
            return 'MySQL'
        elif b'PostgreSQL' in response:
            return 'PostgreSQL'
        else:
            return 'Unknown'
    
    def _extract_version_from_response(self, response: bytes) -> Optional[str]:
        """Extract version information from response"""
        
        response_str = response.decode('utf-8', errors='ignore')
        
        # Common version patterns
        import re
        version_patterns = [
            r'HTTP/(\d+\.\d+)',
            r'SSH-(\d+\.\d+)',
            r'FTP server \(([^)]+)\)',
            r'PostgreSQL/(\d+\.\d+)',
            r'MySQL/(\d+\.\d+)'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, response_str)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_capabilities_from_response(self, response: bytes) -> List[str]:
        """Extract capabilities from response"""
        
        capabilities = []
        response_str = response.decode('utf-8', errors='ignore').lower()
        
        # Common capability indicators
        if 'ssl' in response_str or 'tls' in response_str:
            capabilities.append('SSL/TLS')
        if 'authentication' in response_str:
            capabilities.append('Authentication')
        if 'compression' in response_str:
            capabilities.append('Compression')
        if 'encryption' in response_str:
            capabilities.append('Encryption')
        
        return capabilities 