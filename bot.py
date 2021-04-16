import time
import cv2
import mss
import numpy as np
import pyautogui
import pytesseract

from fuzzywuzzy import fuzz

from utils import queryMousePosition
import rods

class FishingBot():

	title = "Terraria Auto-Fishing Bot"
	sct = None
	config = None
	rod = "Golden Fishing Rod"

	ocr = {
		"enabled": True,
		"exclude": False,
		"list": []
	}

	active = False
	last_catch_time = 0 # catch interval (before new rod will be dropped)
	last_sonar_time = 0 # read sonar time (before it fades)

	def __init__(self, config):
		self.config = config
		self.sct = mss.mss()

	def click(self):
		pyautogui.mouseDown()
		time.sleep(0.01)
		pyautogui.mouseUp()

	def start(self):
		print("Starting bot after",self.config.bot.start_after,"seconds.")
		print("Selected rod:",self.rod)
		print("Please, adjust your rod!")

		if not self.ocr["enabled"]:
			time.sleep(self.config.bot.start_after)

			self.click()
			print("Rod dropped ...")
			self.last_catch_time = time.time()
		else:
			time.sleep(self.config.bot.start_after / 2)

		self.active = True
		self.wait()

	def stop(self):
		self.active = False

	def wait(self):
		if self.ocr["enabled"]:
			# OCR way
			while self.active:
				# minimum catch interval
				if time.time() - self.last_catch_time < self.config.bot.last_catch_interval:
					continue

				# create box shot of sonar label
				cur = queryMousePosition()
				mon = {
					"left": cur['x'] - 200,
					"top": cur['y'] - 75,
					"width": 400,
					"height": 50
				}
				img = np.asarray(self.sct.grab(mon))

				# create RGB for tesseract
				rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

				# read psm 6 & 7
				pcm6 = pytesseract.image_to_string(rgb, lang='rus', config='--psm 6')
				pcm7 = pytesseract.image_to_string(rgb, lang='rus', config='--psm 7')

				# ТЕСТ
				# проверяем что это Эбонкои или нет
				# ЛОВИМ ТОЛЬКО КОИ!
				
				# self.show(self.title, img)

				if(((fuzz.ratio(pcm6.lower(), 'ящик')) > 50 or (fuzz.ratio(pcm7.lower(), 'ящик')) > 50)
				or ('ящик' in pcm6.lower() or 'ящик' in pcm7.lower() or 'яшик' in pcm6.lower() or 'яшик' in pcm7.lower())):
					print("Это Ящик!")
					self.catch(True) # catch ASAP
				else:
					print("Неть ...")
		else:
			# Catch all way
			while self.active:

				# minimum catch interval
				if time.time() - self.last_catch_time < self.config.bot.last_catch_interval:
					continue

				# create box shot around mouse
				cur = queryMousePosition()
				mon = {
					"left": cur['x'] - int((self.config.bot.box_height/2)),
					"top": cur['y'] - int((self.config.bot.box_width/2)),
					"width": self.config.bot.box_width,
					"height": self.config.bot.box_height
				}
				img = np.asarray(self.sct.grab(mon))

				# create HSV
				hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

				# get mask by rod
				mask = rods.golden_fishing_rod.getMask(hsv, np, cv2)

				# check
				hasFish = np.sum(mask)

				if hasFish > 0:
					# no fish
					pass
				else:
					self.catch()

	def catch(self, asap = False):
		print("Catch! ...")
		
		if not asap:
			time.sleep(0.3)

		self.click()

		time.sleep(1) # wait some
		print("New rod dropped ...")
		self.click()

		# reset last catch time
		self.last_catch_time = time.time()

	def show(self, title, img):
		cv2.imshow(title, img)
		if cv2.waitKey(25) & 0xFF == ord("q"):
			cv2.destroyAllWindows()
			quit()