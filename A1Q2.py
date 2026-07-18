import sys


def count_moves(k, src, dst, pos):
    # The optimal solution for k disks has three phases:
    #   1..k-1: src->aux (2^(k-1)-1 moves), disk k: src->dst (1 move), 1..k-1: aux->dst.
    # The position of disk k tells us which phase we are in.
    if k == 0:
        return 0
    aux = 3 - src - dst
    if pos[k] == src:
        return count_moves(k - 1, src, aux, pos)
    if pos[k] == dst:
        rest = count_moves(k - 1, aux, dst, pos)
        return None if rest is None else (1 << (k - 1)) + rest
    return None


def tower_hanoi(n, state):
    # pos[d] = peg index (0=A, 1=B, 2=C) currently holding disk d
    pos = [0] * (n + 1)
    for peg in range(3):
        for d in state[peg]:
            pos[d] = peg

    for src in range(3):
        # Disk 1 always moves counterclockwise (A->C->B->A). Starting from
        # src, the destination peg of the full puzzle is therefore fixed by
        # the parity of n: one step counterclockwise if n is odd, two steps
        # if n is even.
        dst = (src + 2) % 3 if n % 2 == 1 else (src + 1) % 3
        moves = count_moves(n, src, dst, pos)
        # A valid answer must lie in [0, 2^n - 2]. This also enforces the
        # "all disks on one peg" rule: such a state counts as an initial
        # state (0 moves from its own peg), never as a finished state
        # (2^n - 1 moves from another peg, which is out of range).
        if moves is not None and moves <= (1 << n) - 2:
            return '{} {}'.format('ABC'[src], moves)
    return 'impossible'


num_case = int(sys.stdin.readline())
for _ in range(num_case):
    state = [[int(t) for t in s.split()] for s in sys.stdin.readline().split(',')]
    n = len(state[0]) + len(state[1]) + len(state[2])
    print(tower_hanoi(n, state))
