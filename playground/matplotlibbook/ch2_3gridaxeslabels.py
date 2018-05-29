# Adding a grid
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 5)
plt.plot(x, x*1.5, x, x*3.0, x, x/3)
plt.grid(True)

# Handling axes
plt.plot(x, x*1.5, x, x*3.0, x, x/3)
plt.axis([0, 5, -1, 13])

# Labels
plt.plot(x, x*1.5, x, x*3.0, x, x/3)
plt.xlabel('This is the X axis')
plt.ylabel('This is the Y axis')
