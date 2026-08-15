# Binary Search — Pattern Cheat Sheet

Binary Search is not limited to searching for an element in a sorted array.

The broader idea is:

> **Find a boundary in a search space where the answer changes monotonically.**

---

## 1. Core Binary Search

### When to Think Binary Search

Look for:

* Sorted data
* A search space where half can be eliminated
* A monotonic condition
* A minimum / maximum valid answer

### Basic Search Space

```text
low                         high
 ↓                            ↓
[  .  .  .  .  .  .  .  .  .  ]
              ↑
            mid
```

### Standard Formula

```python
mid = low + (high - low) // 2
```

Prefer this over:

```python
mid = (low + high) // 2
```

because the first form avoids integer overflow in languages where integers have fixed limits.

---

# 2. Standard Binary Search

### Goal

Find whether a target exists in a sorted array.

```text
[1, 3, 5, 7, 9, 11, 13]
          ↑
         mid
```

Compare:

```text
target == arr[mid]
target <  arr[mid]
target >  arr[mid]
```

### Decision

```text
target == mid
    → found

target < mid
    → search left

target > mid
    → search right
```

### Pattern

```text
Sorted Array
     ↓
Compare with mid
     ↓
Eliminate half
     ↓
Repeat
```

---

# 3. Lower Bound

### Definition

Find the **first index** where:

```text
arr[index] >= target
```

Example:

```text
arr = [1, 2, 4, 4, 4, 7, 9]
target = 4

Answer = 2

             ↓
[1, 2, 4, 4, 4, 7, 9]
       ↑
   first >= 4
```

### Mental Model

```text
< target       >= target
───────────── | ─────────────
              ↑
          lower_bound
```

### Pattern

When you need:

> **First position satisfying a condition**

think:

```text
Lower Bound
```

---

# 4. Upper Bound

### Definition

Find the **first index** where:

```text
arr[index] > target
```

Example:

```text
arr = [1, 2, 4, 4, 4, 7, 9]
target = 4

Answer = 5

             ↓
[1, 2, 4, 4, 4, 7, 9]
                ↑
             first > 4
```

### Mental Model

```text
<= target       > target
───────────── | ─────────
              ↑
          upper_bound
```

### Quick Difference

```text
Lower Bound → first >= target

Upper Bound → first >  target
```

---

# 5. First / Last Occurrence

For a sorted array containing duplicates:

```text
[1, 2, 2, 2, 2, 5, 7]
    ↑           ↑
  first        last
```

### First Occurrence

Find:

```text
first index where arr[i] == target
```

Equivalent idea:

```text
lower_bound(target)
```

Then verify that the returned index actually contains the target.

### Last Occurrence

Can be found using:

```text
upper_bound(target) - 1
```

Again, verify the result.

### Pattern

```text
Duplicates + sorted array
        ↓
Boundary Search
        ↓
Lower / Upper Bound
```

---

# 6. Count Occurrences

For a sorted array:

```text
count = last_index - first_index + 1
```

Using bounds:

```text
first = lower_bound(target)
last  = upper_bound(target) - 1

count = last - first + 1
```

Or directly:

```text
count = upper_bound(target) - lower_bound(target)
```

provided the target exists.

---

# 7. Floor and Ceil

For a sorted array:

### Floor

Largest value:

```text
<= target
```

### Ceil

Smallest value:

```text
>= target
```

Example:

```text
arr = [1, 3, 5, 7]
target = 6

floor = 5
ceil  = 7
```

### Mental Model

```text
Floor
    → move right while still valid

Ceil
    → move left while still valid
```

This is fundamentally another **boundary-search problem**.

---

# 8. Rotated Sorted Array

Example:

```text
Original:

[1, 2, 3, 4, 5, 6, 7]

Rotated:

[4, 5, 6, 7, 1, 2, 3]
```

The key observation:

> **At least one half of the current search space is always sorted.**

```text
[4, 5, 6, 7 | 1, 2, 3]
  sorted       sorted
```

