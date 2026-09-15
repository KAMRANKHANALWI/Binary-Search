# Aggressive Cows

**Pattern:** Binary Search on Answer — *Maximize the Minimum*

## Problem

Given stall positions `stalls[]` and `k` cows, place all `k` cows in
stalls such that the **minimum distance between any two cows is as
large as possible**. Return that maximum possible minimum distance.

```
stalls = [0, 3, 4, 7, 9, 10]
cows = 4
answer = 3   # e.g. cows at 0, 3, 7, 10 -> gaps of 3, 4, 3
```

## What's different about this one

The last few problems (bouquets, ship capacity, smallest divisor) were
all **minimize** problems: find the smallest value where `possible()`
first turns `True`.

This one **flips direction** — we want the *largest* value where
`possible()` is still `True`:

```
distance:    1     2     3     4     5 ...
feasible:  True  True  True  False False ...
                        ^
                  last True — this is the answer
```

Same overall shape (a monotonic boolean line, binary search finds the
flip point) — just searching for the *last* `True` instead of the
*first* one, so the movement on a hit is reversed: instead of
`high = mid - 1` (look for something smaller), we do
`low = mid + 1` (look for something bigger).

## Why it's monotonic

If `k` cows can all be placed at least `dist` apart, they can
certainly all be placed at least `dist - 1` apart too (looser
requirement). And if `dist` is *too* far apart to fit `k` cows, no
larger distance will fit them either. That one-directional relationship
is what makes binary search valid here.

## Feasibility check — `can_place(stalls, dist, cows)`

Sort the stalls first. Then greedily place each cow at the **earliest**
stall that's at least `dist` away from the last placed cow — placing
cows as early as possible always leaves the most room for the
remaining ones, so greedy is safe here.

```python
def can_place(stalls, dist, cows):
    count = 1
    last = stalls[0]  # first cow always goes in the first stall

    for i in range(1, len(stalls)):
        if stalls[i] - last >= dist:
            count += 1
            last = stalls[i]
        if count >= cows:
            return True

    return False
```

`O(n)` per call.

## Search space

- `low = 1` — the smallest distance worth checking
- `high = stalls[-1] - stalls[0]` — you can never do better than
  putting the two extreme cows at the two extreme stalls

## Optimal — binary search (maximize variant)

```python
def aggressive_cows(stalls, cows):
    stalls.sort()
    low, high = 1, stalls[-1] - stalls[0]
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        if can_place(stalls, mid, cows):
            ans = mid       # mid works, record it
            low = mid + 1   # but keep looking for something bigger
        else:
            high = mid - 1  # mid too far apart, need a smaller distance

    return ans
```

`ans` gets overwritten every time a distance works, and because we keep
searching *right* after a hit, each overwrite is bigger than the last —
so by the end `ans` holds the largest feasible distance. (Same idea as
`return high` in the maximize case — `ans` just makes it explicit
instead of relying on `high` landing there when the loop exits.)

## Dry run

```
stalls = [0, 3, 4, 7, 9, 10] (sorted), cows = 4
low=1, high=10

mid=5 -> 0->7 only, 3rd cow fails      -> False -> high=4
mid=2 -> 0->3->7->9  (4 cows)          -> True  -> ans=2, low=3
mid=3 -> 0->3->7->10 (4 cows)          -> True  -> ans=3, low=4
mid=4 -> 0->4->9 only 3 cows           -> False -> high=3

loop ends (low=4 > high=3) -> ans = 3
```

## Complexity

| | |
|---|---|
| Time | `O(n log n)` sort + `O(n log(max(stalls) - min(stalls)))` search |
| Space | `O(1)` auxiliary |

## Takeaway

Same "guess an answer, check feasibility, eliminate half" idea as
every other binary-search-on-answer problem — the only real difference
here is which half you keep. Minimize problems keep the *left* half on
a hit (`high = mid - 1`, chasing the first `True`); maximize problems
keep the *right* half on a hit (`low = mid + 1`, chasing the last
`True`). Everything else — the monotonic boolean line, the `ans`
tracking variable, the overall template — stays identical.