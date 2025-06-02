# Example Notebook Script
print("Hello from AppSpyder Notebook!")

# You can perform calculations
a = 5
b = 10
print(f"The sum of {a} and {b} is: {a+b}")

# And generate plots with Matplotlib
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 5, 200)
y = x**2

plt.figure(figsize=(6,4))
plt.plot(x, y, label='y = x^2')
plt.title("Parabola Example")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
# The last figure generated will be displayed in the app. 