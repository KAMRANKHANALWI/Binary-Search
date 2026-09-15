# Smallest Divisor Given a Threshold

**Pattern:** Binary Search on Answer

## Problem

Given an array of positive integers and a `threshold`, find the smallest
positive integer `divisor` such that:

```
sum(ceil(arr[i] / divisor) for each i) <= threshold
```

```
arr = [1, 2, 5, 9]
threshold = 6
answer = 5
```

## Why binary search on the answer

We're searching over possible **divisors**, not elements of `arr`.

- smaller divisor → each `arr[i] / divisor` is bigger → sum is bigger
- larger divisor → each `arr[i] / divisor` is smaller → sum is smaller

So as the divisor increases, the sum only ever decreases (or stays the
same) — monotonic. That gives a search space like:

```
divisor:    1     2     3     4     5 ...
feasible:  False False False False True ...
                                    ^
                              first True — this is the answer
```

We need the first divisor where `sum <= threshold` holds.

## Feasibility check — `possible(arr, divisor, threshold)`

For each `x` in `arr`, add `ceil(x / divisor)` to a running total. In
integer arithmetic, `ceil(x / d) == (x + d - 1) // d` — no need for
`math.ceil` or floats.

Bail out early the moment the running total exceeds `threshold`; no
point in finishing the loop.

```python
def possible(arr, divisor, threshold):
    total = 0
    for x in arr:
        total += (x + divisor - 1) // divisor
        if total > threshold:
            return False
    return True
```

`O(n)` per call, with an early exit.

## Search space

- `low = 1` — smallest divisor gives the largest possible sum
- `high = max(arr)` — once the divisor is at least `max(arr)`, every
  `ceil(arr[i] / divisor)` is `1`, so the sum is just `len(arr)`

Standard "find leftmost True" binary search:

```python
ans = high  # max(arr) always works, so it's a safe fallback
while low <= high:
    mid = (low + high) // 2
    if possible(arr, mid, threshold):
        ans = mid         # mid works, record it
        high = mid - 1    # but keep looking for something smaller
    else:
        low = mid + 1     # mid too small, need a bigger divisor
return ans
```

`ans` gets overwritten every time we find a divisor that works, so it
always holds the *smallest* working divisor seen so far — by the end,
that's the answer.

Note there's no impossibility check here — unlike bouquets, there's
always *some* divisor that works (`max(arr)` always keeps the sum at
`len(arr)`), so as long as `threshold >= len(arr)` a valid answer
exists. The problem guarantees this.

## Dry run

```
arr = [1, 2, 5, 9], threshold = 6

search space: [1, 9]

mid=5 -> ceil: 1,1,1,2 -> sum=5  -> 5<=6  -> True  -> high=4
mid=2 -> ceil: 1,1,3,5 -> sum=10 -> 10>6  -> False -> low=3
mid=3 -> ceil: 1,1,2,3 -> sum=7  -> 7>6   -> False -> low=4
mid=4 -> ceil: 1,1,2,3 -> sum=7  -> 7>6   -> False -> low=5

loop ends (low=5 > high=4) -> ans = 5
```

## Complexity

| | |
|---|---|
| Time | `O(n log(max(arr)))` |
| Space | `O(1)` |

## Takeaway

Rephrase "what's the smallest divisor?" as "does this divisor keep the
sum under the threshold?" — a yes/no question that flips exactly once
as the divisor grows. Binary search finds that flip point directly
instead of trying every divisor from 1 up.