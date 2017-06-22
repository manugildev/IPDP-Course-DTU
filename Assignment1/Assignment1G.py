import math


# Function to solve the consine rule for any input given
def consineRule(b, c, A):
	return math.sqrt((b * b) + (c * c) - (2 * b * c * math.cos(A)))


b = 12
c = 10
A = 0.25 * math.pi
a = consineRule(b, c, A)
print(a)
