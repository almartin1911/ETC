# %%
import matplotlib.pyplot as plt
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot([1, 2, 3], [1, 2, 3])
ax2 = fig.add_subplot(212)
ax2.plot([1, 2, 3], [3, 2, 1])
plt.show()
