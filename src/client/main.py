# coding=utf-8

import client.io as io
import client.game as game


def main():
	io.run_socket()
	game.run_game()


if __name__ == "__main__":
	main()
