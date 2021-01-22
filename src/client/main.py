# coding=utf-8

import time
import pygame

import client.game as game
import client.event as event
import common.const as const
import client.entity as entity


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


def main():
	# pygame init
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')
	# global screen
	game.screen = pygame.display.set_mode(const.SCREEN_SIZE)
	screen = game.screen

	# all entities
	master_entity = entity.MasterEntity()

	# control info
	fps = 0
	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)
	lt = time.time()

	while True:
		# clean scene
		screen.fill(const.SCREEN_BACKGROUND)
		# refresh input event
		event.refresh()
		# calc dt
		now = time.time()
		lt, dt = now, now - lt

		# update all entity
		master_entity.update(dt)

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, const.FPS_COLOR)
		screen.blit(fps_text, (0, 0))
		# fps limit
		fps = get_fps(clock.tick(const.FPS))
		# re-draw the scene
		pygame.display.flip()


if __name__ == "__main__":
	main()
