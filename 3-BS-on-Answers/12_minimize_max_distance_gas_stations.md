# Minimize Max Distance Between Gas Stations

**Pattern:** Binary Search on Answer — Minimize the Maximum (continuous version)

This is the trickiest problem in the series so far — not because any
single step is hard, but because there are more moving parts than
usual (two different valid solutions, plus floating-point numbers,
plus a heap). Read this top to bottom even if some sections feel slow
— each one only depends on the one before it.

## The problem, in plain English

You've got some gas stations already placed along a road. You get to
add `k` brand-new stations anywhere you want — even at fractional
positions like `4.5`. After adding them, look at every pair of
stations that end up next to each other, and find the biggest gap
between any such pair. Your job: place the new stations so that
*biggest remaining gap* is as small as possible.

```
arr = [1, 13, 17, 23]
k = 5
answer = 3.0
```

Think of it like watering a garden with a fixed number of sprinklers —
you want to place them so no single dry patch is worse than any other.

## Step 1 — think about just ONE gap first

Forget the whole road. Say there's a single gap of length `L`, and you
get to drop `x` new stations into just that gap. What's the smartest
way to place them?

Spread them out **evenly**. If you don't, one of the leftover pieces
ends up bigger than it needs to be, which only hurts you — so equal
spacing is always at least as good as anything else.

`x` new stations split one gap into `x + 1` pieces (picture: 1 station
cuts a gap into 2 pieces, 2 stations cut it into 3 pieces, and so on).
So the size of the biggest piece left in that gap is:

```
biggest piece = L / (x + 1)
```

Now flip the question around, because this is the direction we'll
actually need: *"If I want every piece in this gap to be at most
`dist`, how many stations does that cost me?"*

```
pieces needed  = ceil(L / dist)      # round UP — a partial piece still needs a station
stations needed = pieces needed - 1   # pieces = stations + 1, so subtract 1 back
```

### A trap worth knowing about: exact division

Say `L = 6` and `dist = 2`. `6 / 2 = 3` exactly. It's tempting to
think "3 stations" — but 3 *pieces* only takes **2** new stations:

```
1 -- 3 -- 5 -- 7        (dashes = 2 units each, 3 pieces, 2 new stations)
```

So whenever the division comes out to a whole number with nothing left
over, subtract one extra. We'll come back to why this needs special
handling in code (floats don't divide as cleanly as you'd hope).

## Step 2 — now bring back the whole road

The whole road isn't one gap — it's several gaps in a row, and you
only have `k` stations to split between *all* of them. Directly
figuring out "put 2 stations here, 1 there, 2 over there" to get the
best possible outcome is genuinely hard to reason out directly.

So — same move as every other problem in this series — **stop trying
to compute the answer directly. Guess it, and check the guess.**

> "Suppose the answer is `X`. Could I actually make every gap's worst
> piece `<= X`, using `k` stations or fewer?"

If yes, maybe a smaller `X` also works — try to shrink it. If no, `X`
was too ambitious — try something bigger. That's a binary search — but
before jumping there, it's worth seeing the dumbest possible version of
"guess and check" first, since it makes the smarter version easier to
trust.

## The dumbest way to guess — brute force

Just try every candidate distance, starting small and working up, and
return the first one that fits within budget:

```python
def minimise_max_distance_brute(arr, k):
    max_gap = 0
    for i in range(len(arr) - 1):
        max_gap = max(max_gap, arr[i + 1] - arr[i])

    step = 1e-3       # how finely to scan candidates
    distance = step    # NOT 0.0 — see note below

    while distance <= max_gap:
        if number_of_gas_stations_required(arr, distance) <= k:
            return distance
        distance += step

    return max_gap
```

Two details worth calling out, because both are easy traps:

**Why `distance` starts at `step`, not `0.0`.** The feasibility check
divides by `distance` (`gap / distance`), so trying `distance = 0.0`
would crash with a `ZeroDivisionError`. Starting one step above zero
sidesteps this entirely.

