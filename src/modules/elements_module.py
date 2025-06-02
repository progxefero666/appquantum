"""
Periodic Elements module for browsing and visualizing chemical elements data.
"""

import os
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, 
    QTextEdit, QLabel, QFrame, QScrollArea, QWidget, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QSplitter, QGroupBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..ui.base_module import BaseModule
from ..database.db_manager import DatabaseManager

class ElementsModule(BaseModule):
    """Module for periodic table elements visualization and data browsing."""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.elements_data = []
        self.filtered_elements = []
        self.current_element = None
        
    def setup_control_panel(self, parent_widget):
        """Setup the elements control panel."""
        layout = QVBoxLayout(parent_widget)
        
        # Title
        title_label = QLabel("Periodic Elements")
        title_label.setObjectName("moduleTitle")
        title_font = QFont("Arial", 14, QFont.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Search and filters
        self.setup_filters(layout)
        
        # Elements list
        list_label = QLabel("Elements:")
        layout.addWidget(list_label)
        
        self.elements_list = QListWidget()
        self.elements_list.setMaximumHeight(300)
        self.elements_list.itemClicked.connect(self.on_element_selected)
        layout.addWidget(self.elements_list)
        
        # Load elements data
        self.load_elements_data()
        
        # Element details section
        details_group = QGroupBox("Element Details")
        details_layout = QVBoxLayout(details_group)
        
        self.element_info = QTextEdit()
        self.element_info.setReadOnly(True)
        self.element_info.setMaximumHeight(200)
        font = QFont("Consolas", 9)
        self.element_info.setFont(font)
        details_layout.addWidget(self.element_info)
        
        layout.addWidget(details_group)
        layout.addStretch()
        
    def setup_filters(self, parent_layout):
        """Setup search and filter controls."""
        filter_group = QGroupBox("Filters")
        filter_layout = QVBoxLayout(filter_group)
        
        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Element name or symbol...")
        self.search_input.textChanged.connect(self.apply_filters)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        filter_layout.addLayout(search_layout)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_label = QLabel("Category:")
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_filter)
        filter_layout.addLayout(category_layout)
        
        # Period filter
        period_layout = QHBoxLayout()
        period_label = QLabel("Period:")
        self.period_filter = QComboBox()
        self.period_filter.addItem("All Periods")
        self.period_filter.currentTextChanged.connect(self.apply_filters)
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_filter)
        filter_layout.addLayout(period_layout)
        
        parent_layout.addWidget(filter_group)
        
    def setup_result_panel(self, parent_widget):
        """Setup the results panel."""
        layout = QVBoxLayout(parent_widget)
        
        # Results title
        results_label = QLabel("Element Visualization & Analysis")
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
        initial_label = QLabel("Select an element to see detailed information and visualizations.")
        initial_label.setAlignment(Qt.AlignCenter)
        initial_label.setStyleSheet("color: #666; font-style: italic; padding: 50px;")
        self.results_layout.addWidget(initial_label)
        
    def load_elements_data(self):
        """Load elements data from database."""
        try:
            self.elements_data = self.db_manager.get_all_elements()
            self.filtered_elements = self.elements_data.copy()
            
            # Populate filter options
            self.populate_filter_options()
            
            # Update elements list
            self.update_elements_list()
            
        except Exception as e:
            self.emit_error(f"Failed to load elements data: {str(e)}")
            
    def populate_filter_options(self):
        """Populate filter dropdown options based on data."""
        try:
            # Categories
            categories = set()
            periods = set()
            
            for element in self.elements_data:
                if element.get('category'):
                    categories.add(element['category'])
                if element.get('period'):
                    periods.add(str(element['period']))
                    
            # Update category filter
            self.category_filter.clear()
            self.category_filter.addItem("All Categories")
            for category in sorted(categories):
                self.category_filter.addItem(category)
                
            # Update period filter
            self.period_filter.clear()
            self.period_filter.addItem("All Periods")
            for period in sorted(periods, key=int):
                self.period_filter.addItem(f"Period {period}")
                
        except Exception as e:
            self.emit_error(f"Failed to populate filters: {str(e)}")
            
    def apply_filters(self):
        """Apply search and filter criteria to elements list."""
        try:
            search_text = self.search_input.text().lower()
            selected_category = self.category_filter.currentText()
            selected_period = self.period_filter.currentText()
            
            self.filtered_elements = []
            
            for element in self.elements_data:
                # Search filter
                matches_search = True
                if search_text:
                    name_match = search_text in element.get('name', '').lower()
                    symbol_match = search_text in element.get('symbol', '').lower()
                    matches_search = name_match or symbol_match
                    
                # Category filter
                matches_category = True
                if selected_category != "All Categories":
                    matches_category = element.get('category') == selected_category
                    
                # Period filter
                matches_period = True
                if selected_period != "All Periods":
                    period_num = selected_period.replace("Period ", "")
                    matches_period = str(element.get('period', '')) == period_num
                    
                if matches_search and matches_category and matches_period:
                    self.filtered_elements.append(element)
                    
            self.update_elements_list()
            
        except Exception as e:
            self.emit_error(f"Failed to apply filters: {str(e)}")
            
    def update_elements_list(self):
        """Update the elements list widget."""
        self.elements_list.clear()
        
        for element in self.filtered_elements:
            name = element.get('name', 'Unknown')
            symbol = element.get('symbol', 'X')
            atomic_number = element.get('atomic_number', 0)
            
            item_text = f"{atomic_number:3d} - {symbol:2s} - {name}"
            self.elements_list.addItem(item_text)
            
    def on_element_selected(self, item):
        """Handle element selection."""
        try:
            row = self.elements_list.row(item)
            if 0 <= row < len(self.filtered_elements):
                self.current_element = self.filtered_elements[row]
                self.display_element_details()
                self.display_element_visualization()
                
        except Exception as e:
            self.emit_error(f"Failed to select element: {str(e)}")
            
    def display_element_details(self):
        """Display detailed information about the selected element."""
        if not self.current_element:
            return
            
        try:
            element = self.current_element
            
            details = f"Element Details:\n"
            details += f"Name: {element.get('name', 'N/A')}\n"
            details += f"Symbol: {element.get('symbol', 'N/A')}\n"
            details += f"Atomic Number: {element.get('atomic_number', 'N/A')}\n"
            details += f"Atomic Weight: {element.get('atomic_weight', 'N/A')}\n"
            details += f"Category: {element.get('category', 'N/A')}\n"
            details += f"Period: {element.get('period', 'N/A')}\n"
            details += f"Group: {element.get('group', 'N/A')}\n"
            details += f"Electronic Configuration: {element.get('electron_configuration', 'N/A')}\n"
            details += f"Electronegativity: {element.get('electronegativity', 'N/A')}\n"
            details += f"Melting Point: {element.get('melting_point', 'N/A')} K\n"
            details += f"Boiling Point: {element.get('boiling_point', 'N/A')} K\n"
            details += f"Density: {element.get('density', 'N/A')} g/cm³\n"
            
            self.element_info.setPlainText(details)
            
        except Exception as e:
            self.emit_error(f"Failed to display element details: {str(e)}")
            
    def display_element_visualization(self):
        """Display visualizations for the selected element."""
        if not self.current_element:
            return
            
        try:
            # Clear previous results
            self.clear_results()
            
            element = self.current_element
            element_name = element.get('name', 'Unknown Element')
            
            # Element header
            header_label = QLabel(f"Element Analysis: {element_name}")
            header_label.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px 0;")
            self.results_layout.addWidget(header_label)
            
            # Create property comparison chart
            self.create_property_chart(element)
            
            # Create electron shell diagram placeholder
            self.create_electron_shell_info(element)
            
        except Exception as e:
            self.emit_error(f"Failed to display element visualization: {str(e)}")
            
    def create_property_chart(self, element):
        """Create a chart showing element properties."""
        try:
            fig = Figure(figsize=(12, 8), dpi=100)
            fig.patch.set_facecolor('white')
            
            # Properties to display
            properties = {
                'Atomic Number': element.get('atomic_number', 0),
                'Atomic Weight': element.get('atomic_weight', 0),
                'Period': element.get('period', 0),
                'Group': element.get('group', 0),
                'Electronegativity': element.get('electronegativity', 0),
                'Melting Point (K)': element.get('melting_point', 0),
                'Boiling Point (K)': element.get('boiling_point', 0),
                'Density (g/cm³)': element.get('density', 0)
            }
            
            # Filter out None and 0 values for better visualization
            valid_properties = {k: v for k, v in properties.items() 
                              if v is not None and v != 0 and v != ''}
            
            if valid_properties:
                # Create bar chart
                ax1 = fig.add_subplot(2, 2, 1)
                names = list(valid_properties.keys())
                values = list(valid_properties.values())
                
                # Convert string values to float if possible
                numeric_values = []
                for v in values:
                    try:
                        numeric_values.append(float(v))
                    except (ValueError, TypeError):
                        numeric_values.append(0)
                
                bars = ax1.bar(range(len(names)), numeric_values, 
                              color='lightblue', edgecolor='navy', alpha=0.7)
                ax1.set_xlabel('Properties')
                ax1.set_ylabel('Values')
                ax1.set_title(f'{element.get("name", "Element")} Properties')
                ax1.set_xticks(range(len(names)))
                ax1.set_xticklabels(names, rotation=45, ha='right')
                ax1.grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bar, value in zip(bars, numeric_values):
                    height = bar.get_height()
                    if height > 0:
                        ax1.text(bar.get_x() + bar.get_width()/2., height,
                               f'{value:.2f}', ha='center', va='bottom', fontsize=8)
            
            # Periodic table position visualization
            ax2 = fig.add_subplot(2, 2, 2)
            period = element.get('period', 1)
            group = element.get('group', 1)
            
            if period and group:
                # Create a simple periodic table grid representation
                ax2.scatter(group, period, s=200, c='red', alpha=0.7, edgecolors='black')
                ax2.set_xlim(0, 19)
                ax2.set_ylim(0, 8)
                ax2.set_xlabel('Group')
                ax2.set_ylabel('Period')
                ax2.set_title('Position in Periodic Table')
                ax2.grid(True, alpha=0.3)
                ax2.invert_yaxis()  # Period 1 at top
                
                # Add element symbol at the position
                ax2.text(group, period, element.get('symbol', 'X'), 
                        ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Element category pie chart (placeholder for future implementation)
            ax3 = fig.add_subplot(2, 2, 3)
            category = element.get('category', 'Unknown')
            ax3.text(0.5, 0.5, f"Category:\n{category}", 
                    transform=ax3.transAxes, ha='center', va='center',
                    fontsize=14, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen", alpha=0.7))
            ax3.set_title('Element Category')
            ax3.axis('off')
            
            # Electron configuration visualization
            ax4 = fig.add_subplot(2, 2, 4)
            electron_config = element.get('electron_configuration', 'Unknown')
            ax4.text(0.5, 0.5, f"Electron Configuration:\n{electron_config}", 
                    transform=ax4.transAxes, ha='center', va='center',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
            ax4.set_title('Electron Configuration')
            ax4.axis('off')
            
            fig.tight_layout()
            
            # Create canvas and add to layout
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(600)
            self.results_layout.addWidget(canvas)
            
        except Exception as e:
            self.emit_error(f"Failed to create property chart: {str(e)}")
            
    def create_electron_shell_info(self, element):
        """Create electron shell information display."""
        try:
            shell_group = QGroupBox("Electron Shell Information")
            shell_layout = QVBoxLayout(shell_group)
            
            atomic_number = element.get('atomic_number', 0)
            electron_config = element.get('electron_configuration', 'Unknown')
            
            info_text = f"Atomic Number: {atomic_number}\n"
            info_text += f"Number of Electrons: {atomic_number}\n"
            info_text += f"Electron Configuration: {electron_config}\n\n"
            
            # Simple shell distribution (K, L, M, N shells)
            if atomic_number > 0:
                shells = self.calculate_electron_shells(atomic_number)
                info_text += "Electron Shell Distribution:\n"
                shell_names = ['K', 'L', 'M', 'N', 'O', 'P', 'Q']
                for i, count in enumerate(shells):
                    if count > 0 and i < len(shell_names):
                        info_text += f"  {shell_names[i]} shell: {count} electrons\n"
            
            info_label = QLabel(info_text)
            info_label.setStyleSheet("font-family: monospace; background: #f0f8ff; padding: 15px; margin: 10px 0;")
            info_label.setWordWrap(True)
            shell_layout.addWidget(info_label)
            
            self.results_layout.addWidget(shell_group)
            
        except Exception as e:
            self.emit_error(f"Failed to create electron shell info: {str(e)}")
            
    def calculate_electron_shells(self, atomic_number):
        """Calculate electron distribution in shells (simplified model)."""
        shells = [0] * 7  # K, L, M, N, O, P, Q shells
        max_electrons = [2, 8, 18, 32, 32, 18, 8]  # Maximum electrons per shell
        
        remaining_electrons = atomic_number
        for i in range(len(shells)):
            if remaining_electrons <= 0:
                break
            electrons_in_shell = min(remaining_electrons, max_electrons[i])
            shells[i] = electrons_in_shell
            remaining_electrons -= electrons_in_shell
            
        return shells
        
    def clear_results(self):
        """Clear the results panel."""
        for i in reversed(range(self.results_layout.count())):
            item = self.results_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
                
    def cleanup(self):
        """Clean up resources."""
        if self.db_manager:
            self.db_manager.close()
            
        # Close any matplotlib figures
        plt.close('all')
