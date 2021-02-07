# coding=utf-8

import sys
import common.base.const as const
import common.net as net
import client.game as game


def main():
	const.IS_CLIENT = True
	net.run_client_socket()
	game.run_game()


if __name__ == "__main__":
	main()
