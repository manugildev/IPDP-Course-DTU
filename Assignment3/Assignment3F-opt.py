import numpy as np

goal_length = 7.32
field_size = np.array([105, 68])
y1_goal = 68 / 2 - (goal_length / 2)
y2_goal = 68 / 2 + (goal_length / 2)


def computePassesGoalLine(point, directionVector):
	xgoal = 105 if directionVector[0] >= 0 else 0
	alpha = (xgoal - point[0]) / directionVector[0]
	ygoal = point[1] + (alpha * directionVector[1])

	return ygoal > y1_goal and ygoal < y2_goal

print(computePassesGoalLine(np.array([30, 20]), np.array([10, 2])))
print(computePassesGoalLine(np.array([75, 20]), np.array([-10, 2])))