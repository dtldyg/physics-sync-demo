# coding=utf-8

import base.const as const
import base.net as net
import logic.world as world


def main():
	const.IS_SERVER = True
	sock = net.run_server_socket()

	w = world.World()
	w.run()

	sock.close()


if __name__ == "__main__":
	main()
