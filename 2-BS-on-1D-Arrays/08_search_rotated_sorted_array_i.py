# ============================================================
# SEARCH IN ROTATED SORTED ARRAY I
# ============================================================
#
# Given a sorted array rotated at some pivot, find target.
#
# Example:
#   arr = [4, 5, 6, 7, 0, 1, 2]
#   x = 0
#
#   Answer = 4
#
# Key Idea:
#   At least ONE half is always sorted.
#
#   1. Find mid.
#   2. Identify the sorted half.
#   3. Check whether target lies in that half.
#   4. Search the appropriate half.
#
# Assumption:
#   All elements are distinct.
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def search(arr, x):
    """Return index of x, otherwise -1."""

    low = 0
    high = len(arr) - 1

    while low <= high:

        mid = low + (high - low) // 2

        # Target found.
        if arr[mid] == x:
            return mid

        # ----------------------------------------------------
        # LEFT HALF IS SORTED
        # ----------------------------------------------------
        if arr[low] <= arr[mid]:

            # Is x inside the sorted left half?
            if arr[low] <= x < arr[mid]:
                high = mid - 1
            else:
                low = mid + 1

        # ----------------------------------------------------
        # RIGHT HALF IS SORTED
        # ----------------------------------------------------
        else:

            # Is x inside the sorted right half?
            if arr[mid] < x <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return -1


# ============================================================
# QUICK PSEUDOCODE
# ============================================================
#
# while low <= high:
#
#     mid
#
#     if arr[mid] == x:
#         return mid
#
#     if left half is sorted:
#
#         if x lies in left range:
#             search left
#         else:
#             search right
#
#     else:
#         # right half is sorted
#
#         if x lies in right range:
#             search right
#         else:
#             search left
#
# return -1
#
# ============================================================


# ============================================================
# TESTING
# ============================================================

if __name__ == "__main__":

    arr = [4, 5, 6, 7, 0, 1, 2]

    print("Array:", arr)

    print("Target 0:", search(arr, 0))  # 4
    print("Target 6:", search(arr, 6))  # 2
    print("Target 3:", search(arr, 3))  # -1

    print("\nEdge Cases:")

    print("Single element:", search([5], 5))  # 0
    print("Not found:", search([5], 5 + 1))  # -1
    print("No rotation:", search([1, 2, 3, 4, 5], 4))  # 3
