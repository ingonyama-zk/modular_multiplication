from primitive_ops import mp_lsb_multiply
from math import ceil


def unit_test_mp_lsb_multiply():
    A = 0xffffffff
    B = 0xffffffff
    bits_in_digit = 8
    # A = 7
    # B = 13
    # bits_in_digit = 3
    num_digits = ceil(max(len(bin(A)[2:]), len(bin(B)[2:])) / bits_in_digit)
    mask = int('1' * num_digits * bits_in_digit, base=2)
    print("num digits = ", num_digits)
    print("bits in digit = ", bits_in_digit)
    c = mp_lsb_multiply(A, B, bits_in_digit, num_digits)
    C = digits_to_num(c, bits_in_digit)
    print("C = ", C)
    print(f"A*B_LSB = {A * B & mask}")
    if ((A * B) & mask) == C:
        print("SUCCESS")
    else:
        print("ERROR!")
