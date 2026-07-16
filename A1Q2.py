import sys


def count_moves(k, src, dst, pos):
    """Recursively determine how many moves of the optimal algorithm have
    been made, given that disks 1..k are being moved from peg src to peg
    dst and disk d currently sits on peg pos[d].

    The optimal (minimum-move) solution for moving k disks from src to dst
    has a unique three-phase structure:
      Phase 1: move disks 1..k-1 from src to aux   (2^(k-1) - 1 moves)
      Phase 2: move disk k from src to dst          (1 move)
      Phase 3: move disks 1..k-1 from aux to dst    (2^(k-1) - 1 moves)

    So the position of the largest disk k tells us which phase we are in:
      - disk k on src: phases 2-3 have not happened; the moves made so far
        all belong to the sub-problem "move 1..k-1 from src to aux".
      - disk k on dst: phases 1-2 are done (2^(k-1)-1 + 1 = 2^(k-1) moves);
        the remaining moves belong to "move 1..k-1 from aux to dst".
      - disk k on aux: never occurs on the optimal path -> unreachable.

    Returns the move count, or None if the state is unreachable.
    """
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
