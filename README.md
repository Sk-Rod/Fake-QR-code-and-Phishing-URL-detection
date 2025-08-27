# QRsafe - Secure QR Code Analysis & Phishing Detection

## Overview
QRsafe is a desktop application that provides comprehensive security analysis for QR codes and URLs. It helps users detect potential phishing attempts and security risks associated with QR codes and web links.

## Features
- **URL Analysis**: Analyze URLs for phishing and security risks
- **QR Code Scanning**: Upload and analyze QR code images
- **Risk Assessment**: Visual risk indicators with detailed analysis
- **History Tracking**: Save and review past analyses
- **Professional UI**: Clean, modern interface with dark theme

## Installation

### Prerequisites
- Python 3.7+
- Required packages (install via pip):

```bash
pip install -r requirements.txt
```

### Required Packages
- customtkinter
- Pillow (PIL)
- opencv-python
- numpy

## Usage

### Method 1: Simple Batch File (Windows)
Double-click `launch_qrsafe.bat` to start the application.

### Method 2: Python Launcher
Run the advanced launcher:
```bash
python QRsafe_Launcher.py
```

### Method 3: Direct Execution
Run the main application directly:
```bash
python gui/advanced_gui.py
```

### Creating Desktop Shortcut (Windows)
1. Run `QRsafe_Launcher.py`
2. Click "Create Desktop Shortcut" button
3. Requires additional packages: `pip install winshell pywin32`

## Application Structure
```
phishqrdetect/
├── gui/
│   └── advanced_gui.py    # Main application GUI
├── app.py                 # Core analysis functionality
├── requirements.txt       # Python dependencies
├── launch_qrsafe.bat     # Simple Windows launcher
├── QRsafe_Launcher.py    # Advanced launcher with GUI
└── README.md             # This file
```

## How It Works
1. **URL Analysis**: Enter any URL to get a comprehensive security assessment
2. **QR Scanning**: Upload QR code images to decode and analyze contained URLs
3. **Risk Scoring**: Get a risk score from 0-10 with detailed analysis
4. **History**: All analyses are saved for future reference

## Security Features
- Domain reputation analysis
- SSL certificate validation
- Suspicious pattern detection
- Phishing attempt identification

## Troubleshooting
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Make sure Python is in your system PATH
- For shortcut creation, install: `pip install winshell pywin32`

## License
This project is for educational and security research purposes.
