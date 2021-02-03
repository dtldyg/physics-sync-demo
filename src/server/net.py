# coding=utf-8

import pygame

import socket
import struct
import threading
import json
import queue

import common.switch as switch

recv_q = queue.Queue(1024)


def run_listen(sock):
	sock.listen()
	while True:
		conn, addr = sock.accept()
		# new client
		send_q = queue.Queue(1024)
		threading.Thread(target=run_conn_recv, args=(conn,)).start()
		threading.Thread(target=run_conn_send, args=(send_q, conn)).start()


def run_conn_recv(conn, client_id):
	while True:
		try:
			# read one package
			pkg_len_b = conn.recv(2, socket.MSG_WAITALL)
			pkg_len = struct.unpack('>H', pkg_len_b)[0]
			pkg_b = conn.recv(pkg_len, socket.MSG_WAITALL)
			pkg_s = pkg_b.decode('utf-8')
			pkg = json.loads(pkg_s)

			pkg['id'] = client_id
			pkg['cmd'] = 'sync'
			recv_q.put(pkg)
		except socket.error:
			return


def run_conn_send(send_q, conn):
	clock = pygame.time.Clock()
	while True:
		while True:
			try:
				pkg = send_q.get_nowait()
				# send one package
				pkg_s = json.dumps(pkg)
				pkg_b = pkg_s.encode('utf-8')
				pkg_len_b = struct.pack('>H', len(pkg_b))
				conn.sendall(pkg_len_b)
				conn.sendall(pkg_b)
			except queue.Empty:
				break
			except socket.error:
				return
		clock.tick(switch.NETWORK_STATE_FPS)


# socket server
def run_socket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	threading.Thread(target=run_listen, args=(sock,)).start()
