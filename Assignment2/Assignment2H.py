import numpy as np

full_row = np.arange(0, 10)


def fillSudokuRow(sudokuRow):
	temp = np.concatenate((full_row, sudokuRow))
	temp, counts = np.unique(temp, return_counts=True)
	i = np.where(counts == 1)
	sudokuRow[sudokuRow == 0] = i
	return sudokuRow
