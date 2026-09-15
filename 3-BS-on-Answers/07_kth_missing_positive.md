# Kth Missing Positive Number

**Pattern:** Binary Search on Index (not on a value/answer directly)

## Problem

Given a **sorted** array of positive integers `arr` and an integer `k`,
find the k-th positive integer missing from `arr`.

```
arr = [2, 3, 4, 7, 11]
k = 5
```

All positive integers, with what's present ticked off:

```
1  2  3  4  5  6  7  8  9  10  11
   ✓  ✓  ✓     ✓  ✓     ✓   ✓
```

Missing, in order: `1, 5, 6, 8, 9, 10, ...` → the 5th one is `9`.

## The one formula everything is built on

At index `i`, if nothing were missing, `arr[i]` would just equal
`i + 1` (1st element is `1`, 2nd is `2`, etc.). Whatever it's short by
is exactly how many positive integers have gone missing *up to and
including* `arr[i]`:

```python
missing_at(i) = arr[i] - (i + 1)
```

Check it against the example — at `i = 3`, `arr[3] = 7`:

```
missing = 7 - (3 + 1) = 3
```

And indeed `1, 5, 6` are the 3 numbers missing before we reach `7`.
Every other idea in this problem is just this formula, reused.

## Brute force

Walk up from `1`, and for every number not found in `arr`, count it.
Stop when the count hits `k`.

```python
def brute_force(arr, k):
    missing_count = 0
    number = 1
    while True:
        if number not in arr:
            missing_count += 1
        if missing_count == k:
            return number
        number += 1
```

`number not in arr` is an `O(n)` scan every time, so worst case this is
roughly `O(n * answer)`. Correct, but slow.

## Better — linear scan with the formula

Instead of testing numbers one at a time, walk the array itself and
ask, at each index: "have we passed `k` missing numbers yet?"

```python
def better(arr, k):
    for i in range(len(arr)):
        missing = arr[i] - (i + 1)
        if missing >= k:
            return k + i
        # else: the kth missing number is still further ahead
    return k + len(arr)   # kth missing number is past the whole array
```

`O(n)` — one pass, no membership checks. The `k + i` return is the same
derivation worked out below for the binary search version, just
applied the moment we find the right index instead of after a search.

## Why binary search works here

Because `arr` is sorted, `missing_at(i)` can only stay the same or grow
as `i` increases — it's monotonic:

```
index:     0  1  2  3  4
arr:       2  3  4  7  11
missing:   1  1  1  3   6
                      ↑
              first index where missing >= k (k=5)
```

We're not searching for a *value* here — we're searching for the first
**index** where `missing_at(i) >= k`. Same "find the flip point" shape
as every other binary-search-on-answer problem, just applied to array
indices instead of days/capacity/divisors.

## Optimal — binary search

```python
def optimal(arr, k):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        missing = arr[mid] - (mid + 1)

        if missing < k:
            low = mid + 1   # not enough missing yet, look right
        else:
            high = mid - 1  # already enough (or more), look left

    return low + k
```

`O(log n)`.

## Where does `low + k` come from?

This is the only non-obvious line in the whole problem, so it's worth
deriving instead of memorizing.

When the loop ends, `high` is the last index where `missing < k` (not
enough missing numbers yet). The answer must sit somewhere after
`arr[high]`. Specifically, we need `more` additional missing numbers
past `arr[high]`:

```
more = k - missing_at(high)
```

Since positive integers past `arr[high]` are missing one after another
with nothing else in the way (by definition — `arr[high]` was the *last*
point where we hadn't reached `k` missing yet), the answer is simply:

```
answer = arr[high] + more
       = arr[high] + k - missing_at(high)
       = arr[high] + k - (arr[high] - (high + 1))
       = k + high + 1
```

`arr[high]` cancels out completely. And since the loop always ends with
`low == high + 1`, that's the same as:

```
answer = k + low
```

So `return low + k` isn't a magic formula — it's `arr[high] + more`
with the algebra worked through until `arr[high]` disappears.

## Dry run

```
arr = [2, 3, 4, 7, 11], k = 5
low=0, high=4

mid=2 -> arr[2]=4  -> missing=4-3=1 -> 1<5  -> low=3
mid=3 -> arr[3]=7  -> missing=7-4=3 -> 3<5  -> low=4
mid=4 -> arr[4]=11 -> missing=11-5=6 -> 6>=5 -> high=3

loop ends (low=4, high=3) -> answer = low + k = 4 + 5 = 9
```

## Complexity

| Approach | Time | Space |
|---|---|---|
| Brute force | ~`O(n * answer)` | `O(1)` |
| Better (linear) | `O(n)` | `O(1)` |
| Optimal (binary search) | `O(log n)` | `O(1)` |

## Takeaway

`missing = arr[i] - (i + 1)` measures the gap between where a value
*should* be and where it *is* — and since the array is sorted, that gap
only ever grows. Once you see a monotonically growing quantity, binary
search for the first index that crosses `k`, then translate "index" back
into "missing count" with one line of algebra (`arr[high] + more`) — the
`arr[high]` term always cancels itself out.