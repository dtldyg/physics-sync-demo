# coding=utf-8

import common.base.const as const
import common.ec as ec
import common.physics as physics


class CompRecord(ec.ClientComponent):
	def __init__(self):
		super(CompRecord, self).__init__('comp_record')
		self.records = []  # {'fr': 0, 'p': (0,0), 'v': (0,0), 'f': (0,0), 'dt': 0}

	def recv_state(self, state):
		if const.MASTER_PREDICT:
			s_frame = state['fr']
			if len(self.records) == 0 or s_frame < self.records[0]['fr']:
				return
			record = self.records[0]
			while s_frame > record['fr']:
				self.records.pop(0)
				record = self.records[0]
			if not self.check_state(record):
				self.replay()

	def check_state(self, record):
		comp_state = self.entity.get_comp('comp_state')
		return record['p'] == comp_state.s_p and record['v'] == comp_state.s_v

	# TODO 临时做法，重构为ecs
	def replay(self):
		comp_state = self.entity.get_comp('comp_state')
		comp_record = self.entity.get_comp('comp_record')
		p, v = comp_state.s_p, comp_state.s_v
		record = comp_record.records[0]
		record['p'], record['v'] = p, v
		for record in comp_record.records[1:]:
			p, v = physics.pv_with_force_normal(p, v, record['f'], record['dt'])
			p, v = physics.pv_with_wall(p, v)
			record['p'], record['v'] = p, v
		comp_state.c_p, comp_state.c_v = p, v

	# last do in each tick
	def update_physics(self, dt):
		if const.MASTER_PREDICT:
			comp_state = self.entity.get_comp('comp_state')
			comp_control = self.entity.get_comp('comp_control')
			record = {'fr': self.entity.frame, 'p': comp_state.c_p, 'v': comp_state.c_v, 'f': comp_control.f_nor, 'dt': dt}
			self.records.append(record)
		else:
			self.records.clear()
