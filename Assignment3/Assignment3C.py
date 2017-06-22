import math
import numpy as np


def acuteAngle(v1, v2):
	t = math.acos(np.dot(v1, v2))
	angle = t if t < math.pi / 2 else math.pi - t
	return angle
