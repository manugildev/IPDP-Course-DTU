import math

# Constant Variables
EARTH_RADIUS = 6.371e6
G0 = 9.82


# Function that returns the gravitational pull at a given distance
def gravitationalPull(x):
	if EARTH_RADIUS <= x:
		return G0 * math.pow(EARTH_RADIUS, 2) / math.pow(x, 2)
	else:
		return G0 * x / EARTH_RADIUS
