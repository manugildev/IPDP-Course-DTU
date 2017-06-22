def pH2Category(pH):
	if pH >= 0 and pH < 3:
		return "Strongly acidic"
	elif pH >= 3 and pH < 6:
		return "Weakly acidic"
	elif pH >= 6 and pH < 9:
		return "Neutral"
	elif pH >= 9 and pH < 11:
		return "Weakly basic"
	elif pH >= 11 and pH <= 14:
		return "Strongly basic"
	else:
		return "pH out of range"
