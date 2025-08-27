#!/usr/bin/env python3
"""
Advanced QR & Phishing Detector Launcher
Choose between basic (Tkinter) and advanced (CustomTkinter) interfaces
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def launch_basic():
    """Launch the basic Tkinter interface"""
    try:
        from app import App
        app = App()
        app.mainloop()
    except ImportError as e:
        messagebox.showerror("Error", f"Could not launch basic interface: {e}")

def launch_advanced():
    """Launch the advanced CustomTkinter interface"""
    try:
        from gui.advanced_gui import AdvancedQRDetector
        app = AdvancedQRDetector()
        app.mainloop()
    except ImportError as e:
        messagebox.showerror("Error", f"Could not launch advanced interface: {e}\n\nMake sure to install requirements: pip install -r requirements.txt")

def show_launcher():
    """Show launcher window"""
    root = tk.Tk()
    root.title("QR Detector Launcher")
    root.geometry("300x200")
    root.resizable(False, False)
    
    tk.Label(root, text="Choose Interface", font=("Arial", 16, "bold")).pack(pady=20)
    
    tk.Button(root, text="Basic Interface", command=lambda: [root.destroy(), launch_basic()], 
              width=20, height=2).pack(pady=5)
    
    tk.Button(root, text="Advanced Interface", command=lambda: [root.destroy(), launch_advanced()], 
              width=20, height=2).pack(pady=5)
    
    tk.Label(root, text="Advanced requires: pip install -r requirements.txt", 
             font=("Arial", 8), fg="gray").pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    show_launcher()
