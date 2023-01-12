from math import *
from random import *


class barrett_domb_sp:
    def __init__(self):
        self.n = 377
        self.s = 258664426012969094010652733694893533536393512754914660539884262666720468348340822774968888139573360124440321458177
        assert (self.s < 2 ** self.n)
        self.m = 2 ** (2 * self.n) // self.s
        self.ms = self.m * self.s

    def run(self, do_print=False):
        a = randint(0, self.s - 1)
        b = randint(0, self.s - 1)
        # a = 258664426012969094010652733694893533536393512754914660539884262666720468348340822774968888139573360124440321458177 - 1
        # b = 258664426012969094010652733694893533536393512754914660539884262666720468348340822774968888139573360124440321458177 - 1
        # direct calc
        ab = a * b
        _l, _r = divmod(ab, self.s)  # sim only (not for synthesis)

        # a*b full mult
        ab_msb = ab >> self.n
        ab_lsb = ab % 2 ** (self.n + 2)

        # ab*m msb mult (attempt)
        abm = ab_msb * self.m
        l1 = abm >> self.n
        _e_l1 = _l - l1  # sim only (not for synthesis)
        assert (_e_l1 < 4)
        assert (_e_l1 >= 0)

        # l1*s lsb mult
        l1s = l1 * self.s
        l1s_lsb = l1s % 2 ** (self.n + 2)

        # ab-l1s fixed width adder
        l1s_lsb_not = ~l1s_lsb % 2 ** (self.n + 2)
        r_plus = (ab_lsb + l1s_lsb_not + 1) % 2 ** (self.n + 2)

        # summary (replace with iterative subtraction)
        r_hat = r_plus - _e_l1 * self.s  # sim only (not for synthesis)
        assert (r_hat == _r)

        # print
        if not do_print:
            return
        print('-- params --')
        print('n = ' + str(self.n))
        print('s[n-1:0] = ' + hex(self.s))
        print('m[n:0] = ' + hex(self.m))
        print('a[n-1:0] = ' + hex(a))
        print('b[n-1:0] = ' + hex(b))
        print()
        print('-- direct calc --')
        print('l[n:0] = ' + hex(_l))
        print('r[n-1:0] = ' + hex(_r))
        print(hex(_r) + ' = ' + hex(a) + ' * ' + hex(b) + ' - ' + hex(_l) + ' * ' + hex(self.s))
        print()
        print('-- a*b full mult --')
        print('ab[2n-1:0] = ' + hex(ab))
        print('ab[2n-1:n] = ' + hex(ab_msb))
        print('ab[n+1:0] = ' + hex(ab_lsb))
        print()
        print('-- ab*m msb mult --')
        print('l1[3n:2n] = ' + hex(l1))
        print('e(l1) = ' + hex(_e_l1))
        print()
        print('-- l1*s lsb mult --')
        print('l1s[n+1:0] = ' + hex(l1s_lsb))
        print()
        print('-- ab-l1s fixed width adder --')
        print('r+[n+1:0] = ' + hex(r_plus))
        print()
        print('-- subtract redundant s --')
        print('r_hat = ' + hex(r_hat))
        print()


if __name__ == '__main__':
    mpm_ = barrett_domb_sp()
    for i in range(1000000):
        mpm_.run()
    mpm_.run(do_print=True)
