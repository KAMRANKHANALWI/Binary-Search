# Capacity to Ship Packages Within D Days

**Pattern:** Binary Search on Answer

## Problem

`weights[i]` is the weight of the i-th package. Packages must ship in
the given order, and you have `days` days to ship them all. Each day
the ship carries packages up to some fixed `capacity`. Find the
minimum capacity that gets everything shipped within `days` days.

```
weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
days = 5
answer = 15
```

## Why binary search on the answer

We're searching over possible **capacities**, not elements of
`weights`.

- smaller capacity → fewer packages fit per day → more days needed
- bigger capacity → more packages fit per day → fewer days needed

So as capacity increases, days-required only ever decreases (or stays
the same) — monotonic:

```
capacity:        10    11    ...   14    15    16 ...
days needed:      6     6     ...   6     5     5 ...
feasible (<=5):  False False ...  False True  True ...
                                          ^
                                    first True — this is the answer
```

We want the first capacity where `days_required(capacity) <= days`.

## Feasibility check — `days_required(weights, capacity)`

Greedily load the current day as much as possible. Once the next
package would overflow the capacity, start a new day.

```python
def days_required(weights, capacity):
    days = 1
    load = 0
    for weight in weights:
        if load + weight > capacity:
            days += 1
            load = weight
        else:
            load += weight
    return days
```

`O(n)` per call. Note this returns a day *count*, not a `True`/`False` —
the binary search compares it against `days` itself.

## Search space

- `low = max(weights)` — capacity can never be smaller than the
  heaviest single package, or that package could never ship
- `high = sum(weights)` — a ship that can carry everything at once
  finishes in exactly 1 day

Standard "find leftmost True" binary search, using `ans` to track the
best capacity found so far:

```python
ans = high  # sum(weights) always works (ships everything in 1 day)

while low <= high:
    mid = (low + high) // 2
    if days_required(weights, mid) <= days:
        ans = mid        # mid works, record it
        high = mid - 1   # but keep looking for something smaller
    else:
        low = mid + 1    # mid too small, need more capacity

return ans
```

`ans` gets overwritten every time a capacity works, so it always holds
the *smallest* capacity seen that still finishes within `days` days.

## Dry run

```
weights = [1..10], days = 5
search space: [10, 55]

mid=32 -> loads: [1..7]=28, [8,9,10]=27      -> 2 days  -> 2<=5  True  -> ans=32, high=31
...
mid=15 -> loads: [1..5]=15, [6,7]=13, 8, 9, 10 -> 5 days -> 5<=5  True  -> ans=15, high=14
mid=14 -> would need 6 days                    -> 6<=5  False -> low=15

loop ends (low=15 > high=14) -> ans = 15
```

## Complexity

| | |
|---|---|
| Time | `O(n log(sum(weights) - max(weights)))` |
| Space | `O(1)` |

## Takeaway

Rephrase "what's the minimum capacity?" as "can capacity `C` finish
shipping within `days` days?" — a yes/no question that flips exactly
once as `C` grows. Binary search finds that flip point directly instead
of testing every capacity from `max(weights)` up.