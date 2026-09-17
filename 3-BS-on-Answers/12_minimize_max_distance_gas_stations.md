# Minimize Maximum Distance Between Gas Stations

**Pattern:** Binary Search on Answer --- Minimize the Maximum
(continuous version)

> **Core idea:** Don\'t try to place the stations directly. Guess the
> maximum allowed distance `X`, count how many new stations are needed
> to make every gap `<= X`, and use that count to decide whether `X` is
> feasible.

------------------------------------------------------------------------

## 1. Problem 

Given sorted gas-station coordinates and `k` new stations, place the new
stations so that the **maximum distance between consecutive stations is
minimized**.

``` text
arr = [1, 13, 17, 23]
k = 5

original gaps = [12, 4, 6]

answer = 3.0
```

------------------------------------------------------------------------

## 2. First understand ONE gap 

Suppose one gap has length `L`.

If we put `x` new stations inside it:

``` text
x new stations
      ↓
x + 1 sections
```

The best placement is to spread them evenly.

``` text
largest section = L / (x + 1)
```

Example:

``` text
1 ---------------- 7
       gap = 6

2 new stations:

1 ---- 3 ---- 5 ---- 7
     2    2    2
```

So the largest section is `2`.

### Reverse the question

If we want every section to be at most `dist`:

``` text
sections needed = ceil(L / dist)

new stations needed = sections needed - 1
```

Therefore:

``` text
stations_needed = ceil(gap / dist) - 1
```

### Important exact-division trap

``` text
gap = 6
dist = 2

6 / 2 = 3
```

`3` means **3 sections**, not 3 new stations:

``` text
1 -- 3 -- 5 -- 7

3 sections
2 new stations
```

Therefore:

``` text
stations_needed = 3 - 1 = 2
```

------------------------------------------------------------------------

# 3. The key transformation 

Direct question:

``` text
"Where should I put the k stations?"
```

is difficult.

Instead ask:

``` text
"Suppose the maximum allowed distance is X.
Can I achieve it using k stations or fewer?"
```

For a candidate `X`:

``` text
For every original gap:
    calculate stations required
    add them

if total <= k:
    X is POSSIBLE
else:
    X is IMPOSSIBLE
```

This is the feasibility function.

------------------------------------------------------------------------

# 4. Approach 1 --- Brute Force 

## Intuition

Try possible decimal distances one by one:

``` text
0.001
0.002
0.003
...
```

For each candidate:

``` text
count required stations
```

Return the first candidate that needs at most `k`.

### Pseudocode

``` text
find maximum original gap

distance = small positive step

while distance <= maximum_gap:

    required = stations_required(distance)

    if required <= k:
        return distance

    distance += step
```

### Code

``` python
def minimise_max_distance_brute(arr, k):
    max_gap = 0

    for i in range(len(arr) - 1):
        max_gap = max(max_gap, arr[i + 1] - arr[i])

    step = 1e-3
    distance = step

    while distance <= max_gap:

        if number_of_gas_stations_required(arr, distance) <= k:
            return distance

        distance += step

    return max_gap
```

### Why it is bad

If precision is `1e-6`, we may check millions of candidates.

So brute force is useful for understanding the idea, but not for the
real solution.

------------------------------------------------------------------------

# 5. Approach 2 --- Greedy + Max Heap 

Instead of guessing the answer, directly attack the **currently largest
gap**.

## Intuition

Our objective is:

``` text
MINIMIZE THE MAXIMUM
```

If current sections are:

``` text
12, 4, 6
```

the maximum is `12`.

Putting a station into `4` first doesn\'t improve the current maximum.

So:

``` text
Always split the currently largest section.
```

Repeat this `k` times.

------------------------------------------------------------------------

## What do we track?

``` text
how_many[i]
```

means:

``` text
number of new stations placed inside original gap i
```

For:

``` text
arr = [1, 13, 17, 23]
```

there are 3 gaps:

``` text
gap 0 = 12
gap 1 = 4
gap 2 = 6

how_many = [0, 0, 0]
```

After `x` stations are placed in a gap:

``` text
sections = x + 1

current largest section =
original_gap / (x + 1)
```

------------------------------------------------------------------------

## Why a heap?

Every time we need:

``` text
"Which gap is currently the largest?"
```

A heap gives us that efficiently.

Python\'s `heapq` is a **min heap**, so use negative lengths:

``` text
actual:   12   6   4
heap:    -12  -6  -4
```

The smallest negative value corresponds to the largest actual value.

Each heap item is:

``` text
(-current_section_length, gap_index)
```

The index is essential because after popping a section we must know
**which original gap** to update.

------------------------------------------------------------------------

## Heap dry run

``` text
arr = [1, 13, 17, 23]
gaps = [12, 4, 6]
k = 5
```

### Station 1

``` text
largest = 12
split gap 0

12 / 2 = 6

current = [6, 4, 6]
```

### Station 2

``` text
largest = 6
split gap 0 again

12 / 3 = 4

current = [4, 4, 6]
```

