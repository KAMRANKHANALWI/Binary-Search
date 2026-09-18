# Binary Search on Answers

## Core Pattern

Here, binary search is **not searching an array index**.

We search the **possible answer space**.

```text
possible answers
       ↓
    mid answer
       ↓
   check(mid)
       ↓
  can it work?
   ↙       ↘
 yes       no
```

The most important question:

> **Is `check(mid)` monotonic?**

Example:

```text
1  2  3  4  5  6  7
✗  ✗  ✗  ✓  ✓  ✓  ✓
         ↑
       boundary
```

Binary search finds this boundary.

---

## 1. Root Problems

### Square Root

Find the largest `x` satisfying:

```text
x² <= n
```

Search:

```text
1 ... n
```

**Pattern:** maximum feasible value.

### N-th Root

Find `x` satisfying:

```text
xⁿ <= m
```

Binary search the possible value of `x`.

---

## 2. Rate / Capacity Problems

### Koko Eating Bananas

Search eating speed:

```text
1 ... max(piles)
```

Check:

```text
hoursNeeded(speed) <= h
```

Larger speed → fewer hours.

```text
too slow → low = mid + 1
works    → high = mid
```

**Pattern:** minimum feasible answer.

### Minimum Days to Make M Bouquets

Search day:

```text
min(bloomDay) ... max(bloomDay)
```

Check whether `m` bouquets can be formed by `mid`.

### Smallest Divisor

Search:

```text
1 ... max(arr)
```

Check:

```text
sum(ceil(arr[i] / mid)) <= limit
```

### Capacity to Ship Packages

Search capacity:

```text
max(weights) ... sum(weights)
```

Check whether everything can be shipped within `days`.

---

## 3. Placement / Partition Problems

### Aggressive Cows

Search minimum possible distance:

```text
1 ... maxPosition - minPosition
```

Check whether `k` cows can be placed with at least `mid` distance.

### Book Allocation

Search maximum pages assigned to one student:

```text
max(pages) ... sum(pages)
```

Check whether the books can be allocated using the required number of students.

### Painter's Partition

Same partition idea as Book Allocation.

Search the maximum work/time assigned to one painter.

### Split Array Largest Sum

Search:

```text
max(arr) ... sum(arr)
```

Check whether the array can be split into at most `k` parts with maximum sum `<= mid`.

---

## 4. K-th Missing Positive

Observation:

```text
missing(i) = arr[i] - (i + 1)
```

This number is monotonic.

Binary search for the first index where:

```text
missing(i) >= k
```

**Pattern:** binary search on a monotonic count.

---

## 5. Minimize Maximum Distance — Gas Stations

### Heap approach

Repeatedly split the interval having the current largest section.

```text
largest section
      ↓
   split it
      ↓
push updated section
```

### Binary Search approach

Search the answer itself:

```text
low  = 0
high = maximum existing gap
```

For candidate distance `d`:

```text
requiredStations(d)
```

If:

```text
requiredStations(d) <= k
```

then `d` is feasible.

Because the answer is floating-point:

```text
while high - low > 1e-6
```

---

## 6. Median of Two Sorted Arrays

This is **binary search on a partition**, not directly on the answer.

Create:

```text
A: [ left | right ]
B: [ left | right ]
```

The left side must contain half the total elements.

For a valid partition:

```text
l1 <= r2
l2 <= r1
```

Then:

```text
odd:
    answer = max(l1, l2)

even:
    answer = (max(l1,l2) + min(r1,r2)) / 2
```

Binary-search the smaller array.

---

## 7. K-th Element of Two Sorted Arrays

Again use a partition.

Put exactly `k` elements on the left:

```text
mid1 + mid2 = k
```

Therefore:

```text
mid2 = k - mid1
```

Valid partition:

```text
l1 <= r2
l2 <= r1
```

Then:

```text
answer = max(l1, l2)
```

Binary-search the smaller array.

---

# How to Recognize BS on Answers

Ask:

### 1. Is there a continuous range of possible answers?

Examples:

```text
speed
days
capacity
distance
divisor
maximum pages
```

### 2. Can I write `check(mid)`?

```text
Can the problem be solved if the answer is `mid`?
```

### 3. Is the check monotonic?

For example:

```text
capacity:

5  6  7  8  9  10
✗  ✗  ✗  ✓  ✓  ✓
```

Once feasible, larger capacities remain feasible.

### 4. Am I finding:

```text
minimum feasible
        OR
maximum feasible?
```

That determines the binary-search movement.

---

# Universal Templates

## Minimum Feasible Answer

```text
low = smallest possible answer
high = largest possible answer

while low < high:

    mid = low + (high - low) // 2

    if check(mid):
        high = mid
    else:
        low = mid + 1

return low
```

## Maximum Feasible Answer

```text
low = smallest possible answer
high = largest possible answer
answer = ...

while low <= high:

    mid = low + (high - low) // 2

    if check(mid):
        answer = mid
        low = mid + 1
    else:
        high = mid - 1

return answer
```

---

# Quick Pattern Map

```text
3-BS-on-Answers/
│
├── Roots
│   ├── Square Root
│   └── N-th Root
│
├── Rate / Capacity
│   ├── Koko
│   ├── Bouquet Days
│   ├── Smallest Divisor
│   └── Ship Packages
│
├── Placement / Partition
│   ├── Aggressive Cows
│   ├── Book Allocation
│   ├── Painter's Partition
│   └── Split Array
│
├── Missing / Distance
│   ├── K-th Missing Positive
│   └── Gas Stations
│
└── Two Sorted Arrays
    ├── Median
    └── K-th Element
```

## Final Mental Model

> **Binary Search on Answers = define the answer space + write a monotonic `check(mid)` + binary-search the feasibility boundary.**

Before coding, identify:

```text
1. What is my answer space?
2. What does check(mid) mean?
3. Is check(mid) monotonic?
4. Do I need minimum or maximum feasible?
5. How should low/high move?
```
