# coding=utf-8

import queue
import threading
import server.io as io
import server.game as game


def main():
	recv_q = queue.Queue(1024)
	# run io socket
	threading.Thread(target=io.run_socket, args=(recv_q,)).start()
	# run game
	threading.Thread(target=game.run_game, args=(recv_q,)).start()
	print('server started')


if __name__ == "__main__":
	main()
