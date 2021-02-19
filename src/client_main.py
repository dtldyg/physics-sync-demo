# coding=utf-8

import common.base.const as const
import common.net as net
import ecs.world as world


def main():
	const.IS_CLIENT = True
	net.run_client_socket()
	w = world.World()
	w.run()


if __name__ == "__main__":
	main()
