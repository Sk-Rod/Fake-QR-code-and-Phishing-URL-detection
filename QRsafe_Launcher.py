#!/usr/bin/env python3
"""
QRsafe Launcher - Desktop application launcher for QRsafe
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def launch_qrsafe():
    """Launch the QRsafe application"""
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Change to the script directory
        os.chdir(script_dir)
        
        # Check if Python is available
        try:
            subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showerror("Error", "Python is not installed or not in PATH")
            return False
        
        # Check if required packages are installed
        try:
            import customtkinter
            import PIL
            import cv2
            import numpy
        except ImportError as e:
            messagebox.showerror(
                "Missing Dependencies", 
                f"Required packages are not installed:\n\n{e}\n\n"
                "Please run: pip install -r requirements.txt"
            )
            return False
        
        # Launch the main application
        subprocess.Popen([sys.executable, "gui/advanced_gui.py"])
        return True
        
    except Exception as e:
        messagebox.showerror("Launch Error", f"Failed to launch QRsafe:\n\n{str(e)}")
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut (Windows only)"""
    if os.name != 'nt':
        messagebox.showinfo("Info", "Desktop shortcuts are only supported on Windows")
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "QRsafe.lnk")
        
        target = sys.executable
        wDir = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(wDir, "icon.ico")  # You can add an icon file later
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.Arguments = f'"{os.path.join(wDir, "QRsafe_Launcher.py")}"'
        shortcut.WorkingDirectory = wDir
        shortcut.IconLocation = icon if os.path.exists(icon) else target
        shortcut.save()
        
        messagebox.showinfo("Success", "Desktop shortcut created successfully!")
        
    except ImportError:
        messagebox.showinfo("Info", "Please install required packages for shortcut creation:\npip install winshell pywin32")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create shortcut:\n\n{str(e)}")

if __name__ == "__main__":
    # Simple GUI for launcher options
    root = tk.Tk()
    root.title("QRsafe Launcher")
    root.geometry("300x200")
    root.resizable(False, False)
    
    # Center the window
    root.eval('tk::PlaceWindow . center')
    
    # Create main frame
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill="both", expand=True)
    
    # Title
    title_label = tk.Label(frame, text="QRsafe Launcher", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)
    
    # Launch button
    launch_btn = tk.Button(
        frame, 
        text="Launch QRsafe", 
        command=launch_qrsafe,
        width=20,
        height=2,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12)
    )
    launch_btn.pack(pady=10)
    
    # Create shortcut button (Windows only)
    if os.name == 'nt':
        shortcut_btn = tk.Button(
            frame,
            text="Create Desktop Shortcut",
            command=create_desktop_shortcut,
            width=20,
            height=2,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10)
        )
        shortcut_btn.pack(pady=5)
    
    # Exit button
    exit_btn = tk.Button(
        frame,
        text="Exit",
        command=root.quit,
        width=20,
        height=2,
        bg="#f44336",
        fg="white",
        font=("Arial", 10)
    )
    exit_btn.pack(pady=10)
    
    root.mainloop()
