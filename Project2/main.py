#!/usr/bin/env python
# title           : Project 2B - Student Grader
# description     : Process data of student's grades
# Name            : Manuel Gil Martinez
# StudentId       : s170019
# usage           : python3 main.py.py
# python_version  : 3.6
# portfolio       : github.com/manugildev
# web             : manugildev.com
# ==============================================================================

from random import randint

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys


# ==============================================================================
class StudentGrader():
	stepScale7 = [12, 10, 7, 4, 2, 0, -3]
	rawImportedData = pd.DataFrame()
	data = np.array([])
	studentIDs = np.array([])

	# This variable will change whenever you check and remove the errors on the data
	dataContainsErrors = True

	def dataLoad(self, filename):
		# DATALOAD Loads the data from the file and turns it into a valid numpy array
		#
		# Usage: data = dataLoad(filename)
		#
		# Input:
		#   filename - file name of the file you want to load
		# Output: Numpy matrix with the valid data NxM (Students x Assignments)
		try:
			self.rawImportedData = pd.read_csv(filename)
			self.studentIDs = np.array(self.rawImportedData.StudentID)
			self.data = np.array(self.rawImportedData.drop(['StudentID', 'Name'], axis=1))
			print("Data imported to the Student Grader.")
			self.dataContainsErrors = True # Since we haven't checked the data yet
		except:
			print("Data Load Error: File '{}' could not be readed.".format(filename))

		return self.data

	def checkRepeatedData(self, data, delete):
		# CHECKDATAFORERRORS Check if some of the data is repeated
		#
		# Usage: noRepeatedData = checkRepeatedData(data)
		#
		# Input:
		#  - data to be checked
		#  - delete: If setted to true, the error data is deleted in the student grader
		# Output: Returns the data without the lines that are repeated, keeps last repeated line
		self.studentIDs = np.array(self.rawImportedData.StudentID)
		unique, inverse, unique_counts = np.unique(self.studentIDs, return_inverse=True, return_counts=True)

		# Look for repeated items and get which ones are repeated
		mask = np.in1d(unique_counts, unique_counts[unique_counts > 1])
		repeatedElements = unique[mask]

		if repeatedElements.size > 0:
			print("Data ERROR: There are {} repeated students in the data imported:".format(repeatedElements.size))
			for r in repeatedElements:
				print("  - StudentID [{}] is repeated.".format(r))
		else:
			print("There are no repeated students.")
			return self.data

		# Only if delete = true the data of this class will be modified with removed data errors
		if delete:
			print("> Removing repeated Students, keeping LAST grades.")
			# Using drop_duplicates, duplicates students are deleted
			self.rawImportedData = self.rawImportedData.drop_duplicates(subset='StudentID', keep='last')
			self.studentIDs = np.array(self.rawImportedData.StudentID)
		return np.array(self.rawImportedData.drop(['StudentID', 'Name'], axis=1))

	def checkInvalidGrades(self, data, delete):
		# CHECKINVALIDGRADES Checks if a grade in the data set is not one of the possible grades on the 7-step-scale
		#
		# Usage: validGrades = checkRepeatedData(data)
		#
		# Input:
		#  - data to be checked
		#  - delete: If setted to true, the error data is deleted in the student grader
		# Output: Returns the data without the invalid row

		dataError = False
		for index, row in enumerate(data):
			for element in row:
				if element not in self.stepScale7:
					studentId = self.studentIDs[index]
					dataError = True
					print("Data ERROR: Student {} has an invalid grade '{}'.".format(studentId, element))
					if delete: self.rawImportedData = self.rawImportedData.drop(self.rawImportedData.index[[index]])

		# We just let the user know that there were no errors in the data
		if not dataError:
			print("There are no invalid grades.")
			return self.data

		# Only if delete = true the data of this class will be modified with removed data errors
		if delete:
			self.studentIDs = np.array(self.rawImportedData.StudentID)
			print("> Removing students with invalid Grades.")
		return np.array(self.rawImportedData.drop(['StudentID', 'Name'], axis=1))

	def checkDataForErrors(self, delete):
		# CHECKDATAFORERRORS Checks if the rawImportedData from this class has errors
		#
		# Usage: noErrorData = checkDataErrors(filename)
		#
		# Input:
		#  - delete: If setted to true, the error data is deleted in the student grader
		# Output: Data without errors
		if self.rawImportedData.empty:
			print("Check Data Error: It seems that the imported data variable is empty. Import something first.")
			return 0
		else:
			self.data = self.checkRepeatedData(self.data, delete)
			self.data = self.checkInvalidGrades(self.data, delete)
			if delete: self.dataContainsErrors = False;

		return self.data

	def roundGrade(self, grades):
		# ROUNDGRADE Loads the data from the file and turns it into a valid numpy array, if there is a tie it will get
		# the higher grade because of how the 7-step-scale is ordered
		#
		# Usage: gradesRounded = roundGrade(grade)
		#
		# Input:
		#   grades - A vector (each element is a number between −3 and 12).
		# Output:
		#  gradesRounded - A vector (each element is a number on the 7-step-scale
		gradesRounded = []
		for grade in grades:
			# The difference between all the elements and the 7 step scale is calculated
			difference = np.absolute(np.subtract(self.stepScale7, grade))
			# ng.argmin returns the index of the minimum difference, only returns first ocurrence
			indexOfMinimum = np.argmin(difference)
			gradesRounded.append(self.stepScale7[indexOfMinimum])

		return np.array(gradesRounded)

	def computeFinalGrade(self, grades):
		# COMPUTEFINALGRADE For each student the final Grade is computed
		#
		# Usage: gradesFinal = computeFinalGrade(grades)
		#
		# Input:
		#   grades - An N × M matrix containing grades on the 7-step-scale given to N students
		#    on M different assignments.
		# Output:
		#  gradesFinal - mA vector of length n containing the final grade for each of the N students.
		gradesFinal = []
		for student_grades in grades:
			student_grades = np.array(student_grades)
			# If in any of the assigments the student has -3, the mean will be -3
			if student_grades[student_grades == -3].size > 0:
				gradesFinal.append(np.array([-3]))
				continue

			if student_grades.size == 1:
				# If there is only one grade we return that grade
				gradesFinal.append(np.array(student_grades))
			elif student_grades.size > 1:
				# When more than one grade, we remove the minimum and return the grades for that
				indexOfMinimum = np.argmin(student_grades)
				student_grades = np.delete(student_grades, indexOfMinimum)
				gradesFinal.append(np.mean(student_grades))

		return np.array(self.roundGrade(gradesFinal))

	def gradesPlot(self, grades):
		# GRADESPLOT Shows a plot of the student grades
		#
		# Usage: dataPlot(data)
		#
		# Input:
		#   grades - numpy grades that you want to plot

		# First we calculate the final grades with tha given grades

		print("Showing plots.")
		finalGrades = self.computeFinalGrade(grades)
		yValues = []

		# We get how many students have scored X final grade based on the 7 step scale
		for step in self.stepScale7:
			current_step_sum = finalGrades[finalGrades == step].size
			yValues.append(current_step_sum)

		fig = plt.figure(figsize=(11, 4), dpi=100)

		# BAR CHART - Final Grades
		plt.subplot(1, 3, 1)
		plt.title("Final Grades")
		plt.xlabel("7 Step Scale")
		plt.ylabel("Students")
		plt.yticks(yValues)
		plt.xticks(self.stepScale7, fontsize=8)
		plt.bar(self.stepScale7, yValues, 0.7)

		# PLOT - Grades per assignment
		plt.subplot(1, 3, 2)
		plt.title("Grades per Assignment")
		plt.xlabel("Assignment Number")
		plt.ylabel("Grades")
		plt.yticks(self.stepScale7, fontsize=8)
		plt.xticks(range(1, grades[0].size + 1), fontsize=8)
		plt.ylim([-4, 13])
		# plt.xlim([.5, grades[0].size+.5])

		# Every plot for every student's assignments
		for i, student_grades in enumerate(grades):
			plt.plot(range(1, student_grades.size + 1), student_grades, marker='o', markersize=randint(2, 7),
			         linestyle='None', label=self.studentIDs[i])

		# Get the average of each assignments by transposing the matrix
		assignments_average = []
		for assignments_notes in grades.T:
			assignments_average.append(np.average(assignments_notes))

		# Plot the assignments averages with a line
		plt.plot(range(1, grades[0].size + 1), assignments_average, marker='o', markersize=5, linestyle=":",
		         label="Assignment\nAverage")

		plt.legend(loc="upper right", bbox_to_anchor=(2, 1), ncol=2)
		fig.tight_layout()
		plt.show()

	def displayListGrades(self):
		# DISPLAYLISTGRADES Shows a table of the students grade sorted by name alphabetically
		#
		# Usage: displayListGrades()
		#
		print("Showing data.")
		print("\n==============================================================================")
		print("======================         GRADES by name         ========================")
		print("==============================================================================\n")
		finalGradesArray = self.computeFinalGrade(self.data)
		listGrades = self.rawImportedData
		listGrades["Final Grades"] = finalGradesArray
		# Sort in alphabetical order by name
		listGrades = listGrades.sort_values(by='Name')
		# The built-in panda print functionality is used to print the table
		print(listGrades)
		input()


