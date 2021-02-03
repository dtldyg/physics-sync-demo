# coding=utf-8

import socket
import struct
import threading
import json
import queue

recv_q = queue.Queue(1024)


# socket listen
def run_listen(sock):
	client_id = -1
	while True:
		conn, addr = sock.accept()
		# new client
		client_id = client_id + 1
		send_q = queue.Queue(1024)
		put_new_pkg(client_id, send_q)
		threading.Thread(target=run_conn_recv, args=(conn, client_id)).start()
		threading.Thread(target=run_conn_send, args=(send_q, conn)).start()
		print('client in:', client_id, addr)


# socket connection recv
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
			print('client del:', client_id)
			put_del_pkg(client_id)
			return


# socket connection send
def run_conn_send(send_q, conn):
	while True:
		try:
			pkg = send_q.get()
			# send one package
			pkg_s = json.dumps(pkg)
			pkg_b = pkg_s.encode('utf-8')
			pkg_len_b = struct.pack('>H', len(pkg_b))
			conn.sendall(pkg_len_b)
			conn.sendall(pkg_b)
		except socket.error:
			return


def put_new_pkg(client_id, send_q):
	pkg = {'cmd': 'new', 'id': client_id, 'send_q': send_q}
	recv_q.put(pkg)


def put_del_pkg(client_id):
	pkg = {'cmd': 'del', 'id': client_id}
	recv_q.put(pkg)


# socket server
def run_socket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	sock.listen()
	threading.Thread(target=run_listen, args=(sock,)).start()
