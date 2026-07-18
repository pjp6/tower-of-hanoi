# FileAI Take-Home Assignment, Tower of Hanoi (Reverse State)

Take-home assignment: given a state of *n* disks (3 ≤ n ≤ 64) on pegs A, B, C, determine which peg all disks initially started on and how many moves of the optimal algorithm were made to reach that state, or report `impossible` if the state is unreachable.

## Repository contents

| File | Description |
|---|---|
| `FileAI_Assignment.pdf` | Assignment question and instructions (provided) |
| `A1Q2.py` | Completed solution (provided template, `tower_hanoi` implemented) |
| `A1Q2.in` | Sample inputs (provided) |
| `README.md` | This file |

Run with:

```
python A1Q2.py < A1Q2.in
```

## Solution explanation

### Key insight

The optimal (minimum-move) solution for moving disks 1..k from peg `src` to peg `dst` always has the same three-phase structure:

1. Move disks 1..k−1 from `src` to the auxiliary peg `aux` — 2^(k−1) − 1 moves
2. Move disk k from `src` to `dst` — 1 move
3. Move disks 1..k−1 from `aux` to `dst` — 2^(k−1) − 1 moves

This means the current position of the **largest disk** tells us exactly which phase the puzzle is in:

- **Disk k on `src`** → phases 2–3 haven't happened yet. All moves made so far belong to the sub-problem "move disks 1..k−1 from `src` to `aux`". Recurse on k−1 disks with target `aux`; add nothing.
- **Disk k on `dst`** → phases 1–2 are complete, contributing exactly (2^(k−1) − 1) + 1 = **2^(k−1)** moves. The remaining moves belong to "move disks 1..k−1 from `aux` to `dst`". Recurse on k−1 disks and add 2^(k−1).
- **Disk k on `aux`** → this never happens on the optimal path, so the state is unreachable from this start peg.

Each recursion level eliminates one disk and adds at most one power of two, so the move count is reconstructed in n steps, no simulation of individual moves is ever needed.

### Determining the start and destination pegs

The assignment's algorithm always moves disk 1 counterclockwise (A→C→B→A). A standard consequence is that the destination peg of the full puzzle is fixed by the start peg and the parity of n: one counterclockwise step from `src` if n is odd, two steps if n is even. So the solver simply tries each of the three pegs as the candidate start, derives its destination from parity, and runs the recursion. A candidate is accepted if the recursion succeeds with a move count in the required range [0, 2^n − 2].

The upper bound 2^n − 2 also handles the special rule for all-disks-on-one-peg states: from its own peg such a state costs 0 moves (an initial state, accepted), while from any other peg it would cost 2^n − 1 moves (a finished state, rejected as out of range) — so it is always reported as an initial state, as required.

### Step-by-step approach

1. **Understand the forward algorithm.** Worked through the PDF's example (3 disks, 5 moves) by hand to confirm how odd moves (disk 1, counterclockwise) and even moves (the only legal non-disk-1 move) generate the unique optimal path, and that the final destination depends on the parity of n.
2. **Reverse the problem.** Recognized that simulating up to 2^64 − 2 moves is infeasible, so the state itself must encode the move count. The three-phase structure above gives exactly that: the largest disk's peg determines the phase, contributing either 0 or 2^(k−1) moves, and reduces the problem to k−1 disks.
3. **Implement.** `count_moves(k, src, dst, pos)` implements the recursion; `tower_hanoi` builds a disk→peg lookup table, tries the three start pegs, and formats the answer. The provided template's I/O code is unmodified.
4. **Verify.** Confirmed all 10 sample cases match the expected output. Additionally verified with a brute-force cross-check: a separate script simulates the assignment's algorithm literally, move by move, from every start peg for n = 3..11, records every reachable state, and compares the solver's answer for **all 3^n possible disk placements** (265,000+ states) — zero mismatches. This also confirmed no state is ever reachable from two different start pegs, so returning the first valid candidate is safe. Finally tested n = 64 boundary cases (maximum recursion depth, move counts near 2^63).

## Time and space complexity

**Time: O(n) per test case.**

- Building the disk→peg lookup table is one pass over n disks: O(n).
- `count_moves` makes exactly **one** recursive call per level (a chain, not a tree — the largest disk's position picks a single branch), each doing O(1) work: O(n) per candidate start peg.
- Three candidate start pegs: 3 × O(n) = O(n).

For T test cases the total is O(T·n). Space is O(n): the lookup table plus the recursion stack of depth n.

This is asymptotically optimal — any correct algorithm must read every disk's position (moving one unread disk can change the answer), which already costs Ω(n). By contrast, step-by-step simulation would take O(2^n) time, since a state can be up to 2^n − 2 moves deep (~1.8 × 10¹⁹ for n = 64) — which is precisely why the solution counts moves in blocks of 2^(k−1) instead of performing them.

## Use of AI tools (Claude)

I used Claude (Anthropic) as a coding agent throughout this assignment, and directed and validated its work at each step:

- **Problem analysis:** After recognizing that step-by-step simulation couldn't scale to n = 64, I worked through the reverse-inference approach with Claude's help: the three-phase structure of the optimal solution, why the largest disk's peg reveals the current phase, and how parity determines the destination. I pressure-tested my understanding at each step so I could defend the approach independently.
- **Implementation:** I wrote the tower_hanoi implementation in this repo myself, based on that understanding and on recursion patterns from my SMU Algorithm Design and Implementation coursework.
- **Verification:** At my direction, correctness was not taken on trust: Claude built an independent brute-force simulator of the assignment's algorithm and exhaustively checked all 3^n placements for n = 3..11 against it, plus the 10 sample cases and n = 64 edge cases. All passed with zero mismatches.



