# coding=utf-8

import time
import pygame

import common.base.const as const
import common.base.clock as clock
import common.scene as scene
import common.net as net

import client.event as event
import client.entity as entity
import client.gui as gui


def run_game():
	game = Game()
	game.run()


class Game(object):
	def __init__(self):
		# pygame init
		pygame.init()
		pygame.display.set_caption('Physics Sync - Demo')
		# surface init
		self.sur_window = pygame.display.set_mode((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]))
		self.sur_game = pygame.Surface(const.SCREEN_SIZE, pygame.SRCALPHA)
		self.sur_gui = pygame.Surface((const.SCREEN_SIZE[0] + const.GUI_WIDTH, const.SCREEN_SIZE[1]), pygame.SRCALPHA)
		# gui init
		self.gui = gui.GUI(self.sur_gui)
		# fps init
		self.fps_frame = 0
		self.fps_lt = time.time()
		self.fps_font = pygame.font.SysFont('arial', 16)
		self.fps_txt = self.fps_font.render('fps:0', True, const.FPS_COLOR)
		# master entity init
		self.master_entity = entity.MasterEntity()
		scene.add_entity(self.master_entity)
		net.global_send_q.put({'pid': net.PID_JOIN})

	def run(self):
		c = clock.Clock()
		c.add(const.LOGIC_FPS, self.tick_logic)
		c.add(const.RENDER_FPS, self.tick_render)
		c.run()

	def tick_logic(self, dt):
		# refresh event
		event.refresh(self.gui)

		# recv states
		for pkg in net.iter_recv_pkg():
			if pkg['pid'] == net.PID_ADD_MASTER:
				self.master_entity.eid = pkg['state']['eid']
				self.master_entity.recv_state(pkg['state'])
				self.master_entity.enable = True
			elif pkg['pid'] == net.PID_ADD_REPLICA:
				en = entity.ReplicaEntity()
				en.eid = pkg['state']['eid']
				en.recv_state(pkg['state'])
				scene.add_entity(en)
			elif pkg['pid'] == net.PID_DEL_REPLICA:
				en = scene.get_entity(pkg['eid'])
				scene.del_entity(en.eid)
			elif pkg['pid'] == net.PID_STATES:
				for state in pkg['states']:
					en = scene.get_entity(state['eid'])
					if en is not None:
						en.recv_state(state)

		# update logic & physics
		scene.iter_entities(lambda e: e.update(dt))

		# send cmd
		if self.master_entity.enable:
			cmd = self.master_entity.send_cmd()
			cmd['pid'] = net.PID_CMD
			cmd['fr'] = self.master_entity.frame
			net.global_send_q.put(cmd)

		if self.master_entity.enable:
			comp_state = self.master_entity.get_comp('comp_state')
			comp_control = self.master_entity.get_comp('comp_control')
			record = {'fr': self.master_entity.frame, 'p': comp_state.c_p, 'v': comp_state.c_v, 'f': comp_control.f_nor, 'dt': dt}
			print(record)

	def tick_render(self, dt):
		# clean game surface
		self.sur_game.fill(const.SCREEN_BACKGROUND)

		# update render & gui
		scene.iter_entities(lambda e: e.update_render(self.sur_game, dt))
		self.gui.update(dt)
		# update fps
		now = time.time()
		self.fps_frame = self.fps_frame + 1
		if now - self.fps_lt >= 1:
			self.fps_txt = self.fps_font.render('fps:{:.1f}'.format(self.fps_frame / (now - self.fps_lt)), True, const.FPS_COLOR)
			self.fps_lt = now
			self.fps_frame = 0
		self.sur_game.blit(self.fps_txt, (0, 0))

		# draw window surface
		self.sur_window.blit(self.sur_game, (0, 0))
		self.sur_window.blit(self.sur_gui, (0, 0))
		pygame.display.flip()
