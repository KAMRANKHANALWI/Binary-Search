# ============================================================
# SEARCH X IN SORTED ARRAY
# ============================================================
#
# Given a sorted array, find the index of x.
# Return -1 if x does not exist.
#
# Pattern:
#   Exact search → basic Binary Search
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def search_x(arr, x):
    """Return any index of x if found, otherwise -1."""

    low = 0
    high = len(arr) - 1

    while low <= high:

        mid = low + (high - low) // 2

        if arr[mid] == x:
            return mid

        elif arr[mid] < x:
            low = mid + 1

        else:
            high = mid - 1

    return -1


# ============================================================
# Example
# ============================================================
#
# arr = [1, 3, 5, 7, 9]
# x   = 7
#
# Answer → 3
#
# If duplicates exist, any occurrence is acceptable unless
# the problem specifically asks for first/last occurrence.
# ============================================================


if __name__ == "__main__":

    arr = [1, 3, 5, 7, 9, 11]

    print(search_x(arr, 7))    # 3
    print(search_x(arr, 10))   # -1