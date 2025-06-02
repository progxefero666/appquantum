"""
File loader utility for dynamically loading and executing Python scripts.
"""

import os
import sys
import importlib.util
import traceback
from typing import Dict, Any
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import io
from contextlib import redirect_stdout
import base64

class FileLoader:
    """Utility class for loading and executing Python script files."""
    
    def __init__(self):
        self.loaded_modules = {}
        
    def load_circuit_file(self, file_path: str) -> Dict[str, Any]:
        """Load and execute a Qiskit circuit file."""
        try:
            # Clear any existing matplotlib figures
            plt.close('all')
            
            # Load the module
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            
            # Add the module directory to sys.path temporarily
            module_dir = os.path.dirname(file_path)
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
                
            try:
                # Execute the module
                spec.loader.exec_module(module)
                
                # Look for common circuit variable names or functions
                circuit = None
                
                # Try different common variable names
                circuit_names = ['circuit', 'qc', 'quantum_circuit', 'main_circuit']
                for name in circuit_names:
                    if hasattr(module, name):
                        circuit = getattr(module, name)
                        break
                        
                # Try to call a function that returns a circuit
                if circuit is None:
                    function_names = ['create_circuit', 'build_circuit', 'get_circuit', 'main']
                    for func_name in function_names:
                        if hasattr(module, func_name):
                            func = getattr(module, func_name)
                            if callable(func):
                                try:
                                    circuit = func()
                                    break
                                except Exception:
                                    continue
                                    
                # If still no circuit, look for any QuantumCircuit object
                if circuit is None:
                    for attr_name in dir(module):
                        if not attr_name.startswith('_'):
                            attr = getattr(module, attr_name)
                            if hasattr(attr, 'num_qubits') and hasattr(attr, 'num_clbits'):
                                circuit = attr
                                break
                                
                if circuit is None:
                    raise Exception("No QuantumCircuit object found in the file")
                    
                return {'circuit': circuit, 'module': module}
                
            finally:
                # Remove the module directory from sys.path
                if module_dir in sys.path:
                    sys.path.remove(module_dir)
                    
        except Exception as e:
            raise Exception(f"Failed to load circuit file '{file_path}': {str(e)}\n{traceback.format_exc()}")
            
    def load_graphics_file(self, file_path: str) -> Dict[str, Any]:
        """Load and execute a matplotlib graphics file."""
        print(f"[FileLoader-GFX] Starting to load graphics file: {file_path}")
        try:
            plt.close('all')
            print("[FileLoader-GFX] plt.close('all') called.")
            
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            
            module_dir = os.path.dirname(file_path)
            path_inserted = False
            if module_dir not in sys.path:
                sys.path.insert(0, module_dir)
                path_inserted = True
                print(f"[FileLoader-GFX] Added {module_dir} to sys.path.")
                
            try:
                print(f"[FileLoader-GFX] Executing module: {module_name}")
                spec.loader.exec_module(module)
                print(f"[FileLoader-GFX] Module {module_name} executed.")
                
                figures_after_exec = plt.get_fignums()
                print(f"[FileLoader-GFX] plt.get_fignums() after exec_module: {figures_after_exec}")
                
                figure_to_return = None

                function_names = ['create_plot', 'plot', 'generate_plot', 'make_plot', 'main']
                for func_name in function_names:
                    if hasattr(module, func_name):
                        print(f"[FileLoader-GFX] Found potential function: {func_name}")
                        func = getattr(module, func_name)
                        if callable(func):
                            print(f"[FileLoader-GFX] Calling function: {func_name}()")
                            try:
                                result = func()
                                print(f"[FileLoader-GFX] Result from {func_name}(): {type(result)}")
                                
                                if isinstance(result, Figure):
                                    print(f"[FileLoader-GFX] Function {func_name} returned a Figure object directly.")
                                    figure_to_return = result
                                    break 
                                
                                current_figures_after_call = plt.get_fignums()
                                print(f"[FileLoader-GFX] plt.get_fignums() after calling {func_name}(): {current_figures_after_call}")
                                if current_figures_after_call:
                                    figure_to_return = plt.figure(current_figures_after_call[-1])
                                    print(f"[FileLoader-GFX] Using figure {current_figures_after_call[-1]} from plt after {func_name}().")
                                    break
                            except Exception as e_func_call:
                                print(f"[FileLoader-GFX] Error calling {func_name}(): {e_func_call}")
                                traceback.print_exc()
                                continue
                    if figure_to_return: break
                
                if figure_to_return is None:
                    print(f"[FileLoader-GFX] No figure returned by functions. Checking active plt figures from initial exec_module.")
                    if figures_after_exec: 
                        figure_to_return = plt.figure(figures_after_exec[-1])
                        print(f"[FileLoader-GFX] Using active figure {figures_after_exec[-1]} from initial exec_module.")

                if figure_to_return is None:
                    print(f"[FileLoader-GFX] No figure from functions or active plt. Checking module attributes.")
                    for attr_name in dir(module):
                        if not attr_name.startswith('_'):
                            attr = getattr(module, attr_name)
                            if isinstance(attr, Figure):
                                print(f"[FileLoader-GFX] Found Figure object in module attribute: {attr_name}")
                                figure_to_return = attr
                                break
                                
                if figure_to_return is None:
                    print(f"[FileLoader-GFX] No specific figure found. Creating fallback image.")
                    figure_to_return = plt.figure(figsize=(8, 6))
                    ax = figure_to_return.add_subplot(111)
                    ax.text(0.5, 0.5, f'Graphics script \'{os.path.basename(file_path)}\' executed.\nNo specific figure was captured or returned.', 
                           transform=ax.transAxes, ha='center', va='center',
                           fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))
                    ax.set_title(f'Output from {os.path.basename(file_path)}')
                    ax.axis('off')
                    print(f"[FileLoader-GFX] Fallback figure created.")
                    
                print(f"[FileLoader-GFX] Returning figure of type: {type(figure_to_return)}")
                return {'figure': figure_to_return, 'module': module}
                
            finally:
                if path_inserted:
                    sys.path.remove(module_dir)
                    print(f"[FileLoader-GFX] Removed {module_dir} from sys.path.")
                    
        except Exception as e:
            print(f"[FileLoader-GFX] CRITICAL ERROR in load_graphics_file for '{file_path}': {str(e)}")
            traceback.print_exc()
            error_fig = plt.figure(figsize=(8,2), dpi=72)
            error_ax = error_fig.add_subplot(111)
            error_ax.text(0.5, 0.5, f"Failed to load graphics file '{os.path.basename(file_path)}':\n{e}",
                          horizontalalignment='center', verticalalignment='center', wrap=True,
                          fontsize=9, color='red')
            error_ax.axis('off')
            return {'figure': error_fig, 'module': None}
            
    def execute_notebook_script(self, file_path: str) -> Dict[str, Any]:
        """Execute a Python script and capture its stdout and any matplotlib figure."""
        print(f"[FileLoader-NB] Starting to execute notebook script: {file_path}")
        captured_stdout = io.StringIO()
        figure_data_base64 = None
        
        try:
            plt.close('all') # Close previous figures
            print("[FileLoader-NB] plt.close('all') called.")

            with open(file_path, 'r', encoding='utf-8') as f:
                script_content = f.read()

            # Prepare a dictionary for the script's global namespace
            # This allows the script to define variables, including 'fig' for matplotlib
            script_globals = {'__name__': '__main__', 'plt': plt}

            print(f"[FileLoader-NB] Executing script content from: {file_path}")
            with redirect_stdout(captured_stdout):
                exec(script_content, script_globals)
            print("[FileLoader-NB] Script content executed.")
            
            stdout_output = captured_stdout.getvalue()
            print(f"[FileLoader-NB] Captured stdout length: {len(stdout_output)}")

            figure_object = None
            if 'fig' in script_globals and isinstance(script_globals['fig'], Figure):
                figure_object = script_globals['fig']
                print("[FileLoader-NB] Found 'fig' variable in script_globals.")
            elif plt.get_fignums():
                figure_object = plt.figure(plt.get_fignums()[-1])
                print(f"[FileLoader-NB] Using active figure {plt.get_fignums()[-1]} from plt.")
            else:
                print("[FileLoader-NB] No specific figure found.")

            if figure_object:
                print(f"[FileLoader-NB] Converting figure of type: {type(figure_object)} to base64.")
                img_buffer = io.BytesIO()
                figure_object.savefig(img_buffer, format='png', bbox_inches='tight')
                plt.close(figure_object)
                img_buffer.seek(0)
                figure_data_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
                print("[FileLoader-NB] Figure converted to base64 and closed.")
            
            return {'stdout_output': stdout_output, 'figure': figure_data_base64}

        except Exception as e:
            print(f"[FileLoader-NB] CRITICAL ERROR in execute_notebook_script for '{file_path}': {str(e)}")
            traceback.print_exc()
            stdout_output = captured_stdout.getvalue()
            stdout_output += f"\n--- ERROR DURING EXECUTION ---\n{str(e)}\n{traceback.format_exc()}"
            
            return {'stdout_output': stdout_output, 'figure': None}
        finally:
            captured_stdout.close()
            plt.close('all')
            print(f"[FileLoader-NB] Execution finished for {file_path}.")

    def clear_cache(self):
        """Clear the loaded modules cache."""
        self.loaded_modules.clear()
        # Also clear matplotlib figures
        plt.close('all')
