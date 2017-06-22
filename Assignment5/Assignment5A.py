# Even though this function should be self-explanatory by the name and the parameters...
def convertTemperature(T, unitFrom, unitTo):
	"""Returns the temperature converted
	Parameter1 - T - Temperature you want to convert
	Parameter2 - unitFrom - Original Temperature
	Parameter3 - unitTo - The final Temperature you want to obtain
	"""

	if unitFrom == "Celsius":
		if unitTo == "Fahrenheit":
			return 1.8 * T + 32
		elif unitTo == "Kelvin":
			return T + 273.15
	elif unitFrom == "Fahrenheit":
		if unitTo == "Celsius":
			return (T - 32) / 1.8
		elif unitTo == "Kelvin":
			return (T + 459.67) / 1.8
	elif unitFrom == "Kelvin":
		if unitTo == "Celsius":
			return T - 273.15
		elif unitTo == "Fahrenheit":
			return 1.8 * T - 459.67
	else:
		return "UnitFrom: Not valid."
