def getMask(hsv, np, cv2):
	# yellow mask
	yellow_lower = np.array([20, 100, 100])
	yellow_upper = np.array([30, 255, 255])
	mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

	return mask