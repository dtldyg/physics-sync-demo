# coding=utf-8

import common.base.const as const
import common.net as net
import ecs.system as system
import ecs.component as component


class SystemPackageDispatch(system.System):
	def __init__(self):
		super(SystemPackageDispatch, self).__init__((component.LABEL_PACKAGE,))

	def update(self, dt, component_tuples):
		component_package_dict = {}
		for eid, component_tuple in component_tuples:
			component_package, = component_tuple
			component_package.packages.clear()
			component_package_dict[eid] = component_package
		for pkg in net.iter_recv_pkg():
			if pkg['pid'] == net.PID_JOIN or \
					pkg['pid'] == net.PID_DEL or \
					pkg['pid'] == net.PID_ADD_MASTER or \
					pkg['pid'] == net.PID_ADD_REPLICA or \
					pkg['pid'] == net.PID_DEL_REPLICA:
				component_package_dict[const.ENTITY_GAME_ID].packages.append(pkg)
			elif pkg['pid'] == net.PID_CMD:
				component_package_dict[pkg['eid']].packages.append(pkg)
			elif pkg['pid'] == net.PID_STATES:
				self.world.game_component(component.LABEL_RECORD).server_frame = pkg['fr']
				for pkg_state in pkg['states']:
					component_package_dict[pkg_state['eid']].packages.append(pkg_state)
