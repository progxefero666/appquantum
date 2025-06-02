import matplotlib.pyplot as plt
import numpy as np

print("Iniciando la generación de un gráfico de ejemplo...")

# Datos para el gráfico
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Crear la figura y el eje
fig, ax = plt.subplots()

# Graficar los datos
ax.plot(x, y)

# Añadir título y etiquetas
ax.set_title("Gráfico de Ejemplo (Seno)")
ax.set_xlabel("Eje X")
ax.set_ylabel("Eje Y")

# No llamamos a plt.show() directamente ya que la figura será capturada
# por el FileLoader.

print("Gráfico generado. La figura debería ser capturada.")

# La figura 'fig' es la que se espera que capture FileLoader. 