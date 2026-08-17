# ============================================================
# UPPER BOUND
# ============================================================
#
# Upper Bound = first index i such that:
#
#       arr[i] > x
#
# If no such index exists, return len(arr).
#
# Example:
#   arr = [1, 2, 4, 4, 6, 8]
#   x = 4
#
#   Answer = 4
#
# Pattern:
#   Found a possible answer → store it → search LEFT
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def upper_bound(arr, x):
    """Return first index where arr[index] > x."""

    low = 0
    high = len(arr) - 1

    # Stores the best valid position found so far.
    ans = len(arr)

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] > x:
            # mid could be the answer.
            ans = mid

            # Look for an earlier position.
            high = mid - 1

        else:
            # arr[mid] <= x → need a larger value.
            low = mid + 1

    return ans


# ============================================================
# Examples
# ============================================================
#
# [1, 2, 4, 4, 6, 8]
#
# x = 4  → 4
# x = 5  → 4
# x = 8  → 6
# x = 0  → 0
#
# Key idea:
#
#   arr[mid] > x  → possible answer → move LEFT
#   arr[mid] <= x → move RIGHT
#
# ============================================================


if __name__ == "__main__":

    arr = [1, 2, 4, 4, 6, 8]

    print(upper_bound(arr, 4))  # 4
    print(upper_bound(arr, 5))  # 4
    print(upper_bound(arr, 8))  # 6
    print(upper_bound(arr, 0))  # 0