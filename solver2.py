'''
This generates solutions to the Sequential Self-referential problem

'''
import numpy as np

solutions = []

n_dict = {
    'm': 2,
    'n': 4,
    'n-1': 3,
    'nbits': 15,
    'n^2': 16,
    'maxbit': 8,
    't': 0,
    'ti': 0,
    's': 0,
    'si': 0,
}


def A(n):
    return [a(i) for i in range(4, n+1)]


def a(n):
    return len(B_n(n))


def B_n(n):
    solutions.clear()
    update_n(n)
    for i in range(n-1):
        grid = base_grid(n)
        update_t(i)
        for j in range(n-1):
            grid[j, j] = 1 << (plusdot(i, j))
        for j in range(n-1):
            if (i == j) or (i == plusdot(j, 2)):
                continue
            for l in range(n-1):
                grid[l, plusdot(l, 2)] = 1 << (plusdot(j, l))
            iterate(grid)
    [show_grid(g) for g in solutions]
    return solutions


def show_grid(grid):
    vec_func = np.vectorize(lsb)
    print(vec_func(grid))


def base_grid(n):
    grid = np.full((n, n), 2**(n-1) - 1)
    return s_0(grid)


def s_0(grid):
    for i in range(nd('n')):
        grid[i, nextdot(i)] = nd('maxbit')
    return grid


def nd(key):
    return n_dict[key]


def n_bits(n):
    return (1 << n) - 1


def update_n(n):
    n_dict['n'] = n
    n_dict['n-1'] = n-1
    n_dict['nbits'] = n_bits(n)
    n_dict['n^2'] = n**2
    n_dict['maxbit'] = 1 << (n - 1)
    if n % 2 == 0:
        n_dict['m'] = n - 2
    else:
        n_dict['m'] = int((n-3)/2)


def update_t(k):
    ti = minusdot(nd('n')-2, k)
    si = minusdot(nd('m')+1, k)
    n_dict['t'] = 1 << ti
    n_dict['ti'] = ti
    n_dict['s'] = 1 << si
    n_dict['si'] = si


def indices(n):
    for i in range(n):
        for j in range(n):
            yield i,j


# lowest_set_bit
def lsb(k):
    if k == 0:
        return None
    i = 0
    while not (k & 1):
        k >>= 1
        i += 1
    return i


# has_single_bit
def hsb(k):
    return k and not (k & (k-1))


def plusdot(k, m):
    n1 = nd('n-1')
    if k == n1:
        return k
    return (k + m) % n1


def nextdot(k):
    n = nd('n')
    if k < n - 2:
        return k + 1
    if k == n - 2:
        return 0
    return k


def minusdot(k, m):
    n1 = nd('n-1')
    if k == n1:
        return k
    return (k - m + n1) % n1


def prevdot(k):
    if k == 0:
        return nd('n')-2
    if k < nd('n-1'):
        return k - 1
    return k


def bits_up(k):
    maxbit = nd('maxbit')
    has_max = k & maxbit
    k &= ~maxbit
    k <<= 1
    if k & maxbit:
        k |= 1
        k &= ~maxbit

    return k | has_max


def bits_up_i(k, i):
    i = i % nd('n-1')
    for j in range(i):
        k = bits_up(k)
    return k


def bits_down(k):
    maxbit = nd('maxbit')
    has_max = k & maxbit
    k &= ~maxbit
    if k & 1:
        k |= maxbit
    k >>= 1
    return k | has_max


def bits_down_i(k, i):
    i = i % nd('n-1')
    for j in range(i):
        k = bits_down(k)
    return k


def keep(red, grid, r, c, val):
    prev = int(grid[r, c])
    grid[r, c] = prev & val
    red[r, c] |= prev & ~val
    change_flag = False
    if prev & ~val:
        change_flag = True
    break_flag = False
    if grid[r, c] == 0:
        break_flag = True
    return red, grid, break_flag, change_flag


def restore(red, grid):
    for r, c in indices(nd('n')):
        grid[r, c] |= red[r, c]

    return grid


def test():
    B_n(8)
    rd = np.full((8,8), 0)
    gd = base_grid(8)
    rd = all_red(rd, gd)
    return gd


