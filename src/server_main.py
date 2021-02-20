# coding=utf-8

import base.const as const
import base.net as net
import logic.world as world


def main():
	const.IS_SERVER = True
	net.run_server_socket()
	w = world.World()
	w.run()


if __name__ == "__main__":
	main()
