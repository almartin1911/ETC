# %% Try this cell only in a shell execution
import matplotlib as mpl
mpl.use('GTK3Agg')
import matplotlib.pyplot as plt
plt.plot([1, 3, 2, 4])
plt.show()
# %%
mpl.rcParams['interactive']
mpl.rcParams['backend']
# Can be set to False or True
mpl.interactive(True)
mpl.rcParams
