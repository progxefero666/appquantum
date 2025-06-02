"""
Quantum Circuits module for visualizing and executing Qiskit circuits.
"""

import os
import sys
import importlib.util
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, 
    QTextEdit, QLabel, QFrame, QScrollArea, QWidget, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import traceback

try:
    from qiskit import QuantumCircuit
    from qiskit.visualization import circuit_drawer
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    import numpy as np
except ImportError as e:
    print(f"Warning: Qiskit not available: {e}")

from ..ui.base_module import BaseModule
from ..utils.file_loader import FileLoader

class CircuitExecutionThread(QThread):
    """Thread for executing quantum circuits without blocking UI."""
    
    circuit_ready = pyqtSignal(object)  # QuantumCircuit object
    result_ready = pyqtSignal(object)   # Execution results
    error_occurred = pyqtSignal(str)    # Error message
    
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        """Execute the circuit file in a separate thread."""
        try:
            # Load and execute the circuit file
            loader = FileLoader()
            circuit_data = loader.load_circuit_file(self.file_path)
            
            if 'circuit' in circuit_data:
                circuit = circuit_data['circuit']
                self.circuit_ready.emit(circuit)
                
                # Execute circuit if it has measurements
                if circuit.num_clbits > 0:
                    simulator = AerSimulator()
                    transpiled_circuit = transpile(circuit, simulator)
                    job = simulator.run(transpiled_circuit, shots=1024)
                    result = job.result()
                    counts = result.get_counts()
                    self.result_ready.emit(counts)
                    
        except Exception as e:
            self.error_occurred.emit(f"Circuit execution failed: {str(e)}\n{traceback.format_exc()}")

