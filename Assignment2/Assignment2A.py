import math


# Function to solve the consine rule for any input given
def evaluateTaylor(x):
	y = (x - 1) - math.pow(x - 1, 2) / 2 + math.pow(x - 1, 3) / 3
	return y

