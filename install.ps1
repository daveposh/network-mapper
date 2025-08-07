# Network Mapper Installation Script for Windows (PowerShell)

Write-Host "🚀 Installing Network Mapper..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is required but not installed." -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Check Python version
$version = python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))" 2>$null
if ($version -lt "3.8") {
    Write-Host "❌ Python 3.8 or higher is required. Found: $version" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Python $version detected" -ForegroundColor Green

# Create virtual environment
Write-Host "📦 Creating virtual environment..." -ForegroundColor Cyan
python -m venv venv

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip

# Install dependencies
Write-Host "📚 Installing Python dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt

# Check for nmap
Write-Host "🔍 Checking for nmap..." -ForegroundColor Cyan
$nmapPath = Get-Command nmap -ErrorAction SilentlyContinue
if ($nmapPath) {
    Write-Host "✅ nmap found" -ForegroundColor Green
} else {
    Write-Host "⚠️  nmap not found. Please install nmap manually." -ForegroundColor Yellow
    Write-Host "Download from: https://nmap.org/download.html" -ForegroundColor Yellow
    Write-Host "Or use Chocolatey: choco install nmap" -ForegroundColor Yellow
    Write-Host "Or use Scoop: scoop install nmap" -ForegroundColor Yellow
}

# Create reports directory
Write-Host "📁 Creating reports directory..." -ForegroundColor Cyan
if (!(Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}

Write-Host "🔧 Setup complete!" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To use Network Mapper:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Run a scan: python network_mapper.py --target 192.168.1.0/24" -ForegroundColor White
Write-Host ""
Write-Host "Example commands:" -ForegroundColor Cyan
Write-Host "  # Basic discovery scan" -ForegroundColor White
Write-Host "  python network_mapper.py --target 192.168.1.0/24" -ForegroundColor White
Write-Host ""
Write-Host "  # Detailed local scan" -ForegroundColor White
Write-Host "  python network_mapper.py --mode local --target 192.168.1.0/24 --detailed" -ForegroundColor White
Write-Host ""
Write-Host "  # Generate HTML report" -ForegroundColor White
Write-Host "  python network_mapper.py --target 192.168.1.0/24 --output html" -ForegroundColor White
Write-Host ""
Write-Host "  # JSON output for automation" -ForegroundColor White
Write-Host "  python network_mapper.py --target 192.168.1.0/24 --output json" -ForegroundColor White
Write-Host "" 