from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd

points = pd.read_csv('data.csv')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.ylabel('z')
plt.xlabel('x')

x = points['x'].values
z = points['y'].values
y = points['z'].values

ax.scatter(x, y, -z, c='r', marker='o')
ax.scatter(0, 0, 0, s=40, c='b', marker='o')
plt.show()
