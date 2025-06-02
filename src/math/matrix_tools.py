"""
Advanced matrix operations and linear algebra tools.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import linalg
import io
import base64
from typing import Dict, Any, Tuple, Optional

class MatrixTools:
    """Advanced matrix operations using NumPy and SciPy."""
    
    def __init__(self):
        self.last_matrix = None
        self.last_result = None
    
    def create_matrix(self, matrix_type: str = "random", size: int = 3, **kwargs) -> np.ndarray:
        """Create different types of matrices."""
        if matrix_type == "random":
            return np.random.rand(size, size)
        elif matrix_type == "identity":
            return np.eye(size)
        elif matrix_type == "zeros":
            return np.zeros((size, size))
        elif matrix_type == "ones":
            return np.ones((size, size))
        elif matrix_type == "diagonal":
            values = kwargs.get('diagonal_values', np.arange(1, size + 1))
            return np.diag(values)
        elif matrix_type == "symmetric":
            A = np.random.rand(size, size)
            return (A + A.T) / 2
        elif matrix_type == "orthogonal":
            # Create orthogonal matrix using QR decomposition
            A = np.random.rand(size, size)
            Q, R = np.linalg.qr(A)
            return Q
        else:
            return np.random.rand(size, size)
    
    def matrix_operations(self, matrix: np.ndarray, operation: str) -> Dict[str, Any]:
        """Perform various matrix operations."""
        self.last_matrix = matrix
        
        results = {
            'matrix': matrix.tolist(),
            'operation': operation,
            'success': True
        }
        
        try:
            if operation == "eigenvalues":
                eigenvals, eigenvecs = linalg.eig(matrix)
                results['eigenvalues'] = eigenvals.tolist()
                results['eigenvectors'] = eigenvecs.tolist()
                results['description'] = f"Matrix has eigenvalues: {eigenvals}"
                
            elif operation == "svd":
                U, s, Vt = linalg.svd(matrix)
                results['U'] = U.tolist()
                results['singular_values'] = s.tolist()
                results['Vt'] = Vt.tolist()
                results['description'] = f"SVD decomposition completed. Singular values: {s}"
                
            elif operation == "determinant":
                det = linalg.det(matrix)
                results['determinant'] = float(det)
                results['description'] = f"Determinant: {det:.6f}"
                
            elif operation == "inverse":
                if matrix.shape[0] != matrix.shape[1]:
                    results['error'] = "Matrix must be square for inversion"
                    results['success'] = False
                else:
                    inv_matrix = linalg.inv(matrix)
                    results['inverse'] = inv_matrix.tolist()
                    results['description'] = "Matrix inverse computed successfully"
                    
            elif operation == "rank":
                rank = np.linalg.matrix_rank(matrix)
                results['rank'] = int(rank)
                results['description'] = f"Matrix rank: {rank}"
                
            elif operation == "condition":
                cond = linalg.norm(matrix) * linalg.norm(linalg.pinv(matrix))
                results['condition_number'] = float(cond)
                results['description'] = f"Condition number: {cond:.6f}"
                
            elif operation == "trace":
                trace = np.trace(matrix)
                results['trace'] = float(trace)
                results['description'] = f"Matrix trace: {trace}"
                
            elif operation == "norm":
                frobenius_norm = linalg.norm(matrix, 'fro')
                spectral_norm = linalg.norm(matrix, 2)
                results['frobenius_norm'] = float(frobenius_norm)
                results['spectral_norm'] = float(spectral_norm)
                results['description'] = f"Frobenius norm: {frobenius_norm:.6f}, Spectral norm: {spectral_norm:.6f}"
                
        except Exception as e:
            results['error'] = str(e)
            results['success'] = False
            
        return results
    
    def visualize_matrix(self, matrix: np.ndarray, visualization_type: str = "heatmap") -> str:
        """Create visualizations for matrices."""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Matrix Analysis Visualization', fontsize=16, fontweight='bold')
        
        # Heatmap of the matrix
        im1 = axes[0, 0].imshow(matrix, cmap='viridis', aspect='auto')
        axes[0, 0].set_title('Matrix Heatmap')
        axes[0, 0].set_xlabel('Column')
        axes[0, 0].set_ylabel('Row')
        plt.colorbar(im1, ax=axes[0, 0])
        
        # Eigenvalue plot
        try:
            eigenvals, _ = linalg.eig(matrix)
            if np.all(np.isreal(eigenvals)):
                eigenvals = np.real(eigenvals)
                axes[0, 1].bar(range(len(eigenvals)), eigenvals, color='skyblue', edgecolor='navy')
                axes[0, 1].set_title('Eigenvalues')
                axes[0, 1].set_xlabel('Index')
                axes[0, 1].set_ylabel('Value')
            else:
                # Complex eigenvalues - plot in complex plane
                axes[0, 1].scatter(np.real(eigenvals), np.imag(eigenvals), 
                                 c='red', s=50, alpha=0.7)
                axes[0, 1].set_title('Eigenvalues (Complex Plane)')
                axes[0, 1].set_xlabel('Real Part')
                axes[0, 1].set_ylabel('Imaginary Part')
                axes[0, 1].grid(True, alpha=0.3)
        except:
            axes[0, 1].text(0.5, 0.5, 'Eigenvalue computation failed', 
                           ha='center', va='center', transform=axes[0, 1].transAxes)
            axes[0, 1].set_title('Eigenvalues - Error')
        
        # Singular values
        try:
            _, s, _ = linalg.svd(matrix)
            axes[1, 0].semilogy(s, 'o-', color='orange', markersize=6)
            axes[1, 0].set_title('Singular Values (Log Scale)')
            axes[1, 0].set_xlabel('Index')
            axes[1, 0].set_ylabel('Singular Value')
            axes[1, 0].grid(True, alpha=0.3)
        except:
            axes[1, 0].text(0.5, 0.5, 'SVD computation failed', 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Singular Values - Error')
        
        # Matrix properties summary
        try:
            det = linalg.det(matrix)
            trace = np.trace(matrix)
            rank = np.linalg.matrix_rank(matrix)
            frobenius_norm = linalg.norm(matrix, 'fro')
            
            properties_text = f"""Matrix Properties:
