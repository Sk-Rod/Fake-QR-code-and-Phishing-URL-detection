#!/usr/bin/env python3
"""
Test script to verify the QR icon was created correctly
"""

from PIL import Image
import os

def test_icon():
    """Test if the icon file exists and is valid"""
    
    icon_path = 'icon.ico'
    
    if not os.path.exists(icon_path):
        print("❌ Error: icon.ico file not found!")
        return False
    
    try:
        # Try to open the icon file
        with Image.open(icon_path) as img:
            print(f"✅ Icon file found: {icon_path}")
            print(f"📏 Format: {img.format}")
            print(f"📐 Size: {img.size}")
            print(f"🎨 Mode: {img.mode}")
            
            # Check if it's a multi-size icon
            if hasattr(img, 'n_frames') and img.n_frames > 1:
                print(f"🖼️  Multiple sizes: {img.n_frames} frames")
            
            return True
            
    except Exception as e:
        print(f"❌ Error opening icon file: {e}")
        return False

if __name__ == "__main__":
    test_icon()
