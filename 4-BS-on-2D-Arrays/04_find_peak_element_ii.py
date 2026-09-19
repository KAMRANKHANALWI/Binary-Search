# 04_find_peak_element_ii.py

# Find Peak Element - II | Binary Search on 2D
#
# A peak element is an element that is greater than:
#     1. left
#     2. right
#     3. top
#     4. bottom
#
# Outside the matrix is considered -1.
#
# We only need to return ANY one peak element.
#
# Example:
#
# matrix =
# [
#     [4, 2, 5, 1, 4, 5],
#     [2, 9, 3, 2, 3, 2],
#     [1, 7, 6, 0, 1, 3],
#     [3, 6, 2, 3, 7, 2]
# ]
#
# One possible peak = 9
#
# Output:
# [1, 1]


# ============================================================
# BRUTE FORCE
# ============================================================
#
# Visit every cell.
#
# For every cell:
#     Check left
#     Check right
#     Check top
#     Check bottom
#
# If current element is greater than all four:
#     return its coordinates
#
# Time  : O(n * m)
# Space : O(1)


def find_peak_brute(matrix):
    n = len(matrix)
    m = len(matrix[0])

    for row in range(n):
        for col in range(m):

            # Outside the matrix = -1
            left = matrix[row][col - 1] if col - 1 >= 0 else -1
            right = matrix[row][col + 1] if col + 1 < m else -1
            top = matrix[row - 1][col] if row - 1 >= 0 else -1
            bottom = matrix[row + 1][col] if row + 1 < n else -1

            if (
                matrix[row][col] > left
                and matrix[row][col] > right
                and matrix[row][col] > top
                and matrix[row][col] > bottom
            ):
                return [row, col]

    return [-1, -1]



# ============================================================
# OPTIMAL
# ============================================================
#
# Binary Search on COLUMNS.
#
# Instead of checking every element:
#
#     low = 0
#     high = m - 1
#
# Take middle column.
#
# Find the MAXIMUM element in this column.
#
# Suppose max element is at:
#
#     (max_row, mid)
#
# Because it is the maximum in its column:
#
#     top < current
#     bottom < current
#
# So we only need to check:
#
#     left
#     right
#
#
# CASE 1:
#
# current > left AND current > right
#
#     => current is a peak
#
#
# CASE 2:
#
# current < left
#
#     => left side contains a possible peak
#     => move left
#
#     high = mid - 1
#
#
# CASE 3:
#
# current < right
#
#     => right side contains a possible peak
#     => move right
#
#     low = mid + 1
#
#
# Time  : O(n * log m)
# Space : O(1)


def find_max_row(matrix, n, col):
    """
    Find the row index of the maximum
    element in a given column.
    """

    max_value = float("-inf")
    max_row = -1

    for row in range(n):

        if matrix[row][col] > max_value:
            max_value = matrix[row][col]
            max_row = row

    return max_row


def find_peak(matrix):
    n = len(matrix)
    m = len(matrix[0])

    low = 0
    high = m - 1

    while low <= high:

        # Middle column
        mid = low + (high - low) // 2

        # Find maximum element in this column
        max_row = find_max_row(matrix, n, mid)

        # Current element
        current = matrix[max_row][mid]

        # Boundary handling
        left = matrix[max_row][mid - 1] if mid - 1 >= 0 else -1
        right = matrix[max_row][mid + 1] if mid + 1 < m else -1

        # Current element is greater than both
        # left and right.
        #
        # Since it is already the maximum
        # in its column, it is also greater
        # than top and bottom.
        #
        # Therefore, it is a peak.
        if current > left and current > right:
            return [max_row, mid]

        # Left neighbor is greater.
        # A peak exists somewhere on the left.
        elif current < left:
            high = mid - 1

        # Otherwise, right neighbor is greater.
        else:
            low = mid + 1

    return [-1, -1]


# ============================================================
# EXAMPLE
# ============================================================

matrix = [
    [4, 2, 5, 1, 4, 5],
    [2, 9, 3, 2, 3, 2],
    [1, 7, 6, 0, 1, 3],
    [3, 6, 2, 3, 7, 2],
]

print("Brute   :", find_peak_brute(matrix))
print("Optimal :", find_peak(matrix))