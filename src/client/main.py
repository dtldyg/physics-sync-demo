# coding=utf-8

import client.game as game
import client.io as io


def main():
	io.run_socket()
	game.run_game()


if __name__ == "__main__":
	main()