### Station 3

``` text
largest = 6
split gap 2

6 / 2 = 3

current = [4, 4, 3]
```

### Station 4

``` text
largest = 4
split gap 0

12 / 4 = 3

current = [3, 4, 3]
```

### Station 5

``` text
largest = 4
split gap 1

4 / 2 = 2

current = [3, 2, 3]
```

Final:

``` text
maximum = 3

answer = 3.0
```

### ASCII picture

``` text
Initial:

        12
       /  \
      4    6


After station 1:

        6
       / \
      4   6


After station 2:

        6
       / \
      4   4


After station 3:

        4
       / \
      4   3


After station 4:

        4
       / \
      3   3


After station 5:

        3
       / \
      2   3
```

The exact tree shape can vary when values tie; the important property is
that the largest current section is always available at the top.

------------------------------------------------------------------------

## Heap pseudocode

``` text
how_many = [0] * (n - 1)

put every original gap into max heap

repeat k times:

    largest_section, gap_index = remove largest

    how_many[gap_index] += 1

    original_gap =
        arr[gap_index + 1] - arr[gap_index]

    new_section =
        original_gap / (how_many[gap_index] + 1)

    push new_section back

return largest section
```

## Heap code

``` python
import heapq


def minimise_max_distance_heap(arr, k):

    n = len(arr)

    how_many = [0] * (n - 1)

    # Python has a min heap.
    # Negate lengths to simulate a max heap.
    pq = []

    for i in range(n - 1):
        gap = arr[i + 1] - arr[i]
        heapq.heappush(pq, (-gap, i))

    for _ in range(k):

        negative_length, index = heapq.heappop(pq)

        how_many[index] += 1

        gap = arr[index + 1] - arr[index]

        new_length = gap / (how_many[index] + 1)

        heapq.heappush(
            pq,
            (-new_length, index)
        )

    return -pq[0][0]
```

------------------------------------------------------------------------

# 6. Approach 3 --- Binary Search on Answer 

This is the optimal approach.

We are **not binary-searching an array**.

We are binary-searching:

``` text
the answer = maximum allowed distance
```

------------------------------------------------------------------------

## Search space

For:

``` text
arr = [1, 13, 17, 23]
```

gaps:

``` text
[12, 4, 6]
```

So:

``` text
low  = 0
high = maximum gap = 12
```

``` text
0 -------------------------------- 12
^                                  ^
low                               high
```

------------------------------------------------------------------------

## Why binary search works

As the allowed distance increases, the number of stations required can
only decrease.

So the answers have this shape:

``` text
IMPOSSIBLE | IMPOSSIBLE | IMPOSSIBLE | POSSIBLE | POSSIBLE | POSSIBLE
                                           ^
                                      first possible
```

We want that boundary.

------------------------------------------------------------------------

## The two cases

### Case 1: `count > k` {#case-1-count--k}

Too many stations are required.

Therefore:

``` text
mid is too SMALL
```

We need a larger distance:

``` python
low = mid
```

### Case 2: `count <= k` {#case-2-count--k}

The candidate is possible.

But we want the **minimum** possible distance.

So try smaller:

``` python
high = mid
```

### Memory trick

``` text
Too many stations
→ distance too small
→ LOW goes UP

Enough stations
→ distance is possible
→ HIGH goes DOWN
```

------------------------------------------------------------------------

# 7. Binary Search dry run 

``` text
arr = [1, 13, 17, 23]
gaps = [12, 4, 6]
k = 5

low = 0
high = 12
```

### Iteration 1

``` text
mid = 6
```

Stations required:

``` text
12 → 1
 4 → 0
 6 → 0

total = 1
```

``` text
1 <= 5
```

Possible:

``` text
high = 6
```

------------------------------------------------------------------------

### Iteration 2

``` text
mid = 3
```

Required:

``` text
12 → 3
 4 → 0
 6 → 1

total = 4
```

``` text
4 <= 5
```

Possible:

``` text
high = 3
```

------------------------------------------------------------------------

### Iteration 3

``` text
mid = 1.5
```

Required:

``` text
12 → 7
 4 → 1
 6 → 3

total = 11
```

``` text
11 > 5
```

Impossible:

``` text
low = 1.5
```

Eventually:

``` text
high - low < 1e-6
```

and:

``` text
answer ≈ 3.0
```

------------------------------------------------------------------------

# 8. Why floating-point Binary Search is different

Integer binary search:

``` python
while low <= high:
    mid = (low + high) // 2

    low = mid + 1
    high = mid - 1
```

doesn\'t work here because the answer can be:

``` text
2.333...
1.875
3.14159
```

There is no meaningful \"next decimal\".

Instead:

``` python
while high - low > 1e-6:
```

Keep shrinking the continuous interval.

``` text
low ---------------- high

        ↓ shrink

low -------- high

        ↓ shrink

low ---- high

        ↓

high - low < 1e-6
```

Return `high` (or a value within the final interval).

------------------------------------------------------------------------

