# coding=utf-8

import base.net as net
import base.ecs as ecs


class SystemPing(ecs.System):
	def __init__(self, world):
		super(SystemPing, self).__init__(world, ())

	def update(self, dt, component_tuples):
		net.do_ping()