def all_red(red, grid):
    m = nd('m')
    n = nd('n')
    n1 = nd('n-1')
    t = nd('t')
    ti = nd('ti')
    s = nd('s')
    si = nd('si')
    for i, j in indices(n):
        ij = grid[i, j]
        if not (minusdot(j, 1) == 1 or i == n1 or j == n1 or i == j):
            val = bits_up(grid[prevdot(i), prevdot(j)])
            red, grid, flag, ch = keep(red, grid, i, j, val)
            if flag:
                return red

        if hsb(ij):
            inj = grid[i, nextdot(j)]
            itj = grid[nextdot(i), j]
            c = lsb(ij)
            if c == ti:
                val = 1 << plusdot(j, ti)
                red, grid, flag, ch = keep(red, grid, i, 0, val)
                if flag:
                    return red
            # if c == si: # fails on evens
            #     val = 1 << plusdot(i, si)
            #     red, grid, flag, ch = keep(red, grid, 0, j, val)
            #     if flag:
            #         return red
            if j == 0:
                offset = minusdot(c, ti)
                red, grid, flag, ch = keep(red, grid, i, offset, t)
                if flag:
                    return red
            # if i == 0: # fails on evens
            #     offset = minusdot(c, si)
            #     red, grid, flag, ch = keep(red, grid, offset, j, s)
            #     if flag:
            #         return red
            if hsb(inj):
                c2 = lsb(inj)
                g = 1 << i
                red, grid, flag, ch = keep(red, grid, c, c2, g)
                if flag:
                    return red
            if hsb(itj):
                c2 = lsb(itj)
                g = 1 << j
                g = bits_up_i(g, m)
                red, grid, flag, ch = keep(red, grid, c, c2, g)
                if flag:
                    return red

            for k in range(n):
                p = grid[k, c]
                q = grid[c, k]
                if hsb(p):
                    if p & (1 << i):
                        red, grid, flag, ch = keep(red, grid, i, prevdot(j), 1 << k)
                        if flag:
                            return red
                    if p & (1 << plusdot(j, m)):
                        red, grid, flag, ch = keep(red, grid, prevdot(i), j, 1 << k)
                        if flag:
                            return red
                if hsb(q):
                    if q & (1 << i):
                        red, grid, flag, ch = keep(red, grid, i, nextdot(j), 1 << k)
                        if flag:
                            return red
                    if q & (1 << plusdot(j, m)):
                        red, grid, flag, ch = keep(red, grid, nextdot(i), j, 1 << k)
                        if flag:
                            return red
                if (k != j) and (grid[i, k] & ij):
                    red, grid, flag, ch = keep(red, grid, i, k, ~ij)
                    if flag:
                        return red
                if (k != i) and (grid[k, j] & ij):
                    red, grid, flag, ch = keep(red, grid, k, j, ~ij)
                    if flag:
                        return red

    return red


def red_all(grid):
    n = nd('n')
    red = np.full((n, n), 0)

    #start
    red = all_red(red, grid)

    return red


def iterate(grid):
    if not validator(grid):
        return False
    next_index = not_one(grid)
    if not next_index:
        solutions.append(grid.copy())
        return True

    rc = grid[next_index]
    for k in ones_of(rc):
        grid[next_index] = 1 << k
        red = red_all(grid)
        iterate(grid)
        restore(red, grid)
    grid[next_index] = rc
    return False


def not_one(grid):
    n = nd('n')
    for row, col in indices(n):
        c = grid[row, col]
        if c.bit_count() != 1:
            return row, col
    return None


def ones_of(k):
    bits = np.array(list(np.binary_repr(k)[::-1]), dtype=int)

    indices_of_ones = np.where(bits == 1)[0]

    return indices_of_ones


def validator(grid):
    n = nd('n')
    for func in [cn_0a, cn_1, cn_2]:
        if not func(grid, n):
            return False
    return True


def cn_0a(grid, n):
    for r, c in indices(n):
        if grid[r, c] == 0:
            return False
    return True


def cn_1(grid, n):
    nbits = nd('nbits')
    # cn_1a
    for row in grid:
        if np.bitwise_or.reduce(row) != nbits:
            return False
    # cn_1b
    for col in grid.T:
        if np.bitwise_or.reduce(col) != nbits:
            return False
    return True


def cn_2(grid, n):
    for r, c in indices(n):
        ref_r = None
        ref_c = None
        if grid[r, c].bit_count() == 1:
            ref_r = lsb(grid[r, c])
        if grid[r, nextdot(c)].bit_count() == 1:
            ref_c = lsb(grid[r, nextdot(c)])
        if ref_r is not None and ref_c is not None and (grid[ref_r, ref_c] & (1 << r)) == 0:
            return False
    return True








