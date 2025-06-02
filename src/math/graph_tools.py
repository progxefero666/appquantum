"""
Graph theory and basic topology tools using NumPy.
"""
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from typing import Dict, Any, List, Tuple

class GraphTools:
    """Basic graph theory and topology operations."""
    
    def __init__(self):
        self.adjacency_matrix = None
        self.nodes = []
        self.edges = []
    
    def create_graph(self, graph_type: str = "random", num_nodes: int = 5, **kwargs) -> Dict[str, Any]:
        """Create different types of graphs."""
        self.nodes = list(range(num_nodes))
        
        if graph_type == "random":
            probability = kwargs.get('probability', 0.3)
            adjacency = np.random.random((num_nodes, num_nodes)) < probability
            # Make symmetric for undirected graph
            adjacency = np.logical_or(adjacency, adjacency.T)
            np.fill_diagonal(adjacency, False)
            
        elif graph_type == "complete":
            adjacency = np.ones((num_nodes, num_nodes), dtype=bool)
            np.fill_diagonal(adjacency, False)
            
        elif graph_type == "cycle":
            adjacency = np.zeros((num_nodes, num_nodes), dtype=bool)
            for i in range(num_nodes):
                adjacency[i, (i + 1) % num_nodes] = True
                adjacency[(i + 1) % num_nodes, i] = True
                
        elif graph_type == "path":
            adjacency = np.zeros((num_nodes, num_nodes), dtype=bool)
            for i in range(num_nodes - 1):
                adjacency[i, i + 1] = True
                adjacency[i + 1, i] = True
                
        elif graph_type == "star":
            adjacency = np.zeros((num_nodes, num_nodes), dtype=bool)
            for i in range(1, num_nodes):
                adjacency[0, i] = True
                adjacency[i, 0] = True
                
        elif graph_type == "wheel":
            # Cycle + center node connected to all
            adjacency = np.zeros((num_nodes, num_nodes), dtype=bool)
            # Create cycle for outer nodes
            for i in range(1, num_nodes):
                adjacency[i, 1 + (i % (num_nodes - 1))] = True
                adjacency[1 + (i % (num_nodes - 1)), i] = True
            # Connect center (node 0) to all others
            for i in range(1, num_nodes):
                adjacency[0, i] = True
                adjacency[i, 0] = True
                
        else:
            adjacency = np.random.random((num_nodes, num_nodes)) < 0.3
            adjacency = np.logical_or(adjacency, adjacency.T)
            np.fill_diagonal(adjacency, False)
        
        self.adjacency_matrix = adjacency.astype(int)
        self.edges = [(i, j) for i in range(num_nodes) for j in range(i+1, num_nodes) 
                      if adjacency[i, j]]
        
        return {
            'adjacency_matrix': self.adjacency_matrix.tolist(),
            'num_nodes': num_nodes,
            'num_edges': len(self.edges),
            'edges': self.edges,
            'graph_type': graph_type
        }
    
    def graph_properties(self) -> Dict[str, Any]:
        """Calculate basic graph properties."""
        if self.adjacency_matrix is None:
            return {'error': 'No graph created yet'}
        
        num_nodes = self.adjacency_matrix.shape[0]
        num_edges = np.sum(self.adjacency_matrix) // 2  # Undirected graph
        
        # Degree sequence
        degrees = np.sum(self.adjacency_matrix, axis=1)
        
        # Check if connected (simple check using adjacency matrix powers)
        reachability = self.adjacency_matrix.copy()
        for _ in range(num_nodes):
            reachability = np.logical_or(reachability, 
                                       np.dot(reachability, self.adjacency_matrix) > 0)
        is_connected = np.all(reachability + np.eye(num_nodes))
        
        # Basic topological properties
        max_degree = int(np.max(degrees))
        min_degree = int(np.min(degrees))
        avg_degree = float(np.mean(degrees))
        
        # Density
        density = 2 * num_edges / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0
        
        return {
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'degree_sequence': degrees.tolist(),
            'max_degree': max_degree,
            'min_degree': min_degree,
            'average_degree': avg_degree,
            'density': density,
            'is_connected': bool(is_connected)
        }
    
    def shortest_paths(self) -> Dict[str, Any]:
        """Calculate shortest paths using Floyd-Warshall algorithm."""
        if self.adjacency_matrix is None:
            return {'error': 'No graph created yet'}
        
        num_nodes = self.adjacency_matrix.shape[0]
        
        # Initialize distance matrix
        dist = np.full((num_nodes, num_nodes), np.inf)
        
        # Distance from node to itself is 0
        np.fill_diagonal(dist, 0)
        
        # Distance between adjacent nodes is 1
        dist[self.adjacency_matrix == 1] = 1
        
        # Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if dist[i, k] + dist[k, j] < dist[i, j]:
                        dist[i, j] = dist[i, k] + dist[k, j]
        
        # Replace infinities with -1 for JSON serialization
        dist[dist == np.inf] = -1
        
        return {
            'distance_matrix': dist.tolist(),
            'diameter': float(np.max(dist[dist != -1])) if np.any(dist != -1) else -1,
            'average_distance': float(np.mean(dist[dist != -1])) if np.any(dist != -1) else -1
        }
    
    def visualize_graph(self) -> str:
        """Create a visualization of the graph."""
        if self.adjacency_matrix is None:
            return ""
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('Graph Analysis', fontsize=16, fontweight='bold')
        
        num_nodes = self.adjacency_matrix.shape[0]
        
        # 1. Graph visualization with spring layout
        ax1 = axes[0, 0]
        
        # Simple spring layout algorithm
        pos = self._spring_layout(num_nodes)
        
        # Draw edges
        for i, j in self.edges:
            x_vals = [pos[i][0], pos[j][0]]
            y_vals = [pos[i][1], pos[j][1]]
            ax1.plot(x_vals, y_vals, 'b-', alpha=0.6, linewidth=1)
        
        # Draw nodes
        x_coords = [pos[i][0] for i in range(num_nodes)]
        y_coords = [pos[i][1] for i in range(num_nodes)]
        ax1.scatter(x_coords, y_coords, c='red', s=200, alpha=0.8, zorder=5)
        
        # Label nodes
        for i in range(num_nodes):
            ax1.annotate(str(i), (pos[i][0], pos[i][1]), 
                        xytext=(0, 0), textcoords='offset points',
                        ha='center', va='center', fontweight='bold', color='white')
        
        ax1.set_title('Graph Structure')
        ax1.set_aspect('equal')
        ax1.axis('off')
        
        # 2. Adjacency matrix heatmap
        ax2 = axes[0, 1]
        im = ax2.imshow(self.adjacency_matrix, cmap='Blues', aspect='auto')
        ax2.set_title('Adjacency Matrix')
        ax2.set_xlabel('Node')
        ax2.set_ylabel('Node')
        
        # Add text annotations
        for i in range(num_nodes):
            for j in range(num_nodes):
                ax2.text(j, i, str(self.adjacency_matrix[i, j]),
                        ha="center", va="center", color="red" if self.adjacency_matrix[i, j] else "gray")
        
        # 3. Degree distribution
        ax3 = axes[1, 0]
        degrees = np.sum(self.adjacency_matrix, axis=1)
        ax3.bar(range(num_nodes), degrees, color='skyblue', edgecolor='navy')
        ax3.set_title('Degree Distribution')
        ax3.set_xlabel('Node')
        ax3.set_ylabel('Degree')
        
        # 4. Graph properties text
        ax4 = axes[1, 1]
        properties = self.graph_properties()
        
        properties_text = f"""Graph Properties:
Nodes: {properties['num_nodes']}
Edges: {properties['num_edges']}
Density: {properties['density']:.3f}
Max Degree: {properties['max_degree']}
Min Degree: {properties['min_degree']}
Avg Degree: {properties['average_degree']:.2f}
Connected: {properties['is_connected']}"""
        
        ax4.text(0.05, 0.95, properties_text, 
                transform=ax4.transAxes, fontsize=11,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        ax4.set_title('Graph Properties')
        ax4.axis('off')
        
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_data
    
    def _spring_layout(self, num_nodes: int, iterations: int = 50) -> Dict[int, Tuple[float, float]]:
        """Simple spring layout algorithm for graph visualization."""
        # Initialize random positions
        pos = {i: (np.random.random(), np.random.random()) for i in range(num_nodes)}
        
        k = 1.0 / np.sqrt(num_nodes)  # Optimal distance
        
        for _ in range(iterations):
            # Calculate forces
            forces = {i: (0.0, 0.0) for i in range(num_nodes)}
            
            # Repulsive forces between all nodes
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    dx = pos[i][0] - pos[j][0]
                    dy = pos[i][1] - pos[j][1]
                    dist = max(np.sqrt(dx*dx + dy*dy), 0.01)
                    
                    # Repulsive force
                    force = k * k / dist
                    fx = force * dx / dist
                    fy = force * dy / dist
                    
                    forces[i] = (forces[i][0] + fx, forces[i][1] + fy)
                    forces[j] = (forces[j][0] - fx, forces[j][1] - fy)
            
            # Attractive forces for connected nodes
            for i, j in self.edges:
                dx = pos[i][0] - pos[j][0]
                dy = pos[i][1] - pos[j][1]
                dist = max(np.sqrt(dx*dx + dy*dy), 0.01)
                
                # Attractive force
                force = dist * dist / k
                fx = force * dx / dist
                fy = force * dy / dist
                
                forces[i] = (forces[i][0] - fx, forces[i][1] - fy)
                forces[j] = (forces[j][0] + fx, forces[j][1] + fy)
            
            # Update positions
            for i in range(num_nodes):
                displacement = np.sqrt(forces[i][0]**2 + forces[i][1]**2)
                if displacement > 0:
                    # Limit displacement
                    max_displacement = min(0.1, 0.1 / displacement)
                    pos[i] = (
                        pos[i][0] + forces[i][0] * max_displacement,
                        pos[i][1] + forces[i][1] * max_displacement
                    )
        
        return pos