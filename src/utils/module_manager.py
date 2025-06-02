"""
Module manager for AppSpyder application.
Simple file and module management system.
"""

import os
import glob
import json
from typing import List, Dict, Any, Optional

class ModuleManager:
    """Simple module manager for file operations."""
    
    def __init__(self):
        self.base_path = "."
        self.modules = {
            'circuits': 'public/circuits',
            'graphics': 'public/graphs',
            'elements': 'data'
        }
    
    def get_module_files(self, module_name: str) -> List[str]:
        """Get list of Python files from a module directory."""
        try:
            if module_name not in self.modules:
                return []
            
            directory = os.path.join(self.base_path, self.modules[module_name])
            if not os.path.exists(directory):
                return []
            
            files = glob.glob(os.path.join(directory, "*.py"))
            return [os.path.basename(f) for f in files if os.path.isfile(f)]
        except Exception:
            return []
    
    def get_file_content(self, module_name: str, filename: str) -> Optional[str]:
        """Get content of a specific file."""
        try:
            if module_name not in self.modules:
                return None
            
            directory = os.path.join(self.base_path, self.modules[module_name])
            filepath = os.path.join(directory, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception:
            return None
    
    def generate_frontend_config(self) -> Dict[str, Any]:
        """Generate configuration for frontend modules."""
        config = {
            'modules': [
                {
                    'id': 'circuits',
                    'name': 'Quantum Circuits',
                    'description': 'Qiskit quantum circuit visualization',
                    'available': True
                },
                {
                    'id': 'graphics',
                    'name': 'Math Graphics',
                    'description': 'Mathematical visualizations',
                    'available': True
                },
                {
                    'id': 'elements',
                    'name': 'Periodic Elements',
                    'description': 'Chemical elements database',
                    'available': True
                },
                {
                    'id': 'waves',
                    'name': 'Quantum Waves',
                    'description': 'Quantum wave physics',
                    'available': True
                },
                {
                    'id': 'pandas',
                    'name': 'Data Analysis',
                    'description': 'Pandas data processing',
                    'available': True
                }
            ]
        }
        return config
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get status of all modules."""
        status = {}
        for module_name in self.modules:
            files = self.get_module_files(module_name)
            status[module_name] = {
                'available': len(files) > 0,
                'file_count': len(files),
                'files': files
            }
        return status