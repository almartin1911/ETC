# As Python Zen has teached us: Explicit is better than implicit
# This "heavy" expressiveness will be apreciated when embeding matplotlib
# inside GUI applications is required

import matplotlib as mpl
mpl.use('GTK3Agg')
print(mpl.rcParams['backend'])
import matplotlib.pyplot as plt
import numpy as np
x = np.arange(0, 10, 0.1)
y = np.random.randn(len(x))
fig = plt.figure()
print(fig)
ax = fig.add_subplot(111)
print(ax)
l, = plt.plot(x, y)
print(l)
t = ax.set_title('random numbers')
print(t)
plt.show()
