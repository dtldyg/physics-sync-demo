# coding=utf-8

import socket
import struct
import threading
import json
import queue


# socket connection
def run_conn_recv(recv_q, conn, client_id):
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
			print('client over:', client_id)
			put_over_pkg(recv_q, client_id)
			return


def put_in_pkg(recv_q, send_q, client_id):
	pkg = {'cmd': 'in', 'id': client_id, 'send_q': send_q}
	recv_q.put(pkg)


def put_over_pkg(recv_q, client_id):
	pkg = {'cmd': 'over', 'id': client_id}
	recv_q.put(pkg)


# socket connection
def run_conn_send(send_q, conn, _):
	while True:
		try:
			pkg = send_q.get()
			# send one pkg
			pkg_s = json.dumps(pkg)
			pkg_b = pkg_s.encode('utf-8')
			pkg_len_b = struct.pack('>H', len(pkg_b))
			conn.sendall(pkg_len_b)
			conn.sendall(pkg_b)
		except socket.error:
			return


# socket listener
def run_socket(recv_q):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	sock.listen()

	client_id = 0
	while True:
		conn, addr = sock.accept()
		# new client
		print('client in:', client_id)
		send_q = queue.Queue(1024)
		put_in_pkg(recv_q, send_q, client_id)
		threading.Thread(target=run_conn_recv, args=(recv_q, conn, client_id)).start()
		threading.Thread(target=run_conn_send, args=(send_q, conn, client_id)).start()
		client_id = client_id + 1
