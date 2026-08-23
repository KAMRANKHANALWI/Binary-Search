# ============================================================
# FIRST AND LAST OCCURRENCE
# ============================================================
#
# Given a sorted array with duplicates, find the first and
# last occurrence of x.
#
# Example:
#   arr = [1, 2, 4, 4, 4, 7, 9]
#   x = 4
#
#   Answer = (2, 4)
#
# ============================================================
#
# APPROACHES
#
# 1. Brute Force:
#      Scan the array once.
#      Time: O(n), Space: O(1)
#
# 2. Binary Search (Optimal):
#      First occurrence → found → go LEFT
#      Last occurrence  → found → go RIGHT
#      Time: O(log n), Space: O(1)
#
# 3. Bound Approach:
#      First = Lower Bound(x)
#      Last  = Upper Bound(x) - 1
#      Time: O(log n), Space: O(1)
#
# ============================================================


# ============================================================
# 1. BRUTE FORCE
# ============================================================
#
# PSEUDOCODE:
#
#   first = -1
#   last = -1
#
#   for every index i:
#       if arr[i] == x:
#           if first == -1:
#               first = i
#           last = i
#
#   return (first, last)
#
# ============================================================


def first_and_last_brute(arr, x):
    """Return first and last occurrence using linear search."""

    first = -1
    last = -1

    for i in range(len(arr)):

        if arr[i] == x:

            # First time we see x.
            if first == -1:
                first = i

            # Keep updating → eventually becomes last.
            last = i

    return first, last


# ============================================================
# 2. BINARY SEARCH — OPTIMAL
# ============================================================
#
# Core idea:
#
#   FIRST:
#       x found → store index → search LEFT
#
#   LAST:
#       x found → store index → search RIGHT
#
# ============================================================


def first_occurrence(arr, x):
    """Return the first index of x, otherwise -1."""

    low = 0
    high = len(arr) - 1
    first = -1

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] == x:
            first = mid

            # x found, but an earlier x may exist.
            high = mid - 1

        elif arr[mid] < x:
            # x must be on the right.
            low = mid + 1

        else:
            # x must be on the left.
            high = mid - 1

    return first


def last_occurrence(arr, x):
    """Return the last index of x, otherwise -1."""

    low = 0
    high = len(arr) - 1
    last = -1

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] == x:
            last = mid

            # x found, but a later x may exist.
            low = mid + 1

        elif arr[mid] < x:
            # x must be on the right.
            low = mid + 1

        else:
            # x must be on the left.
            high = mid - 1

    return last


def first_and_last(arr, x):
    """Return (first occurrence, last occurrence)."""

    first = first_occurrence(arr, x)

    # If x doesn't exist, don't search for last.
    if first == -1:
        return -1, -1

    last = last_occurrence(arr, x)

    return first, last


# ============================================================
# 3. LOWER / UPPER BOUND APPROACH
# ============================================================
#
# Connection:
#
#   Lower Bound = first index where arr[i] >= x
#   Upper Bound = first index where arr[i] >  x
#
# Therefore:
#
#   First occurrence = Lower Bound(x)
#   Last occurrence  = Upper Bound(x) - 1
#
# PSEUDOCODE:
#
#   first = lower_bound(arr, x)
#
#   if first == len(arr) OR arr[first] != x:
#       return (-1, -1)
#
#   last = upper_bound(arr, x) - 1
#
#   return (first, last)
#
# ============================================================


def lower_bound(arr, x):
    """Return first index where arr[i] >= x."""

    low = 0
    high = len(arr)

    while low < high:

        mid = low + (high - low) // 2

        if arr[mid] >= x:
            high = mid
        else:
            low = mid + 1

    return low


def upper_bound(arr, x):
    """Return first index where arr[i] > x."""

    low = 0
    high = len(arr)

    while low < high:

        mid = low + (high - low) // 2

        if arr[mid] > x:
            high = mid
        else:
            low = mid + 1

    return low


def first_and_last_using_bounds(arr, x):
    """Find first and last occurrence using bounds."""

    first = lower_bound(arr, x)

    # x does not exist.
    if first == len(arr) or arr[first] != x:
        return -1, -1

    last = upper_bound(arr, x) - 1

    return first, last


# ============================================================
# COMPLEXITY
# ============================================================
#
# Brute Force:
#   Time  = O(n)
#   Space = O(1)
#
# Binary Search:
#   Time  = O(log n)
#   Space = O(1)
#
# Bound Approach:
#   Time  = O(log n)
#   Space = O(1)
#
# ============================================================


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    arr = [1, 2, 4, 4, 4, 7, 9]

    print("Array:", arr)

    # Brute Force
    print("Brute Force:", first_and_last_brute(arr, 4))

    # Optimal Binary Search
    print("Binary Search:", first_and_last(arr, 4))

    # Lower/Upper Bound
    print("Using Bounds:", first_and_last_using_bounds(arr, 4))

    print("\nEdge Cases:")

    print("First element:", first_and_last(arr, 1))
    print("Last element:", first_and_last(arr, 9))
    print("Not found:", first_and_last(arr, 5))
    print("Single element:", first_and_last([4], 4))
    print("All same:", first_and_last([4, 4, 4, 4], 4))