At every iteration:

1. Find `mid`
2. Identify which half is sorted
3. Check whether target lies inside that sorted half
4. Search there if yes
5. Otherwise search the other half

### Pattern

```text
Rotated Sorted Array
        ↓
One half is always sorted
        ↓
Identify sorted half
        ↓
Check target range
        ↓
Eliminate one half
```

---

# 9. Rotated Sorted Array With Duplicates

Duplicates create ambiguity.

Example:

```text
[2, 2, 2, 3, 2, 2]
 ↑        ↑
low      high
```

Sometimes:

```text
arr[low] == arr[mid] == arr[high]
```

We cannot determine which half is sorted.

### Solution

Shrink the search space:

```python
low += 1
high -= 1
```

### Important

This is why the duplicate version can degrade to:

```text
O(n)
```

in the worst case.

---

# 10. Minimum in Rotated Sorted Array

Example:

```text
[4, 5, 6, 7, 1, 2, 3]
             ↑
          minimum
```

### Key Observation

The minimum is the point where the sorted order "wraps."

Compare:

```text
arr[mid] > arr[high]
```

If true:

```text
minimum is to the right
```

Otherwise:

```text
minimum is at mid or to the left
```

### Pattern

```text
Rotated sorted array
        ↓
Find sorted / unsorted side
        ↓
Determine where minimum can exist
        ↓
Shrink search space
```

---

# 11. Number of Rotations

For a rotated sorted array:

> **Number of rotations = index of the minimum element**

Example:

```text
[4, 5, 6, 7, 1, 2, 3]
             ↑
            min

index = 4

rotations = 4
```

So:

```text
Find minimum
    ↓
Return its index
```

---

# 12. Single Element in Sorted Array

Example:

```text
[1, 1, 2, 2, 3, 3, 4, 5, 5]
                  ↑
                unique
```

Before the single element:

```text
pairs start at even indices
```

After the single element:

```text
pair alignment shifts
```

### Key Observation

Check the parity of `mid`.

If `mid` is even:

```text
arr[mid] == arr[mid + 1]
    → unique element is to the right
```

Otherwise:

```text
unique element is to the left
```

The exact direction depends on the pair relationship, but the core idea is:

> **The single element causes the pair-index pattern to shift.**

---

# 13. Peak Element

A peak satisfies:

```text
arr[i] > arr[i - 1]
and
arr[i] > arr[i + 1]
```

Example:

```text
        5
       / \
      3   4
     /
    2
```

### Key Observation

Look at:

```text
arr[mid]
arr[mid + 1]
```

If:

```text
arr[mid] < arr[mid + 1]
```

we are climbing upward.

Therefore:

```text
a peak must exist on the right
```

Otherwise:

```text
peak exists on the left or at mid
```

### Pattern

```text
Slope ↑ → move right

Slope ↓ → move left
```

---

# 14. Binary Search on Answer

This is the most important advanced Binary Search pattern.

The array itself may not be sorted.

Instead, the **possible answers** are ordered.

Example:

```text
Possible answers:

1  2  3  4  5  6  7  8
X  X  X  X  ✓  ✓  ✓  ✓
            ↑
       first valid answer
```

The important property is:

> **Feasibility is monotonic.**

Once an answer becomes valid, every answer beyond it may remain valid.

Or the reverse:

```text
✓ ✓ ✓ ✓ X X X X
        ↑
    last valid answer
```

### Recognition

Ask:

> "Can I check whether a candidate answer works?"

If yes, ask:

> "Does feasibility change monotonically as the candidate changes?"

If yes:

```text
Binary Search on Answer
```

---

# 15. Minimum Feasible Answer

Common structure:

```text
X X X X ✓ ✓ ✓ ✓
        ↑
      answer
```

We want:

> **smallest valid answer**

Typical problems:

* Koko Eating Bananas
* Minimum Days to Make M Bouquets
* Smallest Divisor
* Ship Packages Within D Days
* Book Allocation
* Split Array Largest Sum

