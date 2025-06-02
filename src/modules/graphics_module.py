"""
Mathematical Graphics module for visualizing matplotlib plots and figures.
"""

import os
import sys
import importlib.util
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, 
    QTextEdit, QLabel, QFrame, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import traceback

from ..ui.base_module import BaseModule
from ..utils.file_loader import FileLoader

class GraphicsExecutionThread(QThread):
    """Thread for executing graphics scripts without blocking UI."""
    
    figure_ready = pyqtSignal(object)   # Figure object
    error_occurred = pyqtSignal(str)    # Error message
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        """Execute the graphics file in a separate thread."""
        try:
            # Load and execute the graphics file
            loader = FileLoader()
            graphics_data = loader.load_graphics_file(self.file_path)
            
            if 'figure' in graphics_data:
                figure = graphics_data['figure']
                self.figure_ready.emit(figure)
                
        except Exception as e:
            self.error_occurred.emit(f"Graphics execution failed: {str(e)}\n{traceback.format_exc()}")

class GraphicsModule(BaseModule):
    """Module for mathematical graphics visualization."""
    
    def __init__(self):
        super().__init__()
        self.graphics_dir = "public/graphs"
        self.current_figure = None
        self.execution_thread = None
        
    def setup_control_panel(self, parent_widget):
        """Setup the graphics control panel."""
        layout = QVBoxLayout(parent_widget)
        
        # Title
        title_label = QLabel("Mathematical Graphics")
        title_label.setObjectName("moduleTitle")
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Graphics files list
        files_label = QLabel("Available Plots:")
        layout.addWidget(files_label)
        
        self.graphics_list = QListWidget()
        self.graphics_list.setMaximumHeight(200)
        self.graphics_list.itemClicked.connect(self.on_graphics_selected)
        layout.addWidget(self.graphics_list)
        
        # Load graphics files
        self.load_graphics_files()
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Load Script")
        self.load_btn.clicked.connect(self.load_selected_graphics)
        self.load_btn.setEnabled(False)
        buttons_layout.addWidget(self.load_btn)
        
        self.execute_btn = QPushButton("Generate Plot")
        self.execute_btn.clicked.connect(self.execute_graphics)
        self.execute_btn.setEnabled(False)
        buttons_layout.addWidget(self.execute_btn)
        
        layout.addLayout(buttons_layout)
        
        # Graphics code display
        code_label = QLabel("Script Code:")
        layout.addWidget(code_label)
        
        self.code_display = QTextEdit()
        self.code_display.setReadOnly(True)
        self.code_display.setMaximumHeight(300)
        font = QFont("Consolas", 10)
        self.code_display.setFont(font)
        layout.addWidget(self.code_display)
        
        layout.addStretch()
        
    def setup_result_panel(self, parent_widget):
        """Setup the results panel."""
        layout = QVBoxLayout(parent_widget)
        
        # Results title
        results_label = QLabel("Mathematical Plots & Visualizations")
        results_label.setObjectName("resultsTitle")
        results_font = QFont("Arial", 12, QFont.Bold)
        results_label.setFont(results_font)
        layout.addWidget(results_label)
        
        # Scroll area for results
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        scroll_area.setWidget(self.results_widget)
        
        layout.addWidget(scroll_area)
        
        # Initial message
        initial_label = QLabel("Select and execute a graphics script to see mathematical visualizations.")
        initial_label.setAlignment(Qt.AlignCenter)
        initial_label.setStyleSheet("color: #666; font-style: italic; padding: 50px;")
        self.results_layout.addWidget(initial_label)
        
    def load_graphics_files(self):
        """Load available graphics files from the graphics directory."""
        self.graphics_list.clear()
        
        if not os.path.exists(self.graphics_dir):
            os.makedirs(self.graphics_dir, exist_ok=True)
            
        try:
            for file_name in os.listdir(self.graphics_dir):
                if file_name.endswith('.py'):
                    self.graphics_list.addItem(file_name)
        except Exception as e:
            self.emit_error(f"Failed to load graphics files: {str(e)}")
            
    def on_graphics_selected(self, item):
        """Handle graphics file selection."""
        self.load_btn.setEnabled(True)
        
    def load_selected_graphics(self):
        """Load the selected graphics file and display its code."""
        current_item = self.graphics_list.currentItem()
        if not current_item:
            return
            
        file_name = current_item.text()
        file_path = os.path.join(self.graphics_dir, file_name)
        
        try:
            # Read and display file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
                self.code_display.setPlainText(code_content)
                
            self.execute_btn.setEnabled(True)
            
        except Exception as e:
            self.emit_error(f"Failed to load graphics file: {str(e)}")
            
    def execute_graphics(self):
        """Execute the loaded graphics script."""
        current_item = self.graphics_list.currentItem()
        if not current_item:
            return
            
        file_name = current_item.text()
        file_path = os.path.join(self.graphics_dir, file_name)
        
        # Clear previous results
        self.clear_results()
        
        # Start execution in thread
        self.execution_thread = GraphicsExecutionThread(file_path)
        self.execution_thread.figure_ready.connect(self.display_figure)
        self.execution_thread.error_occurred.connect(self.emit_error)
        self.execution_thread.start()
        
    def clear_results(self):
        """Clear the results panel."""
        for i in reversed(range(self.results_layout.count())):
            item = self.results_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                
    def display_figure(self, figure):
        """Display the matplotlib figure."""
        try:
            self.current_figure = figure
            
            # Create info label
            info_label = QLabel(f"Generated Mathematical Plot")
            info_label.setStyleSheet("font-weight: bold; margin: 10px 0;")
            self.results_layout.addWidget(info_label)
            
            # Create canvas and add to layout
            canvas = FigureCanvas(figure)
            canvas.setMinimumHeight(500)
            self.results_layout.addWidget(canvas)
            
            # Add figure information
            axes_count = len(figure.axes)
            info_text = f"Figure contains {axes_count} subplot(s)"
            
            for i, ax in enumerate(figure.axes):
                info_text += f"\nSubplot {i+1}: {ax.get_title() or 'Untitled'}"
                
            info_display = QLabel(info_text)
            info_display.setStyleSheet("font-family: monospace; background: #f5f5f5; padding: 10px; margin: 10px 0;")
            info_display.setWordWrap(True)
            self.results_layout.addWidget(info_display)
            
        except Exception as e:
            self.emit_error(f"Failed to display figure: {str(e)}")
            
    def cleanup(self):
        """Clean up resources."""
        if self.execution_thread and self.execution_thread.isRunning():
            self.execution_thread.quit()
            self.execution_thread.wait()
            
        # Close any matplotlib figures
        plt.close('all')
