@echo off
REM Network Mapper Installation Script for Windows

echo 🚀 Installing Network Mapper...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version.split()[0])"') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detected

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📚 Installing Python dependencies...
pip install -r requirements.txt

REM Check for nmap
echo 🔍 Checking for nmap...
where nmap >nul 2>&1
if errorlevel 1 (
    echo ⚠️  nmap not found. Please install nmap manually.
    echo Download from: https://nmap.org/download.html
    echo Or use Chocolatey: choco install nmap
    echo Or use Scoop: scoop install nmap
) else (
    echo ✅ nmap found
)

REM Create reports directory
echo 📁 Creating reports directory...
if not exist reports mkdir reports

REM Make the main script executable (Windows doesn't need this but for consistency)
echo 🔧 Setup complete!

echo.
echo 🎉 Installation completed successfully!
echo.
echo To use Network Mapper:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run a scan: python network_mapper.py --target 192.168.1.0/24
echo.
echo Example commands:
echo   # Basic discovery scan
echo   python network_mapper.py --target 192.168.1.0/24
echo.
echo   # Detailed local scan
echo   python network_mapper.py --mode local --target 192.168.1.0/24 --detailed
echo.
echo   # Generate HTML report
echo   python network_mapper.py --target 192.168.1.0/24 --output html
echo.
echo   # JSON output for automation
echo   python network_mapper.py --target 192.168.1.0/24 --output json
echo.
pause 