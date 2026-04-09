import pathlib

import numpy as np
X = np.memmap(r'C:\users\Jonah Benton\GO_trainig_data\test_x.npy', dtype=np.uint8, mode='r+', shape=(999027, 19, 19, 4))
y = np.memmap(r'C:\users\Jonah Benton\GO_trainig_data\test_y.npy', dtype=np.uint16, mode='r+', shape=(999027,))

print(X[999026])
print(y[999027-500:])
print(y.mean(axis=0))
print(y)


