# coding=utf-8

import time
import pygame

import _global
import _input
import _const

import entity


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


def main():
	# pygame init
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')
	# global screen
	_global.screen = pygame.display.set_mode(_const.SCREEN_SIZE)
	screen = _global.screen

	# all entities
	master_entity = entity.MasterEntity()

	# control info
	fps = 0
	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)
	lt = time.time()

	while True:
		# clean scene
		screen.fill(_const.SCREEN_BACKGROUND)
		# refresh input
		_input.refresh()
		# calc dt
		now = time.time()
		lt, dt = now, now - lt

		# update all entity
		master_entity.update(dt)

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, _const.FPS_COLOR)
		screen.blit(fps_text, (0, 0))
		# fps limit
		fps = get_fps(clock.tick(_const.FPS))
		# re-draw the scene
		pygame.display.flip()


if __name__ == "__main__":
	main()
