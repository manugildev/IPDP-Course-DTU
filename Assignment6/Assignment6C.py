import numpy as np

def movingAvg(y):
	""" Returns the moving average of the sinal given
	Information: In this function the matrix to the the opteraions is created and not given
	Parameter1 - T - Temperature you want to convert
	Parameter2 - unitFrom - Original Temperature
	Parameter3 - unitTo - The final Temperature you want to obtain
	"""
	# First we create the 5 row matrix of the same y signal
	A = y
	for i in range(4):
		y = np.vstack((A, y))

	# The Matrix M stores how much do we have to shift the final matrix
	M = np.array([np.arange(-2, 3)]) # [-2,-1,0,1,2]

	# The Matrix M1 stores the multiplication factor per row
	M1 = (np.absolute(M.T) * -1) + 3 # [1,2,3,2,1]

	# Each number of the final matrix is multiplied by i
	multiplied_matrix = (y * (M1))

	# We initialize an empty array
	final = np.zeros(shape=(5, y[0].size))
	i = -1 # Column counter, starts at -1 because it is used in the first line of the loop
	# This for loop is used to find each final number for the matrix
	# also the rows are shifted using the pad
	for row in multiplied_matrix:
		i += 1
		shif_factor = M[0, i]
		if shif_factor > 0:
			final[i] = np.array([np.pad(row, (shif_factor, 0), mode='constant')[:-shif_factor]])
		elif shif_factor < 0:
			final[i] = np.array([np.pad(row, (0, abs(shif_factor)), mode='constant')[-shif_factor:]])
		else:
			final[i] = np.array([row])

	# Finally we sum app all the columns and divide by 9
	return np.sum(final, axis=0) / 9

print(movingAvg(np.array([0.8, 0.9, 0.7, 0.6, 0.3, 0.4])))
print(movingAvg(np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])))
