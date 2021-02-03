# coding=utf-8

import time
import pygame
import queue

import common.const as const
import common.scene as scene
import common.switch as switch

import client.event as event
import client.entity as entity
import client.io as io
import client.ui.gui as gui
import client.ui.window as window


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


def run_game():
	# pygame init
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')
	# global screen
	window_all = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.PANEL_WIDTH, const.SCREEN_SIZE[1]))
	screen = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
	panel = pygame.Surface((const.SCREEN_SIZE[0] + const.PANEL_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
	panel_bg = pygame.Surface((const.PANEL_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
	panel_bg.fill(const.PANEL_BACKGROUND)
	window.screen = screen
	window.panel = panel
	# gui
	panel_gui = gui.GUI()

	# all entities
	scene.add_entity(entity.MasterEntity())
	scene.add_entity(entity.MasterShadowEntity())

	# control info
	fps = 0
	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)
	render_lt = time.time()
	io_lt = time.time()

	while True:
		# clean scene
		screen.fill(const.SCREEN_BACKGROUND)
		# clean panel
		panel.blit(panel_bg, (const.SCREEN_SIZE[0], 0))

		# refresh event
		if not event.refresh(panel_gui):
			return
		# calc dt
		now = time.time()
		render_lt, dt = now, now - render_lt

		# io in
		while True:
			try:
				pkg = io.recv_q.get_nowait()
			except queue.Empty:
				break
			scene.iter_entities(lambda e: e.io_in(pkg))

		# update logic
		scene.iter_entities(lambda e: e.update_logic(dt))
		# update physics
		scene.iter_entities(lambda e: e.update_physics(dt))
		# update render
		scene.iter_entities(lambda e: e.update_render(dt))

		# io out
		if now - io_lt >= 1 / switch.NETWORK_CMD_FPS:
			io_lt = now
			scene.iter_entities(lambda e: e.io_out())

		# update gui
		panel_gui.update(dt)

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, const.FPS_COLOR)
		screen.blit(fps_text, (0, 0))
		# fps limit
		fps = get_fps(clock.tick(const.LOGIC_FPS))

		# re-draw the window
		window_all.blit(screen, (0, 0))
		window_all.blit(panel, (0, 0))
		pygame.display.flip()
