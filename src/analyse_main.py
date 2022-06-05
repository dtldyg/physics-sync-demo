# coding=utf-8

import inspect
import base.const as const
import base.ecs as component
import logic.world as world


def main():
	component_list = {}
	for name, obj in inspect.getmembers(component):
		if isinstance(obj, int):
			component_list[obj] = name.replace('LABEL_', '').title()
	const.IS_CLIENT = True
	w = world.World()
	print('------client------')
	for sys in w.system_logic:
		print(sys.__class__.__name__)
		for label in sys.component_labels:
			print('\t{}'.format(component_list[label]))
	const.IS_CLIENT = False
	const.IS_SERVER = True
	w = world.World()
	print('------server------')
	for sys in w.system_logic:
		print(sys.__class__.__name__)
		for label in sys.component_labels:
			print('\t{}'.format(component_list[label]))


if __name__ == "__main__":
	main()
