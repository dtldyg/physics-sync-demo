# coding=utf-8

import common.base.const as const
import common.net as net
import server.game as game


def main():
	const.IS_SERVER = True
	net.run_server_socket()
	game.run_game()


if __name__ == "__main__":
	main()
