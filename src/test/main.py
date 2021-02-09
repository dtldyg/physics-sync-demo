# coding=utf-8

d = {1: 1, 2: 2, 3: 3}
a = [d[e] for e in [1, 3] if e in d]
print(a)
