"""
Database manager for SQLite operations with periodic elements data.
"""

import sqlite3
import os
from typing import List, Dict, Optional

class DatabaseManager:
    """Manager for SQLite database operations."""
    
    def __init__(self, db_path: str = "public/elements.db"):
        self.db_path = db_path
        self.connection = None
        self.init_database()
        
    def init_database(self):
        """Initialize database connection and create tables if needed."""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            # Connect to database
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row  # Enable dict-like access
            
            # Create tables if they don't exist
            self.create_tables()
            
            # Insert default data if tables are empty
            if self.get_element_count() == 0:
                self.insert_default_elements()
                
        except Exception as e:
            raise Exception(f"Failed to initialize database: {str(e)}")
            
    def create_tables(self):
        """Create the elements table."""
        cursor = self.connection.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS elements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                atomic_number INTEGER UNIQUE NOT NULL,
                symbol TEXT NOT NULL,
                name TEXT NOT NULL,
                atomic_weight REAL,
                category TEXT,
                period INTEGER,
                group_number INTEGER,
                electron_configuration TEXT,
                electronegativity REAL,
                melting_point REAL,
                boiling_point REAL,
                density REAL,
                discovery_year INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        
    def insert_default_elements(self):
        """Insert default periodic table elements."""
        elements_data = [
            (1, 'H', 'Hydrogen', 1.008, 'Nonmetal', 1, 1, '1s¹', 2.20, 14.01, 20.28, 0.00008988, 1766),
            (2, 'He', 'Helium', 4.0026, 'Noble gas', 1, 18, '1s²', None, 0.95, 4.22, 0.0001785, 1868),
            (3, 'Li', 'Lithium', 6.94, 'Alkali metal', 2, 1, '[He] 2s¹', 0.98, 453.69, 1615, 0.534, 1817),
            (4, 'Be', 'Beryllium', 9.0122, 'Alkaline earth metal', 2, 2, '[He] 2s²', 1.57, 1560, 2742, 1.85, 1797),
            (5, 'B', 'Boron', 10.81, 'Metalloid', 2, 13, '[He] 2s² 2p¹', 2.04, 2349, 4200, 2.34, 1808),
            (6, 'C', 'Carbon', 12.011, 'Nonmetal', 2, 14, '[He] 2s² 2p²', 2.55, 3915, 4827, 2.267, None),
            (7, 'N', 'Nitrogen', 14.007, 'Nonmetal', 2, 15, '[He] 2s² 2p³', 3.04, 63.15, 77.36, 0.0012506, 1772),
            (8, 'O', 'Oxygen', 15.999, 'Nonmetal', 2, 16, '[He] 2s² 2p⁴', 3.44, 54.36, 90.20, 0.001429, 1774),
            (9, 'F', 'Fluorine', 18.998, 'Halogen', 2, 17, '[He] 2s² 2p⁵', 3.98, 53.53, 85.03, 0.001696, 1886),
            (10, 'Ne', 'Neon', 20.180, 'Noble gas', 2, 18, '[He] 2s² 2p⁶', None, 24.56, 27.07, 0.0008999, 1898),
            (11, 'Na', 'Sodium', 22.990, 'Alkali metal', 3, 1, '[Ne] 3s¹', 0.93, 370.87, 1156, 0.971, 1807),
            (12, 'Mg', 'Magnesium', 24.305, 'Alkaline earth metal', 3, 2, '[Ne] 3s²', 1.31, 923, 1363, 1.738, 1755),
            (13, 'Al', 'Aluminum', 26.982, 'Post-transition metal', 3, 13, '[Ne] 3s² 3p¹', 1.61, 933.47, 2792, 2.698, 1825),
            (14, 'Si', 'Silicon', 28.085, 'Metalloid', 3, 14, '[Ne] 3s² 3p²', 1.90, 1687, 3538, 2.3296, 1824),
            (15, 'P', 'Phosphorus', 30.974, 'Nonmetal', 3, 15, '[Ne] 3s² 3p³', 2.19, 317.30, 553, 1.82, 1669),
            (16, 'S', 'Sulfur', 32.06, 'Nonmetal', 3, 16, '[Ne] 3s² 3p⁴', 2.58, 388.36, 717.87, 2.067, None),
            (17, 'Cl', 'Chlorine', 35.45, 'Halogen', 3, 17, '[Ne] 3s² 3p⁵', 3.16, 171.6, 239.11, 0.003214, 1774),
            (18, 'Ar', 'Argon', 39.948, 'Noble gas', 3, 18, '[Ne] 3s² 3p⁶', None, 83.80, 87.30, 0.0017837, 1894),
            (19, 'K', 'Potassium', 39.098, 'Alkali metal', 4, 1, '[Ar] 4s¹', 0.82, 336.53, 1032, 0.862, 1807),
            (20, 'Ca', 'Calcium', 40.078, 'Alkaline earth metal', 4, 2, '[Ar] 4s²', 1.00, 1115, 1757, 1.54, 1808),
        ]
        
        cursor = self.connection.cursor()
        
        cursor.executemany("""
            INSERT OR IGNORE INTO elements 
            (atomic_number, symbol, name, atomic_weight, category, period, group_number, 
             electron_configuration, electronegativity, melting_point, boiling_point, density, discovery_year)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, elements_data)
        
        self.connection.commit()
        
    def get_all_elements(self) -> List[Dict]:
        """Get all elements from the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM elements ORDER BY atomic_number")
        rows = cursor.fetchall()
        
        elements = []
        for row in rows:
            element = {
                'id': row['id'],
                'atomic_number': row['atomic_number'],
                'symbol': row['symbol'],
                'name': row['name'],
                'atomic_weight': row['atomic_weight'],
                'category': row['category'],
                'period': row['period'],
                'group': row['group_number'],
                'electron_configuration': row['electron_configuration'],
                'electronegativity': row['electronegativity'],
                'melting_point': row['melting_point'],
                'boiling_point': row['boiling_point'],
                'density': row['density'],
                'discovery_year': row['discovery_year']
            }
            elements.append(element)
            
        return elements
        
    def get_element_by_atomic_number(self, atomic_number: int) -> Optional[Dict]:
        """Get a specific element by atomic number."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM elements WHERE atomic_number = ?", (atomic_number,))
        row = cursor.fetchone()
        
        if row:
            return {
                'id': row['id'],
                'atomic_number': row['atomic_number'],
                'symbol': row['symbol'],
                'name': row['name'],
                'atomic_weight': row['atomic_weight'],
                'category': row['category'],
                'period': row['period'],
                'group': row['group_number'],
                'electron_configuration': row['electron_configuration'],
                'electronegativity': row['electronegativity'],
                'melting_point': row['melting_point'],
                'boiling_point': row['boiling_point'],
                'density': row['density'],
                'discovery_year': row['discovery_year']
            }
        return None
        
    def get_elements_by_category(self, category: str) -> List[Dict]:
        """Get elements by category."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM elements WHERE category = ? ORDER BY atomic_number", (category,))
        rows = cursor.fetchall()
        
        elements = []
        for row in rows:
            element = {
                'id': row['id'],
                'atomic_number': row['atomic_number'],
                'symbol': row['symbol'],
                'name': row['name'],
                'atomic_weight': row['atomic_weight'],
                'category': row['category'],
                'period': row['period'],
                'group': row['group_number'],
                'electron_configuration': row['electron_configuration'],
                'electronegativity': row['electronegativity'],
                'melting_point': row['melting_point'],
                'boiling_point': row['boiling_point'],
                'density': row['density'],
                'discovery_year': row['discovery_year']
            }
            elements.append(element)
            
        return elements
        
    def get_element_count(self) -> int:
        """Get the total number of elements in the database."""
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM elements")
        return cursor.fetchone()[0]
        
    def search_elements(self, search_term: str) -> List[Dict]:
        """Search elements by name or symbol."""
        cursor = self.connection.cursor()
        search_pattern = f"%{search_term}%"
        cursor.execute("""
            SELECT * FROM elements 
            WHERE name LIKE ? OR symbol LIKE ? 
            ORDER BY atomic_number
        """, (search_pattern, search_pattern))
        rows = cursor.fetchall()
        
        elements = []
        for row in rows:
            element = {
                'id': row['id'],
                'atomic_number': row['atomic_number'],
                'symbol': row['symbol'],
                'name': row['name'],
                'atomic_weight': row['atomic_weight'],
                'category': row['category'],
                'period': row['period'],
                'group': row['group_number'],
                'electron_configuration': row['electron_configuration'],
                'electronegativity': row['electronegativity'],
                'melting_point': row['melting_point'],
                'boiling_point': row['boiling_point'],
                'density': row['density'],
                'discovery_year': row['discovery_year']
            }
            elements.append(element)
            
        return elements
        
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