### Mental Template

```text
low = smallest possible answer
high = largest possible answer

while low <= high:

    mid = candidate answer

    if mid is feasible:
        save answer
        search left
    else:
        search right
```

---

# 16. Maximum Feasible Answer

Common structure:

```text
✓ ✓ ✓ ✓ X X X X
        ↑
      answer
```

We want:

> **largest valid answer**

Typical examples:

* Aggressive Cows
* Certain partition / placement problems

### Mental Template

```text
if mid is feasible:
    move right
else:
    move left
```

---

# 17. The Feasibility Function

For Binary Search on Answer, think:

```text
answer
   ↓
check(answer)
   ↓
True / False
```

Example:

```text
Koko speed = k

check(k):
    Can Koko finish within h hours?
```

or:

```text
Capacity = C

check(C):
    Can all packages be shipped within D days?
```

The Binary Search doesn't need to understand the entire problem.

It only needs:

```text
candidate answer
        ↓
feasibility check
        ↓
True / False
```

---

# 18. Search Space Identification

Before writing Binary Search, always ask:

### What exactly am I searching?

It may be:

```text
Array indices
```

or:

```text
Numeric answer
```

or:

```text
Distance
```

or:

```text
Capacity
```

or:

```text
Speed
```

or:

```text
Divisor
```

or:

```text
Partition boundary
```

or:

```text
Matrix values
```

If you cannot clearly define the search space, **don't write Binary Search yet.**

---

# 19. Binary Search Invariant

At every iteration, maintain:

> **The answer, if it exists, is still inside `[low, high]`.**

Every decision should preserve this.

```text
Before decision:

[ low ---------------- high ]
          answer
```

After eliminating one half:

```text
[ low -------- mid ]
                    ❌ eliminated
```

or:

```text
❌ eliminated
[ mid -------- high ]
       answer
```

This is the foundation of correct Binary Search.

---

# 20. Partition-Based Binary Search

Used for:

* Median of Two Sorted Arrays
* K-th Element of Two Sorted Arrays

Instead of searching for the answer directly, we search for the **correct partition**.

Example:

```text
A: [1, 3, 8]
B: [2, 7, 10, 12]

          left        |       right
A:       [1, 3]        |      [8]
B:       [2, 7]        |      [10, 12]
```

We want a partition where:

```text
max(left side) <= min(right side)
```

and:

```text
left side contains the required number of elements
```

### Core Idea

> **Binary Search the partition position, not the median itself.**

---

# 21. Binary Search on 2D Arrays

There are several different patterns.

### Matrix I

If the matrix behaves like one globally sorted array:

```text
1  3  5
7  9  11
13 15 17
```

Treat it as:

```text
[1, 3, 5, 7, 9, 11, 13, 15, 17]
```

Map:

```python
row = mid // columns
col = mid % columns
```

---

### Matrix II

If rows and columns are individually sorted:

```text
1   4   7
2   5   8
3   6   9
```

A different strategy is required.

Use the matrix's **ordering in two dimensions** to eliminate regions.

---

# 22. Matrix Median

The matrix may not be globally sorted.

Instead:

```text
Search over possible values
        ↓
For candidate x:
    count how many elements <= x
        ↓
Compare count with required position
```

This is another:

```text
Binary Search on Answer / Value Space
```

### Pattern

```text
value range
    ↓
candidate value
    ↓
count elements <= candidate
    ↓
move left/right
```

---

# 23. Peak Element II

The 2D version follows the same fundamental idea as the 1D peak problem.

Choose a column:

```text
        ↓
   [ column ]
```

Find the maximum element in that column.

Compare its left and right neighbours.

```text
left  < current > right
```

If current is a peak:

```text
answer found
```

Otherwise move toward the larger neighbour.

### Pattern

```text
2D Peak
   ↓
Binary Search over columns
   ↓
Find column maximum
   ↓
Compare neighbours
   ↓
Eliminate half the columns
```

