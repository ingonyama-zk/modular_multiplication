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
    else:
        LS = LS[:k]  # remove extra digit from lsb mult

    # adders and sub, not in multiprecision.
    if z < 4 + log2(k / (2 ** z)):
        AB_lsb = AB[:k + 1]
    else:
        AB_lsb = AB[:k]

    R = mp_subtract(AB_lsb, LS, w, n, k, z)
    R, num_red = mp_subtract_red(R, S, w, k)

    assert num_red < (k / 2 ** z) + 4  # check subtract redundant didn't pass bound

    return R


def domb_barrett_mp_redc_wrapper(s, a, b, w):
    n = len(bin(s)[2:])
    k = ceil(n / w)
    z = k * w - n
    m, _ = divmod(2 ** (2 * n + z), s)  # prime approximation, n + 1 bits
    A = num_to_digits(a, w, k)
    B = num_to_digits(b, w, k)
    M = num_to_digits(m, w, k + 1)[:k]
    S = num_to_digits(s, w, k)
    RES = domb_barett_mp_redc(A, B, S, M, w=w, k=k, n=n)
    res = digits_to_num(RES, w)
    return res


