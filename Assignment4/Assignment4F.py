import numpy as np
import math


# Function that returns if an specific experiment is complete or not
def isComplete(temp):
	if temp.size == 3:
		return True
	return False


def removeIncomplete(id):
	# This array will hold elements to remove
	numsToDelete = np.array([])
	for i in id:
		temp = id[id > math.floor(i)]
		temp = temp[temp < math.floor(i) + 1]
		# We check if the experiment is not completed
		if not isComplete(temp):
			# Append not completed to the array
			numsToDelete = np.append(numsToDelete, temp)

		# We mask the elements in the that we need to remove from the original array
	mask = np.in1d(id, numsToDelete)
	return id[np.logical_not(mask)]


print(removeIncomplete(np.array([1.3, 2.2, 2.3, 4.2, 5.1, 3.2, 5.3, 3.3, 2.1, 1.1, 5.2, 3.1])))
