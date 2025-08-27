#!/usr/bin/env python3
"""
QR Icon Generator - Creates a desktop shortcut icon with QR letters on black background
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_qr_icon():
    """Create a QR icon with blue letters on black background"""
    
    print("Creating QR icon...")
    
    # Create a simple 256x256 icon first (main size)
    size = 256
    img = Image.new('RGB', (size, size), 'black')
    draw = ImageDraw.Draw(img)
    
    # Use default font
    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()
        print("Using default font")
    
    # Draw "QR" text in blue
    text = "QR"
    draw.text((70, 80), text, fill=(0, 120, 255), font=font)
    
    # Save as .ico file
    img.save('icon.ico', format='ICO')
    
    print("✅ QR icon created successfully as 'icon.ico'")
    print(f"📏 Size: {size}x{size} pixels")
    print("🎨 Colors: Blue 'QR' text on black background")

if __name__ == "__main__":
    create_qr_icon()
