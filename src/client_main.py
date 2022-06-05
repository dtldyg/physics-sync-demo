# coding=utf-8

import base.const as const
import base.net as net
import logic.world as world


def main():
	const.IS_CLIENT = True
	conn = net.run_client_socket()
	const.ONLY_CLIENT = conn is None

	w = world.World()
	w.run()

	conn.close()


if __name__ == "__main__":
	main()
