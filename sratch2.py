from sklearn.linear_model import LinearRegression
import numpy as np

x = np.array([0, 0.5, 1, 2, 3])
i = np.where(x == 0.)

print(i[0])

x = np.delete(x, i[0], 0)

print(x)