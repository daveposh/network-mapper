# Network Mapper

A comprehensive network mapping tool that scans IP ranges to discover devices, determine protocols, applications, operating systems, device types, and MAC address manufacturers.

## Features

### Local Scan Mode (Detailed Analysis)
- **Deep Protocol Analysis**: Identifies HTTP, HTTPS, SSH, FTP, SMTP, DNS, MySQL, PostgreSQL, RDP, and more
- **Application Fingerprinting**: Detects specific applications and services running on devices
- **Operating System Detection**: Uses nmap OS detection and TTL analysis
- **Device Type Classification**: Automatically categorizes devices as routers, switches, servers, printers, cameras, IoT devices, etc.
- **Connection Analysis**: Maps upstream and downstream dependencies
- **Service Enumeration**: Comprehensive port scanning with service identification
- **Response Time Analysis**: Measures network latency and performance metrics

### Network Discovery Mode (Rogue Device Detection)
- **Fast Network Discovery**: Quick scanning for device enumeration
- **MAC Address Analysis**: Identifies device manufacturers from MAC addresses with comprehensive vendor database
- **Rogue Device Detection**: Finds unauthorized devices on the network
- **Basic Device Classification**: Quick categorization of device types
- **Network Topology Mapping**: Creates network maps and device relationships
- **Manufacturer Database**: Built-in MAC address vendor lookup with API fallback and local database
- **Cross-Platform MAC Collection**: Optimized MAC address collection for macOS, Linux, and Windows

### Advanced Capabilities
- **Multi-format Output**: JSON, CSV, HTML, and console output formats
- **Async Performance**: High-performance concurrent scanning
- **Configurable Scanning**: Customizable timeouts, ports, and scan parameters
- **Report Generation**: Professional HTML reports with device details
- **Error Handling**: Robust error handling and fallback mechanisms
- **Cross-platform**: Works on Linux, macOS, and Windows

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Cross-Platform Setup

#### macOS/Linux
```bash
# Clone the repository
git clone <repository-url>
cd network-mapper

# Run automated installation
./install.sh
```

#### Windows
```cmd
# Clone the repository
git clone <repository-url>
cd network-mapper

# Run automated installation
install.bat
```

#### Manual Installation
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install system dependencies
# macOS: brew install nmap
# Ubuntu/Debian: sudo apt-get install nmap
# CentOS/RHEL: sudo yum install nmap
# Windows: Download from https://nmap.org/download.html
```

## Usage

### Quick Start
```bash
# Install the tool
./install.sh

# Activate virtual environment
source venv/bin/activate

# Run a discovery scan
python network_mapper.py --mode discovery --target 192.168.1.0/24
```

### Local Scan Mode (Detailed Analysis)
```bash
# Detailed local scan with deep analysis
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed

# Generate HTML report
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed --output html

# Generate JSON report
python network_mapper.py --mode local --target 192.168.1.0/24 --detailed --output json
```

### Network Discovery Mode (Rogue Device Detection)
```bash
# Quick discovery scan
python network_mapper.py --mode discovery --target 10.0.0.0/8 --quick

# Discovery scan with CSV output
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output csv
```

### Command Line Options
- `--mode`: Scan mode (local/discovery)
- `--target`: Target IP range (CIDR notation)
- `--detailed`: Enable detailed scanning (local mode)
- `--quick`: Enable quick scanning (discovery mode)
- `--output`: Output format (json/csv/html/console)
- `--timeout`: Scan timeout in seconds
- `--config`: Configuration file path

### Example Scenarios

#### 1. Home Network Discovery
```bash
# Scan your home network for all devices
python network_mapper.py --mode discovery --target 192.168.1.0/24 --output html
```

#### 2. Corporate Network Analysis
```bash
# Detailed analysis of corporate network
python network_mapper.py --mode local --target 10.0.0.0/16 --detailed --output json
```

#### 3. Rogue Device Detection
```bash
# Quick scan to find unauthorized devices
python network_mapper.py --mode discovery --target 172.16.0.0/12 --quick --output csv
```

#### 4. Server Infrastructure Mapping
```bash
# Map server infrastructure with detailed analysis
python network_mapper.py --mode local --target 10.10.0.0/24 --detailed --output html
```

## Output Formats

The tool supports multiple output formats:
- JSON: Structured data for programmatic use
- CSV: Spreadsheet-compatible format
- HTML: Interactive web report
- Console: Real-time scanning progress

## Cross-Platform Compatibility

The Network Mapper is designed to work across multiple platforms:

### Supported Operating Systems
- **macOS**: Full support with automated installation via Homebrew
- **Linux**: Full support with automated installation via package managers (apt, yum, dnf, pacman)
- **Windows**: Full support with manual nmap installation

### Platform-Specific Features
- **macOS/Linux**: Native ARP table lookup, ping commands, netstat
- **Windows**: Windows-specific ARP commands, ping syntax, network utilities
- **Cross-platform**: Python-based scanning, async operations, multi-format output

### Installation Methods
- **macOS**: `./install.sh` (automated)
- **Linux**: `./install.sh` (automated)
- **Windows**: `install.bat` (automated) or manual setup

## Architecture

- **Scanner Engine**: Core scanning functionality with cross-platform support
- **Protocol Analyzer**: Deep packet inspection
- **Device Classifier**: OS and device type detection
- **MAC Lookup**: Manufacturer database integration
- **Report Generator**: Multi-format output generation

## Security Considerations

- Requires appropriate permissions for network scanning
- Respect network policies and scanning regulations
- Use responsibly and only on networks you own or have permission to scan
- Some features may require elevated privileges (admin/sudo)

## License

MIT License - see LICENSE file for details 