# coding=utf-8

import time
import threading


def foo():
	while True:
		time.sleep(1)


threading.Thread(target=foo).start()
