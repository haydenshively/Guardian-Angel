import numpy as np

dir_in = '_E_Vectors/'

X_threat = np.load(dir_in + '1.npy')
X_chill = np.load(dir_in + '2.npy')

Y_threat = np.ones((X_threat.shape[0]), dtype = 'float32')
Y_chill = np.ones((X_chill.shape[0]), dtype = 'float32')

X = np.vstack((X_threat, X_chill))
Y = np.vstack((Y_threat, Y_chill))
