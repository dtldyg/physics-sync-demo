# coding=utf-8

import socket
import queue
import threading


def run_conn(conn, q):
	while True:
		conn.


def run_socket(q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	sock.listen()

	while True:
		conn, addr = sock.accept()
		conn.recvfrom()
		threading.Thread(target=run_conn, args=(conn, q)).start()


def run_game(q):
	pass


def main():
	q = queue.Queue(1024)
	# run io socket
	threading.Thread(target=run_socket, args=(q,)).start()
	# run game
	threading.Thread(target=run_game, args=(q,)).start()


if __name__ == "__main__":
	main()