class CircuitsModule(BaseModule):
    """Module for quantum circuit visualization and execution."""
    
    def __init__(self):
        super().__init__()
        self.circuits_dir = "public/circuits"
        self.current_circuit = None
        self.execution_thread = None
        
    def setup_control_panel(self, parent_widget):
        """Setup the circuit control panel."""
        layout = QVBoxLayout(parent_widget)
        
        # Title
        title_label = QLabel("Quantum Circuits")
        title_label.setObjectName("moduleTitle")
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Circuit files list
        files_label = QLabel("Available Circuits:")
        layout.addWidget(files_label)
        
        self.circuits_list = QListWidget()
        self.circuits_list.setMaximumHeight(200)
        self.circuits_list.itemClicked.connect(self.on_circuit_selected)
        layout.addWidget(self.circuits_list)
        
        # Load circuit files
        self.load_circuit_files()
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        self.load_btn = QPushButton("Load Circuit")
        self.load_btn.clicked.connect(self.load_selected_circuit)
        self.load_btn.setEnabled(False)
        buttons_layout.addWidget(self.load_btn)
        
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.execute_circuit)
        self.execute_btn.setEnabled(False)
        buttons_layout.addWidget(self.execute_btn)
        
        layout.addLayout(buttons_layout)
        
        # Circuit code display
        code_label = QLabel("Circuit Code:")
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
        results_label = QLabel("Circuit Visualization & Results")
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
        initial_label = QLabel("Select and load a circuit to see visualization and results.")
        initial_label.setAlignment(Qt.AlignCenter)
        initial_label.setStyleSheet("color: #666; font-style: italic; padding: 50px;")
        self.results_layout.addWidget(initial_label)
        
    def load_circuit_files(self):
        """Load available circuit files from the circuits directory."""
        self.circuits_list.clear()
        
        if not os.path.exists(self.circuits_dir):
            os.makedirs(self.circuits_dir, exist_ok=True)
            
        try:
            for file_name in os.listdir(self.circuits_dir):
                if file_name.endswith('.py'):
                    self.circuits_list.addItem(file_name)
        except Exception as e:
            self.emit_error(f"Failed to load circuit files: {str(e)}")
            
    def on_circuit_selected(self, item):
        """Handle circuit file selection."""
        self.load_btn.setEnabled(True)
        
    def load_selected_circuit(self):
        """Load the selected circuit file and display its code."""
        current_item = self.circuits_list.currentItem()
        if not current_item:
            return
            
        file_name = current_item.text()
        file_path = os.path.join(self.circuits_dir, file_name)
        
        try:
            # Read and display file content
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
                self.code_display.setPlainText(code_content)
                
            self.execute_btn.setEnabled(True)
            
        except Exception as e:
            self.emit_error(f"Failed to load circuit file: {str(e)}")
            
    def execute_circuit(self):
        """Execute the loaded circuit."""
        current_item = self.circuits_list.currentItem()
        if not current_item:
            return
            
        file_name = current_item.text()
        file_path = os.path.join(self.circuits_dir, file_name)
        
        # Clear previous results
        self.clear_results()
        
        # Start execution in thread
        self.execution_thread = CircuitExecutionThread(file_path)
        self.execution_thread.circuit_ready.connect(self.display_circuit)
        self.execution_thread.result_ready.connect(self.display_results)
        self.execution_thread.error_occurred.connect(self.emit_error)
        self.execution_thread.start()
        
    def clear_results(self):
        """Clear the results panel."""
        for i in reversed(range(self.results_layout.count())):
            item = self.results_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                
    def display_circuit(self, circuit):
        """Display the quantum circuit diagram."""
        try:
            self.current_circuit = circuit
            
            # Create circuit info
            info_label = QLabel(f"Circuit: {circuit.num_qubits} qubits, {circuit.num_clbits} classical bits")
            info_label.setStyleSheet("font-weight: bold; margin: 10px 0;")
            self.results_layout.addWidget(info_label)
            
            # Create matplotlib figure for circuit diagram
            fig = Figure(figsize=(12, 6), dpi=100)
            fig.patch.set_facecolor('white')
            
            try:
                # Draw circuit
                ax = fig.add_subplot(111)
                circuit_drawer(circuit, output='mpl', ax=ax, style='iqx')
                ax.set_title(f"Quantum Circuit Diagram", fontsize=14, fontweight='bold')
                
            except Exception as e:
                # Fallback to text representation
                ax = fig.add_subplot(111)
                ax.text(0.5, 0.5, str(circuit), transform=ax.transAxes, 
                       fontsize=10, ha='center', va='center', fontfamily='monospace')
                ax.set_title("Circuit Text Representation", fontsize=14)
                ax.axis('off')
            
            # Create canvas and add to layout
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(400)
            self.results_layout.addWidget(canvas)
            
        except Exception as e:
            self.emit_error(f"Failed to display circuit: {str(e)}")
            
    def display_results(self, counts):
        """Display execution results."""
        try:
            # Results label
            results_label = QLabel("Execution Results:")
            results_label.setStyleSheet("font-weight: bold; margin: 20px 0 10px 0;")
            self.results_layout.addWidget(results_label)
            
            # Create histogram
            fig = Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)
            
            states = list(counts.keys())
            values = list(counts.values())
            
            bars = ax.bar(states, values, color='skyblue', edgecolor='navy', alpha=0.7)
            ax.set_xlabel('Measurement States', fontsize=12)
            ax.set_ylabel('Counts', fontsize=12)
            ax.set_title('Measurement Results Histogram', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(values),
                       f'{value}', ha='center', va='bottom', fontweight='bold')
            
            fig.tight_layout()
            
            # Create canvas and add to layout
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(400)
            self.results_layout.addWidget(canvas)
            
            # Add text summary
            summary_text = f"Total shots: {sum(values)}\n"
            summary_text += "Measurement probabilities:\n"
            total_shots = sum(values)
            for state, count in counts.items():
                probability = count / total_shots
                summary_text += f"  |{state}⟩: {count}/{total_shots} ({probability:.3f})\n"
                
            summary_label = QLabel(summary_text)
            summary_label.setStyleSheet("font-family: monospace; background: #f5f5f5; padding: 10px; margin: 10px 0;")
            summary_label.setWordWrap(True)
            self.results_layout.addWidget(summary_label)
            
        except Exception as e:
            self.emit_error(f"Failed to display results: {str(e)}")
            
    def cleanup(self):
        """Clean up resources."""
        if self.execution_thread and self.execution_thread.isRunning():
            self.execution_thread.quit()
            self.execution_thread.wait()
