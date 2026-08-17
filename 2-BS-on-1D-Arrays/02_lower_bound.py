# ============================================================
# LOWER BOUND
# ============================================================
#
# Lower Bound = first index i such that:
#
#       arr[i] >= x
#
# If no such index exists, return len(arr).
#
# Example:
#   arr = [1, 2, 4, 4, 6, 8]
#   x = 4
#
#   Answer = 2
#
# Pattern:
#   Found a possible answer → store it → search LEFT
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def lower_bound(arr, x):
    """Return first index where arr[index] >= x."""

    low = 0
    high = len(arr) - 1

    # `ans` stores the best valid position found so far.
    ans = len(arr)

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] >= x:
            # mid could be the answer.
            ans = mid

            # But there may be an earlier valid position.
            high = mid - 1

        else:
            # arr[mid] < x → need a larger value.
            low = mid + 1

    return ans


# ============================================================
# Examples
# ============================================================
#
# [1, 2, 4, 4, 6, 8]
#
# x = 4  → 2
# x = 5  → 4
# x = 9  → 6  (no valid index)
# x = 0  → 0
#
# Key idea:
#
#   arr[mid] >= x → possible answer → move LEFT
#   arr[mid] <  x → move RIGHT
# ============================================================


if __name__ == "__main__":

    arr = [1, 2, 4, 4, 6, 8]

    print(lower_bound(arr, 4))  # 2
    print(lower_bound(arr, 5))  # 4
    print(lower_bound(arr, 9))  # 6
    print(lower_bound(arr, 0))  # 0