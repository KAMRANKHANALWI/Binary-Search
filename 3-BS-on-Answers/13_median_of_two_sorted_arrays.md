# Median of Two Sorted Arrays of Different Sizes

> **Pattern:** Two Pointers → Binary Search on Partition  
> **Goal:** Find the median of two sorted arrays without actually merging them.

---

## 1. Problem

Given two sorted arrays `a` and `b`, find the median of all their elements combined.

### Example

```text
a = [1, 3, 4, 7, 10, 12]
b = [2, 3, 6, 15]

Combined:
[1, 2, 3, 3, 4, 6, 7, 10, 12, 15]

Median = (4 + 6) / 2 = 5
```

### Median rule

```text
Odd total  → middle element
Even total → average of two middle elements
```

---

# 2. The Three Approaches

```text
Brute
  ↓
Merge completely
  ↓
O(n1 + n2) time, O(n1 + n2) space

Better
  ↓
Two pointers, but stop at the middle
  ↓
O(n1 + n2) time, O(1) space

Optimal
  ↓
Binary search for the correct partition
  ↓
O(log(min(n1, n2))) time, O(1) space
```

The key improvement is:

> Instead of walking through elements to find the middle, find the **correct partition** directly.

---

# 3. Approach 1 — Brute Force

## Intuition

Both arrays are sorted, so use the standard merge process.

```text
A → 1  3  4  7  10  12
     ↑

B → 2  3  6  15
     ↑
```

Take the smaller element each time and build the complete sorted array.

### Pseudocode

```text
i = 0, j = 0

while both arrays have elements:
    take the smaller of A[i] and B[j]

add remaining elements

if total is odd:
    return middle element
else:
    return average of two middle elements
```

### Complexity

```text
Time  : O(n1 + n2)
Space : O(n1 + n2)
```

The problem: we create the entire merged array even though we only need its middle.

---

# 4. Approach 2 — Better

## Key Observation

We don't need to store the merged array.

We only need to reach the middle.

Maintain:

```text
prev = previous element
curr = current element
```

For an even-sized array, the two middle elements are `prev` and `curr`.

Example:

```text
1  2  3  3  4  6  7  10  12  15
            ↑  ↑
           prev curr
```

```text
median = (4 + 6) / 2 = 5
```

For odd total:

```text
1  2  3  3  4  6  7
            ↑
           curr

median = 4
```

### Pseudocode

```text
i = 0
j = 0
prev = 0
curr = 0

repeat until middle:
    prev = curr

    if A[i] <= B[j]:
        curr = A[i]
        i++
    else:
        curr = B[j]
        j++

if total is odd:
    return curr

return (prev + curr) / 2
```

### Complexity

```text
Time  : O(n1 + n2) worst case
Space : O(1)
```

We improved space, but we still walk through elements one by one.

Can we jump directly to the middle?

**Yes — binary search.**

---

# 5. Approach 3 — Optimal: Binary Search on Partition

## The Big Idea

Instead of asking:

> "What is the next smallest element?"

ask:

> **"Where should I cut the two arrays so that the left half contains exactly half of all elements?"**

Example:

```text
A = [1, 3, 4 | 7, 10, 12]
B = [2, 3    | 6, 15]
```

There are `10` total elements, so the left side needs `5`.

```text
3 elements from A
2 elements from B
-----------------
5 elements on left
```

---

# 6. What Are We Binary Searching?

We binary-search the **partition position in the smaller array**.

Possible cuts:

```text
| 1  3  4  7  10  12
  0  1  2  3   4   5  6
```

If we choose:

```text
cutA = 3
```

then the number of elements needed from B is forced:

```text
cutB = left_size - cutA
```

This guarantees that the left side contains exactly the required number of elements.

---

# 7. The Four Boundary Values

After partitioning:

```text
A = [ ... L1 | R1 ... ]
B = [ ... L2 | R2 ... ]
```

where:

```text
L1 = largest element on A's left
R1 = smallest element on A's right

L2 = largest element on B's left
R2 = smallest element on B's right
```

For:

```text
A = [1, 3, 4 | 7, 10, 12]
B = [2, 3    | 6, 15]
```

we get:

```text
L1 = 4    R1 = 7
L2 = 3    R2 = 6
```

---

# 8. When Is the Partition Correct?

We need:

```text
L1 <= R2
AND
L2 <= R1
```

Why?

Because every element on the left must be `<=` every element on the right.

It is enough to check the largest left values against the smallest right values:

```text
L1 <= R2
L2 <= R1
```

Example:

```text
4 <= 6  ✓
3 <= 7  ✓
```

So the partition is correct.

---

# 9. Finding the Median

Once the partition is correct, only the boundary values matter.

## Odd total

The left side has one extra element:

```text
median = max(L1, L2)
```

---

## Even total

The two middle elements are:

```text
left middle  = max(L1, L2)
right middle = min(R1, R2)
```

Therefore:

```text
median = (max(L1, L2) + min(R1, R2)) / 2
```

Example:

```text
L1 = 4, L2 = 3
R1 = 7, R2 = 6

left middle  = max(4, 3) = 4
right middle = min(7, 6) = 6

median = (4 + 6) / 2 = 5
```

---

