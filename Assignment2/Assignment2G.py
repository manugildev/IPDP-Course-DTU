
def boxArea(boxCorners, area):
	x1, x2, x3, x4, y1, y2, y3, y4 = boxCorners
	box1_area = (x2 - x1) * (y2 - y1)
	box2_area = (x4 - x3) * (y4 - y3)
	t1 = max(0, min(x2, x4) - max(x1, x3))
	t2 = max(0, min(y2, y4) - max(y1, y3))
	boxes_intersection = t1 * t2

	if area == "Box1":
		return box1_area
	elif area == "Box2":
		return box2_area
	elif area == "Intersection":
		return boxes_intersection
	elif area == "Union":
		return box1_area + box2_area - boxes_intersection
