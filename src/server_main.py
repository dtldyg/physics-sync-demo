# coding=utf-8

import base.const as const
import base.net as net
import base.log as log
import logic.world as world


def main():
	const.IS_SERVER = True
	sock = net.run_server_socket()
	log.info('net run')

	w = world.World()
	w.run()

	sock.close()
	log.info('net close')


if __name__ == "__main__":
	main()
