# %%
import matplotlib.pyplot as plt
import numpy as np

plt.plot([1, 3, 2, 4])
# %%
x = range(6)
plt.plot(x, [xi**2 for xi in x])
# %%
x = np.arange(0.0, 6.0, 0.01)
plt.plot(x, [x**2 for x in x])
# %%
x = range(1, 5)
plt.plot(x, [xi*1.5 for xi in x])
plt.plot(x, [xi*3.0 for xi in x])
plt.plot(x, [xi/3.0 for xi in x])
# %%
x = list(range(1, 5))  # same as range(1, 5)
plt.plot(x, [xi*1.5 for xi in x],
         x, [xi*3.0 for xi in x],
         x, [xi/3 for xi in x])
# %%
x = np.arange(1, 5)
plt.plot(x, x*1.5, x, x*3, x, x/3)
# %%
plt.interactive(True)
plt.hold(False)  # is deprecated
# https://matplotlib.org/api/api_changes.html#hold-functionality-deprecated
plt.plot([1, 2, 3])
plt.plot([2, 4, 6])