# 9. Feasibility helper 

``` python
import math


def number_of_gas_stations_required(arr, distance):

    count = 0

    for i in range(len(arr) - 1):

        gap = arr[i + 1] - arr[i]

        stations = math.floor(gap / distance)

        # Exact division correction.
        if math.isclose(
            gap,
            stations * distance,
            rel_tol=1e-12,
            abs_tol=1e-12
        ):
            stations -= 1

        count += stations

    return count
```

### Why the correction?

For:

``` text
gap = 6
distance = 2
```

`floor(6 / 2) = 3`, but we need only 2 new stations.

So exact division requires:

``` text
3 - 1 = 2
```

`math.isclose()` is used because decimal floating-point calculations are
not always represented exactly.

------------------------------------------------------------------------

# 10. Optimal Binary Search code 

``` python
def minimise_max_distance(arr, k):

    low = 0.0

    high = 0.0

    for i in range(len(arr) - 1):
        gap = arr[i + 1] - arr[i]
        high = max(high, gap)

    epsilon = 1e-6

    while high - low > epsilon:

        mid = (low + high) / 2.0

        count = number_of_gas_stations_required(
            arr,
            mid
        )

        if count > k:
            # Too many stations.
            # Distance is too small.
            low = mid

        else:
            # Possible.
            # Try smaller distance.
            high = mid

    return high
```

------------------------------------------------------------------------

# 11. The deepest pattern 

The whole problem becomes:

``` text
                 MINIMIZE
                    ↓
             maximum distance
                    ↓
               Guess X
                    ↓
        Can every gap be <= X?
                    ↓
          Count stations needed
                    ↓
          ┌─────────┴─────────┐
          ↓                   ↓
       count > K           count <= K
          ↓                   ↓
      X too small          X possible
          ↓                   ↓
      low = X              high = X
          ↓                   ↓
              Binary Search
                    ↓
          minimum feasible X
```

------------------------------------------------------------------------

# 12. Connection to other Binary Search problems 

This is the same **Binary Search on Answer** pattern as:

``` text
Book Allocation
Painter's Partition
Split Array Largest Sum
Gas Stations
```

### Book Allocation

``` text
Guess maximum pages
        ↓
Count students required
        ↓
Too many?
        ↓
Increase allowed pages
```

### Gas Stations

``` text
Guess maximum distance
        ↓
Count stations required
        ↓
Too many?
        ↓
Increase allowed distance
```

The main new idea here is:

``` text
The answer is continuous.
```

Therefore we shrink a floating-point interval instead of using `mid + 1`
/ `mid - 1`.

------------------------------------------------------------------------

# 13. Heap vs Binary Search 

### Heap

``` text
Start with actual gaps
        ↓
Find WORST gap
        ↓
Fix it
        ↓
Find WORST gap again
        ↓
Fix it
        ↓
repeat K times
```

**Heap = attack the worst spot from the inside out.**

### Binary Search

``` text
Start with possible answers
        ↓
Guess X
        ↓
Check X
        ↓
Too small? Increase
Possible? Decrease
        ↓
repeat
```

**Binary Search = shrink the answer space from the outside in.**

------------------------------------------------------------------------

# 14. Complexity 

  Approach        Time                            Space
  --------------- ------------------------------- --------
  Brute Force     `O(max_gap / step * N)`         `O(1)`
  Heap / Greedy   `O(N log N + K log N)`          `O(N)`
  Binary Search   `O(N log(max_gap / epsilon))`   `O(1)`

------------------------------------------------------------------------

# 15. Final Cheat Sheet 

``` text
PROBLEM
-------
Minimize maximum distance between gas stations.

INPUT
-----
arr = sorted station coordinates
k   = number of new stations

GOAL
----
Minimize the largest distance between
consecutive stations.


ONE GAP
-------
gap = L
x new stations
→ x + 1 sections

largest section = L / (x + 1)


FEASIBILITY
-----------
stations_needed = ceil(gap / dist) - 1


EXACT DIVISION
--------------
gap = 6
dist = 2

6 / 2 = 3 sections
new stations = 3 - 1 = 2


HEAP
----
Always split the currently largest section.

how_many[i] = stations placed in gap i

repeat K times:
    pop largest
    increment how_many[index]
    recalculate section length
    push back

return largest section


BINARY SEARCH
-------------
low  = 0
high = maximum original gap

while high - low > 1e-6:

    mid = (low + high) / 2

    count = stations_required(mid)

    if count > k:
        low = mid
    else:
        high = mid

return high


MOST IMPORTANT LOGIC
--------------------
count > K
→ mid is too small
→ low = mid

count <= K
→ mid is possible
→ high = mid


CORE SENTENCE
-------------
"I am not searching for where to place stations.

I am searching for the minimum possible
maximum distance.

For every guessed distance X,
I can count how many stations X would require."
```

------------------------------------------------------------------------

## One-line memory hook

**Guess the maximum distance → count the stations it costs → too many
means increase distance → feasible means decrease distance.**
