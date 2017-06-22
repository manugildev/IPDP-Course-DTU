import numpy as np


def letterFrequency(filename):
	result = []
	file = open(filename, "r").read().lower()
	letters = ""
	alphabet = str('ABCDEFGHIJKLMNOPQRSTUVWXYZ').lower()

	for l in str(file):
		if l in alphabet:
			letters += l

	for a in alphabet:
		result.append([letters.count(a) / len(letters) * 100])

	result = np.array(result)
	return result


print(letterFrequency("small_text.txt"))
