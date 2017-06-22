import numpy as np


def thermoEquilibrium(N, r):
	NL = 0

	t = 0
	while NL != N:
		pLR = (NL / N)
		pRL = 1 - pLR
		if r[t] <= pLR:
			NL = NL - 1
			N = N + 1
		else:
			N = N - 1
			NL = NL + 1

		t = t + 1
		if t > r.size:
			return 0

	return t


print(thermoEquilibrium(2.0, np.array([0.16, 0.04, 0.72, 0.09, 0.17, 0.60, 0.26, 0.65, 0.69, 0.74, 0.45, 0.61,
                                       0.23, 0.37, 0.15, 0.83, 0.61, 1.00, 0.08, 0.44])))
print(thermoEquilibrium(12.0, np.array(
	[0.16, 0.04, 0.72, 0.09, 0.17, 0.60, 0.26, 0.65, 0.69, 0.74, 0.45, 0.61, 0.23, 0.37, 0.15, 0.83, 0.61, 1.00, 0.08,
	 0.44])))
