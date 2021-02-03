# coding=utf-8

import client.net as net
import client.game as game


def main():
	net.run_socket()
	game.run_game()


if __name__ == "__main__":
	main()
