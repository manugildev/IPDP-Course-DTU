import math


# Function to solve the quadratic formula for any input given
def quadratic(a, b, c):
	return (-b - math.sqrt(b * b - (4 * a * c))) / (2 * a), (-b + math.sqrt(b * b - (4 * a * c))) / (2 * a)


a = 2
b = -5
c = 2
x1, x2 = quadratic(a, b, c)
print(x1, x2)
