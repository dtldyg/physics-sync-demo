# coding=utf-8

import common.base.const as const
import common.ec as ec


class CompRecord(ec.ClientComponent):
	def __init__(self):
		super(CompRecord, self).__init__('comp_record')
		self.records = []

	def recv_state(self, state):
		if const.MASTER_PREDICT:
			server_frame = state['fr']
			if server_frame < 0 or len(self.records) == 0 or server_frame < self.records[0][0]:
				return
			print(server_frame, self.records[0][0], '-', self.records[-1][0])
			comp_state = self.entity.get_comp('comp_state')
			if server_frame > self.records[-1][0]:
				print('set', server_frame, self.records[0][0], '-', self.records[-1][0])
				self.records.clear()
				self.entity.frame = server_frame
				comp_state.c_p, comp_state.c_v = comp_state.s_p, comp_state.s_v
				return
			else:
				idx = server_frame - self.records[0][0]
				record = self.records[idx]
				self.records = self.records[idx + 1:]
				record_state = record[1]
				if record_state[0] != comp_state.s_p or record_state[1] != comp_state.s_v:
					print('replay', record[0])
					self.entity.get_comp('comp_physics').replay()

	# last do in each tick
	def update_physics(self, dt):
		if const.MASTER_PREDICT:
			comp_state = self.entity.get_comp('comp_state')
			comp_control = self.entity.get_comp('comp_control')
			record = (self.entity.frame, (comp_state.c_p, comp_state.c_v), (comp_control.f_nor, dt))
			self.records.append(record)
		else:
			self.records.clear()
