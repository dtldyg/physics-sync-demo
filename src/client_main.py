# coding=utf-8

import base.const as const
import base.net as net
import logic.world as world


def main():
	const.IS_CLIENT = True
	# net.run_client_socket()
	w = world.World()
	w.run()


if __name__ == "__main__":
	main()
