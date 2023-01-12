from math import *
from primitive_ops import *
from utils import *


def domb_barett_mp_redc(A, B, S, M, w, k, n):
    """
    A: input number. represented by k digits.
    B: input number. represented by k digits
    S: mod field. represented by k digits
    M: [2**(wk - n) * floor(2<<n / s)][k-1:0] 1/S Barett approximation, represented by k bits
    w: bits in each digit
    k: number of digits required to represent S
    n: ceil(log2(S))

    outputs:
        R = A * B mod S
    """

    # Full multiply and break into LSB, MSB parts
    AB = mp_full_multiply(A, B, w, k)

    # AB msb extraction (+ shift)
    wk = w * k
    z = (wk-n)
    AB_shift = mp_shifter(AB, 2 * z, w, k * 2, 'left')
    AB_msb = AB_shift[k:2 * k]

    # L estimation
    L = mp_msb_multiply(AB_msb, M, w, k)  # calculate l estimator (MSB multiply)
    L = mp_adder(L, AB_msb, w, k)[:k]  # Add another AB_msb because m[n] = 1
    L = mp_shifter(L, z, w, k, 'right')

    # LS calculation
    LS = mp_lsb_multiply(L, S, w, k, return_extra_digit=True)
    # If needed, calculate extra diagonal.
    if z < 4 + log2(k/(2**z)):
        lsb_mult_carry_extra = LS[k]
        lsb_mult_extra = mp_lsb_extra_diagonal(L, S, w, k)
        LS[k] = (lsb_mult_carry_extra + lsb_mult_extra)
    #else:
    #    LS = LS[:k]  # remove extra digit from lsb mult

    # adders and sub, not in multiprecision.
    AB_lsb = AB[:k + 1]
    ab_lsb = digits_to_num(AB_lsb, w)
    ls = digits_to_num(LS, w)
    minus_ls_plus_1 = (~ls + 1) % 2 ** (n + ceil(log2(4 + (k / 2 ** z))))
    r = (ab_lsb + minus_ls_plus_1) % 2 ** (n + ceil(log2(4 + (k / 2 ** z))))
    if r < 0:
        print("R < 0")
    num_red = 0
    s = digits_to_num(S, w)
    while r > s:
        r = r - s
        num_red += 1
    if num_red > 2**((k / 2 ** z)) + 4:
        print("ERROR: NUM OF REDUNDENCY IS GREATER THAN 2**num_digits + 4")

    return r


def domb_barrett_mp_redc_wrapper(s, a, b, w):
    n = len(bin(s)[2:])
    k = ceil(n / w)
    z = k * w - n
    m, _ = divmod(2 ** (2 * n + z), s)  # prime approximation, n + 1 bits
    A = num_to_digits(a, w, k)
    B = num_to_digits(b, w, k)
    M = num_to_digits(m, w, k + 1)[:k]
    S = num_to_digits(s, w, k)
    res = domb_barett_mp_redc(A, B, S, M, w=w, k=k, n=n)
    return res