**Why the step here (`1e-3`) is coarser than the binary search's
precision (`1e-6`) later on.** If this loop scanned in steps of
`0.000001`, checking a gap of size `12` would take 12 million
iterations — painfully slow for something that's meant to just
illustrate the idea. `1e-3` is fine enough to demonstrate the pattern
without taking forever. The binary search version doesn't have this
problem, because it never checks every candidate — it eliminates half
the remaining possibilities on every step instead.

This works, but it's obviously wasteful — checking thousands of
candidates one at a time when most of them tell you nothing you
couldn't infer from the last one. That's exactly the gap binary search
closes.

## The feasibility check — `number_of_gas_stations_required(arr, distance)`

This function answers exactly the guess above: "if every piece must be
at most `distance`, how many total stations does that require, across
every gap on the road?" Just apply Step 1's formula to each gap and
add up the costs.

```python
import math

def number_of_gas_stations_required(arr, distance):
    count = 0
    for i in range(len(arr) - 1):
        gap = arr[i + 1] - arr[i]
        stations = math.floor(gap / distance)

        # exact-division fix from Step 1's trap, explained below
        if math.isclose(gap, stations * distance, rel_tol=1e-12, abs_tol=1e-12):
            stations -= 1

        count += stations
    return count
```

**Why `math.isclose` instead of `gap == sections * dist`?**
Because `dist` is a decimal, and computers don't store decimals
perfectly — a division that's mathematically exact, like `6 / 2`, can
sometimes come out as `2.9999999999998` instead of a clean `3.0`.
A plain `==` check could wrongly say "not equal" even when the numbers
really should match. `math.isclose()` checks "close enough to count as
the same," which is the safe way to compare two floats.

## Search space

- `low = 0` — a distance can't be negative
- `high = the largest existing gap` — if you added zero stations
  (`k = 0`), the worst gap is just whatever the biggest one already
  is; adding stations can only shrink things from there, never grow them

## Binary search on the answer — why it looks a little different here

Every earlier problem in this series (book allocation, painters,
split-array) had a **whole-number** answer, so the loop could hop
between integers with `mid + 1` / `mid - 1`. Here the answer can be
`3.0`, or `1.8`, or `2.333...` — there's no "next" decimal after `mid`
the way there's a next integer after `5`. So instead of jumping between
discrete values, we just keep **shrinking the window** between `low`
and `high` until it's so small the difference no longer matters
(smaller than `0.000001`, say) and call that good enough.

```python
def minimise_max_distance(arr, k, epsilon=1e-6):
    low, high = 0.0, max_gap   # max_gap = the largest existing gap

    while high - low > epsilon:
        mid = (low + high) / 2
        if number_of_gas_stations_required(arr, mid) > k:
            low = mid    # too many stations needed — dist was too small, aim bigger
        else:
            high = mid   # feasible — try to find something even smaller

    return high
```

The *direction* of the logic is identical to every other minimize-the-
maximum problem in this series (`too many needed → grow the limit`,
`feasible → shrink the limit`) — only the mechanics of "shrink a window"
vs "jump between integers" differ.

### Dry run — binary search

```
arr = [1, 13, 17, 23] -> gaps: [12, 4, 6], k = 5
low = 0, high = 12

mid=6   -> stations needed: gap12->1, gap4->0, gap6->0 = 1   -> 1<=5  -> high=6
mid=3   -> stations needed: gap12->3, gap4->0, gap6->1 = 4   -> 4<=5  -> high=3
mid=1.5 -> stations needed: gap12->7, gap4->1, gap6->3 = 11  -> 11>5  -> low=1.5
...
window keeps shrinking around 3.0 until high - low < 1e-6

answer ≈ 3.0
```

## A completely different way to solve it — greedy with a heap

Binary search *guesses* a distance and checks it. This second approach
never guesses at all — it just directly attacks the single worst gap,
over and over, `k` times:

