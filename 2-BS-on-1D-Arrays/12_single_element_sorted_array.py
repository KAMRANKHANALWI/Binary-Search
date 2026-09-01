# ============================================================
# 12 — SINGLE ELEMENT IN SORTED ARRAY
# ============================================================
#
# Every element appears twice except one element.
# Array is sorted.
#
# Example:
#   arr = [1, 1, 2, 2, 3, 4, 4, 5, 5]
#   Answer = 3
#
# Key observation:
#   Before the single element:
#       even index -> pair with right
#       odd index  -> pair with left
#
#   After the single element:
#       this pattern breaks.
#
# Approaches:
#   1. Brute force      -> O(n)
#   2. Binary search    -> O(log n)
#
# Space: O(1)
# ============================================================


# ============================================================
# APPROACH 1 — BRUTE FORCE
# ============================================================
#
# Check every element.
#
# First and last elements need separate checks.
# For every middle element:
#   if it differs from both neighbours,
#   it is the single element.
#
# Time:  O(n)
# Space: O(1)
#
# ------------------------------------------------------------
# PSEUDOCODE
#
# n = length of arr
#
# if n == 1:
#     return arr[0]
#
# if arr[0] != arr[1]:
#     return arr[0]
#
# if arr[n - 1] != arr[n - 2]:
#     return arr[n - 1]
#
# for i = 1 to n - 2:
#
#     if arr[i] != arr[i - 1] AND arr[i] != arr[i + 1]:
#         return arr[i]
#
# return -1
# ------------------------------------------------------------


def single_non_duplicate_brute(arr):

    n = len(arr)

    if n == 1:
        return arr[0]

    if arr[0] != arr[1]:
        return arr[0]

    if arr[n - 1] != arr[n - 2]:
        return arr[n - 1]

    for i in range(1, n - 1):

        if arr[i] != arr[i - 1] and arr[i] != arr[i + 1]:
            return arr[i]

    return -1


# ============================================================
# APPROACH 2 — BINARY SEARCH ⭐
# ============================================================
#
# Before the single element:
#
#   even index -> pair with right
#   odd index  -> pair with left
#
# Example:
#   (0,1) (2,3) (4,5) ...
#
# After the single element, this pairing pattern breaks.
#
# If the expected pairing is correct:
#   single element is on the RIGHT.
#
# If the pairing is broken:
#   single element is on the LEFT.
#
# Time:  O(log n)
# Space: O(1)
#
# ------------------------------------------------------------
# PSEUDOCODE
#
# n = length of arr
#
# if n == 1:
#     return arr[0]
#
# if arr[0] != arr[1]:
#     return arr[0]
#
# if arr[n - 1] != arr[n - 2]:
#     return arr[n - 1]
#
# low = 1
# high = n - 2
#
# while low <= high:
#
#     mid = middle of low and high
#
#     if arr[mid] != arr[mid - 1]
#        AND arr[mid] != arr[mid + 1]:
#
#         return arr[mid]
#
#     if (mid is even AND arr[mid] == arr[mid + 1])
#        OR
#        (mid is odd AND arr[mid] == arr[mid - 1]):
#
#         # Pairing is correct
#         # Single is on the right
#         low = mid + 1
#
#     else:
#
#         # Pairing is broken
#         # Single is on the left
#         high = mid - 1
#
# return -1
# ------------------------------------------------------------


def single_non_duplicate(arr):

    n = len(arr)

    if n == 1:
        return arr[0]

    if arr[0] != arr[1]:
        return arr[0]

    if arr[n - 1] != arr[n - 2]:
        return arr[n - 1]

    low = 1
    high = n - 2

    while low <= high:

        mid = low + (high - low) // 2

        # Single element found
        if arr[mid] != arr[mid - 1] and arr[mid] != arr[mid + 1]:
            return arr[mid]

        # Pairing is correct -> single is on the right
        if (mid % 2 == 0 and arr[mid] == arr[mid + 1]) or (
            mid % 2 == 1 and arr[mid] == arr[mid - 1]
        ):

            low = mid + 1

        # Pairing is broken -> single is on the left
        else:
            high = mid - 1

    return -1


# ============================================================
# EXAMPLES
# ============================================================

if __name__ == "__main__":

    test_cases = [
        [1, 1, 2, 2, 3, 4, 4, 5, 5],
        [1, 1, 2, 3, 3, 4, 4],
        [1, 1, 2, 2, 3],
        [1],
        [1, 2, 2, 3, 3],
    ]

    for arr in test_cases:

        print(arr)
        print("brute  :", single_non_duplicate_brute(arr))
        print("optimal:", single_non_duplicate(arr))
        print()
