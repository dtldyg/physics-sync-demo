# coding=utf-8

import time
import pygame
import queue

import common.base.const as const
import common.scene as scene

import client.event as event
import client.ec as entity
import common.net as net
import client.display.gui as gui
import client.display.surface as surface


def get_fps(t):
	if t <= 0:
		return 1
	return int(1 / t * 1000)


def run_game():
	# pygame init
	pygame.init()
	pygame.display.set_caption('Physics Sync - Demo')
	# surface init
	surface.sur_window = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
	surface.sur_game = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
	surface.sur_gui = pygame.Surface((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
	# gui
	gui_pnl = gui.GUI()

	# all entities
	scene.add_entity(entity.MasterEntity())
	scene.add_entity(entity.MasterShadowEntity())

	# control info
	fps = 0
	clock = pygame.time.Clock()
	font = pygame.font.SysFont('arial', 16)
	render_lt = time.time()

	while True:
		# clean game surface
		surface.sur_game.fill(const.SCREEN_BACKGROUND)

		# refresh event
		if not event.refresh(gui_pnl):
			return
		# calc dt
		now = time.time()
		render_lt, dt = now, now - render_lt

		# io in
		while True:
			try:
				pkg = net.recv_q.get_nowait()
			except queue.Empty:
				break
			scene.iter_entities(lambda e: e.io_in(pkg))

		# update logic
		scene.iter_entities(lambda e: e.update_logic(dt))
		# update physics
		scene.iter_entities(lambda e: e.update_physics(dt))
		# update render
		scene.iter_entities(lambda e: e.update_render(dt))

		scene.iter_entities(lambda e: e.io_out())

		# update gui panel
		gui_pnl.update(dt)

		# calc fps
		fps_text = font.render('fps:{}'.format(fps), True, const.FPS_COLOR)
		surface.sur_game.blit(fps_text, (0, 0))
		# fps limit
		fps = get_fps(clock.tick(const.LOGIC_FPS))

		# draw window surface
		surface.sur_window.blit(surface.sur_game, (0, 0))
		surface.sur_window.blit(surface.sur_gui, (0, 0))
		pygame.display.flip()
