# coding=utf-8

import common.net as net
import ecs.system as system
import ecs.component as component


class SystemSyncCmd(system.System):
	def __init__(self):
		super(SystemSyncCmd, self).__init__((component.LABEL_CONTROL, component.LABEL_PHYSICS))

	def update(self, dt, component_tuples):
		component_frame = self.world.game_component(component.LABEL_FRAME)
		component_frame.frame += 1
		for eid, component_tuple in component_tuples:
			_, component_physics = component_tuple
			sync_package = {'pid': net.PID_CMD, 'eid': eid, 'fr': component_frame.frame, 'f': component_physics.force_normal.dict()}
			net.send_client_pkg(sync_package)