# 10. How Does Binary Search Move?

This is the most important part to understand.

## Case 1 — `L1 > R2`

```text
L1 > R2
```

We took **too many elements from A**.

So A's partition is too far right.

```text
high = cutA - 1
```

Think:

```text
A = [ LEFT | RIGHT ]
          ↑
       too far →
```

Move the partition **left**.

---

## Case 2 — `L2 > R1`

```text
L2 > R1
```

We took **too few elements from A**.

We need more elements from A on the left.

```text
low = cutA + 1
```

Move the partition **right**.

### Memory trick

```text
L1 > R2  → A cut too RIGHT → move LEFT

L2 > R1  → A cut too LEFT  → move RIGHT
```

---

# 11. Why Search the Smaller Array?

Always make A the smaller array:

```python
if len(a) > len(b):
    a, b = b, a
```

Then the binary search range is only:

```text
0 ... min(n1, n2)
```

Therefore:

```text
Time = O(log(min(n1, n2)))
```

---

# 12. Boundary Cases: -∞ and +∞

A partition can be at either end of an array.

If there is nothing on the left:

```text
L = -∞
```

If there is nothing on the right:

```text
R = +∞
```

For example:

```text
| 1 2 3
```

has:

```text
L = -∞
```

and:

```text
1 2 3 |
```

has:

```text
R = +∞
```

In Python:

```python
L1 = float("-inf") if cut1 == 0 else a[cut1 - 1]
R1 = float("inf") if cut1 == n1 else a[cut1]

L2 = float("-inf") if cut2 == 0 else b[cut2 - 1]
R2 = float("inf") if cut2 == n2 else b[cut2]
```

This lets the same logic handle edge cases cleanly.

---

# 13. Optimal Pseudocode

```text
if A is larger:
    swap A and B

n1 = len(A)
n2 = len(B)

left_size = (n1 + n2 + 1) // 2

low = 0
high = n1

while low <= high:

    cutA = (low + high) // 2
    cutB = left_size - cutA

    L1 = A[cutA - 1] or -∞
    R1 = A[cutA]     or +∞

    L2 = B[cutB - 1] or -∞
    R2 = B[cutB]     or +∞

    if L1 <= R2 and L2 <= R1:

        if total is odd:
            return max(L1, L2)

        return (max(L1, L2) + min(R1, R2)) / 2

    elif L1 > R2:
        high = cutA - 1

    else:
        low = cutA + 1
```

---

# 14. Dry Run — Optimal Approach

```text
A = [1, 3, 4, 7, 10, 12]
B = [2, 3, 6, 15]

total = 10
left_size = 5
```

Initial binary search:

```text
low = 0
high = 6
```

Suppose:

```text
cutA = 3
cutB = 5 - 3 = 2
```

Partition:

```text
A = [1, 3, 4 | 7, 10, 12]
B = [2, 3    | 6, 15]
```

Boundary values:

```text
L1 = 4    R1 = 7
L2 = 3    R2 = 6
```

Check:

```text
L1 <= R2
4 <= 6 ✓

L2 <= R1
3 <= 7 ✓
```

Correct partition.

Total is even:

```text
left middle  = max(4, 3) = 4
right middle = min(7, 6) = 6

answer = (4 + 6) / 2
       = 5
```

---

# 15. Mental Model

Don't memorize the binary-search code first.

Remember this:

```text
A: [ left A | right A ]
       L1        R1

B: [ left B | right B ]
       L2        R2
```

We want:

```text
        LEFT        |        RIGHT

largest LEFT <= smallest RIGHT
```

So:

```text
L1 <= R2
L2 <= R1
```

If correct:

```text
Odd:
    max(L1, L2)

Even:
    (max(L1, L2) + min(R1, R2)) / 2
```

If wrong:

```text
L1 > R2 → move A partition LEFT

L2 > R1 → move A partition RIGHT
```

That's the whole binary-search idea.

---

# 16. Complexity Comparison

| Approach | Idea | Time | Extra Space |
|---|---|---:|---:|
| Brute | Fully merge | O(n1 + n2) | O(n1 + n2) |
| Better | Merge only to middle | O(n1 + n2) | O(1) |
| Optimal | Binary search partition | O(log(min(n1,n2))) | O(1) |

---

# 17. Common Mistakes

### 1. Binary-searching for the median

We are **not** binary-searching for a value.

We are binary-searching for:

```text
the correct partition position
```

### 2. Forgetting the smaller array

```python
if len(a) > len(b):
    a, b = b, a
```

### 3. Wrong formula for even total

Correct:

```text
(max(L1, L2) + min(R1, R2)) / 2
```

### 4. Mixing up partition movement

```text
L1 > R2 → move LEFT

L2 > R1 → move RIGHT
```

---

# 18. Final Takeaway

The progression is the real lesson:

```text
Brute:
"Merge everything."

        ↓

Better:
"Why merge everything?
I only need the middle."

        ↓

Optimal:
"Why walk to the middle?
Can I directly find the partition?"

        ↓

Binary Search:
"Yes — binary search the partition
in the smaller array."
```

> **One-line memory trick:**  
> Find a partition where the left side has the correct number of elements and `max(left) <= min(right)`. Then the median is determined by the boundary values.
