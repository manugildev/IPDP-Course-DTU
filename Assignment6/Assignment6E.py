import numpy as np
import pandas as pd

def computeLanguageError(freq):
	result = []
	language_frequencies = pd.read_csv("letter_frequencies.csv").drop('Letter', axis=1)
	final = np.power(freq - np.array(language_frequencies).T, 2)
	for i in final:
		result.append(np.sum(i))
	return np.array(result)


print(computeLanguageError(np.array(
	[8.101852, 2.237654, 2.469136, 4.552469, 12.345679, 2.006173, 1.929012, 6.712963, 7.175926, 0.077160, 1.157407,
	 3.395062, 1.080247, 6.712963, 7.870370, 1.466049, 0.077160, 6.018519, 5.401235, 10.956790, 2.854938, 0.925926,
	 2.932099, 0.000000, 1.543210, 0.000000])))
