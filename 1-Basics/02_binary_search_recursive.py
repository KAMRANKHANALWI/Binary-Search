# ============================================================
# BINARY SEARCH — RECURSIVE
# ============================================================
#
# Find target in a sorted array using recursion.
#
# Core idea:
#   Compare with mid → eliminate half → search remaining half.
#
# Time:  O(log n)
# Space: O(log n)  # Recursive call stack
#
# ============================================================


def binary_search(arr, low, high, target):
    """
    Recursive Binary Search.

    Returns target's index if found, otherwise -1.
    """

    # Base case: search space is empty.
    if low > high:
        return -1

    # Middle of the current search space.
    mid = low + (high - low) // 2

    # Target found.
    if arr[mid] == target:
        return mid

    # Target is larger → search right half.
    elif arr[mid] < target:
        return binary_search(arr, mid + 1, high, target)

    # Target is smaller → search left half.
    else:
        return binary_search(arr, low, mid - 1, target)


# ============================================================
# DRY RUN
# ============================================================
#
# arr    = [2, 5, 8, 12, 16, 23, 38]
# target = 23
#
# Call 1:
#   low=0, high=6 → mid=3 → arr[3]=12
#   12 < 23 → search right → (4, 6)
#
# Call 2:
#   low=4, high=6 → mid=5 → arr[5]=23
#   23 == 23 → return 5
#
# `return binary_search(...)` passes the result back through
# the recursive calls.
#
# ============================================================


# ============================================================
# ITERATIVE vs RECURSIVE
# ============================================================
#
# Iterative:
#   while loop → O(1) extra space
#
# Recursive:
#   function calls → O(log n) call-stack space
#
# The Binary Search logic itself is exactly the same.
#
# ============================================================


# ============================================================
# KEY TAKEAWAY
# ============================================================
#
# Iterative:
#   low = mid + 1
#   high = mid - 1
#
# Recursive:
#   binary_search(arr, mid + 1, high, target)
#   binary_search(arr, low, mid - 1, target)
#
# Recursion simply replaces the loop.
#
# ============================================================


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    arr = [2, 5, 8, 12, 16, 23, 38]

    print("Array:", arr)

    print("Target 23:", binary_search(arr, 0, len(arr) - 1, 23))
    print("Target 10:", binary_search(arr, 0, len(arr) - 1, 10))

    # Edge cases
    print("Empty:", binary_search([], 0, -1, 10))
    print("First:", binary_search([10, 20, 30], 0, 2, 10))
    print("Last:", binary_search([10, 20, 30], 0, 2, 30))