# ============================================================
# SEARCH INSERT POSITION
# ============================================================
#
# Given a sorted array and x:
#   - Return x's index if it exists.
#   - Otherwise return the index where x should be inserted
#     to keep the array sorted.
#
# Key Observation:
#   Search Insert Position = Lower Bound
#   = first index where arr[i] >= x
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def search_insert_position(arr, x):
    """Return the index where x exists or should be inserted."""

    low = 0
    high = len(arr) - 1
    ans = len(arr)

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] >= x:
            # mid can be the insertion position.
            ans = mid

            # Look for an earlier valid position.
            high = mid - 1

        else:
            # arr[mid] is too small → move right.
            low = mid + 1

    return ans


if __name__ == "__main__":

    arr = [1, 3, 5, 6]

    print(search_insert_position(arr, 5))   # 2
    print(search_insert_position(arr, 2))   # 1
    print(search_insert_position(arr, 7))   # 4
    print(search_insert_position(arr, 0))   # 0