# %%
import matplotlib.pyplot as plt
import numpy as np

plt.plot([1, 3, 2, 4])
plt.title('Simple plot')
plt.show()
# %%
x = np.arange(1, 5)
plt.plot(x, x*1.5, label='Normal')
plt.plot(x, x*3.0, label='Fast')
plt.plot(x, x/3.0, label='Slow')
plt.legend()
plt.show()
# %% Still not an optimal solution
plt.plot(x, x*1.5)
plt.plot(x, x*3.0)
plt.plot(x, x/3.0)
plt.legend(['Normal', 'Fast', 'Slow'])
plt.show()
# %%
