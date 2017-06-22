import numpy as np

def step(cluster1, cluster2, previous):
	result = []
	cl1 = []
	cl2 = []

	for element in previous:
		if abs(np.mean(cluster1) - element) >= abs(np.mean(cluster2)-element):
			result.append(2)
			cl2.append(float(element))
		else:
			result.append(1)
			cl1.append(float(element))

	return cl1, cl2, np.array(result)


def clusterAnalysis(reflectance):
	cluster1 = reflectance[1::2]
	cluster2 = reflectance[::2]

	cluster1, cluster2, current = step(cluster1, cluster2, reflectance)
	previous = np.zeros(reflectance.size)

	while not (current == previous).all():
		previous = current
		cluster1, cluster2, current = step(cluster1, cluster2, reflectance)

	return current


print(clusterAnalysis(np.array([1.7, 1.6, 1.3, 1.3, 2.8, 1.4, 2.8, 2.6, 1.6, 2.7])))

print(clusterAnalysis(np.array([10.0, 12.0, 10.0, 12.0, 9.0, 11.0, 11.0, 13.0]))) #[1 2 1 2 1 1 1 2]
