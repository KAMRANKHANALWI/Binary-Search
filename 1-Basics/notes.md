# Binary Search — Basics

## Core Idea

Binary Search works on a **sorted search space**.

```text
Compare → Eliminate half → Repeat
```

---

## Iterative Pattern

```python
low = 0
high = len(arr) - 1

while low <= high:
    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

return -1
```

---

## Recursive Pattern

```python
def binary_search(arr, low, high, target):

    if low > high:
        return -1

    mid = low + (high - low) // 2

    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search(arr, mid + 1, high, target)
    else:
        return binary_search(arr, low, mid - 1, target)
```

---

## Key Rules

| Condition            | Action       |
| -------------------- | ------------ |
| `arr[mid] == target` | Found        |
| `arr[mid] < target`  | Search right |
| `arr[mid] > target`  | Search left  |

```text
Right half → low = mid + 1
Left half  → high = mid - 1
```

### Mid

```python
mid = low + (high - low) // 2
```

---

## Complexity

| Approach                  |       Time |      Space |
| ------------------------- | ---------: | ---------: |
| Linear Search             |     `O(n)` |     `O(1)` |
| Binary Search — Iterative | `O(log n)` |     `O(1)` |
| Binary Search — Recursive | `O(log n)` | `O(log n)` |

---

## Must Remember

- Binary Search requires a **sorted** search space.
- `low` and `high` define the current search space.
- `low <= high` keeps the last element searchable.
- `low > high` means the search space is empty.
- Iterative → repetition using a loop.
- Recursive → repetition using function calls.
- The **search logic is the same** in both approaches.
