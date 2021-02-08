# coding=utf-8

import common.base.const as const
import common.ec as ec


class CompRecord(ec.ClientComponent):
	def __init__(self):
		super(CompRecord, self).__init__('comp_record')
		self.records = []  # frame, (p,v), (f,t)

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
				self.entity.get_comp('comp_physics').replay()
				print('replay', record)

	def check_state(self, record):
		comp_state = self.entity.get_comp('comp_state')
		return record['p'] == comp_state.s_p and record['v'] == comp_state.s_v

	# last do in each tick
	def update_physics(self, dt):
		if const.MASTER_PREDICT:
			comp_state = self.entity.get_comp('comp_state')
			comp_control = self.entity.get_comp('comp_control')
			record = {'fr': self.entity.frame, 'p': comp_state.c_p, 'v': comp_state.c_v, 'f': comp_control.f_nor, 'dt': dt}
			self.records.append(record)
		else:
			self.records.clear()
