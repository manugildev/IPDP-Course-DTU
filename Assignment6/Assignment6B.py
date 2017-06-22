import numpy as np


def computeItemCost(resourceItemMatrix, resourceCost):
	itemCost = resourceCost * resourceItemMatrix.T
	return np.sum(itemCost, axis=1)
