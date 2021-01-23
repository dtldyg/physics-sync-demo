# coding=utf-8

import time
import pygame
import queue

import client.window as window
import client.event as event
import client.entity as entity
import client.io as io
import common.const as const


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


def run_game():
	# pygame init
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')
	# global screen
	window.screen = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.PANEL_WIDTH, const.SCREEN_SIZE[1]))
	screen = window.screen

	# all entities
	master_entity = entity.MasterEntity()
	master_shadow_entity = entity.MasterShadowEntity()

	# control info
	fps = 0
	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)
	render_lt = time.time()
	io_lt = time.time()

	while True:
		# clean scene
		screen.fill(const.SCREEN_BACKGROUND)
		pygame.draw.line(screen, const.PANEL_COLOR, (const.SCREEN_SIZE[0], 0), const.SCREEN_SIZE, 1)
		# refresh input event
		if not event.refresh():
			return
		# calc dt
		now = time.time()
		render_lt, dt = now, now - render_lt

		# input io
		while True:
			try:
				pkg = io.recv_q.get_nowait()
			except queue.Empty:
				break
			master_entity.sync_in(pkg)
			master_shadow_entity.sync_in(pkg)

		# update all entities
		master_entity.update(dt)
		master_shadow_entity.update(dt)

		# output io
		if now - io_lt >= 1 / const.IO_FPS:
			io_lt = now
			master_entity.sync_out()
			master_shadow_entity.sync_out()

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, const.FPS_COLOR)
		screen.blit(fps_text, (0, 0))
		# fps limit
		fps = get_fps(clock.tick(const.CLIENT_FPS))
		# re-draw the scene
		pygame.display.flip()
