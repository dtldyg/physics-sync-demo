# coding=utf-8

def foo(x=0, y=0):
	print(x, y)


d = {'x': 1, 'y': 2}
foo(**d)
