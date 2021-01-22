# coding=utf-8

import json
import socket
import struct
import threading
import queue

send_q = queue.Queue(1024)
recv_q = queue.Queue(1024)


def run_conn_send(sock):
	while True:
		try:
			pkg = send_q.get()
			# send one pkg
			pkg_s = json.dumps(pkg)
			pkg_b = pkg_s.encode('utf-8')
			pkg_len_b = struct.pack('>H', len(pkg_b))
			sock.sendall(pkg_len_b)
			sock.sendall(pkg_b)
		except socket.error:
			return


def run_conn_recv(sock):
	while True:
		try:
			# read one package
			pkg_len_b = sock.recv(2, socket.MSG_WAITALL)
			pkg_len = struct.unpack('>H', pkg_len_b)[0]
			pkg_b = sock.recv(pkg_len, socket.MSG_WAITALL)
			pkg_s = pkg_b.decode('utf-8')
			pkg = json.loads(pkg_s)
			recv_q.put(pkg)
		except socket.error:
			return


# socket client
def run_socket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('127.0.0.1', 9999))
	threading.Thread(target=run_conn_send, args=(sock,)).start()
	threading.Thread(target=run_conn_recv, args=(sock,)).start()
