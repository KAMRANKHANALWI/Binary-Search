# ============================================================
# ARRAY ROTATION COUNT
# ============================================================
#
# In a rotated sorted array:
# index of minimum element = number of rotations
#
# Example:
# arr = [4, 5, 6, 7, 0, 1, 2]
# minimum = 0
# index = 4
# rotations = 4
#
# Time:  O(log n)
# Space: O(1)
# ============================================================


def rotation_count(arr):
    low = 0
    high = len(arr) - 1

    ans = float("inf")
    index = 0

    while low <= high:

        mid = low + (high - low) // 2

        # Search space is already sorted.
        # arr[low] is the minimum of this part.
        if arr[low] <= arr[high]:

            if arr[low] < ans:
                ans = arr[low]
                index = low

            break

        # Left half is sorted.
        if arr[low] <= arr[mid]:

            if arr[low] < ans:
                ans = arr[low]
                index = low

            low = mid + 1

        # Right half contains the minimum.
        else:

            high = mid - 1

            if arr[mid] < ans:
                ans = arr[mid]
                index = mid

    return index


# ============================================================
# EXAMPLES
# ============================================================

if __name__ == "__main__":

    print(rotation_count([4, 5, 6, 7, 0, 1, 2]))  # 4
    print(rotation_count([3, 4, 5, 1, 2]))        # 3
    print(rotation_count([1, 2, 3, 4, 5]))        # 0
    print(rotation_count([2, 3, 4, 5, 1]))        # 4
    

# Try do it with array containing duplicate 