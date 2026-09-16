# Painter's Partition

**Pattern:** Binary Search on Answer — Minimize the Maximum

## Same skeleton as Book Allocation / Split Array

Third costume for the same algorithm — see [[book-allocation]] for the
full derivation. Here:

| | Book Allocation | Painter's Partition |
|---|---|---|
| Dividing | pages | boards (by length) |
| Into | students | `k` painters |
| Helper name | `students_required` | `count_painters` |

## Problem

`boards[i]` is the length of the i-th board. Assign contiguous boards
to `k` painters (each painter paints in unit time per unit length, so
"time" and "board length" are interchangeable here). Minimize the
maximum amount of work any single painter is assigned.

```
boards = [10, 20, 30, 40]
k = 2
answer = 60   # [10, 20, 30] | [40] -> max(60, 40) = 60
```

## Feasibility check — `count_painters(boards, max_work)`

Same greedy loading pattern as every problem in this family: keep
adding boards to the current painter until the next one would exceed
`max_work`, then start a new painter.

```python
def count_painters(boards, max_work):
    painters = 1
    current_work = 0

    for board in boards:
        if current_work + board <= max_work:
            current_work += board
        else:
            painters += 1
            current_work = board

    return painters
```

## Search space

- `low = max(boards)` — no painter can take on less than the single
  longest board
- `high = sum(boards)` — one painter could do every board (`k = 1`)

## Brute force

Linear scan over every possible `max_work`, reusing `count_painters`.

```python
def brute_force(boards, k):
    if k > len(boards):
        return -1

    low, high = max(boards), sum(boards)
    for max_work in range(low, high + 1):
        if count_painters(boards, max_work) <= k:
            return max_work
    return -1
```

## Optimal — binary search

```python
def painters_partition(boards, k):
    if k > len(boards):
        return -1

    low, high = max(boards), sum(boards)
    ans = high  # sum(boards) always works: one painter, k=1

    while low <= high:
        mid = (low + high) // 2
        if count_painters(boards, mid) <= k:
            ans = mid       # mid works, record it
            high = mid - 1  # keep looking for something smaller
        else:
            low = mid + 1   # too small, need more capacity per painter

    return ans
```

## Dry run

```
boards = [10, 20, 30, 40], k = 2
low=40, high=100

mid=70 -> painters: [10,20,30]=60, [40]=40 -> 2 -> 2<=2 True  -> ans=70, high=69
mid=54 -> painters: [10,20]=30, [30], [40] -> 3 -> 3<=2 False -> low=55
mid=62 -> painters: [10,20,30]=60, [40]=40 -> 2 -> 2<=2 True  -> ans=60, high=61
mid=60 -> painters: [10,20,30]=60, [40]=40 -> 2 -> 2<=2 True  -> ans=60, high=59
mid=59 -> painters: [10,20]=30, [30], [40] -> 3 -> 3<=2 False -> low=60

loop ends (low=60 > high=59) -> ans = 60
```

Identical arithmetic to split-array-largest-sum — same array, same
`k`, same everything except the label on the numbers.

## Complexity

| Approach | Time | Space |
|---|---|---|
| Brute force (linear scan) | `O((sum(boards) - max(boards)) * n)` | `O(1)` |
| Optimal (binary search) | `O(n log(sum(boards)))` | `O(1)` |

## Takeaway

By this third variant, the recognition should be instant: "divide a
contiguous sequence into `k` groups, minimize the maximum group total"
→ `low = max(arr)`, `high = sum(arr)`, greedy group-counter, binary
search for the smallest feasible limit. Book pages, array sums, board
lengths — all the same problem underneath.