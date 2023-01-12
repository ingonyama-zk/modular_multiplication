from random import *
import sys
sys.path.append("..")
from domb_barrett_mp import  domb_barrett_mp_redc_wrapper


def random_unit_test(num_rep, bits_in_digit=32):
    seed(0)
    corrects = 0
    wrongs = 0
    for i in range(num_rep):
        s = randint(2**64, 2**512)
        a = randint(0, s)
        b = randint(0, s)
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


random_unit_test(10000)