#!/usr/bin/env python
# title           : Project 1A - Bacteria Data Analyzer
# description     : Handles data related with bacteria growth rates
# Name            : Manuel Gil Martinez
# StudentId       : s170019
# usage           : python3 main.py.py
# python_version  : 3.6
# portfolio       : github.com/manugildev
# web             : manugildev.com
# ==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import sys


# ==============================================================================
class BacteriaAnalyzer:
	# BACTERIAANALYZER Class Holds all the contents of the bacteria data analyzer

	bacteria_names = ["Salmonella enterica", "Bacillus cereus", "Listeria", "Brochothrix thermosphacta"]
	column_names = ["Temperature", "Growth rate", "Bacteria"]
	statistics = ["Mean Temperature", "Mean Growth rate", "Std Temperature", "Std Growth rate", "Rows",
	              "Mean Cold Growth rate", "Mean Hot Growth rate"]
	filters = []
	data = np.array([])

	def checkDataErrors(self, line, temperature, growth_rate, bacteria):
		# CHECKDATAERRORS Checks if the data in the file is valid
		#
		# Usage: error = checkDataErrors(self, line, temperature, growth_rate, bacteria)
		#
		# Input:
		#   line - line number of the file
		#   temperature - temperature of the bacteria
		#   growth_rate - grwoth rate of the bacteria
		#   bacteria - bacteria type in int from 1-4
		# Output: True if there is any error in the input, False if there isn't
		try:
			if float(temperature) < 10 or float(temperature) > 60:
				print("Data Error: Temperature must be within the 10-60 range - Data line {}".format(line))
				return True
			if float(growth_rate) < 0:
				print("Data Error: Growth Rate must be a positive number - Data line {}".format(line))
				return True
			if float(bacteria) not in range(1, 5):
				print("Data Error: Bacteria must be within the 1-4 range - Data line {}".format(line))
				return True
			return False
		except ValueError:
			print("Value Error: One of inputs its not a number - Data line {}".format(line))
			return False

	def dataLoad(self, filename):
		# DATALOAD Loads the data from the file and turns it into a valid numpy array
		#
		# Usage: data = dataLoad(filename)
		#
		# Input:
		#   filename - file name of the file you want to load
		# Output: Numpy array with the valid data

		# Data array that will hold the results, only the valid ones
		data = np.empty((0, 3), float)
		try:
			# Open the file, and do the operations and checks ONLY if the file has been opened
			with open(filename, "r") as f:
				contents = f.read().split("\n")
				# Read line by line, saving the index to know in which line we are at1
				for index, line in enumerate(contents):
					# Save the values into the respective variables
					try:
						temperature, growth_rate, bacteria = line.split(" ")
						# If there is an error in the values, the if will be true, and we will skip the saving of this element
						if self.checkDataErrors(index + 1, temperature, growth_rate, bacteria):
							continue
						# If there are no errors, we save it into the final array
						data = np.vstack((data, [float(temperature), float(growth_rate), float(bacteria)]))
					except ValueError:
						print("Value Error: One of inputs its not a number - Data line {}".format(index + 1))
				print("Success: Data succesfully imported to the analyzer. Data Size: {}".format(np.size(data, axis=0)))
			# Data is sorted by temperature
			return data[data[:,0].argsort()]
		except IOError as e:
			print("I/O error({0}) reading file '{1}': {2}".format(e.errno, filename, e.strerror))

	def dataStatistics(self, data, statistic):
		# DATASTATISTICS Calculates the statistic asked by the user based on the data
		#
		# Usage: statistic = dataStatistics(data, statistic)
		#
		# Input:
		#   data - numpy data used to calculate the statistic
		#   stastic - String that indicates what kind of statistic you want
		# Output: Calculated statistic, None if not valid

		# First we apply the filters saved in the filter array to the data
		data = self.applyFilters(data)

		if statistic == "Mean Temperature":
			return np.mean(data[:, 0])
		elif statistic == "Mean Growth rate":
			return np.mean(data[:, 1])
		elif statistic == "Std Temperature":
			return np.std(data[:, 0])
		elif statistic == "Std Growth rate":
			return np.std(data[:, 1])
		elif statistic == "Rows":
			return np.size(data, axis=0)
		elif statistic == "Mean Cold Growth rate":
			coldRows = data[data[:, 0] < 20]
			if coldRows.size == 0:
				print("No data below 20.")
				return None
			return np.mean(coldRows[:, 1])
		elif statistic == "Mean Hot Growth rate":
			hotRows = data[data[:, 0] > 50]
			if hotRows.size == 0:
				print("No data above 50.")
				return None
			return np.mean(hotRows[:, 1])
		else:
			print("Input Error: In function dataStatistics() input statistic='{}' was not recognized".format(statistic))
			return None

	def dataPlot(self, data):
		# DATAPLOT Shows a plot of the filtered data
		#
		# Usage: dataPlot(data)
		#
		# Input:
		#   data - numpy data that you want to plot

		# First we apply the filters saved in the filter array to the data
		data = self.applyFilters(data)

		print("Showing plots.")
		fig = plt.figure(figsize=(11, 4), dpi=100)
		# BAR CHART
		plt.subplot(1, 3, 1)
		bacteria_array, bacteria_counts = np.unique(data[:, 2], return_counts=True)
		plt.title("Number of bacteria")
		plt.xlabel("Bacteria Type")
		plt.ylabel("Number")
		plt.yticks(bacteria_counts)

		# Legends are in two line mode just for aesthetics
		legends = list(map(lambda i: i.replace(" ", "\n"), self.bacteria_names))
		plt.xticks(bacteria_array, legends, fontsize=8)
		plt.bar(bacteria_array, bacteria_counts, 0.7)

		# PLOT - Growth rate by temperature
		plt.subplot(1, 3, 2)
		plt.title("Growth rate by temperature")
		plt.xlabel("Temperature")
		plt.ylabel("Growth rate")
		for i, type in enumerate(bacteria_array):
			tempData = data[data[:, 2] == type]
			plt.plot(tempData[:, 0], tempData[:, 1], marker='o',
			         label=self.bacteria_names[int(type - 1)])

		plt.legend(loc="upper center", bbox_to_anchor=(1.5, 1), ncol=1)
		plt.xlim([10, 60])
		plt.ylim(ymin=0)
		fig.tight_layout()
		plt.show()

	def applyFilters(self, data):
		# APPLYFILTERS Applies filters in the filter array inside this class to the data
		#
		# Usage: filteredData = applyFilters(data)
		#
		# Input:
		#   data - numpy data that you want to filter
		# Output: numpy array with the filtered data
		filteredData = data
		for f in self.filters:
			# Interate through all the filters that have been already checked in checkValidFilter()
			if f.count("=") == 1:
				# (First type of filter)
				columnName, value = f.split("=")
				if columnName.lower() == bacteria_analyzer.column_names[0].lower():
					# Filter by temperature
					value = float(value)
					filteredData = filteredData[filteredData[:, 0] == value]
				elif columnName.lower() == bacteria_analyzer.column_names[1].lower():
					# Filter by growth rate
					value = float(value)
					filteredData = filteredData[filteredData[:, 1] == value]
				elif columnName == bacteria_analyzer.column_names[2]:
					# By bacteria type, which can be a number or a name
					if value in self.bacteria_names:
						bacteria_index = self.bacteria_names.index(value)
						filteredData = filteredData[filteredData[:, 2] == bacteria_index + 1]
					else:
						filteredData = filteredData[filteredData[:, 2] == float(value)]
			elif f.count("<=") == 2:
				# If smaller or equal than (Second type of filter)
				lowerBound, columnName, upperBound = f.split("<=")
				lowerBound = float(lowerBound)
				upperBound = float(upperBound)
				column_number = list(map(str.lower, bacteria_analyzer.column_names)).index(columnName.lower())
				filteredData = filteredData[filteredData[:, column_number] >= lowerBound]
				filteredData = filteredData[filteredData[:, column_number] <= upperBound]

		if len(self.filters) > 0:
			print("{} filters applied.".format(len(self.filters)))
		return filteredData

	def checkValidFilter(self, filter):
		# CHECKVALIDFILTER Checks if the filter given by the user is valid and can be applied
		#
		# Usage: valid = checkValidFilter(filter)
		#
		# Input:
		#   filter - String with the filter given by the user
		# Output: returns True if valid, False if not

		try:
			if filter.count("=") == 1:
				columnName, value = filter.split("=")
				if columnName.lower() == self.column_names[0].lower():
					value = float(value)
					return True
				elif columnName.lower() == self.column_names[1].lower():
					value = float(value)
					return True
				elif columnName == self.column_names[2]:
					if value.lower() in map(str.lower, self.bacteria_names) or int(value) in range(1, 5):
						return True
				else:
					return False
			elif filter.count("<=") == 2:
				# Second type of filter with range
				lowerBound, columnName, upperBound = filter.split("<=")
				# Check if data is float, if not the except will popup
				lowerBound = float(lowerBound)
				upperBound = float(upperBound)
				if columnName.lower() in map(str.lower, self.column_names):
					return True
			else:
				return False
			return False
		except ValueError:
			return False


