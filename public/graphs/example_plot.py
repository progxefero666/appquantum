"""
Example matplotlib plot for the AppSpyder Graphics module.
This creates a mathematical visualization with multiple subplots.
"""

import numpy as np
import matplotlib.pyplot as plt

def create_plot():
    """Create an example mathematical plot with multiple visualizations."""
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Mathematical Functions Visualization', fontsize=16, fontweight='bold')
    
    # Generate data
    x = np.linspace(-2*np.pi, 2*np.pi, 1000)
    
    # Plot 1: Trigonometric functions
    ax1.plot(x, np.sin(x), 'b-', label='sin(x)', linewidth=2)
    ax1.plot(x, np.cos(x), 'r-', label='cos(x)', linewidth=2)
    ax1.plot(x, np.tan(x), 'g-', label='tan(x)', linewidth=1, alpha=0.7)
    ax1.set_ylim(-3, 3)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Trigonometric Functions')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Exponential and logarithmic functions
    x2 = np.linspace(0.1, 3, 1000)
    ax2.plot(x2, np.exp(x2), 'purple', label='e^x', linewidth=2)
    ax2.plot(x2, np.log(x2), 'orange', label='ln(x)', linewidth=2)
    ax2.plot(x2, x2**2, 'brown', label='x²', linewidth=2)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('Exponential & Power Functions')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: 3D-like visualization (parametric plot)
    t = np.linspace(0, 4*np.pi, 1000)
    x3 = t * np.cos(t)
    y3 = t * np.sin(t)
    ax3.plot(x3, y3, 'magenta', linewidth=2)
    ax3.set_xlabel('x')
    ax3.set_ylabel('y')
    ax3.set_title('Parametric Spiral: (t·cos(t), t·sin(t))')
    ax3.grid(True, alpha=0.3)
    ax3.axis('equal')
    
    # Plot 4: Statistical visualization
    np.random.seed(42)
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(2, 1.5, 1000)
    
    ax4.hist(data1, bins=30, alpha=0.7, label='Dataset 1 (μ=0, σ=1)', color='skyblue')
    ax4.hist(data2, bins=30, alpha=0.7, label='Dataset 2 (μ=2, σ=1.5)', color='lightcoral')
    ax4.set_xlabel('Value')
    ax4.set_ylabel('Frequency')
    ax4.set_title('Normal Distribution Comparison')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# Create the plot (this will be found by the file loader)
figure = create_plot()
