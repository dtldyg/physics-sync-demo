# coding=utf-8

import json
import socket
import struct
import threading
import queue

global_recv_q = queue.Queue(1024)
global_send_q = queue.Queue(1024)


def iter_recv_pkg():
	while True:
		try:
			pkg = global_recv_q.get_nowait()
			yield pkg
		except queue.Empty:
			break


# --------- network ---------
def run_conn_recv(recv_q, conn, eid=None, send_q=None):
	while True:
		try:
			# read one package
			pkg_len_b = conn.recv(2, socket.MSG_WAITALL)
			pkg_len = struct.unpack('>H', pkg_len_b)[0]
			pkg_b = conn.recv(pkg_len, socket.MSG_WAITALL)
			pkg_s = pkg_b.decode('utf-8')
			pkg = json.loads(pkg_s)
			if pkg['pid'] == PID_JOIN:
				pkg['eid'] = eid
				pkg['send_q'] = send_q
			recv_q.put(pkg)
		except socket.error:
			if eid is not None:
				recv_q.put({'pid': PID_DEL, 'eid': eid})
			return


def run_conn_send(send_q, conn):
	while True:
		try:
			# send one pkg
			pkg = send_q.get()
			if pkg['pid'] == PID_DEL:
				return
			pkg_s = json.dumps(pkg)
			pkg_b = pkg_s.encode('utf-8')
			pkg_len_b = struct.pack('>H', len(pkg_b))
			conn.sendall(pkg_len_b)
			conn.sendall(pkg_b)
		except socket.error:
			return


def run_listen(sock):
	sock.listen()
	eid = 0
	while True:
		conn, addr = sock.accept()
		local_send_q = queue.Queue(1024)
		threading.Thread(target=run_conn_recv, args=(global_recv_q, conn, eid, local_send_q)).start()
		threading.Thread(target=run_conn_send, args=(local_send_q, conn)).start()
		eid = eid + 1


# socket client
def run_client_socket():
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.connect(('127.0.0.1', 9999))
	threading.Thread(target=run_conn_recv, args=(global_recv_q, conn,), daemon=True).start()
	threading.Thread(target=run_conn_send, args=(global_send_q, conn,), daemon=True).start()


# socket server
def run_server_socket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', 9999))
	threading.Thread(target=run_listen, args=(sock,)).start()


# --------- pkg ---------
PID_CMD = 0
PID_STATES = 1
PID_JOIN = 10
PID_ADD_MASTER = 11
PID_ADD_REPLICA = 12
PID_DEL_REPLICA = 13
PID_DEL = 99

# up
example_pkg_join = {'pid': 0, 'eid': 0, 'send_q': None}  # eid、send_q仅server内部使用
example_pkg_cmd = {'pid': 0, 'eid': 0, 'f': {'x': 0, 'y': 0}}
# down
example_pkg_add_master = {'pid': 0, 'eid': 0}
example_pkg_add_replica = {'pid': 0, 'eid': 0}
example_pkg_del_replica = {'pid': 0, 'eid': 0}
example_pkg_states = {'pid': 0, 'frame': 0, 'states': [{'eid': 0, 'p': {'x': 0, 'y': 0, }, 'v': {'x': 0, 'y': 0, }}]}
# inner
example_pkg_del = {'pid': 0, 'eid': 0}
