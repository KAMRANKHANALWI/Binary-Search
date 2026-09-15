# Minimum Days to Make M Bouquets

**Pattern:** Binary Search on Answer

## Problem

`arr[i]` is the day flower `i` blooms. A bouquet needs exactly `k`
**adjacent** bloomed flowers. Find the minimum day by which you can make
at least `m` bouquets, or `-1` if it's impossible.

```
arr = [1, 10, 3, 10, 2]
m = 3, k = 1
answer = 3
```

## Why binary search on the answer

We're not searching for a value *in* `arr` — we're searching over the
space of possible **days**, looking for the earliest one that works.

The feasibility function is monotonic:

```
day:        1     2     3     4     5 ...
feasible:  False False True  True  True ...
                        ^
                  first True — this is the answer
```

If `m` bouquets are possible on day `D`, they're also possible on every
day after `D` (more flowers only ever bloom, never un-bloom). That
monotonicity is what makes binary search valid here.

## Feasibility check — `possible(arr, day, m, k)`

Scan `arr` once, tracking a run of adjacent bloomed flowers:

- `arr[i] <= day` → flower has bloomed → extend the current run
- `arr[i] > day` → run breaks → `bouquets += run // k`, reset run to 0

Don't forget to flush the final run after the loop.

```python
def possible(arr, day, m, k):
    run = 0
    bouquets = 0
    for bloom_day in arr:
        if bloom_day <= day:
            run += 1
        else:
            bouquets += run // k
            run = 0
    bouquets += run // k
    return bouquets >= m
```

`O(n)` per call.

## Impossibility check

Each bouquet costs `k` flowers, so `m` bouquets cost `m * k` flowers
total. If that exceeds `len(arr)`, no day will ever work — bail out
before searching:

```python
if m * k > len(arr):
    return -1
```

## Search space

- `low  = min(arr)` — nothing has bloomed before this
- `high = max(arr)` — everything has bloomed by this

Standard "find leftmost True" binary search:

```python
ans = -1
while low <= high:
    mid = (low + high) // 2
    if possible(arr, mid, m, k):
        ans = mid         # mid works, record it
        high = mid - 1    # but keep looking for something earlier
    else:
        low = mid + 1     # mid doesn't work, need more time
return ans
```

`ans` starts at `-1` and gets overwritten every time we find a working
day, so by the end it holds the *earliest* working day we saw — no
need to reason about what `low` equals when the loop exits.

## Dry run

```
arr = [1, 10, 3, 10, 2], m = 3, k = 1

search space: [1, 10]

mid=5 -> bloomed {1,3,2} -> 3 bouquets -> True  -> high=4
mid=2 -> bloomed {1,2}   -> 2 bouquets -> False -> low=3
mid=3 -> bloomed {1,3,2} -> 3 bouquets -> True  -> high=2

loop ends (low=3 > high=2) -> ans = 3
```

## Complexity

| | |
|---|---|
| Time | `O(n log(max(arr) - min(arr)))` |
| Space | `O(1)` |

## Takeaway

Rephrase "what's the minimum day?" as "can I hit `m` bouquets by day
`D`?" — a yes/no question with a monotonic answer over `D`. Binary
search then finds the flip point directly instead of scanning every
day.