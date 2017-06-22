nato_dictionary = {'A': 'Alpha', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo', 'F': 'Foxtrot', 'G': 'Golf',
                   'H': "Hotel", 'I': 'India', 'J': 'Juliet', 'K': 'Kilo', 'L': 'Lima', 'M': 'Mike', 'N': 'November',
                   'O': 'Oscar', 'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo', 'S': 'Sierra', 'T': 'Tango', 'U': 'Uniform',
                   'V': 'Victor', 'W': 'Whiskey', 'X': 'Xray', 'Y': 'Yankee', 'Z': 'Zulu'}


def textToNato(plainText):
	nato_words = [nato_dictionary[l] for l in plainText.upper()]
	return "-".join(nato_words)


def natoToText(natoText):
	letters = [l[0:1] for l in natoText.split("-")]
	return ''.join(letters).lower()


print(textToNato("hello"))