import math
import numpy as np


def computeProjection(a):
	b = np.ones(a.size)
	projection = ((np.dot(a, b)) / math.pow(np.linalg.norm(a), 2)) * a
	return projection


print(computeProjection(np.array([2, -1])))
