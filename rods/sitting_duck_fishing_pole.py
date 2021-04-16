def getMask(hsv, np, cv2):
	# lower mask (0-10)
	lower_red = np.array([0,50,50])
	upper_red = np.array([10,255,255])
	mask0 = cv2.inRange(hsv, lower_red, upper_red)

	# upper mask (170-180)
	lower_red = np.array([170,50,50])
	upper_red = np.array([180,255,255])
	mask1 = cv2.inRange(hsv, lower_red, upper_red)

	# join masks
	mask = mask0+mask1

	return mask