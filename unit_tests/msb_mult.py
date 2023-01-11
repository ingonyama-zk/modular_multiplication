
from barret_domb_mp import mp_msb_multiply
from barret_domb_mp import num_to_digits
from barret_domb_mp import digits_to_num


def test():
    a = 0xFFFFFFFFFFFFFFFF
    b = 0xFFFFFFFFFFFFFFFF
    num_digits = 8
    bits_in_digit = 8
    A = num_to_digits(a, bits_in_digit, num_digits)
    B = num_to_digits(b, bits_in_digit, num_digits)

    noisy_res = mp_msb_multiply(A, B, bits_in_digit, num_digits)
    noisy_res = digits_to_num(noisy_res, bits_in_digit)
    real_res = (a*b) >> (num_digits*bits_in_digit)
    e = real_res - noisy_res
    print("e = ", e)
    print("k = ", num_digits)
    if e > num_digits:
        print("ERROR e > k")