---

# 24. Universal Binary Search Checklist

Before solving a problem, ask:

```text
1. Is there a search space?

2. Is the search space ordered?

3. Can I eliminate half?

4. What is my candidate?

5. What condition tells me which half to eliminate?

6. Is the condition monotonic?

7. Am I looking for:
       - exact value?
       - first valid?
       - last valid?
       - minimum valid?
       - maximum valid?

8. What should happen when mid is valid?

9. What should happen when mid is invalid?

10. What does low/high represent at the end?
```

---

# 25. Pattern Recognition Cheat Sheet

```text
Sorted array + find target
        ↓
Standard Binary Search


Need first position >= target
        ↓
Lower Bound


Need first position > target
        ↓
Upper Bound


Need first / last occurrence
        ↓
Boundary Search


Sorted array + duplicates
        ↓
Lower / Upper Bound


Rotated sorted array
        ↓
Find the sorted half


Minimum in rotated array
        ↓
Find where sorted order breaks


Unique element among pairs
        ↓
Parity / index pattern


Peak element
        ↓
Follow the slope


Answer lies in numeric range
        +
Can check whether candidate works
        +
Feasibility is monotonic
        ↓
Binary Search on Answer


Need minimum feasible answer
        ↓
Search for first TRUE


Need maximum feasible answer
        ↓
Search for last TRUE


Two sorted arrays + median / kth
        ↓
Partition Binary Search


Globally sorted matrix
        ↓
Flatten + Binary Search


Rows/columns sorted
        ↓
2D elimination / matrix-specific Binary Search


Matrix median
        ↓
Binary Search on Value Space
```

---

# 26. The Golden Question

Whenever you see a Binary Search problem, don't immediately ask:

> "Where is the binary search?"

Ask:

> **"What is the search space, and what monotonic property allows me to eliminate half?"**

That question is more important than memorizing any template.

---

# 27. Core Templates

### Standard Binary Search

```python
low = 0
high = n - 1

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

### Lower Bound

```python
low = 0
high = n - 1
answer = n

while low <= high:

    mid = low + (high - low) // 2

    if arr[mid] >= target:
        answer = mid
        high = mid - 1
    else:
        low = mid + 1

return answer
```

### First Valid Answer

```python
low = smallest_possible
high = largest_possible
answer = high

while low <= high:

    mid = low + (high - low) // 2

    if feasible(mid):
        answer = mid
        high = mid - 1
    else:
        low = mid + 1

return answer
```

### Last Valid Answer

```python
low = smallest_possible
high = largest_possible
answer = low

while low <= high:

    mid = low + (high - low) // 2

    if feasible(mid):
        answer = mid
        low = mid + 1
    else:
        high = mid - 1

return answer
```

---

# 28. Revision in 30 Seconds

If I see a problem tomorrow:

```text
Binary Search?
     ↓
What is the search space?
     ↓
Array indices?
     → Normal BS / Boundary BS

Rotated array?
     → Find sorted half

Need first/last?
     → Lower/Upper Bound

Numeric answer?
     → BS on Answer

Minimum valid?
     → First TRUE

Maximum valid?
     → Last TRUE

Two sorted arrays?
     → Partition BS

2D matrix?
     → Identify its ordering first
```

---

## Final Mental Model

```text
                 BINARY SEARCH
                       │
          ┌────────────┴────────────┐
          │                         │
      Search Array             Search Space
          │                         │
          │                  ┌──────┴──────┐
          │                  │             │
      Sorted Data        Index / Value   Answer
          │                  │             │
          │              Boundary       Feasibility
          │                  │             │
          │              Lower/Upper    Monotonic
          │                  │             │
          │              Occurrences   Min / Max
          │                                │
          └──────────────┬─────────────────┘
                         │
                  Eliminate Half
                         │
                      ANSWER
```

> **Don't memorize Binary Search solutions.**
>
> **Recognize the search space, identify the monotonic property, and find the boundary.**
