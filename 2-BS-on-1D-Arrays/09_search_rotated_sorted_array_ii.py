# ============================================================
# SEARCH IN ROTATED SORTED ARRAY II
# ============================================================
#
# Sorted array is rotated.
# Duplicates ARE allowed.
#
# Example:
#   arr = [2, 5, 6, 0, 0, 1, 2]
#   x = 0
#   Answer = True
#
# Key idea:
#   1. Find which half is sorted.
#   2. Check whether x belongs to that half.
#   3. Duplicates can make both halves look identical.
#      → shrink both ends.
#
# Time:  O(log n) average, O(n) worst case
# Space: O(1)
# ============================================================


def search(arr, x):
    low = 0
    high = len(arr) - 1

    while low <= high:

        mid = low + (high - low) // 2

        # Found target
        if arr[mid] == x:
            return True

        # Cannot determine which half is sorted
        # because all three values are equal.
        if arr[low] == arr[mid] == arr[high]:
            low += 1
            high -= 1
            continue

        # Left half is sorted
        if arr[low] <= arr[mid]:

            # Target lies in sorted left half
            if arr[low] <= x <= arr[mid]:
                high = mid - 1
            else:
                low = mid + 1

        # Right half is sorted
        else:

            # Target lies in sorted right half
            if arr[mid] <= x <= arr[high]:
                low = mid + 1
            else:
                high = mid - 1

    return False


# ============================================================
# EXAMPLES
# ============================================================

if __name__ == "__main__":

    print(search([2, 5, 6, 0, 0, 1, 2], 0))  # True
    print(search([2, 5, 6, 0, 0, 1, 2], 3))  # False
    print(search([1, 0, 1, 1, 1], 0))         # True
    print(search([1, 1, 1, 1, 1], 2))         # False