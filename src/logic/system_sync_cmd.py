# coding=utf-8

import base.net as net
import base.ecs as ecs


class SystemSyncCmd(ecs.System):
	def __init__(self):
		super(SystemSyncCmd, self).__init__((ecs.LABEL_FRAME, ecs.LABEL_PHYSICS))

	def update(self, dt, component_tuples):
		for eid, comp_tuple in component_tuples:
			comp_frame, comp_physics = comp_tuple
			comp_frame.frame += 1
			sync_package = {'pid': net.PID_CMD, 'eid': eid, 'fr': comp_frame.frame, 'f': comp_physics.force_normal.dict()}
			net.send_client_pkg(sync_package)
