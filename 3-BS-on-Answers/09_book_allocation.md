# Book Allocation

**Pattern:** Binary Search on Answer — Minimize the Maximum

## Problem

`arr[i]` is the number of pages in the i-th book. Allocate all books to
`m` students such that:

- every student gets at least one book
- every book goes to exactly one student
- books are allocated in **contiguous** order (no skipping around)

Minimize the maximum number of pages any single student ends up with.
Return `-1` if allocation isn't possible (more students than books).

```
arr = [25, 46, 28, 49, 24]
m = 4
answer = 71
```

## Recognizing the pattern

This is the same shape as [[ship-within-days]] wearing a different
costume — "minimize the maximum" instead of "minimize the capacity",
but the mechanics are identical: guess a page limit, greedily count
how many students it takes, adjust.

## Why binary search on the answer

- smaller page limit → each student can hold fewer pages → more
  students needed
- bigger page limit → each student can hold more pages → fewer
  students needed

So as the limit increases, students-required only ever decreases —
monotonic:

```
limit:            49  ...  70   71   72 ...
students needed:   5  ...   5    4    4 ...
feasible (<=m=4): False ... False True True ...
                                   ^
                             first True — this is the answer
```

We want the first limit where `students_required(limit) <= m`.

## Brute force

Reuse the exact same feasibility check the binary search will use
(`students_required`, defined below) — just call it on **every**
possible limit from `low` to `high` instead of jumping straight to the
answer with binary search. The first limit that works is the answer,
since feasibility only turns `True` once and stays `True`.

```python
def brute_force(arr, m):
    n = len(arr)
    if m > n:
        return -1

    low, high = max(arr), sum(arr)
    for limit in range(low, high + 1):
        if students_required(arr, limit) <= m:
            return limit
    return -1
```

`O((sum(arr) - max(arr)) * n)` — checks every limit in the range, each
check costing `O(n)`. Correct, but binary search gets to the same
answer in `O(n log(sum(arr)))` by skipping most of that range.

*(A different, more combinatorial brute force also exists for this
problem — recursively trying every way to split the array into `m`
contiguous groups, `C(n-1, m-1)` ways total. It works but doesn't reuse
`students_required`, so it's left out here in favor of the version
above that shares the same feasibility logic as the optimal solution.)*

```python
def brute_force_combinatorial(arr, m):
    n = len(arr)
    if m > n:
        return -1

    def solve(index, students, current_max):
        # Last student gets all remaining books
        if students == 1:
            return max(current_max, sum(arr[index:]))

        pages, answer = 0, float("inf")

        # Try every possible split point for the current student
        for i in range(index, n - students + 1):
            pages += arr[i]
            new_max = max(current_max, pages)
            answer = min(answer, solve(i + 1, students - 1, new_max))

        return answer

    return solve(0, m, 0)
```

Tries every partition, keeps the best one. `O(C(n-1, m-1) * n)` time
and `O(n)` recursion depth — combinatorial, which is why it's kept out
of `solution.py` in favor of the linear-scan version above.

## Feasibility check — `students_required(arr, limit)`

Greedily load the current student with books until the next one would
exceed `limit`, then move to a new student.

```python
def students_required(arr, limit):
    students = 1
    pages_used = 0

    for pages in arr:
        if pages_used + pages <= limit:
            pages_used += pages
        else:
            students += 1
            pages_used = pages

    return students
```

`O(n)` per call. Note this returns a *count*, same as
`days_required()` in ship-within-days — the binary search compares it
against `m` directly rather than getting a `True`/`False` back.

## Search space

- `low = max(arr)` — no student can take less than the single biggest
  book; the limit can't be smaller than that or the biggest book has
  nowhere to go
- `high = sum(arr)` — one student could carry every book

## Optimal — binary search

```python
def find_pages(arr, m):
    n = len(arr)
    if m > n:
        return -1

    low, high = max(arr), sum(arr)
    ans = high  # sum(arr) always works: one student takes everything

    while low <= high:
        mid = (low + high) // 2
        if students_required(arr, mid) <= m:
            ans = mid        # mid works, record it
            high = mid - 1   # but keep looking for something smaller
        else:
            low = mid + 1    # mid too small, need a bigger limit

    return ans
```

`ans` gets overwritten every time a limit works, and because we search
*left* after a hit, each overwrite is smaller than the last — so by the
end `ans` holds the smallest feasible page limit.

## Dry run

```
arr = [25, 46, 28, 49, 24], m = 4
low=49, high=172

mid=110 -> students needed: [99, 73]           -> 2 -> 2<=4 True  -> ans=110, high=109
...
mid=71  -> students needed: [71, 28, 49, 24]   -> 4 -> 4<=4 True  -> ans=71,  high=70
mid=70  -> students needed: [25,46,28,49,24] each own -> 5 -> 5<=4 False -> low=71

loop ends (low=71 > high=70) -> ans = 71
```

## Complexity

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan) | `O((sum(arr) - max(arr)) * n)` | `O(1)` |
| Optimal (binary search) | `O(n log(sum(arr)))` | `O(1)` |

## Takeaway

"Minimize the maximum pages" is really "what's the smallest limit that
still only needs `m` students?" — a yes/no question that flips exactly
once as the limit grows. Same template as bouquets, ship capacity, and
smallest divisor: guess a value, write a greedy feasibility check, binary
search for the flip point.