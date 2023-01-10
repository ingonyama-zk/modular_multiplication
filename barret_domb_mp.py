import random
from math import *
from random import *


def machine_two_digit_add(x, y, bits_in_digit):
    """
    :param x: 2 digits number
    :param y: 2 digits number
    :param bits_in_digit: bits in each digit
    :return: x+y as 3 digit number (with carry)
    """
    X = digits_to_num(x, bits_in_digit)
    Y = digits_to_num(y, bits_in_digit)
    RES = X+Y
    res = num_to_digits(RES, bits_in_digit, 3)
    return res


def machine_multiply(x, y, bits_in_digit):
    return num_to_digits(x*y, bits_in_digit, 2)


def mp_full_multiply(A, B, bits_in_digit, num_digits):
    if num_digits >= 2**bits_in_digit:
        raise("MP multiplier works only if: num_digits >= 2**bits_in_digit")
    c = [0]*(num_digits*2 + 1)
    for l in range(num_digits*2 - 2 + 1):
        i_min = max(0, l - (num_digits - 1))
        i_max = min(l, num_digits - 1) + 1  # + 1 for inclusive
        for i in range(i_min, i_max):
            mult_res = machine_multiply(A[i], B[l-i], bits_in_digit)
            add_res = machine_two_digit_add(mult_res, [c[l], c[l+1]], bits_in_digit)
            [c[l], c[l+1]] = [add_res[0], add_res[1]]
            c[l+2] = c[l+2] + add_res[2]
    return c[:num_digits*2]


def mp_lsb_multiply(A, B, bits_in_digit, num_digits, return_extra_digit=False):
    if num_digits >= 2**bits_in_digit:
        raise("MP multiplier works only if: num_digits >= 2**bits_in_digit")
    c = [0]*(num_digits*2 + 1)
    for l in range(num_digits):  # num_digits
        i_min = max(0, l - (num_digits - 1))
        i_max = min(l, num_digits - 1) + 1  # + 1 for inclusive
        for i in range(i_min, i_max):
            mult_res = machine_multiply(A[i], B[l-i], bits_in_digit)
            add_res = machine_two_digit_add(mult_res, [c[l], c[l+1]], bits_in_digit)
            [c[l], c[l+1]] = [add_res[0], add_res[1]]
            c[l+2] = c[l+2] + add_res[2]
    if return_extra_digit:
        return c[:num_digits+1]
    else:
        return c[:num_digits]


def mp_lsb_diagonal(A, B, bits_in_digit, num_digits):
    if num_digits >= 2**bits_in_digit:
        raise("MP multiplier works only if: num_digits >= 2**bits_in_digit")
    c = [0]*(num_digits*2 + 1)
    l = num_digits
    i_min = max(0, l - (num_digits - 1))
    i_max = min(l, num_digits - 1) + 1  # + 1 for inclusive
    for i in range(i_min, i_max):
        mult_res = machine_multiply(A[i], B[l-i], bits_in_digit)
        add_res = machine_two_digit_add(mult_res, [c[l], c[l+1]], bits_in_digit)
        [c[l], c[l+1]] = [add_res[0], add_res[1]]
        c[l+2] = c[l+2] + add_res[2]

    return c[l]


def mp_msb_multiply(A, B, bits_in_digit, num_digits):
    """
    Returns [A*B]_msb + e
    e is in [0, 1]
    """
    if num_digits >= 2**bits_in_digit:
        raise("MP multiplier works only if: num_digits >= 2**bits_in_digit")
    c = [0]*(num_digits*2 + 1)
    for l in range(num_digits-1 - 4, num_digits*2 - 2 + 1):  # num_digits
        i_min = max(0, l - (num_digits - 1))
        i_max = min(l, num_digits - 1) + 1  # + 1 for inclusive
        for i in range(i_min, i_max):
            mult_res = machine_multiply(A[i], B[l-i], bits_in_digit)
            add_res = machine_two_digit_add(mult_res, [c[l], c[l+1]], bits_in_digit)
            [c[l], c[l+1]] = [add_res[0], add_res[1]]
            c[l+2] = c[l+2] + add_res[2]
    return c[num_digits:2*num_digits]


