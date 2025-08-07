#!/usr/bin/env python3
"""
Network Mapper - Comprehensive network discovery and analysis tool
"""

import asyncio
import click
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

from src.scanner import NetworkScanner
from src.protocol_analyzer import ProtocolAnalyzer
from src.device_classifier import DeviceClassifier
from src.mac_lookup import MACLookup
from src.report_generator import ReportGenerator
from src.config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

@dataclass
class ScanResult:
    """Represents a single device scan result"""
    ip_address: str
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    manufacturer: Optional[str] = None
    device_type: Optional[str] = None
    operating_system: Optional[str] = None
    open_ports: List[int] = None
    services: Dict[str, str] = None
    protocols: List[str] = None
    response_time: Optional[float] = None
    last_seen: Optional[datetime] = None
    scan_mode: str = "unknown"
    
    def __post_init__(self):
        if self.open_ports is None:
            self.open_ports = []
        if self.services is None:
            self.services = {}
        if self.protocols is None:
            self.protocols = []

class NetworkMapper:
    """Main network mapping application"""
    
    def __init__(self, config: Config):
        self.config = config
        self.scanner = NetworkScanner(config)
        self.protocol_analyzer = ProtocolAnalyzer(config)
        self.device_classifier = DeviceClassifier(config)
        self.mac_lookup = MACLookup(config)
        self.report_generator = ReportGenerator(config)
        
    async def scan_network(self, target: str, mode: str, detailed: bool = False) -> List[ScanResult]:
        """Main scanning method"""
        
        console.print(f"[bold blue]Starting {mode} scan of {target}[/bold blue]")
        
        # Initialize scan components
        scan_results = []
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            
            # Phase 1: Basic network discovery
            task = progress.add_task("Discovering devices...", total=None)
            devices = await self.scanner.discover_devices(target)
            progress.update(task, completed=True)
            
            # Phase 2: Detailed analysis based on mode
            if mode == "local" and detailed:
                task = progress.add_task("Performing detailed local analysis...", total=len(devices))
                for device in devices:
                    result = await self._detailed_local_scan(device)
                    scan_results.append(result)
                    progress.advance(task)
            else:
                task = progress.add_task("Performing network discovery...", total=len(devices))
                for device in devices:
                    result = await self._discovery_scan(device)
                    scan_results.append(result)
                    progress.advance(task)
        
        return scan_results
    
    async def _detailed_local_scan(self, device: Dict[str, Any]) -> ScanResult:
        """Perform detailed local scan with deep analysis"""
        
        result = ScanResult(
            ip_address=device['ip'],
            mac_address=device.get('mac'),
            scan_mode="local_detailed"
        )
        
        # MAC address analysis
        if result.mac_address:
            result.manufacturer = await self.mac_lookup.get_manufacturer(result.mac_address)
        
        # Device classification
        result.device_type = await self.device_classifier.classify_device(device)
        result.operating_system = await self.device_classifier.detect_os(device)
        
        # Protocol analysis
        protocols = await self.protocol_analyzer.analyze_device(device['ip'])
        result.protocols = protocols
        
        # Service discovery
        services = await self.scanner.scan_services(device['ip'])
        result.services = services
        result.open_ports = list(services.keys())
        
        # Connection analysis
        connections = await self.scanner.analyze_connections(device['ip'])
        result.response_time = connections.get('response_time')
        
        return result
    
    async def _discovery_scan(self, device: Dict[str, Any]) -> ScanResult:
        """Perform quick discovery scan"""
        
        result = ScanResult(
            ip_address=device['ip'],
            mac_address=device.get('mac'),
            scan_mode="discovery"
        )
        
        # Basic MAC analysis
        if result.mac_address:
            try:
                result.manufacturer = await self.mac_lookup.get_manufacturer(result.mac_address)
            except Exception as e:
                console.print(f"[yellow]Warning: MAC lookup failed for {result.mac_address}: {e}[/yellow]")
        
        # Quick device classification
        try:
            result.device_type = await self.device_classifier.quick_classify(device)
        except Exception as e:
            console.print(f"[yellow]Warning: Device classification failed for {device['ip']}: {e}[/yellow]")
            result.device_type = "unknown"
        
        # Basic port scan
        try:
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080]
            open_ports = await self.scanner.quick_port_scan(device['ip'], common_ports)
            result.open_ports = open_ports
        except Exception as e:
            console.print(f"[yellow]Warning: Port scan failed for {device['ip']}: {e}[/yellow]")
            result.open_ports = []
        
        return result

@click.command()
@click.option('--mode', type=click.Choice(['local', 'discovery']), 
              default='discovery', help='Scan mode')
@click.option('--target', required=True, help='Target IP range (CIDR notation)')
@click.option('--detailed', is_flag=True, help='Enable detailed scanning (local mode)')
@click.option('--quick', is_flag=True, help='Enable quick scanning (discovery mode)')
@click.option('--output', type=click.Choice(['json', 'csv', 'html', 'console']), 
              default='console', help='Output format')
@click.option('--timeout', type=int, default=30, help='Scan timeout in seconds')
@click.option('--config', type=click.Path(exists=True), help='Configuration file path')
def main(mode: str, target: str, detailed: bool, quick: bool, 
         output: str, timeout: int, config: Optional[str]):
    """Network Mapper - Comprehensive network discovery tool
    
    EXAMPLES:
        python network_mapper.py --target 192.168.1.0/24
        python network_mapper.py --mode local --target 192.168.1.0/24 --detailed
        python network_mapper.py --target 192.168.1.0/24 --output html
        python network_mapper.py --target 192.168.1.0/24 --output json
    """
    
    try:
        # Load configuration
        config_path = config or "config.yaml"
        config_obj = Config.from_file(config_path)
        config_obj.timeout = timeout
        
        # Initialize network mapper
        mapper = NetworkMapper(config_obj)
        
        # Run scan
        results = asyncio.run(
            mapper.scan_network(target, mode, detailed)
        )
        
        # Generate output
        if output == 'console':
            _display_console_results(results, mode)
        else:
            mapper.report_generator.generate_report(results, output)
            
        console.print(f"\n[bold green]Scan completed! Found {len(results)} devices.[/bold green]")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Scan interrupted by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error: {str(e)}[/red]")
        logger.exception("Scan failed")
        sys.exit(1)

def _display_console_results(results: List[ScanResult], mode: str):
    """Display results in console format"""
    
    table = Table(title=f"Network Scan Results - {mode.title()} Mode")
    
    # Add columns based on mode
    table.add_column("IP Address", style="cyan")
    table.add_column("MAC Address", style="magenta")
    table.add_column("Manufacturer", style="green")
    table.add_column("Device Type", style="yellow")
    
    if mode == "local":
        table.add_column("OS", style="blue")
        table.add_column("Open Ports", style="red")
        table.add_column("Protocols", style="white")
    
    for result in results:
        row = [
            result.ip_address,
            result.mac_address or "Unknown",
            result.manufacturer or "Unknown",
            result.device_type or "Unknown"
        ]
        
        if mode == "local":
            row.extend([
                result.operating_system or "Unknown",
                ", ".join(map(str, result.open_ports)) or "None",
                ", ".join(result.protocols) or "None"
            ])
        
        table.add_row(*row)
    
    console.print(table)

if __name__ == "__main__":
    main() 