# ==============================================================================
class Menu:
	# MENU Class has all the logic, the menu loop and the menu options for the user

	options = ["Load data.", "Add Filter.", "Delete Filter", "Display statistics.", "Generate Plots.", "Quit"]

	def __init__(self, bacteria_analyzer):
		# MENU Constructor
		#
		# Usage: menu = menu(bacteria_analyzer)
		#
		# Input: bacteria analyzer instance in order to access to the data of the data analyzer
		self.bacteria_analyzer = bacteria_analyzer

	def inputNumber(self, prompt):
		# INPUTNUMBER Prompts user to input a number
		#
		# Usage: num = inputNumber(prompt) Displays prompt and asks user to input a
		# number. Repeats until user inputs a valid number.
		#
		# Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015
		while True:
			try:
				num = float(input(prompt))
				break
			except ValueError:
				pass
		return num

	def printHeader(self):
		# PRINTHEADER Prints a header fo the command line interface
		#
		# Usage: printHeader()

		print("\n==============================================================================")
		print("==================          BACTERIA DATA ANALYZER            ================")

	def displayMenu(self, options):
		# DISPLAYMENU Displays a menu of options, ask the user to choose an item
		# and returns the number of the menu item chosen.
		#
		# Usage: choice = displayMenu(options)
		#
		# Input options Menu options (array of strings)
		# Output choice Chosen option (integer)
		#
		# Author: Mikkel N. Schmidt, mnsc@dtu.dk, 2015

		# Display menu options
		print("==============================================================================")
		for i in range(len(options)):
			print(" [{:d}] - {:s}".format(i + 1, options[i]))

		# Get a valid menu choice
		choice = 0
		while not (np.any(choice == np.arange(len(options)) + 1)):
			choice = self.inputNumber(" [?] Please choose a menu item: ")

		print("==============================================================================")
		return choice

	def choiceSelector(self, number):
		# CHOICESELECTOR With the user chose it selects which function needs to run
		#
		# Usage: choiceSelector(choice)
		#
		# Input: Number of choice

		if number == 1:
			self.loadData()
		elif number == 2:
			self.filterData()
		elif number == 3:
			self.deleteFilter()
		elif number == 4:
			self.displayStatistics()
		elif number == 5:
			self.generatePlots()
		elif number == 6:
			quit()

	def loadData(self):
		# LOADDATA Uses the dataLoad from bacteria analyzer to load the data
		#
		# Usage: loadData()

		filename = input("Write the name of the file you want to open: ")
		bacteria_analyzer.data = self.bacteria_analyzer.dataLoad(filename)

	def filterData(self):
		# FILTERDATA Runs the menu options for letting the user write a filter and check if its valid or not
		#
		# Usage: filterData()
		print("You can filter the data by using regular text expressions.Keep in mind that\n"
		      "you can apply more than one filter, and they are added one above the next one\n"
		      "in the order you save them. Some examples are: ")
		print(" ------------------------------------")
		print(" -  Bacteria=Bacillus cereus")
		print(" -  Bacteria=1")
		print(" -  Temperature=25")
		print(" -  0.1<=Growth rate<=0.3")
		print(" -  10<=Temperature<=30")
		print(" -  1<=Bacteria<=2")
		print(" ------------------------------------")
		fSize = len(bacteria_analyzer.filters)
		print("[?] Current number of filters: {}".format(fSize))
		print("[0] Press 0 at any time to exit.")
		print(" ------------------------------------")
		correct = True
		while correct:
			filter = input("Write your filter: ")
			if filter == '0': return False
			if not bacteria_analyzer.checkValidFilter(filter):
				if input("Invalid Filter. ") == '0':
					correct = False
			else:
				bacteria_analyzer.filters.append(filter)
				fSize = len(bacteria_analyzer.filters)
				print("Current number of filters: {}".format(fSize))
				correct = False

	def deleteFilter(self):
		# DELETEFITLER Lets the user delete the filters already saved
		#
		# Usage: deleteFilter()

		fSize = len(bacteria_analyzer.filters)
		if fSize == 0:
			print("You do not have any filters saved.")
			return

		print("  Current number of filters: {}".format(fSize))
		print("  [0] - {:s}".format("Delete all filters."))
		choice = input("  [?] Please choose a menu item: ")
		if choice == '0':
			bacteria_analyzer.filters.clear()
			print("  {} Filters deleted.".format(fSize))
		else:
			print("Invalid input. Going back to menu.")

	def displayStatistics(self):
		# DISPLAYSTATISTICS The different statistic options are displayed and the user can select one
		#
		# Usage: displayStatistics()
		if bacteria_analyzer.data.size == 0:
			print("Data Error: There is no data imported to the analyzer.")
		else:
			choice = self.displayMenu(bacteria_analyzer.statistics)
			selectedStatistic = bacteria_analyzer.statistics[int(choice) - 1]
			result = bacteria_analyzer.dataStatistics(bacteria_analyzer.data, selectedStatistic)
			print("-> {}: {}".format(selectedStatistic, result))

	def generatePlots(self):
		# GENERATEPLOTS Generates the plots from the bacteria_analyzer class
		#
		# Usage: generatePlots()
		if bacteria_analyzer.data.size == 0:
			print("Data Error: There is no data imported to the analyzer.")
		else:
			bacteria_analyzer.dataPlot(bacteria_analyzer.data)

	def loop(self):
		# LOOP Runs the menu over and over again until the input is QUIT and the user exists
		#
		# Usage: loop()
		self.printHeader()
		while True:
			self.choiceSelector(self.displayMenu(self.options))


# ==============================================================================
# Instance of the Bacteria Analyzer class
bacteria_analyzer = BacteriaAnalyzer()
# The menu runs in a loop
menu = Menu(bacteria_analyzer)
menu.loop()
# ==============================================================================
