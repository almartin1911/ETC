# %%
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(1, 5)
plt.plot(x, x*1.5, label='Normal')
plt.plot(x, x*3.0, label='Fast')
plt.plot(x, x/3.0, label='Slow')
plt.grid(True)
plt.title('Sample Growth of a Measure')
plt.xlabel('Samples')
plt.ylabel('Values Measured')
# plt.legend(loc='upper left')
plt.legend()
plt.show()
# plt.savefig('completeexample.png', dpi=200)
# %% Multiply dpi by size
import matplotlib as mpl
mpl.rcParams['figure.figsize']
mpl.rcParams['savefig.dpi']
mpl.rcParams['figure.dpi']
# %%
mpl.use('Agg')
import matplotlib.pyplot as plt
plt.plot([1, 2, 3])
plt.savefig('plot123.png')
