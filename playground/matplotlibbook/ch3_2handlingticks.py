# %%
import matplotlib.pyplot as plt
x = [5, 3, 7, 2, 4, 1]
plt.plot(x)
plt.xticks(range(len(x)), ['a', 'b', 'c', 'd', 'e', 'f'])
plt.yticks(range(1, 8 ,2))
plt.show()
