# ============================================================
# BINARY SEARCH — ITERATIVE
# ============================================================
#
# Goal:
#   Find the index of a target in a SORTED array.
#
# Core Idea:
#   Compare target with the middle element.
#   Eliminate the half that cannot contain the target.
#
# Pattern:
#
#   compare → eliminate half → repeat
#
# Time Complexity:  O(log n)
# Space Complexity: O(1)
#
# ============================================================


# ============================================================
# 1. PROBLEM STATEMENT
# ============================================================
#
# Given a sorted array and a target, return the index of target.
# Return -1 if target does not exist.
#
# Example:
#
#   arr    = [2, 5, 8, 12, 16, 23, 38]
#   target = 23
#
#   Answer = 5
#
# IMPORTANT:
#   Binary Search requires the search space to be sorted.
#
# ============================================================


# ============================================================
# 2. INTUITION
# ============================================================
#
# Instead of checking every element one by one like Linear
# Search, Binary Search looks at the middle.
#
# Example:
#
#   [2, 5, 8, 12, 16, 23, 38]
#              ↑
#             mid
#
# If:
#
#   arr[mid] == target → FOUND
#
#   arr[mid] < target
#       → target must be on the RIGHT
#
#   arr[mid] > target
#       → target must be on the LEFT
#
# Because the array is sorted, we can safely eliminate HALF
# of the search space after every comparison.
#
# ============================================================


# ============================================================
# 3. LOW, HIGH AND MID
# ============================================================
#
# `low`  → first index of current search space
# `high` → last index of current search space
#
# Initially, the whole array is the search space:
#
#   low                         high
#    ↓                            ↓
#   [2, 5, 8, 12, 16, 23, 38]
#
# We calculate:
#
#   mid = low + (high - low) // 2
#
# Example:
#
#   low  = 4
#   high = 10
#
#   mid = 4 + (10 - 4) // 2
#       = 4 + 6 // 2
#       = 7
#
# NOTE:
#   This does NOT cancel `low`.
#   The `low` outside the parentheses is still added.
#
# `(low + high) // 2` also gives the same midpoint in Python.
#
# The low + (high - low) // 2 form avoids integer overflow
# in languages with fixed-size integers such as C++/Java.
#
# ============================================================


# ============================================================
# 4. BRUTE FORCE — LINEAR SEARCH
# ============================================================
#
# Check every element one by one.
#
# Time:  O(n)
# Space: O(1)
#
# ============================================================


def linear_search(arr, target):
    """Return target's index using Linear Search, else -1."""

    for i in range(len(arr)):
        if arr[i] == target:
            return i

    return -1


# ============================================================
# 5. OPTIMAL — ITERATIVE BINARY SEARCH
# ============================================================
#
# Search space:
#
#       [low ................. high]
#
# Every iteration:
#
#   1. Find mid.
#   2. Compare arr[mid] with target.
#   3. Eliminate one half.
#
# ============================================================


def binary_search(arr, target):
    """
    Return target's index in a sorted array.
    Return -1 if target is not present.
    """

    # Initial search space = entire array.
    low = 0
    high = len(arr) - 1

    # `<=` is important because when low == high,
    # one valid element is still left to check.
    while low <= high:

        # Find the middle of the current search space.
        mid = low + (high - low) // 2

        # Case 1: Target found.
        if arr[mid] == target:
            return mid

        # Case 2: Target must be on the right.
        elif arr[mid] < target:
            low = mid + 1

        # Case 3: Target must be on the left.
        else:
            high = mid - 1

    # Search space became empty → target not found.
    return -1


# ============================================================
# 6. DRY RUN
# ============================================================
#
# arr    = [2, 5, 8, 12, 16, 23, 38]
# target = 23
#
# Iteration 1:
#
#   low = 0, high = 6
#   mid = 0 + (6 - 0) // 2 = 3
#   arr[mid] = 12
#
#   12 < 23
#   → target must be RIGHT
#   → low = 4
#
#
# Iteration 2:
#
#   low = 4, high = 6
#   mid = 4 + (6 - 4) // 2 = 5
#   arr[mid] = 23
#
#   23 == 23
#   → FOUND at index 5
#
# ============================================================


# ============================================================
# 7. WHY O(log n)?
# ============================================================
#
# Search space gets roughly divided by 2 each time:
#
#   n
#   n/2
#   n/4
#   n/8
#   ...
#   1
#
# Therefore:
#
#   Time  = O(log n)
#   Space = O(1)
#
# ============================================================


# ============================================================
# 8. IMPORTANT EDGE CASES
# ============================================================
#
# Empty array:
#   [] → -1
#
# Single element:
#   [10], target=10 → 0
#
# Target absent:
#   [2, 5, 8], target=7 → -1
#
# Target at first/last position:
#   Both are handled naturally.
#
# ============================================================


# ============================================================
# 9. KEY TAKEAWAY
# ============================================================
#
# Binary Search is basically:
#
#       while search space exists:
#
#           find middle
#
#           if target == middle:
#               FOUND
#
#           elif target > middle:
#               search RIGHT
#
#           else:
#               search LEFT
#
#
# Golden Pattern:
#
#   low = 0
#   high = len(arr) - 1
#
#   while low <= high:
#       mid = low + (high - low) // 2
#
# ============================================================


# ============================================================
# 10. TESTING
# ============================================================

if __name__ == "__main__":

    arr = [2, 5, 8, 12, 16, 23, 38]

    print("Array:", arr)

    print("\nLinear Search:")
    print("23 →", linear_search(arr, 23))
    print("10 →", linear_search(arr, 10))

    print("\nBinary Search:")
    print("23 →", binary_search(arr, 23))
    print("10 →", binary_search(arr, 10))

    print("\nEdge Cases:")
    print("Empty array →", binary_search([], 10))
    print("First element →", binary_search([10, 20, 30], 10))
    print("Last element →", binary_search([10, 20, 30], 30))
    print("Single element →", binary_search([10], 10))