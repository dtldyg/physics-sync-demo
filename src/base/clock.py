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

	def set_fps(self, idx, fps):
		dt = 1 / fps
		self.blocks[idx][0] = dt

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
						f = t // block[0]
						if f != block[2]:
							block[1](block[0])
							block[2] = f
				time.sleep(0.001)
			except QuitError:
				return
			except KeyboardInterrupt:
				return
