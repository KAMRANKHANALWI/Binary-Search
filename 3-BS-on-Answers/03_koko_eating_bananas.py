"""
03 - Koko Eating Bananas

Problem:
Given piles of bananas and h hours, find the minimum integer eating speed k
such that Koko can finish all bananas within h hours.

Example:
piles = [3, 6, 7, 11], h = 8
answer = 4
"""

# ============================================================
# 1. BRUTE FORCE
# ============================================================
"""
Idea:
Try every possible eating speed from 1 to max(piles).

For each speed k:
    calculate how many hours are needed.
    if hours <= h, return k immediately.

Pseudocode:

function calculate_hours(piles, k):
    total_hours = 0

    for pile in piles:
        total_hours += ceil(pile / k)

    return total_hours


function koko_brute(piles, h):
    max_pile = max(piles)

    for k from 1 to max_pile:
        total_hours = calculate_hours(piles, k)

        if total_hours <= h:
            return k
"""


def calculate_hours(piles, k):
    total_hours = 0

    for pile in piles:
        total_hours += (pile + k - 1) // k

    return total_hours


def koko_brute(piles, h):
    max_pile = max(piles)

    for k in range(1, max_pile + 1):
        if calculate_hours(piles, k) <= h:
            return k

    return -1


# Time:  O(n * max(piles))
# Space: O(1)


# ============================================================
# 2. OPTIMAL — BINARY SEARCH ON ANSWER
# ============================================================
"""
Key observation:

Minimum possible speed = 1
Maximum possible speed = max(piles)

For a speed k:

    if total_hours <= h:
        k works
        -> try a smaller speed
        -> high = mid - 1

    else:
        k is too slow
        -> try a larger speed
        -> low = mid + 1

Pseudocode:

function koko_optimal(piles, h):
    low = 1
    high = max(piles)

    while low <= high:
        mid = (low + high) // 2
        total_hours = calculate_hours(piles, mid)

        if total_hours <= h:
            high = mid - 1
        else:
            low = mid + 1

    return low
"""


def koko_optimal(piles, h):
    low = 1
    high = max(piles)

    while low <= high:
        mid = (low + high) // 2
        total_hours = calculate_hours(piles, mid)

        if total_hours <= h:
            high = mid - 1
        else:
            low = mid + 1

    return low


# Time:  O(n * log(max(piles)))
# Space: O(1)


# ============================================================
# 3. QUICK TEST
# ============================================================

if __name__ == "__main__":
    piles = [3, 6, 7, 11]
    h = 8

    print("Brute:", koko_brute(piles, h))
    print("Optimal:", koko_optimal(piles, h))

    # Expected:
    # Brute: 4
    # Optimal: 4


"""
============================================================
PATTERN TO REMEMBER
============================================================

We are NOT binary-searching the array.

We are binary-searching the ANSWER (eating speed).

Search space:
    [1 ... max(piles)]

Condition:
    can Koko finish within h hours?

Monotonic behaviour:

    smaller speed -> more hours
    larger speed  -> fewer hours

So:

    feasible -> move LEFT
    not feasible -> move RIGHT

This is the classic "Binary Search on Answers" pattern.
"""
