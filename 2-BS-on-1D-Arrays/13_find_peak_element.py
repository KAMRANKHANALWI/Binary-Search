# 13_find_peak_element.py
# Find Peak Element
#
# A peak element is an element that is greater than its neighbors.
# For boundary elements, only the existing neighbor matters.
#
# Example:
# arr = [1, 2, 3, 4, 5, 6, 7, 8, 5, 1]
# Peak = 8 (index 7)


# ============================================================
# 1. BRUTE FORCE
# ============================================================
#
# Idea:
# Check every element one by one.
# If arr[i] is greater than both neighbors, return i.
#
# PSEUDOCODE
#
# function findPeakBrute(arr):
#     n = length(arr)
#
#     if n == 1:
#         return 0
#
#     if arr[0] > arr[1]:
#         return 0
#
#     if arr[n-1] > arr[n-2]:
#         return n-1
#
#     for i from 1 to n-2:
#         if arr[i] > arr[i-1] AND arr[i] > arr[i+1]:
#             return i
#
#     return -1
#
# Time:  O(n)
# Space: O(1)


def find_peak_brute(arr):
    n = len(arr)

    if n == 1:
        return 0

    if arr[0] > arr[1]:
        return 0

    if arr[n - 1] > arr[n - 2]:
        return n - 1

    for i in range(1, n - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            return i

    return -1


# ============================================================
# 2. OPTIMAL - BINARY SEARCH
# ============================================================
#
# Key observation:
#
# Look at mid and mid+1.
#
# Case 1:
#     arr[mid] < arr[mid+1]
#
#     We are going UPHILL.
#     Therefore, a peak must exist on the RIGHT side.
#
#     low = mid + 1
#
# Case 2:
#     arr[mid] > arr[mid+1]
#
#     We are going DOWNHILL.
#     Therefore, a peak exists at mid or on the LEFT side.
#
#     high = mid - 1
#
# We do NOT need to check both sides.
# One direction is guaranteed to contain a peak.
#
#
# PSEUDOCODE
#
# function findPeakOptimal(arr):
#     n = length(arr)
#
#     if n == 1:
#         return 0
#
#     if arr[0] > arr[1]:
#         return 0
#
#     if arr[n-1] > arr[n-2]:
#         return n-1
#
#     low = 1
#     high = n - 2
#
#     while low <= high:
#         mid = (low + high) // 2
#
#         if arr[mid] > arr[mid-1] AND arr[mid] > arr[mid+1]:
#             return mid
#
#         else if arr[mid] < arr[mid+1]:
#             low = mid + 1
#
#         else:
#             high = mid - 1
#
#     return -1
#
# Time:  O(log n)
# Space: O(1)


def find_peak_optimal(arr):
    n = len(arr)

    if n == 1:
        return 0

    # Check boundaries first so mid can safely use mid-1 and mid+1.
    if arr[0] > arr[1]:
        return 0

    if arr[n - 1] > arr[n - 2]:
        return n - 1

    low = 1
    high = n - 2

    while low <= high:
        mid = (low + high) // 2

        # Found a peak.
        if arr[mid] > arr[mid - 1] and arr[mid] > arr[mid + 1]:
            return mid

        # We are going uphill -> peak is on the right.
        elif arr[mid] < arr[mid + 1]:
            low = mid + 1

        # We are going downhill -> peak is on the left (or at mid).
        else:
            high = mid - 1

    return -1


# ============================================================
# 3. DRY RUN
# ============================================================
#
# arr = [1, 2, 3, 4, 5, 6, 7, 8, 5, 1]
#
# low = 1, high = 8
# mid = 4
# arr[4] = 5
# 5 < 6  -> uphill
# move RIGHT
# low = 5
#
# mid = 6
# arr[6] = 7
# 7 < 8  -> uphill
# move RIGHT
# low = 7
#
# mid = 7
# arr[7] = 8
# 8 > 7 AND 8 > 5
# PEAK FOUND
# return 7
#
# Answer = index 7


# ============================================================
# 4. TEST CASES
# ============================================================

test_cases = [
    [1, 2, 3, 4, 5, 6, 7, 8, 5, 1],
    [1, 2, 3, 1],
    [1],
    [2, 1],
    [1, 2],
]

for arr in test_cases:
    brute = find_peak_brute(arr)
    optimal = find_peak_optimal(arr)

    print(f"Array: {arr}")
    print(f"Brute:   index = {brute}, value = {arr[brute]}")
    print(f"Optimal: index = {optimal}, value = {arr[optimal]}")
    print()