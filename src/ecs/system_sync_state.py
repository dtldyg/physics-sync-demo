# coding=utf-8

import common.net as net
import ecs.system as system
import ecs.component as component


class SystemSyncState(system.System):
	def __init__(self):
		super(SystemSyncState, self).__init__((component.LABEL_CONNECTION, component.LABEL_CONTROL, component.LABEL_TRANSFORM))

	def update(self, dt, component_tuples):
		states = []
		for eid, component_tuple in component_tuples:
			_, component_control, component_transform = component_tuple
			states.append({'eid': eid, 'fr': component_control.frame, 'p': component_transform.position.dict(), 'v': component_transform.velocity.dict()})
		sync_package = {'pid': net.PID_STATES, 'states': states}
		for _, component_tuple in component_tuples:
			component_connection, _, _ = component_tuple
			component_connection.send_q.put(sync_package)
