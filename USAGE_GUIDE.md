# Network Mapper Usage Guide

## 🚀 Quick Start

### macOS/Linux
1. **Install the tool:**
   ```bash
   ./install.sh
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Run your first scan:**
   ```bash
   python network_mapper.py --mode discovery --target 192.168.1.0/24
   ```

### Windows
1. **Install the tool:**
   ```cmd
   install.bat
   ```

2. **Activate the virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Run your first scan:**
   ```cmd
   python network_mapper.py --mode discovery --target 192.168.1.0/24
   ```

## 📋 Scan Modes

### Discovery Mode (Rogue Device Detection)
Quick scanning for finding unauthorized devices and basic network enumeration.

```bash
# Basic discovery scan
python network_mapper.py --mode discovery --target 192.168.1.0/24

# Quick discovery with CSV output
python network_mapper.py --mode discovery --target 192.168.1.0/24 --quick --output csv

# Discovery scan with JSON output
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output json
```

**What it detects:**
- Device presence and basic connectivity
- MAC address manufacturer identification
- Basic device type classification
- Open ports on common services
- Network topology mapping

### Local Mode (Detailed Analysis)
Deep analysis with comprehensive device profiling and protocol analysis.

```bash
# Detailed local scan
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed

# Detailed scan with HTML report
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed --output html

# Detailed scan with JSON output
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed --output json
```

**What it detects:**
- Deep protocol analysis (HTTP, HTTPS, SSH, FTP, SMTP, DNS, MySQL, PostgreSQL, RDP)
- Operating system detection using multiple methods
- Comprehensive device classification (router, server, printer, camera, IoT, workstation)
- Service enumeration and version detection
- Connection analysis and dependency mapping
- Response time and performance metrics

## 🎯 Use Cases

### 1. Home Network Security
```bash
# Scan your home network for all devices
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output html
```

### 2. Corporate Network Analysis
```bash
# Detailed analysis of corporate network
python network_mapper.py --mode local --target 10.0.0.0/16 --detailed --output json
```

### 3. Rogue Device Detection
```bash
# Quick scan to find unauthorized devices
python network_mapper.py --mode discovery --target 172.16.0.0/12 --quick --output csv
```

### 4. Server Infrastructure Mapping
```bash
# Map server infrastructure with detailed analysis
python network_mapper.py --mode local --target 10.10.0.0/24 --detailed --output html
```

### 5. IoT Device Discovery
```bash
# Find and classify IoT devices
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output console
```

## 📊 Output Formats

### Console Output
Real-time scanning progress with formatted tables:
```bash
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output console
```

### HTML Reports
Professional web reports with device details:
```bash
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output html
```

### JSON Output
Structured data for programmatic use:
```bash
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output json
```

### CSV Output
Spreadsheet-compatible format:
```bash
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output csv
```

## 🔧 Configuration

### Custom Configuration File
Create a custom `config.yaml` file:

```yaml
# Scan settings
timeout: 30
max_concurrent_scans: 10
retry_attempts: 3

# Network settings
default_ports: [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080, 8443]

# Detailed scan settings
detailed_scan_ports: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080, 8443]
service_detection: true
os_detection: true
protocol_analysis: true

# Output settings
output_directory: "reports"
log_level: "INFO"
```

Use custom configuration:
```bash
python network_mapper.py --mode discovery --target 192.168.1.0/24 --config custom_config.yaml
```

## 🛠️ Advanced Usage

### Programmatic Usage
```python
import asyncio
from network_mapper import NetworkMapper
from src.config import Config

async def custom_scan():
    config = Config()
    mapper = NetworkMapper(config)
    
    results = await mapper.scan_network("192.168.1.0/24", "discovery")
    
    for result in results:
        print(f"Device: {result.ip_address}")
        print(f"  Type: {result.device_type}")
        print(f"  OS: {result.operating_system}")
        print(f"  Ports: {result.open_ports}")

asyncio.run(custom_scan())
```

### Testing
```bash
# Run basic functionality tests
python test_scan.py

# Run example usage
python example_usage.py
```

## 🔍 Device Classification

The tool automatically classifies devices into these categories:

- **Router**: Network gateway devices (Cisco, Juniper, etc.)
- **Switch**: Network switching devices
- **Server**: Web servers, database servers, application servers
- **Printer**: Network printers and print servers
- **Camera**: IP cameras and surveillance systems
- **IoT**: Smart home devices, sensors, automation
- **Mobile**: Smartphones, tablets, mobile devices
- **Workstation**: Desktop and laptop computers
- **Unknown**: Devices that couldn't be classified

## 📈 Performance Tips

1. **Use appropriate scan modes:**
   - Use `discovery` mode for quick scans
   - Use `local` mode with `--detailed` for comprehensive analysis

2. **Optimize network ranges:**
   - Start with smaller subnets (e.g., /24) for testing
   - Use larger ranges (e.g., /16) for production scans

3. **Adjust timeouts:**
   - Use `--timeout 10` for faster scans
   - Use `--timeout 60` for more thorough scans

4. **Monitor system resources:**
   - Large scans may use significant CPU and memory
   - Consider running during off-peak hours

## 🚨 Security Considerations

- **Only scan networks you own or have permission to scan**
- **Respect network policies and scanning regulations**
- **Use responsibly and ethically**
- **Some scans may trigger security alerts**
- **Consider running scans during maintenance windows**

## 🐛 Troubleshooting

### Common Issues

1. **Permission denied errors:**
   ```bash
   # Run with sudo for certain operations
   sudo python network_mapper.py --mode discovery --target 192.168.1.0/24
   ```

2. **Nmap not found:**
   ```bash
   # Install nmap manually
   brew install nmap  # macOS
   sudo apt-get install nmap  # Ubuntu/Debian
   ```

3. **Slow scans:**
   - Reduce timeout: `--timeout 10`
   - Use discovery mode instead of local mode
   - Scan smaller network ranges

4. **No devices found:**
   - Check network connectivity
   - Verify target IP range
   - Try scanning localhost first: `127.0.0.1`

### Debug Mode
```bash
# Enable verbose logging
export LOG_LEVEL=DEBUG
python network_mapper.py --mode discovery --target 192.168.1.0/24
```

## 📝 Examples

### Example 1: Home Network Audit
```bash
# Scan home network and generate HTML report
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output html

# Detailed analysis of specific device
python network_mapper.py --mode local --target 192.168.1.1 --detailed --output console
```

### Example 2: Corporate Network Security
```bash
# Quick rogue device detection
python network_mapper.py --mode discovery --target 10.0.0.0/16 --quick --output csv

# Detailed infrastructure mapping
python network_mapper.py --mode local --target 10.0.0.0/16 --detailed --output html
```

### Example 3: Server Infrastructure
```bash
# Map server infrastructure
python network_mapper.py --mode local --target 10.10.0.0/24 --detailed --output json

# Analyze specific server
python network_mapper.py --mode local --target 10.10.0.100 --detailed --output console
```

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs in the console output
3. Test with smaller network ranges first
4. Ensure all dependencies are properly installed

The Network Mapper is designed to be robust and user-friendly while providing comprehensive network analysis capabilities. 