# ==============================================================================
class Menu:
	# MENU Class has all the logic, the menu loop and the menu options for the user

	options = ["Load new data.", "Check for data errors.", "Remove Data with Errors", "Generate plots.",
	           "Display list of grades.", "Quit"]

	def __init__(self, student_grader):
		# MENU Constructor
		#
		# Usage: menu = menu(student_grader)
		#
		# Input: StudentGrader instance in order to access to the data and methods of the student grader
		self.student_grader = student_grader

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
		print("==================              STUDENT GRADER                ================")

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
		# CHOICESELECTOR With the user chose it selects wich function needs to run
		#
		# Usage: choiceSelector(choice)
		#
		# Input: Number of choice

		if number == 1:
			self.loadData()
		elif number == 2:
			self.checkDataErrors()
		elif number == 3:
			self.removeDataErrors()
		elif number == 4:
			self.generatePlots()
		elif number == 5:
			self.displayListGrades()
		elif number == 6:
			sys.exit()

	def checkDataErrors(self):
		# CHECKDATAERRORS Uses the dataLoad from student grader to check if the data has errors
		# this function does not delete the data with
		#
		# Usage: checkDataErrors()
		# Output: grades checked
		student_grader.checkDataForErrors(delete=False)

	def removeDataErrors(self):
		# REMOVEDATAERRORS Uses the dataLoad from student grader to check if the data has errors
		# this function does delete the data with
		#
		# Usage: removeDataErrors()
		# Output: grades without errors
		student_grader.checkDataForErrors(delete=True)

	def displayListGrades(self):
		# DISPLAYLISTGRADESD This function shows in the command line a table with the grades by using the function
		# in the student grader class
		#
		# Usage: displayListGrades()
		if student_grader.data.size == 0:
			print("Data Error: There is no data imported to the analyzer.")
		else:
			self.askForDeleteFirst()
			student_grader.displayListGrades()

	def askForDeleteFirst(self):
		if student_grader.dataContainsErrors:
			if input("Do you want to delete data with errors first? [Y/N]: ").lower() == 'y':
				student_grader.checkDataForErrors(delete=True)

	def loadData(self):
		# LOADDATA Uses the dataLoad from student grader to import data
		#
		# Usage: loadData()

		filename = input("Write the name of the file you want to open: ")
		student_grader.data = self.student_grader.dataLoad(filename)

	def generatePlots(self):
		# GENERATEPLOTS Generates the plots from the studentGrader class
		#
		# Usage: generatePlots()
		if student_grader.data.size == 0:
			print("Data Error: There is no data imported to the analyzer.")
		else:
			self.askForDeleteFirst()
			student_grader.gradesPlot(student_grader.data)

	def loop(self):
		# LOOP Runs the menu over and over again until the input is QUIT and the user exists
		#
		# Usage: loop()
		self.printHeader()
		while True:
			self.choiceSelector(self.displayMenu(self.options))


# ==============================================================================
student_grader = StudentGrader()
menu = Menu(student_grader)
menu.loop()
# ==============================================================================
