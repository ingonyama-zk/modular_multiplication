import sys
sys.path.append("..")
from primitive_ops import mp_lsb_multiply
from math import ceil
from utils import digits_to_num, num_to_digits


def unit_test_mp_lsb_multiply():
    a = 0xffffffff
    b = 0xffffffff
    w = 8
    k = ceil(max(len(bin(a)[2:]), len(bin(b)[2:])) / w)
    mask = int('1' * k * w, base=2)
    A = num_to_digits(a, w, k)
    B = num_to_digits(b, w, k)
    print("num digits = ", k)
    print("bits in digit = ", w)
    c = mp_lsb_multiply(A, B, w, k)
    C = digits_to_num(c, w)
    print("C = ", C)
    print(f"A*B_LSB = {a * b & mask}")
    if ((a * b) & mask) == C:
        print("SUCCESS")
    else:
        print("ERROR!")


unit_test_mp_lsb_multiply()