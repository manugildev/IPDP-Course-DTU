import numpy as  np


def fermentationRate(measuredRate, lowerBound, upperBound):
	measuredRate = measuredRate[measuredRate > lowerBound]
	measuredRate = measuredRate[measuredRate < upperBound]
	return np.average(measuredRate)
