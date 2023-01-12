import sys
sys.path.append("..")
from primitive_ops import mp_full_multiply
from math import *
from utils import num_to_digits, digits_to_num


def unit_test_mp_full_multiply():
    a = 0xffffff
    b = 0xffffff
    w = 8 # bits in digit
    print(f"A*B = {a*b}")
    k = ceil(max(len(bin(a)[2:]), len(bin(b)[2:])) / w)  # num of digits
    A = num_to_digits(a, w, k)
    B = num_to_digits(b, w, k)
    print("num digits = ", k)
    print("bits in digit = ", w)
    c = mp_full_multiply(A, B, w, k)
    C = digits_to_num(c, w)
    print("C = ", C)
    if (a*b==C):
        print("SUCCESS")
    else:
        print("ERROR!")


unit_test_mp_full_multiply()