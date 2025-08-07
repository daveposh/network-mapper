"""
Configuration management for Network Mapper
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class Config:
    """Configuration class for Network Mapper"""
    
    # Scan settings
    timeout: int = 30
    max_concurrent_scans: int = 10
    retry_attempts: int = 3
    
    # Network settings
    default_ports: list = field(default_factory=lambda: [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 
        3306, 3389, 5432, 8080, 8443
    ])
    
    # Detailed scan settings
    detailed_scan_ports: list = field(default_factory=lambda: list(range(1, 1025)))
    service_detection: bool = True
    os_detection: bool = True
    protocol_analysis: bool = True
    
    # Discovery scan settings
    quick_scan_ports: list = field(default_factory=lambda: [
        21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 
        3306, 3389, 5432, 8080, 8443
    ])
    
    # MAC address lookup
    mac_lookup_enabled: bool = True
    mac_database_path: Optional[str] = None
    
    # Output settings
    output_directory: str = "reports"
    log_level: str = "INFO"
    
    # Performance settings
    async_timeout: int = 10
    connection_pool_size: int = 100
    
    @classmethod
    def from_file(cls, config_path: str) -> 'Config':
        """Load configuration from YAML file"""
        config_path = Path(config_path)
        
        if not config_path.exists():
            return cls()
        
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        
        return cls(**config_data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        return {
            'timeout': self.timeout,
            'max_concurrent_scans': self.max_concurrent_scans,
            'retry_attempts': self.retry_attempts,
            'default_ports': self.default_ports,
            'detailed_scan_ports': self.detailed_scan_ports,
            'service_detection': self.service_detection,
            'os_detection': self.os_detection,
            'protocol_analysis': self.protocol_analysis,
            'quick_scan_ports': self.quick_scan_ports,
            'mac_lookup_enabled': self.mac_lookup_enabled,
            'mac_database_path': self.mac_database_path,
            'output_directory': self.output_directory,
            'log_level': self.log_level,
            'async_timeout': self.async_timeout,
            'connection_pool_size': self.connection_pool_size
        }
    
    def save(self, config_path: str):
        """Save configuration to YAML file"""
        config_path = Path(config_path)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False) 