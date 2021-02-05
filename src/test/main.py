# coding=utf-8

import common.base.clock as clock

f1, f2, f3 = 0, 0, 0


def foo1(_):
	global f1
	f1 = f1 + 1


def foo2(_):
	global f2
	f2 = f2 + 1


def foo3(_):
	global f3
	f3 = f3 + 1


def foo(_):
	global f1, f2, f3
	print(f1, f2, f3)
	f1, f2, f3 = 0, 0, 0


c = clock.Clock()
c.add(11, foo1)
c.add(33, foo2)
c.add(79, foo3)
c.add(1, foo)
c.run()
