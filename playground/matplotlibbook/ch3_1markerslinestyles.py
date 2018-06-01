# %% Specifying colors
import matplotlib.pyplot as plt
import numpy as np

y = np.arange(1, 3)
# plt.plot(y, color=(1, 0, 1, 1))
plt.plot(y, 'y')
plt.plot(y+1, 'm')
plt.plot(y+2, 'c')
plt.show()
# %%
plt.plot(y, 'y', y+1, 'm', y+2, 'c')
plt.show()
# %% Line styles
plt.plot(y, '--', y+1, '-.', y+2, ':')
plt.show()
# %% TODO: Markers examples
