import numpy as np


def circleAreaMC(xvals, yvals):
	n = 0
	for i in range(xvals.size):
		if np.linalg.norm(np.array([xvals[i], yvals[i]])) < 1:
			n += 1
	return 4 * (n / xvals.size)
