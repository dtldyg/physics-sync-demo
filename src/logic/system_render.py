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
		game_comp_surface = self.world.game_component(ecs.LABEL_SURFACE)
		game_comp_info = self.world.game_component(ecs.LABEL_INFO)
		game_comp_gui = self.world.game_component(ecs.LABEL_GUI)

		# game
		game_comp_surface.game.fill(const.SCREEN_BACKGROUND)
		# game - entity
		for eid, comp_tuple in component_tuples:
			comp_transform, comp_render, = comp_tuple
			# draw client
			if eid == self.world.master_eid():
				if const.MASTER_BEHAVIOR != const.MASTER_NONE:
					client_position = position_interpolation(*comp_render.interpolation)
				else:
					client_position = comp_transform.server_position
			else:
				if const.REPLICA_INTERPOLATION:
					client_position = position_interpolation(*comp_render.interpolation)
				else:
					client_position = comp_transform.server_position
			client_surface = comp_render.client_surface
			game_comp_surface.game.blit(client_surface[0], (client_position - client_surface[1]).tuple())
			# draw server
			if const.SHOW_SERVER:
				server_surface = comp_render.server_surface
				game_comp_surface.game.blit(server_surface[0], (comp_transform.server_position - server_surface[1]).tuple())
			# draw other
			for other_render in comp_render.other_renders:
				other_render[0](game_comp_surface.game, *other_render[1])
		# game - info
		now = time.time()
		game_comp_info.fps_frame += 1
		if now - game_comp_info.fps_lt >= 1:
			fps = game_comp_info.fps_frame / (now - game_comp_info.fps_lt)
			game_comp_info.fps_txt = game_comp_info.font.render('fps:{:.1f}'.format(fps), True, const.FPS_COLOR)
			game_comp_info.fps_lt = now
			game_comp_info.fps_frame = 0
		game_comp_surface.game.blit(game_comp_info.fps_txt, (0, 0))
		rtt_info = 'rtt:{:.0f}ms,c-s:{:+.0f}ms'.format(net.client_rtt[0] * 1000, net.client_rtt[1] * 1000)
		rtt_txt = game_comp_info.font.render(rtt_info, True, const.FPS_COLOR)
		game_comp_surface.game.blit(rtt_txt, (0, 18))

		# gui
		game_comp_surface.gui.blit(game_comp_gui.ui_bg, (const.SCREEN_SIZE[0], 0))
		game_comp_gui.ui_manager.update(dt)
		game_comp_gui.ui_manager.draw_ui(game_comp_surface.gui)

		# blit
		game_comp_surface.window.blit(game_comp_surface.game, (0, 0))
		game_comp_surface.window.blit(game_comp_surface.gui, (0, 0))
		pygame.display.flip()


def position_interpolation(a_p, a_t, b_p, b_t):
	if a_p is None:
		return b_p
	t = time.time() - b_t
	if t >= b_t - a_t:
		return b_p
	return (b_p - a_p) * t / (b_t - a_t) + a_p