> Look at every gap right now. Find whichever one currently has the
> biggest piece. Drop one more station into *that* gap. Repeat.

This is greedy, and it happens to be provably correct here: the final
answer is always bottlenecked by whichever piece is currently the
largest, so improving anything else first would be wasted effort.

### Why we need a heap, and why the numbers get negated

To repeatedly ask "which gap currently has the biggest piece?"
efficiently, we use a **heap** — a data structure built to hand you
the smallest item, fast, every time you ask.

There's a catch: we want the *largest* piece, not the smallest, and
Python's `heapq` module only ever gives you the smallest. The standard
workaround: store every length as its **negative**. The most negative
number corresponds to the largest original number (`-12` is "more
negative", i.e. smaller, than `-4`), so asking the heap for "the
smallest" now correctly hands us "the largest gap" — we just remember
to flip the sign back with a `-` whenever we read a value out.

```python
import heapq

def minimise_max_distance_heap(arr, k):
    n = len(arr)
    how_many = [0] * (n - 1)   # how many stations we've placed in each gap so far

    # one entry per gap: (negative length, which gap this is)
    # the index travels alongside the length so that once we pop the
    # "biggest" gap off the heap, we still know WHICH gap it was
    pq = [(-(arr[i + 1] - arr[i]), i) for i in range(n - 1)]
    heapq.heapify(pq)

    for _ in range(k):
        neg_len, i = heapq.heappop(pq)   # pulls out whichever gap is currently worst
        how_many[i] += 1
        gap = arr[i + 1] - arr[i]        # the gap's ORIGINAL length
        new_len = gap / (how_many[i] + 1)  # its new worst piece, after this station
        heapq.heappush(pq, (-new_len, i))  # put it back so it competes fairly next round

    return -pq[0][0]   # peek at the biggest piece left, undo the negation
```

### Dry run — heap approach

```
arr = [1, 13, 17, 23] -> gaps [12, 4, 6], k = 5

station 1: worst=12 -> split gap0 into 2 -> piece=6   -> [6, 4, 6]
station 2: worst=6  -> split gap0 into 3 -> piece=4   -> [4, 4, 6]
station 3: worst=6  -> split gap2 into 2 -> piece=3   -> [4, 4, 3]
station 4: worst=4  -> split gap0 into 4 -> piece=3   -> [3, 4, 3]
station 5: worst=4  -> split gap1 into 2 -> piece=2   -> [3, 2, 3]

worst piece remaining = 3 -> answer = 3.0
```

Same final answer as binary search, arrived at completely differently
— one shrinks a window from the outside in, the other attacks the
worst spot from the inside out.

## Complexity

| Approach | Time | Space |
|---|---|---|
| Brute force (step through decimals) | `O(max_gap / step * n)` — fine for demos, impractical at real precision | `O(1)` |
| Heap (greedy) | `O(n log n + k log n)` | `O(n)` |
| Binary search on answer | `O(n log(max_gap / epsilon))` | `O(1)` |

## The one-paragraph version, if everything above was a lot

Guess a max allowed distance. Write a function that says how many new
stations that guess would cost. If it costs too many, your guess was
too small — try a bigger one. If it fits within budget, your guess
might be shrinkable — try a smaller one. Keep narrowing until the
window is tiny; that's your answer. That's the entire binary search
half of this problem — everything else (float comparisons, the exact-
division fix, the heap's negation trick) is implementation detail in
service of that one idea.

## Takeaway

Same "guess a value, count what it costs, compare to a budget" shape
as book allocation, painters, and split-array — the only genuinely new
idea is that the answer is continuous, so the search shrinks an
interval instead of hopping between integers. The heap approach solves
the identical problem with a totally different tool: instead of
guessing the final answer, it greedily fixes whatever's currently worst
until it runs out of stations. Both are worth knowing — binary search
generalizes better to problems where "guess and check" is easy but
"attack the worst thing directly" isn't obviously safe; greedy is
often simpler to write when, like here, you can prove attacking the
worst spot first is never a mistake.