def unit_test_mp_msb_multiply():
    # A = 0xFFFFFFFFFFFFFFFFFFFFFFFF
    # B = 0xFFFFFFFFFFFFFFFFFFFFFFFF
    # bits_in_digit = 8
    A = 0xFFFFFFFFFFFF
    B = 0xFFFFFFFFFFFF
    bits_in_digit = 8
    # A = 7
    # B = 13
    # bits_in_digit = 3
    num_digits = ceil(max(len(bin(A)[2:]), len(bin(B)[2:])) / bits_in_digit)
    print("num digits = ", num_digits)
    print("bits in digit = ", bits_in_digit)
    c = mp_msb_multiply(A, B, bits_in_digit, num_digits)
    C = digits_to_num(c, bits_in_digit)
    print("C = ", C)
    print(f"A*B_MSB = {A * B >> bits_in_digit * num_digits}")
    if ((A * B >> bits_in_digit * num_digits)) == C:
        print("SUCCESS, ERROR = 0")
    elif (A * B >> bits_in_digit * num_digits) == C:
        print("SUCCESS ERROR = 1")
    else:
        print("ERROR!")


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


def unit_test_mp_full_multiply():
    A = 0xffffff
    B = 0xffffff
    bits_in_digit = 8
    # A = 7
    # B = 13
    # bits_in_digit = 3
    print(f"A*B = {A*B}")
    num_digits = ceil(max(len(bin(A)[2:]), len(bin(B)[2:])) / bits_in_digit)
    print("num digits = ", num_digits)
    print("bits in digit = ", bits_in_digit)
    c = mp_full_multiply(A, B, bits_in_digit, num_digits)
    C = digits_to_num(c, bits_in_digit)
    print("C = ", C)
    if (A*B==C):
        print("SUCCESS")
    else:
        print("ERROR!")


def mp_adder(A, B, bits_in_digit, num_digits):  # returns num_digits + 1 number
    C = [0] * (num_digits + 1)
    carry = 0
    for i in range(num_digits):
        carry, res = divmod(A[i] + B[i] + carry, 2**bits_in_digit)
        C[i] = res
    C[num_digits] = carry
    return C


def shifter(A, shift, bits_in_digit, num_digits):
    a = digits_to_num(A, bits_in_digit)
    a_shift = a << shift
    A_SHIFT = num_to_digits(a_shift, bits_in_digit, num_digits)
    return A_SHIFT


def barett_domb_reduction_multiprecision(A, B, M, S, bits_in_digit, num_digits, n):

    # Full multiply and break into LSB, MSB parts
    AB = mp_full_multiply(A, B, bits_in_digit, num_digits)
    AB_lsb = AB[:num_digits+1]

    # Shift MSB if needed (fractional digit shift)
    mk = bits_in_digit * num_digits
    if mk != n:
        shift = mk-n
        AB_shift = shifter(AB, shift, bits_in_digit, num_digits*2)
        AB_msb = AB_shift[num_digits:2*num_digits]
    else:
        shift = 0
        AB_msb = AB[num_digits:2 * num_digits]

    # calculate l estimator (MSB multiply)
    L = mp_msb_multiply(AB_msb, M, bits_in_digit, num_digits)
    # Add another AB_msb because m[n] = 1 by definition.
    L = mp_adder(L, AB_msb, bits_in_digit, num_digits)[:num_digits]

    # calculate L*S (LSB multiply)
    LS = mp_lsb_multiply(L, S, bits_in_digit, num_digits, return_extra_digit=True)
    # Extra 2 bits handling
    lsb_mult_carry_extra = LS[num_digits]  # carry to 2^n, 2^(n+1) bits from LSB mult
    lsb_mult_extra = mp_lsb_diagonal(L, S, bits_in_digit, num_digits)
    LS[num_digits] = (lsb_mult_carry_extra + lsb_mult_extra)

    # adders and sub, not in multiprecision
    ab_lsb = digits_to_num(AB_lsb, bits_in_digit)
    ls = digits_to_num(LS, bits_in_digit)
    minus_ls_plus_1 = (~ls + 1) % 2 ** (n + 2)
    r = (ab_lsb + minus_ls_plus_1) % 2 ** (n + 2)
    if r < 0:
        print("R < 0")
    num_red = 0
    s = digits_to_num(S, bits_in_digit)
    while r > s:
        r = r - s
        num_red += 1
    if num_red > 5:
        print("ERROR: NUM OF REDUNDENCY IS GREATER THAN 4")

    return r


