"""
Main window implementation for AppSpyder application.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QSplitter, QFrame, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor

from modules.circuits_module import CircuitsModule
from modules.graphics_module import GraphicsModule
from modules.elements_module import ElementsModule

class MainWindow(QMainWindow):
    """Main application window with modular interface."""
    
    def __init__(self):
        super().__init__()
        self.current_module = None
        self.modules = {}
        self.init_ui()
        self.setup_modules()
        self.load_default_module()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("AppSpyder - Scientific Learning Platform")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create top menu bar
        self.create_menu_bar(main_layout)
        
        # Create content area with splitter
        self.create_content_area(main_layout)
        
    def create_menu_bar(self, parent_layout):
        """Create the top menu bar with module buttons."""
        menu_frame = QFrame()
        menu_frame.setObjectName("menuFrame")
        menu_frame.setFixedHeight(60)
        menu_frame.setFrameStyle(QFrame.StyledPanel)
        
        menu_layout = QHBoxLayout(menu_frame)
        menu_layout.setContentsMargins(20, 10, 20, 10)
        
        # Application title
        title_label = QLabel("AppSpyder")
        title_label.setObjectName("titleLabel")
        title_font = QFont("Arial", 16, QFont.Bold)
        title_label.setFont(title_font)
        menu_layout.addWidget(title_label)
        
        menu_layout.addStretch()
        
        # Module buttons
        self.module_buttons = {}
        
        modules_info = [
            ("circuits", "Quantum Circuits", "🔬"),
            ("graphics", "Math Graphics", "📊"),
            ("elements", "Periodic Elements", "⚛️")
        ]
        
        for module_id, module_name, icon in modules_info:
            btn = QPushButton(f"{icon} {module_name}")
            btn.setObjectName("moduleButton")
            btn.setMinimumWidth(150)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, mid=module_id: self.switch_module(mid))
            self.module_buttons[module_id] = btn
            menu_layout.addWidget(btn)
            
        parent_layout.addWidget(menu_frame)
        
    def create_content_area(self, parent_layout):
        """Create the main content area with left and right panels."""
        # Create splitter for left and right panels
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setObjectName("mainSplitter")
        
        # Left panel (controls/data)
        self.left_panel = QFrame()
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setMinimumWidth(350)
        self.left_panel.setMaximumWidth(500)
        
        # Right panel (results)
        self.right_panel = QFrame()
        self.right_panel.setObjectName("rightPanel")
        
        # Add panels to splitter
        self.splitter.addWidget(self.left_panel)
        self.splitter.addWidget(self.right_panel)
        
        # Set splitter proportions (30% left, 70% right)
        self.splitter.setSizes([400, 1000])
        
        parent_layout.addWidget(self.splitter)
        
    def setup_modules(self):
        """Initialize all available modules."""
        try:
            self.modules = {
                "circuits": CircuitsModule(),
                "graphics": GraphicsModule(),
                "elements": ElementsModule()
            }
            
            # Connect module signals
            for module in self.modules.values():
                if hasattr(module, 'result_ready'):
                    module.result_ready.connect(self.display_result)
                if hasattr(module, 'error_occurred'):
                    module.error_occurred.connect(self.show_error)
                    
        except Exception as e:
            self.show_error(f"Failed to initialize modules: {str(e)}")
            
    def switch_module(self, module_id):
        """Switch to the specified module."""
        if module_id not in self.modules:
            self.show_error(f"Module '{module_id}' not found")
            return
            
        # Update button states
        for btn_id, btn in self.module_buttons.items():
            if btn_id == module_id:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
        # Clear current panels
        self.clear_panel(self.left_panel)
        self.clear_panel(self.right_panel)
        
        # Load new module
        self.current_module = self.modules[module_id]
        
        # Setup left panel (controls)
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        self.current_module.setup_control_panel(self.left_panel)
        
        # Setup right panel (results)
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)
        self.current_module.setup_result_panel(self.right_panel)
        
    def clear_panel(self, panel):
        """Clear all widgets from a panel."""
        if panel.layout():
            while panel.layout().count():
                child = panel.layout().takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            panel.layout().deleteLater()
            
    def display_result(self, result_widget):
        """Display a result widget in the right panel."""
        if self.right_panel.layout():
            # Clear existing results
            layout = self.right_panel.layout()
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                if item and item.widget():
                    item.widget().deleteLater()
            
            # Add new result
            layout.addWidget(result_widget)
            
    def show_error(self, error_message):
        """Display an error message to the user."""
        QMessageBox.critical(self, "Error", error_message)
        
    def load_default_module(self):
        """Load the default module (circuits)."""
        self.switch_module("circuits")
        
    def closeEvent(self, event):
        """Handle application close event."""
        # Clean up modules
        for module in self.modules.values():
            if hasattr(module, 'cleanup'):
                module.cleanup()
        event.accept()
