# 13_median_of_two_sorted_arrays.py

# ============================================================
# Median of Two Sorted Arrays of Different Sizes
# ============================================================
#
# Goal:
# Find the median of two sorted arrays.
#
# Approaches:
# 1. Brute    -> Merge completely
# 2. Better   -> Merge only until the middle
# 3. Optimal  -> Binary Search on the partition
#
# Example:
# a = [1, 3, 4, 7, 10, 12]
# b = [2, 3, 6, 15]
#
# Combined:
# [1, 2, 3, 3, 4, 6, 7, 10, 12, 15]
#
# Median = (4 + 6) / 2 = 5
# ============================================================


# ============================================================
# APPROACH 1: BRUTE FORCE
# ============================================================
#
# Pattern:
# Merge two sorted arrays.
#
# Intuition:
# Since both arrays are sorted, use two pointers and build
# the complete sorted array.
#
# Then directly access the middle element(s).
#
# Time  : O(n1 + n2)
# Space : O(n1 + n2)
# ============================================================

def median_brute(a, b):
    merged = []

    i = 0
    j = 0

    n1 = len(a)
    n2 = len(b)

    # Merge while both arrays have elements
    while i < n1 and j < n2:

        if a[i] <= b[j]:
            merged.append(a[i])
            i += 1

        else:
            merged.append(b[j])
            j += 1

    # Add remaining elements of a
    while i < n1:
        merged.append(a[i])
        i += 1

    # Add remaining elements of b
    while j < n2:
        merged.append(b[j])
        j += 1

    n = n1 + n2

    # Odd -> one middle element
    if n % 2 == 1:
        return float(merged[n // 2])

    # Even -> average of two middle elements
    return (merged[n // 2 - 1] + merged[n // 2]) / 2.0


# ============================================================
# APPROACH 2: BETTER
# ============================================================
#
# Pattern:
# Two-pointer merge, but don't store the merged array.
#
# Key observation:
# We only need the middle element(s), not every element.
#
# Therefore maintain:
#
# prev -> previous element in merged order
# curr -> current element in merged order
#
# Time  : O(n1 + n2)
# Space : O(1)
# ============================================================

def median_better(a, b):
    n1 = len(a)
    n2 = len(b)
    n = n1 + n2

    i = 0
    j = 0

    prev = 0
    curr = 0

    # We only need to reach the middle
    for _ in range(n // 2 + 1):

        prev = curr

        # Pick the smaller current element
        if i < n1 and (j >= n2 or a[i] <= b[j]):
            curr = a[i]
            i += 1

        else:
            curr = b[j]
            j += 1

    # Odd:
    # curr is the middle element
    if n % 2 == 1:
        return float(curr)

    # Even:
    # prev and curr are the two middle elements
    return (prev + curr) / 2.0


# ============================================================
# APPROACH 3: OPTIMAL
# ============================================================
#
# Pattern:
# Binary Search on the partition.
#
# IMPORTANT:
# We are NOT binary-searching for the median.
#
# We are binary-searching for the CORRECT PARTITION.
#
#
# Suppose:
#
# A = [1, 3, 4 | 7, 10, 12]
# B = [2, 3    | 6, 15]
#
# Left side contains the required number of elements.
#
# We need:
#
# L1 <= R2
# L2 <= R1
#
# where:
#
# L1 = largest element on left of A
# R1 = smallest element on right of A
#
# L2 = largest element on left of B
# R2 = smallest element on right of B
#
#
# Time  : O(log(min(n1, n2)))
# Space : O(1)
# ============================================================

def median_optimal(a, b):

    # --------------------------------------------------------
    # Step 1: Binary search the smaller array
    # --------------------------------------------------------
    if len(a) > len(b):
        a, b = b, a

    n1 = len(a)
    n2 = len(b)

    total = n1 + n2

    # Number of elements required on the left side
    left_size = (total + 1) // 2

    # We are choosing how many elements to take from A
    #
    # Possible choices:
    # 0, 1, 2, ..., n1
    low = 0
    high = n1

    while low <= high:

        # ----------------------------------------------------
        # Step 2: Choose partition in A
        # ----------------------------------------------------
        cut1 = (low + high) // 2

        # Remaining elements required from B
        cut2 = left_size - cut1

        # ----------------------------------------------------
        # Step 3: Find the four boundary values
        # ----------------------------------------------------

        # A:
        # [ LEFT | RIGHT ]
        #
        # If cut1 == 0, there is nothing on A's left.
        L1 = float("-inf") if cut1 == 0 else a[cut1 - 1]

        # If cut1 == n1, there is nothing on A's right.
        R1 = float("inf") if cut1 == n1 else a[cut1]

        # B:
        # [ LEFT | RIGHT ]

        L2 = float("-inf") if cut2 == 0 else b[cut2 - 1]

        R2 = float("inf") if cut2 == n2 else b[cut2]

        # ----------------------------------------------------
        # Step 4: Check whether partition is correct
        # ----------------------------------------------------
        #
        # We need:
        #
        # L1 <= R2
        # L2 <= R1
        #
        # If both are true:
        #
        # everything on LEFT <= everything on RIGHT
        #
        # Therefore this is the correct partition.

        if L1 <= R2 and L2 <= R1:

            # ------------------------------------------------
            # Step 5: Calculate median
            # ------------------------------------------------

            # Odd number of elements:
            #
            # left side has one extra element.
            #
            # Therefore median = largest element on LEFT.
            if total % 2 == 1:
                return float(max(L1, L2))

            # Even number of elements:
            #
            # left-middle  = max(L1, L2)
            # right-middle = min(R1, R2)
            #
            # Median = average of both.
            left_middle = max(L1, L2)
            right_middle = min(R1, R2)

            return (left_middle + right_middle) / 2.0

        # ----------------------------------------------------
        # Step 6: Adjust binary search
        # ----------------------------------------------------

        # L1 > R2
        #
        # Too many elements were taken from A.
        #
        # Move A's partition LEFT.
        elif L1 > R2:
            high = cut1 - 1

        # L2 > R1
        #
        # Too few elements were taken from A.
        #
        # Need more elements from A.
        #
        # Move A's partition RIGHT.
        else:
            low = cut1 + 1

    # Valid sorted input should always find a partition.
    raise ValueError("Input arrays must be sorted")


# ============================================================
# QUICK TESTING
# ============================================================

a = [1, 3, 4, 7, 10, 12]
b = [2, 3, 6, 15]

print("Brute   :", median_brute(a, b))
print("Better  :", median_better(a, b))
print("Optimal :", median_optimal(a, b))


# Expected:
#
# Brute   : 5.0
# Better  : 5.0
# Optimal : 5.0