# Example Graphics Script
import matplotlib.pyplot as plt
import numpy as np

def create_plot():
    """Creates a simple sine wave plot."""
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title("Simple Sine Wave")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    return fig

# The function to be called by the app should be named create_plot
# or the figure object should be the last expression.
# For example: plot_figure = create_plot() 