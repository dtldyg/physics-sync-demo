# coding=utf-8

import base.const as const
import base.net as net
import base.ecs as ecs


class SystemPackageDispatch(ecs.System):
	def __init__(self):
		super(SystemPackageDispatch, self).__init__((ecs.LABEL_PACKAGE,))

	def update(self, dt, component_tuples):
		# collect
		comp_package_dict = {}
		for eid, comp_tuple in component_tuples:
			comp_package, = comp_tuple
			comp_package.packages.clear()
			comp_package_dict[eid] = comp_package
		# dispatch
		for pkg in net.iter_recv_pkg():
			if pkg['pid'] == net.PID_JOIN or \
					pkg['pid'] == net.PID_DEL or \
					pkg['pid'] == net.PID_ADD_MASTER or \
					pkg['pid'] == net.PID_ADD_REPLICA or \
					pkg['pid'] == net.PID_DEL_REPLICA or \
					pkg['pid'] == net.PID_BUFFER or \
					pkg['pid'] == net.PID_SYNC_CONF or \
					pkg['pid'] == net.PID_BROAD_CONF or \
					pkg['pid'] == net.PID_SYNC_BUFFER:
				comp_package_dict[const.ENTITY_GAME_ID].packages.append(pkg)
			elif pkg['pid'] == net.PID_CMD:
				comp_package_dict[pkg['eid']].packages.append(pkg)
			elif pkg['pid'] == net.PID_STATES:
				master_comp_frame = self.world.master_component(ecs.LABEL_FRAME)
				master_comp_frame.server_frame = pkg['fr']
				for pkg_state in pkg['states']:
					if pkg_state['eid'] not in comp_package_dict:
						continue
					comp_package_dict[pkg_state['eid']].packages.append(pkg_state)
