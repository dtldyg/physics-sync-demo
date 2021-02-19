# coding=utf-8

import time
import pygame
import common.base.const as const
import common.net as net
import ecs.system as system
import ecs.component as component


class SystemRender(system.System):
	def __init__(self):
		super(SystemRender, self).__init__((component.LABEL_TRANSFORM, component.LABEL_RENDER))

	def update(self, dt, component_tuples):
		component_surface = self.world.game_component(component.LABEL_SURFACE)
		component_info = self.world.game_component(component.LABEL_INFO)
		component_gui = self.world.game_component(component.LABEL_GUI)

		# game
		component_surface.game.fill(const.SCREEN_BACKGROUND)
		# game - entity
		for _, component_tuple in component_tuples:
			component_transform, component_render, = component_tuple
			if const.MASTER_PREDICT:
				interpolation = component_render.client_interpolation
			else:
				interpolation = component_render.server_interpolation
			client_surface = component_render.client_surface
			component_surface.game.blit(client_surface[0], (position_interpolation(*interpolation) - client_surface[1]).tuple())
			if const.MASTER_SERVER:
				server_surface = component_render.server_surface
				component_surface.game.blit(server_surface[0], (component_transform.server_position - server_surface[1]).tuple())
			for other_render in component_render.other_renders:
				other_render[0](component_surface.game, *other_render[1])
		# game - info
		now = time.time()
		component_info.fps_frame += 1
		if now - component_info.fps_lt >= 1:
			fps = component_info.fps_frame / (now - component_info.fps_lt)
			component_info.fps_txt = component_info.info_font.render('fps:{:.1f}'.format(fps), True, const.FPS_COLOR)
			component_info.fps_lt = now
			component_info.fps_frame = 0
		component_surface.game.blit(component_info.fps_txt, (0, 0))
		rtt_info = 'rtt:{:.0f}ms,c-s:{:+.0f}ms'.format(net.client_rtt[0] * 1000, net.client_rtt[1] * 1000)
		rtt_txt = component_info.info_font.render(rtt_info, True, const.FPS_COLOR)
		component_surface.game.blit(rtt_txt, (0, 18))

		# gui
		component_surface.gui.blit(component_gui.ui_bg, (const.SCREEN_SIZE[0], 0))
		component_gui.ui_manager.update(dt)
		component_gui.ui_manager.draw_ui(component_surface.gui)

		# blit
		component_surface.window.blit(component_surface.game, (0, 0))
		component_surface.window.blit(component_surface.gui, (0, 0))
		pygame.display.flip()


def position_interpolation(a_p, a_t, b_p, b_t):
	if a_p is None:
		return b_p
	t = time.time() - b_t
	if t >= b_t - a_t:
		return b_p
	return (b_p - a_p) * t / (b_t - a_t) + a_p
