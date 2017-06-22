import numpy as np # Import NumPy
import matplotlib.pyplot as plt # Import the matplotlib.pyplot module

x = (1, 3, 4, 5) # Make some data, x- and y-values
y = (2, 3, 3, 4)
plt.plot(x, y) # Plot line graph of x and y
plt.title("Simple line graph") # Set the title of the graph
plt.xlabel("x-values") # Set the x-axis label
plt.ylabel("y-values") # Set the y-axis label
plt.xlim([0, 6]) # Set the limits of the x-axis
plt.ylim([0, 5]) # Set the limits of the y-axis
plt.show()