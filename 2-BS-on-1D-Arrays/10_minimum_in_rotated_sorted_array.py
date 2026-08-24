# ============================================================
# 10 — MINIMUM IN ROTATED SORTED ARRAY
# ============================================================
#
# Sorted array is rotated.
# Elements are UNIQUE.
#
# Example:
#   arr = [4, 5, 6, 7, 0, 1, 2]
#   Answer = 0
#
# Two binary-search approaches:
#
# 1. Track answer:
#       Find a sorted half.
#       Its minimum is known.
#       Store it in ans.
#
# 2. No ans variable:
#       Eliminate the half that cannot contain the minimum.
#       Keep the minimum inside [low, high].
#       When low == high, that index is the answer.
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


# ============================================================
# APPROACH 1 — WITH ans
# ============================================================
#
# If left half is sorted:
#   arr[low] is the minimum of that half.
#   Save it and search right.
#
# Otherwise:
#   Minimum is in the left half, including mid.
#   Save arr[mid] and search left.
#
# ------------------------------------------------------------


def find_min_with_ans(arr):

    low = 0
    high = len(arr) - 1
    ans = float("inf")

    while low <= high:

        mid = low + (high - low) // 2

        # Left half is sorted
        if arr[low] <= arr[mid]:

            ans = min(ans, arr[low])

            # Minimum cannot be in this sorted half
            # except for arr[low], which we already saved.
            low = mid + 1

        else:

            # Rotation point / minimum is in left half.
            ans = min(ans, arr[mid])

            high = mid - 1

    return ans


# ============================================================
# APPROACH 2 — WITHOUT ans ⭐
# ============================================================
#
# Instead of remembering the minimum:
#   Keep the minimum inside [low, high].
#
# If arr[mid] > arr[high]:
#   Minimum must be on the right.
#
# Else:
#   Minimum is at mid or on the left.
#
# Eventually:
#   low == high
#   arr[low] is the minimum.
#
# ------------------------------------------------------------


def find_min(arr):

    low = 0
    high = len(arr) - 1

    while low < high:

        mid = low + (high - low) // 2

        if arr[mid] > arr[high]:

            # Minimum is on the right.
            low = mid + 1

        else:

            # Minimum is at mid or on the left.
            high = mid

    return arr[low]


# ============================================================
# QUICK PSEUDOCODE — WITH ans
# ============================================================
#
# low = 0
# high = n - 1
# ans = INF
#
# while low <= high:
#     mid = middle
#
#     if left half is sorted:
#         ans = min(ans, arr[low])
#         low = mid + 1
#
#     else:
#         ans = min(ans, arr[mid])
#         high = mid - 1
#
# return ans
#
#
# ============================================================
# QUICK PSEUDOCODE — WITHOUT ans
# ============================================================
#
# low = 0
# high = n - 1
#
# while low < high:
#     mid = middle
#
#     if arr[mid] > arr[high]:
#         low = mid + 1
#     else:
#         high = mid
#
# return arr[low]
#
#
# ============================================================
# EXAMPLES
# ============================================================

if __name__ == "__main__":

    test_cases = [
        [4, 5, 6, 7, 0, 1, 2],
        [3, 4, 5, 1, 2],
        [11, 13, 15, 17],
        [2, 1],
        [1],
    ]

    for arr in test_cases:
        print(arr)
        print("with ans   :", find_min_with_ans(arr))
        print("without ans:", find_min(arr))
        print()
