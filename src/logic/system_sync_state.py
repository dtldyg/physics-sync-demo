# coding=utf-8

import base.net as net
import base.ecs as ecs


class SystemSyncState(ecs.System):
	def __init__(self):
		super(SystemSyncState, self).__init__((ecs.LABEL_CONNECTION, ecs.LABEL_PHYSICS, ecs.LABEL_TRANSFORM, ecs.LABEL_FRAME))

	def update(self, dt, component_tuples):
		states = []
		for eid, comp_tuple in component_tuples:
			_, comp_physics, comp_transform, comp_frame = comp_tuple
			states.append({'eid': eid, 'p': comp_transform.position.dict(), 'v': comp_transform.velocity.dict()})
		for _, comp_tuple in component_tuples:
			comp_connection, _, _, comp_frame = comp_tuple
			if comp_frame.frame == 0:
				continue
			sync_package = {'pid': net.PID_STATES, 'fr': comp_frame.frame, 'states': states}
			comp_connection.send_q.put(sync_package)
