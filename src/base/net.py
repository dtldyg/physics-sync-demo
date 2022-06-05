# coding=utf-8

import json
import socket
import struct
import threading
import queue
import time

global_recv_q = queue.Queue(1024)  # thread-safety
global_send_q = queue.Queue(1024)  # thread-safety

rtt = [.0, .0]  # in game thread
rtt_q = queue.Queue(8)  # thread-safety


# --------- interface (in game thread) ---------
def iter_recv_pkg():
	while global_recv_q.qsize() > 0:
		yield global_recv_q.get()


def send_client_pkg(pkg):
	global_send_q.put(pkg)


def do_ping():
	rtt1 = 0
	rtt2 = 0
	count = 0
	while rtt_q.qsize() > 0:
		pkg = rtt_q.get()
		r = pkg['t3'] - pkg['t1']
		rtt1 += r
		rtt2 += pkg['t1'] + r / 2 - pkg['t2']
		count += 1
	if count > 0:
		rtt[0] = rtt1 / count
		rtt[1] = rtt2 / count
	send_client_pkg({'pid': PID_PING, 't1': time.time()})


# --------- network (in network thread) ---------
def _run_conn_recv(recv_q, conn, eid=None, send_q=None):
	while True:
		try:
			# read one package
			pkg_len_b = conn.recv(2, socket.MSG_WAITALL)
			pkg_len = struct.unpack('>H', pkg_len_b)[0]
			pkg_b = conn.recv(pkg_len, socket.MSG_WAITALL)
			pkg_s = pkg_b.decode('utf-8')
			pkg = json.loads(pkg_s)
			# network logic
			if pkg['pid'] == PID_JOIN:
				# add id, send_q
				pkg['eid'] = eid
				pkg['send_q'] = send_q
			elif pkg['pid'] == PID_PING:
				# echo pong
				pkg['pid'] = PID_PONG
				pkg['t2'] = time.time()
				send_q.put(pkg)
				continue
			elif pkg['pid'] == PID_PONG:
				pkg['t3'] = time.time()
				rtt_q.put(pkg)
				continue
			recv_q.put(pkg)
		except (socket.error, struct.error):
			if eid is not None:
				recv_q.put({'pid': PID_DEL, 'eid': eid})
			return


def _run_conn_send(send_q, conn):
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


def _run_listen(sock):
	sock.listen()
	eid = 0
	while True:
		try:
			conn, addr = sock.accept()
		except socket.error:
			return
		eid = eid + 1
		local_send_q = queue.Queue(1024)
		threading.Thread(target=_run_conn_recv, args=(global_recv_q, conn, eid, local_send_q), daemon=True).start()
		threading.Thread(target=_run_conn_send, args=(local_send_q, conn), daemon=True).start()


# socket client
def run_client_socket():
	conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	conn.settimeout(1)
	try:
		conn.connect(('127.0.0.1', 9999))
		threading.Thread(target=_run_conn_recv, args=(global_recv_q, conn,), daemon=True).start()
		threading.Thread(target=_run_conn_send, args=(global_send_q, conn,), daemon=True).start()
		return conn
	except OSError:
		return None


# socket server
def run_server_socket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('0.0.0.0', 9999))
	threading.Thread(target=_run_listen, args=(sock,), daemon=True).start()
	return sock


# --------- pkg ---------
# sync
PID_CMD = 0
PID_STATES = 1
# rpc
PID_PING = 10
PID_PONG = 11
PID_JOIN = 12
PID_ADD_MASTER = 13
PID_ADD_REPLICA = 14
PID_DEL_REPLICA = 15
PID_BUFFER = 16
PID_SYNC_CONF = 17
PID_BROAD_CONF = 18
PID_SYNC_BUFFER = 19
# inner
PID_DEL = 99

# up
example_pkg_ping = {'pid': 0, 't1': 0}
example_pkg_join = {'pid': 0, 'eid': 0, 'send_q': None}  # eid、send_q仅server内部使用
example_pkg_cmd = {'pid': 0, 'eid': 0, 'fr': 0, 'dt': 0, 'f': {'x': 0, 'y': 0}}
example_pkg_sync_conf = {'pid': 0, 'k': '', 'v': ''}
# down
example_pkg_pong = {'pid': 0, 't1': 0, 't2': 0}
example_pkg_add_master = {'pid': 0, 'eid': 0, 'p': {'x': 0, 'y': 0, }}
example_pkg_add_replica = {'pid': 0, 'eid': 0, 'p': {'x': 0, 'y': 0, }}
example_pkg_del_replica = {'pid': 0, 'eid': 0}
example_pkg_states = {'pid': 0, 'fr': 0, 'states': [{'eid': 0, 'p': {'x': 0, 'y': 0, }, 'v': {'x': 0, 'y': 0, }}]}
example_pkg_buffer = {'pid': 0, 'opt': 0}  # opt: 0-reset, 1-up, 2-down
example_pkg_broad_conf = {'pid': 0, 'k': '', 'v': ''}
example_pkg_sync_buffer = {'pid': 0, 'v': 0}
# inner
example_pkg_del = {'pid': 0, 'eid': 0}
