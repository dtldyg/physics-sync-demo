# coding=utf-8

import socket
import queue
import struct
import threading


# socket connection
def run_conn(q, conn, client_id):
	while True:
		# read one package
		len_b = conn.recv(2, socket.MSG_WAITALL)
		len = struct.unpack('i', len_b)[0]
		pkg_b = conn.recv(len, socket.MSG_WAITALL)


# socket listener
def run_socket(q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	sock.listen()

	client_id = 0
	while True:
		conn, addr = sock.accept()
		client_id = client_id + 1
		threading.Thread(target=run_conn, args=(q, conn, client_id)).start()


# game
def run_game(q):
	pass


def main():
	q = queue.Queue(1024)
	# run io socket
	threading.Thread(target=run_socket, args=(q,)).start()
	# run game
	threading.Thread(target=run_game, args=(q,)).start()
	print('server started')


if __name__ == "__main__":
	main()
