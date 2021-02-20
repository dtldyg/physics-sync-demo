# coding=utf-8

import time


class QuitError(Exception):
	pass


class Clock(object):
	def __init__(self):
		self.blocks = []

	def add(self, fps, func):
		dt = 1 / fps
		self.blocks.append([dt, func, 0])

	def run(self):
		b = 0
		while True:
			n = time.time()
			t = n - b
			try:
				if t >= 1:
					for block in self.blocks:
						block[1](block[0])
						block[2] = 1
					b = n
				else:
					for block in self.blocks:
						if t / block[0] >= block[2]:
							block[1](block[0])
							block[2] = block[2] + 1
			except QuitError:
				return
			time.sleep(0.001)
