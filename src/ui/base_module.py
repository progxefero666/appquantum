"""
Base module class for AppSpyder modules.
"""

from abc import ABC, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget

class BaseModule(QObject):
    """Base class for all AppSpyder modules."""
    
    # Signals
    result_ready = pyqtSignal(QWidget)  # Emitted when results are ready to display
    error_occurred = pyqtSignal(str)    # Emitted when an error occurs
    
    def __init__(self):
        super().__init__()
        self.control_panel = None
        self.result_panel = None
        
    @abstractmethod
    def setup_control_panel(self, parent_widget):
        """Setup the control panel (left side) for this module."""
        pass
        
    @abstractmethod
    def setup_result_panel(self, parent_widget):
        """Setup the result panel (right side) for this module."""
        pass
        
    def cleanup(self):
        """Clean up resources when module is destroyed."""
        pass
        
    def emit_result(self, widget):
        """Emit a result widget to be displayed."""
        self.result_ready.emit(widget)
        
    def emit_error(self, message):
        """Emit an error message."""
        self.error_occurred.emit(message)
