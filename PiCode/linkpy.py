from ctypes import *
import os

so_file = os.path.join(os.path.dirname(__file__), "linkc.so")

linkc = CDLL(so_file)

linkc.set_up()

print(linkc.test_vals())


import random
linkc.write_vals(bytes(str(random.randint(1,20)).encode("ascii")))

