# coding=utf-8

import time
import pygame
import base.const as const
import base.net as net
import base.ecs as ecs


class SystemRender(ecs.System):
	def __init__(self):
		super(SystemRender, self).__init__((ecs.LABEL_TRANSFORM, ecs.LABEL_RENDER))

	def update(self, dt, component_tuples):
		comp_surface = self.world.game_component(ecs.LABEL_SURFACE)
		comp_info = self.world.game_component(ecs.LABEL_INFO)
		comp_gui = self.world.game_component(ecs.LABEL_GUI)

		# game
		comp_surface.game.fill(const.SCREEN_BACKGROUND)
		# game - entity
		for _, comp_tuple in component_tuples:
			comp_transform, comp_render, = comp_tuple
			if const.MASTER_PREDICT:
				interpolation = comp_render.client_interpolation
			else:
				interpolation = comp_render.server_interpolation
			client_surface = comp_render.client_surface
			comp_surface.game.blit(client_surface[0], (position_interpolation(*interpolation) - client_surface[1]).tuple())
			if const.MASTER_SERVER:
				server_surface = comp_render.server_surface
				comp_surface.game.blit(server_surface[0], (comp_transform.server_position - server_surface[1]).tuple())
			for other_render in comp_render.other_renders:
				other_render[0](comp_surface.game, *other_render[1])
		# game - info
		now = time.time()
		comp_info.fps_frame += 1
		if now - comp_info.fps_lt >= 1:
			fps = comp_info.fps_frame / (now - comp_info.fps_lt)
			comp_info.fps_txt = comp_info.font.render('fps:{:.1f}'.format(fps), True, const.FPS_COLOR)
			comp_info.fps_lt = now
			comp_info.fps_frame = 0
		comp_surface.game.blit(comp_info.fps_txt, (0, 0))
		rtt_info = 'rtt:{:.0f}ms,c-s:{:+.0f}ms'.format(net.client_rtt[0] * 1000, net.client_rtt[1] * 1000)
		rtt_txt = comp_info.font.render(rtt_info, True, const.FPS_COLOR)
		comp_surface.game.blit(rtt_txt, (0, 18))

		# gui
		comp_surface.gui.blit(comp_gui.ui_bg, (const.SCREEN_SIZE[0], 0))
		comp_gui.ui_manager.update(dt)
		comp_gui.ui_manager.draw_ui(comp_surface.gui)

		# blit
		comp_surface.window.blit(comp_surface.game, (0, 0))
		comp_surface.window.blit(comp_surface.gui, (0, 0))
		pygame.display.flip()


def position_interpolation(a_p, a_t, b_p, b_t):
	if a_p is None:
		return b_p
	t = time.time() - b_t
	if t >= b_t - a_t:
		return b_p
	return (b_p - a_p) * t / (b_t - a_t) + a_p