def mp_barrett_domb_wrapper(s, a, b, bits_in_digit):
    n = len(bin(s)[2:])
    num_digits = ceil(n / bits_in_digit)
    m, _ = divmod(2 ** (2 * n), s)  # prime approximation, n + 1 bits
    num_msb_zeros = num_digits * bits_in_digit - n
    if (num_msb_zeros > 0):
        m = m << num_msb_zeros
    A = num_to_digits(a, bits_in_digit, num_digits)
    B = num_to_digits(b, bits_in_digit, num_digits)
    M = num_to_digits(m, bits_in_digit, num_digits + 1)[:num_digits]
    S = num_to_digits(s, bits_in_digit, num_digits)
    res = barett_domb_reduction_multiprecision(A, B, M, S, bits_in_digit=bits_in_digit, num_digits=num_digits, n=n)
    return res


def random_unit_test(num_rep, bits_in_digit=32):
    seed(0)
    corrects = 0
    wrongs = 0
    for i in range(num_rep):
        s = randint(2**64, 2**512)
        a = randint(0, s)
        b = randint(0, s)
        res = mp_barrett_domb_wrapper(s, a, b, bits_in_digit)
        reference = a * b % s
        if reference == res:
            corrects += 1
        else:
            print("WRONG")
            print(f's = {s}')
            wrongs += 1
    print(f"Total corrects = {corrects}")
    print(f"Total wrongs = {wrongs}")


def edge_unit_test(bits_in_digit=32):
    seed(0)
    corrects = 0
    wrongs = 0
    for i in range(64, 32*50):
        s = randint(2**i, 2**(i+1))
        a = s-1
        b = s-1
        res = mp_barrett_domb_wrapper(s, a, b, bits_in_digit)
        reference = a * b % s
        if reference == res:
            corrects += 1
        else:
            print("WRONG")
            print(f's = {s}')
            wrongs += 1
    print(f"Total corrects = {corrects}")
    print(f"Total wrongs = {wrongs}")


def main():
    a = 0x1ff2f1f0  # 16 bits
    b = 0x1ff2f1f0  # 16 bits
    p = 0x1ff2f1f1
    assert a < p
    assert b < p
    n = len(bin(p)[2:])
    bits_in_digit = 4
    num_digits = ceil(n/bits_in_digit)
    z = num_digits*bits_in_digit - n
    print("n = ", n)
    print("z = ", z)
    print("n = ", n)
    print("num_digits = ", num_digits)
    print("bits_in_digit = ", bits_in_digit)
    # import random
    # a = random.randint(0, 2**377 - 1)
    # b = random.randint(0, 2**377 - 1)
    # n = 377
    # p = 258664426012969094010652733694893533536393512754914660539884262666720468348340822774968888139573360124440321458177
    # bits_in_digit = 13
    # num_digits = int(377/bits_in_digit)
    # a = 34417742317182120018878071992578734443345380140324348504725908104674990279357368829402877632118637584522104719869
    # b = 20586266327374793683517775089400306838020121138543508095482142045451134346728927206370377876725213598883040048788
    # n = 4
    # a = int('1111', base=2)
    # b = int('1111', base=2)
    # p = int('1011', base=2)
    # bits_in_digit = 2
    # num_digits = 2


    # pre-calculation
    s = p  # prime number
    assert s == s & (int('1'*n, base=2))
    m, _ = divmod(2 ** (2*n), p)  # prime approximation, n + 1 bits
    assert m == m & (int('1'*(n+1), base=2))
    # shift m if needed
    num_msb_zeros = num_digits*bits_in_digit - n
    if (num_msb_zeros> 0):
        m = m << num_msb_zeros

    # Prepare multiprecision words:
    A = num_to_digits(a, bits_in_digit, num_digits)
    B = num_to_digits(b, bits_in_digit, num_digits)
    M = num_to_digits(m, bits_in_digit, num_digits+1)[:num_digits]
    S = num_to_digits(s, bits_in_digit, num_digits)
    res = barett_domb_reduction_multiprecision(A, B, M, S, bits_in_digit=bits_in_digit, num_digits=num_digits, n=n)
    reference = a*b % p
    print("res = ", res)
    print("reference = ", reference)
    if reference == res:
        print("SUCCESS!")
    else:
        print("ERROR!")


def digits_to_num(arr, bits_in_digit):
    """
    Little endian
    """
    num = 0
    for i in range(len(arr)):
        weight = 2 ** (i * bits_in_digit)
        num += arr[i] * weight
    return num


def num_to_digits(num, bits_in_digit, num_digits):
    """
    Little endian
    """
    temp_num = num
    words = [0] * num_digits
    mask = int('1' * bits_in_digit, base=2)
    for i in range(num_digits):
        words[i] = temp_num & mask
        temp_num = temp_num >> bits_in_digit
    return words


edge_unit_test()

