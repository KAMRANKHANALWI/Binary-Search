# ============================================================
# COUNT OCCURRENCES
# ============================================================
#
# Given a sorted array with duplicates, count how many times
# x occurs.
#
# Example:
#   arr = [2, 4, 6, 8, 8, 8, 11, 13]
#   x = 8
#
#   Answer = 3
#
# Key idea:
#   count = last - first + 1
#
# Or using bounds:
#   count = upper_bound(x) - lower_bound(x)
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


# ============================================================
# 1. BRUTE FORCE
# ============================================================
#
# PSEUDOCODE:
#
#   count = 0
#
#   for every element:
#       if element == x:
#           count += 1
#
#   return count
#
# Time: O(n)
# ============================================================


def count_brute(arr, x):
    """Count x using linear search."""

    count = 0

    for num in arr:
        if num == x:
            count += 1

    return count


# ============================================================
# 2. BINARY SEARCH — OPTIMAL
# ============================================================
#
# Find first and last occurrence using Binary Search.
#
#   First → found → go LEFT
#   Last  → found → go RIGHT
#
# Then:
#
#   count = last - first + 1
# ============================================================


def first_occurrence(arr, x):
    """Return first index of x, otherwise -1."""

    low = 0
    high = len(arr) - 1
    first = -1

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] == x:
            first = mid
            high = mid - 1

        elif arr[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return first


def last_occurrence(arr, x):
    """Return last index of x, otherwise -1."""

    low = 0
    high = len(arr) - 1
    last = -1

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] == x:
            last = mid
            low = mid + 1

        elif arr[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return last


def count_occurrences(arr, x):
    """Return number of occurrences of x."""

    first = first_occurrence(arr, x)

    # x does not exist.
    if first == -1:
        return 0

    last = last_occurrence(arr, x)

    return last - first + 1


# ============================================================
# 3. BOUND APPROACH
# ============================================================
#
# Lower Bound = first index where arr[i] >= x
# Upper Bound = first index where arr[i] >  x
#
# Therefore:
#
#   count = upper_bound(x) - lower_bound(x)
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


def count_using_bounds(arr, x):
    """Count x using Lower Bound and Upper Bound."""

    return upper_bound(arr, x) - lower_bound(arr, x)


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
# ============================================================


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    arr = [2, 4, 6, 8, 8, 8, 11, 13]

    print("Array:", arr)

    print("Brute Force:", count_brute(arr, 8))
    print("Binary Search:", count_occurrences(arr, 8))
    print("Using Bounds:", count_using_bounds(arr, 8))

    print("\nEdge Cases:")

    print("Not found:", count_occurrences(arr, 5))
    print("Single occurrence:", count_occurrences(arr, 6))
    print("All same:", count_occurrences([8, 8, 8, 8], 8))
    print("Empty:", count_occurrences([], 8))
