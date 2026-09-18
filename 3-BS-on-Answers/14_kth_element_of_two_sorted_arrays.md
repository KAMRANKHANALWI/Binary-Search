# K-th Element of Two Sorted Arrays | Binary Search

## 1. Problem

Given two sorted arrays `A` and `B`, find the **k-th element** of the combined sorted array.

> `k` is **1-based**: `k = 1` means the smallest element.

### Example

```text
A = [2, 3, 6, 7, 9]
B = [1, 4, 8, 10]
k = 4

Combined:
[1, 2, 3, 4, 6, 7, 8, 9, 10]
         ↑
        4th = 4
```

---

# 2. Main Intuition

We do **not** need to actually merge the arrays.

We only need to decide:

> How many elements should come from `A` and how many from `B` to form the first `k` elements?

Suppose we take:

```text
mid1 elements from A
mid2 elements from B
```

Since the left side must contain exactly `k` elements:

```text
mid1 + mid2 = k

therefore:

mid2 = k - mid1
```

So if we choose `mid1`, `mid2` is automatically decided.

The problem becomes:

> Find the correct partition between A and B.

---

# 3. Visualizing the Partition

Suppose:

```text
A = [2  3  6 | 7  9]
             ↑
             mid1

B = [1  4 | 8  10]
           ↑
           mid2
```

The left side contains:

```text
A: 2, 3, 6
B: 1, 4

total = 5 elements
```

If `k = 5`, this is the required partition.

Define:

```text
l1 = element just LEFT of partition in A
r1 = element just RIGHT of partition in A

l2 = element just LEFT of partition in B
r2 = element just RIGHT of partition in B
```

For the above:

```text
A = [2  3  6 | 7  9]
          l1   r1

B = [1  4 | 8  10]
       l2   r2
```

---

# 4. What Makes a Partition Correct?

Because both arrays are already sorted, we only need to check the **two cross-boundary conditions**:

```text
l1 <= r2
l2 <= r1
```

Why?

We need every element on the left to be `<=` every element on the right.

Inside each array this is already guaranteed because the arrays are sorted.

So only these cross comparisons matter:

```text
A-left  <= B-right
B-left  <= A-right
```

If:

```text
l1 <= r2 && l2 <= r1
```

then the partition is correct.

Since there are exactly `k` elements on the left:

```text
k-th element = max(l1, l2)
```

---

# 5. Why Binary Search?

We binary-search how many elements to take from the **smaller array**.

Let:

```text
n1 = A.size()
n2 = B.size()
```

Always make `A` the smaller array.

```text
if n1 > n2:
    swap(A, B)
```

This keeps the binary-search range small.

---

# 6. Search Space

We choose `mid1` = number of elements taken from `A`.

Normally:

```text
0 <= mid1 <= n1
```

But `k` also limits it.

We cannot take more than `k` elements from `A`:

```text
mid1 <= k
```

And `B` can contain at most `n2` elements:

```text
mid2 <= n2

k - mid1 <= n2

mid1 >= k - n2
```

Therefore:

```text
low  = max(0, k - n2)
high = min(k, n1)
```

This is an important part of the algorithm.

---

# 7. Boundary Values

Sometimes the partition is at the beginning or end of an array.

Example:

```text
A = [2 3 6 | 7 9]
```

If `mid1 = 0`, there is nothing on A's left.

So:

```text
l1 = -infinity
```

If `mid1 = n1`, there is nothing on A's right.

So:

```text
r1 = +infinity
```

Similarly for `B`.

In C++:

```cpp
l1 = INT_MIN
r1 = INT_MAX
l2 = INT_MIN
r2 = INT_MAX
```

This lets the same comparison work at the boundaries.

---

# 8. How Binary Search Moves

### Case 1: Too many elements taken from A

If:

```text
l1 > r2
```

then A's left side has become too large.

We need to take **fewer elements from A**:

```text
high = mid1 - 1
```

---

### Case 2: Too few elements taken from A

If:

```text
l2 > r1
```

then B's left side is too large compared with A's right side.

We need to take **more elements from A**:

```text
low = mid1 + 1
```

---

### Case 3: Correct partition

```text
l1 <= r2 && l2 <= r1
```

Answer:

```text
max(l1, l2)
```

---

# 9. Pseudocode

```text
kthElement(A, B, k):

    if A is larger than B:
        swap(A, B)

    n1 = size(A)
    n2 = size(B)

    low  = max(0, k - n2)
    high = min(k, n1)

    while low <= high:

        mid1 = (low + high) / 2
        mid2 = k - mid1

        l1 = A[mid1 - 1] or -INF
        r1 = A[mid1]     or +INF

        l2 = B[mid2 - 1] or -INF
        r2 = B[mid2]     or +INF

        if l1 <= r2 AND l2 <= r1:
            return max(l1, l2)

        else if l1 > r2:
            high = mid1 - 1

        else:
            low = mid1 + 1
```

---

# 10. Dry Run

```text
A = [2, 3, 6, 7, 9]
B = [1, 4, 8, 10]
k = 4
```

`A` is larger, so swap them:

```text
A = [1, 4, 8, 10]     n1 = 4
B = [2, 3, 6, 7, 9]   n2 = 5
```

Search range:

```text
low  = max(0, 4 - 5) = 0
high = min(4, 4) = 4
```

Suppose:

```text
mid1 = 2
mid2 = 4 - 2 = 2
```

Partition:

```text
A = [1, 4 | 8, 10]
          ↑

B = [2, 3 | 6, 7, 9]
          ↑
```

Therefore:

```text
l1 = 4
r1 = 8

l2 = 3
r2 = 6
```

Check:

```text
l1 <= r2
4 <= 6   ✓

l2 <= r1
3 <= 8   ✓
```

Correct partition.

Therefore:

```text
answer = max(4, 3)
       = 4
```

---

# 11. Complexity

Let:

```text
n1 = size of smaller array
```

### Time

```text
O(log(min(n1, n2)))
```

### Space

```text
O(1)
```

No merged array is created.

---

# 12. Key Mental Model

Remember this problem as:

```text
Don't merge.
        ↓
Create a partition.
        ↓
Exactly k elements on the left.
        ↓
mid2 = k - mid1
        ↓
Check cross-boundaries:
    l1 <= r2
    l2 <= r1
        ↓
Correct partition?
        ↓
max(l1, l2)
```

### One-line takeaway

> **Binary-search the partition of the smaller array so that exactly `k` elements lie on the left, then return the largest left-side element.**