Shape: {matrix.shape}
Determinant: {det:.4f}
Trace: {trace:.4f}
Rank: {rank}
Frobenius Norm: {frobenius_norm:.4f}
Is Square: {matrix.shape[0] == matrix.shape[1]}
Is Symmetric: {np.allclose(matrix, matrix.T) if matrix.shape[0] == matrix.shape[1] else False}"""
            
            axes[1, 1].text(0.05, 0.95, properties_text, 
                           transform=axes[1, 1].transAxes, fontsize=10,
                           verticalalignment='top', fontfamily='monospace',
                           bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
            axes[1, 1].set_title('Matrix Properties')
            axes[1, 1].axis('off')
        except:
            axes[1, 1].text(0.5, 0.5, 'Property computation failed', 
                           ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Properties - Error')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_data
    
    def compare_matrices(self, matrix1: np.ndarray, matrix2: np.ndarray) -> Dict[str, Any]:
        """Compare two matrices and their properties."""
        results = {
            'success': True,
            'matrix1_shape': matrix1.shape,
            'matrix2_shape': matrix2.shape
        }
        
        try:
            # Basic comparisons
            results['are_equal'] = np.allclose(matrix1, matrix2)
            results['max_difference'] = float(np.max(np.abs(matrix1 - matrix2)))
            results['frobenius_distance'] = float(linalg.norm(matrix1 - matrix2, 'fro'))
            
            # Property comparisons
            if matrix1.shape == matrix2.shape and matrix1.shape[0] == matrix1.shape[1]:
                det1, det2 = linalg.det(matrix1), linalg.det(matrix2)
                trace1, trace2 = np.trace(matrix1), np.trace(matrix2)
                
                results['determinant_diff'] = float(abs(det1 - det2))
                results['trace_diff'] = float(abs(trace1 - trace2))
                
        except Exception as e:
            results['error'] = str(e)
            results['success'] = False
            
        return results