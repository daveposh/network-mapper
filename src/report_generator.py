"""
Report generation for network scan results
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import jinja2

from .config import Config

class ReportGenerator:
    """Generate reports in various formats"""
    
    def __init__(self, config: Config):
        self.config = config
        self.output_dir = Path(config.output_directory)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(self, results: List[Any], format_type: str):
        """Generate report in specified format"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == 'json':
            self._generate_json_report(results, timestamp)
        elif format_type == 'csv':
            self._generate_csv_report(results, timestamp)
        elif format_type == 'html':
            self._generate_html_report(results, timestamp)
    
    def _generate_json_report(self, results: List[Any], timestamp: str):
        """Generate JSON report"""
        
        report_data = {
            'scan_timestamp': timestamp,
            'total_devices': len(results),
            'devices': [self._result_to_dict(result) for result in results]
        }
        
        output_file = self.output_dir / f"network_scan_{timestamp}.json"
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
    
    def _generate_csv_report(self, results: List[Any], timestamp: str):
        """Generate CSV report"""
        
        output_file = self.output_dir / f"network_scan_{timestamp}.csv"
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'IP Address', 'MAC Address', 'Manufacturer', 'Device Type',
                'Operating System', 'Open Ports', 'Protocols', 'Scan Mode'
            ])
            
            # Write data
            for result in results:
                writer.writerow([
                    result.ip_address,
                    result.mac_address or '',
                    result.manufacturer or '',
                    result.device_type or '',
                    result.operating_system or '',
                    ','.join(map(str, result.open_ports)),
                    ','.join(result.protocols),
                    result.scan_mode
                ])
    
    def _generate_html_report(self, results: List[Any], timestamp: str):
        """Generate HTML report"""
        
        template = self._get_html_template()
        
        report_data = {
            'timestamp': timestamp,
            'total_devices': len(results),
            'devices': [self._result_to_dict(result) for result in results]
        }
        
        html_content = template.render(report_data)
        
        output_file = self.output_dir / f"network_scan_{timestamp}.html"
        with open(output_file, 'w') as f:
            f.write(html_content)
    
    def _result_to_dict(self, result: Any) -> Dict[str, Any]:
        """Convert scan result to dictionary"""
        
        return {
            'ip_address': result.ip_address,
            'mac_address': result.mac_address,
            'manufacturer': result.manufacturer,
            'device_type': result.device_type,
            'operating_system': result.operating_system,
            'open_ports': result.open_ports,
            'services': result.services,
            'protocols': result.protocols,
            'response_time': result.response_time,
            'scan_mode': result.scan_mode
        }
    
    def _get_html_template(self) -> jinja2.Template:
        """Get HTML template for reports"""
        
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Scan Report</title>
    <meta charset="UTF-8">
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #f5f5f5; 
            color: #333;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px; 
            text-align: center;
        }
        .header h1 { margin: 0 0 10px 0; font-size: 2.5em; }
        .header p { margin: 5px 0; opacity: 0.9; }
        .stats { 
            background: #f8f9fa; 
            padding: 20px; 
            border-bottom: 1px solid #dee2e6;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; font-size: 0.9em; }
        .devices { padding: 20px; }
        .device { 
            border: 1px solid #e9ecef; 
            margin: 15px 0; 
            padding: 20px; 
            border-radius: 10px; 
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s ease;
        }
        .device:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .device-header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f8f9fa;
        }
        .device-ip { 
            font-size: 1.5em; 
            font-weight: bold; 
            color: #495057; 
            margin: 0;
        }
        .device-type { 
            background: #667eea; 
            color: white; 
            padding: 5px 15px; 
            border-radius: 20px; 
            font-size: 0.9em;
        }
        .device-info { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 15px;
        }
        .info-section { background: #f8f9fa; padding: 15px; border-radius: 8px; }
        .info-section h4 { margin: 0 0 10px 0; color: #495057; font-size: 1.1em; }
        .info-item { 
            display: flex; 
            justify-content: space-between; 
            margin: 8px 0; 
            padding: 5px 0;
            border-bottom: 1px solid #e9ecef;
        }
        .info-label { font-weight: 500; color: #6c757d; }
        .info-value { font-weight: 600; color: #495057; }
        .ports { 
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
            padding: 15px; 
            border-radius: 8px; 
            margin: 10px 0;
        }
        .protocols { 
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); 
            padding: 15px; 
            border-radius: 8px; 
            margin: 10px 0;
        }
        .section-title { 
            font-weight: bold; 
            margin-bottom: 10px; 
            color: #495057;
            font-size: 1.1em;
        }
        .port-list, .protocol-list { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 8px; 
        }
        .port-item, .protocol-item { 
            background: rgba(255,255,255,0.7); 
            padding: 4px 12px; 
            border-radius: 15px; 
            font-size: 0.9em;
            font-weight: 500;
        }
        .manufacturer { color: #28a745; font-weight: 600; }
        .unknown { color: #dc3545; font-style: italic; }
        .footer { 
            background: #f8f9fa; 
            padding: 20px; 
            text-align: center; 
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }
        @media (max-width: 768px) {
            .device-info { grid-template-columns: 1fr; }
            .device-header { flex-direction: column; gap: 10px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Network Scan Report</h1>
            <p>Generated: {{ timestamp }}</p>
            <p>Scan completed successfully</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ total_devices }}</div>
                <div class="stat-label">Total Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ devices | selectattr('manufacturer', 'ne', 'Unknown') | list | length }}</div>
                <div class="stat-label">Identified Manufacturers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ devices | selectattr('device_type', 'ne', 'unknown') | list | length }}</div>
                <div class="stat-label">Classified Devices</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ devices | selectattr('open_ports') | list | length }}</div>
                <div class="stat-label">Devices with Open Ports</div>
            </div>
        </div>
        
        <div class="devices">
            {% for device in devices %}
            <div class="device">
                <div class="device-header">
                    <h3 class="device-ip">📍 {{ device.ip_address }}</h3>
                    <span class="device-type">🔧 {{ device.device_type or 'Unknown' }}</span>
                </div>
                
                <div class="device-info">
                    <div class="info-section">
                        <h4>📋 Device Information</h4>
                        <div class="info-item">
                            <span class="info-label">MAC Address:</span>
                            <span class="info-value">{{ device.mac_address or 'Not Found' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Manufacturer:</span>
                            <span class="info-value {% if device.manufacturer and device.manufacturer != 'Unknown' %}manufacturer{% else %}unknown{% endif %}">
                                {{ device.manufacturer or 'Unknown' }}
                            </span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Operating System:</span>
                            <span class="info-value">{{ device.operating_system or 'Unknown' }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Scan Mode:</span>
                            <span class="info-value">{{ device.scan_mode }}</span>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h4>⚡ Network Details</h4>
                        <div class="info-item">
                            <span class="info-label">Response Time:</span>
                            <span class="info-value">{{ device.response_time or 'Unknown' }}ms</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Open Ports:</span>
                            <span class="info-value">{{ device.open_ports | length }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Protocols:</span>
                            <span class="info-value">{{ device.protocols | length }}</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">Services:</span>
                            <span class="info-value">{{ device.services | length if device.services else 0 }}</span>
                        </div>
                    </div>
                </div>
                
                {% if device.open_ports %}
                <div class="ports">
                    <div class="section-title">🔓 Open Ports ({{ device.open_ports | length }})</div>
                    <div class="port-list">
                        {% for port in device.open_ports %}
                        <span class="port-item">Port {{ port }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
                
                {% if device.protocols %}
                <div class="protocols">
                    <div class="section-title">🌐 Protocols ({{ device.protocols | length }})</div>
                    <div class="protocol-list">
                        {% for protocol in device.protocols %}
                        <span class="protocol-item">{{ protocol }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
                
                {% if device.services %}
                <div class="services">
                    <div class="section-title">🔧 Services</div>
                    <div class="service-list">
                        {% for port, service in device.services.items() %}
                        <div class="service-item">
                            <strong>Port {{ port }}:</strong> {{ service }}
                        </div>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <div class="footer">
            <p>📊 Network Scan Report generated by Network Mapper</p>
            <p>Total scan time and detailed analysis completed</p>
        </div>
    </div>
</body>
</html>
        """
        
        return jinja2.Template(template_str) 