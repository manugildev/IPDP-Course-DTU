def bacteriaGrowth(n0, alpha, K, N):
	tN = 0
	result = n0
	while result < N:
		result = (1 + alpha * (1 - (result / K))) * result
		tN = tN + 1
	return tN
