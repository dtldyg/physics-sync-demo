# coding=utf-8

import server.net as net
import server.game as game


def main():
	net.run_socket()
	game.run_game()


if __name__ == "__main__":
	main()
