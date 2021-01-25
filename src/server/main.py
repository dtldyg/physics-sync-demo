# coding=utf-8

import server.io as io
import server.game as game


def main():
	io.run_socket()
	game.run_game()


if __name__ == "__main__":
	main()
