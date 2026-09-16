# Split Array Largest Sum

**Pattern:** Binary Search on Answer — Minimize the Maximum

## Same skeleton as Book Allocation

This is [[book-allocation]] wearing different clothes — literally the
same algorithm, just renamed:

| | Book Allocation | Split Array Largest Sum |
|---|---|---|
| Dividing | pages | array elements |
| Into | students | `k` subarrays |
| Helper name | `students_required` | `count_subarrays` |

If you've internalized one, you've internalized both. This file keeps
the explanation short and points back to book-allocation for the full
derivation.

## Problem

Split `arr` into `k` non-empty **contiguous** subarrays. Minimize the
largest sum among those subarrays.

```
arr = [10, 20, 30, 40]
k = 2
answer = 60   # split as [10, 20, 30] | [40] -> max(60, 40) = 60
```

## Feasibility check — `count_subarrays(arr, max_sum)`

Greedily keep adding elements to the current subarray until the next
one would push it over `max_sum`, then start a new subarray.

```python
def count_subarrays(arr, max_sum):
    subarrays = 1
    current_sum = 0

    for num in arr:
        if current_sum + num <= max_sum:
            current_sum += num
        else:
            subarrays += 1
            current_sum = num

    return subarrays
```

## Search space

- `low = max(arr)` — no subarray can hold less than the single
  biggest element
- `high = sum(arr)` — one subarray could hold everything (`k = 1`)

## Brute force

Linear scan over every possible `max_sum`, reusing `count_subarrays` —
same idea as book-allocation's brute force.

```python
def brute_force(arr, k):
    if k > len(arr):
        return -1

    low, high = max(arr), sum(arr)
    for max_sum in range(low, high + 1):
        if count_subarrays(arr, max_sum) <= k:
            return max_sum
    return -1
```

## Optimal — binary search

```python
def split_array(arr, k):
    if k > len(arr):
        return -1

    low, high = max(arr), sum(arr)
    ans = high  # sum(arr) always works: one subarray, k=1

    while low <= high:
        mid = (low + high) // 2
        if count_subarrays(arr, mid) <= k:
            ans = mid       # mid works, record it
            high = mid - 1  # keep looking for something smaller
        else:
            low = mid + 1   # too small, need a bigger max_sum

    return ans
```

## Dry run

```
arr = [10, 20, 30, 40], k = 2
low=40, high=100

mid=70 -> subarrays: [10,20,30]=60, [40]=40   -> 2 -> 2<=2 True  -> ans=70, high=69
mid=54 -> subarrays: [10,20]=30, [30], [40]   -> 3 -> 3<=2 False -> low=55
mid=62 -> subarrays: [10,20,30]=60, [40]=40   -> 2 -> 2<=2 True  -> ans=60, high=61
mid=60 -> subarrays: [10,20,30]=60, [40]=40   -> 2 -> 2<=2 True  -> ans=60, high=59
mid=59 -> subarrays: [10,20]=30, [30]=30, [40] -> 3 -> 3<=2 False -> low=60

loop ends (low=60 > high=59) -> ans = 60
```

## Complexity

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan) | `O((sum(arr) - max(arr)) * n)` | `O(1)` |
| Optimal (binary search) | `O(n log(sum(arr)))` | `O(1)` |

## Takeaway

Whenever a problem says "divide a contiguous array/sequence into `k`
groups, minimize the maximum group total" — it's this same template:
`low = max(arr)`, `high = sum(arr)`, greedy group-counter, binary
search for the smallest feasible limit. Only the variable names change.