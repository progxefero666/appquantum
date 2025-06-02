#!/usr/bin/env python3
"""
Main entry point for the AppSpyder application.
A modular desktop application for scientific learning and visualization.
"""

import sys
import os

# Configure display for Replit VNC
os.environ['QT_QPA_PLATFORM'] = 'vnc'
os.environ['DISPLAY'] = ':0'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.main_window import MainWindow

def main():
    """Initialize and run the AppSpyder application."""
    # Create QApplication instance
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("AppSpyder")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AppSpyder")
    
    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Load and apply stylesheet
    try:
        with open('assets/styles.qss', 'r') as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("Warning: Could not load stylesheet file")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
