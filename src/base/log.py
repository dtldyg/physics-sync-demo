# coding=utf-8

import time


def info(*args, sep=' ', end='\n', file=None):
	print('[{}]'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))), *args, sep=sep, end=end, file=file)
