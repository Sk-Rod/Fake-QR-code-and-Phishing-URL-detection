#!/usr/bin/env python3
"""
Test script to verify the desktop shortcut can be created with the new icon
"""

import os
import sys
from QRsafe_Launcher import create_desktop_shortcut

def test_shortcut_creation():
    """Test if the shortcut creation works with our new icon"""
    
    print("Testing desktop shortcut creation...")
    print(f"Current directory: {os.getcwd()}")
    print(f"Icon file exists: {os.path.exists('icon.ico')}")
    
    if os.path.exists('icon.ico'):
        print("✅ icon.ico file is ready for use")
        print("Attempting to create desktop shortcut...")
        
        # Import and test the shortcut creation
        try:
            create_desktop_shortcut()
            print("✅ Shortcut creation function executed successfully")
        except Exception as e:
            print(f"❌ Error during shortcut creation: {e}")
    else:
        print("❌ icon.ico file not found")

if __name__ == "__main__":
    test_shortcut_creation()
