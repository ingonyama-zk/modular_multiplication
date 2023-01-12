from random import *
import sys
sys.path.append("..")
from domb_barrett_mp import domb_barrett_mp_redc_wrapper


def edge_unit_test(bits_in_digit=32):
    seed(0)
    corrects = 0
    wrongs = 0
    for i in range(64, 32*50):
        s = randint(2**i, 2**(i+1))
        a = s-1
        b = s-1
        res = domb_barrett_mp_redc_wrapper(s, a, b, bits_in_digit)
        reference = a * b % s
        if reference == res:
            corrects += 1
        else:
            print("WRONG")
            print(f's = {s}')
            wrongs += 1
    print(f"Total corrects = {corrects}")
    print(f"Total wrongs = {wrongs}")



edge_unit_test()