# Search in a 2D Matrix - II
#
# Given a matrix where:
# - Every row is sorted from left to right.
# - Every column is sorted from top to bottom.
#
# Find whether target exists in the matrix.
#
# Example:
#
# matrix = [
#     [1,  4,  7,  11, 15],
#     [2,  5,  8,  12, 19],
#     [3,  6,  9,  16, 22],
#     [10, 13, 14, 17, 24],
#     [18, 21, 23, 26, 30]
# ]
#
# target = 14
#
# Output:
# True


# ============================================================
# BRUTE FORCE
# ============================================================
#
# Check every element.
#
# Time  : O(n * m)
# Space : O(1)


def search_matrix_brute(matrix, target):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(m):

            if matrix[i][j] == target:
                return True

    return False


# ============================================================
# BETTER
# ============================================================
#
# Every row is sorted.
#
# Therefore, we can perform Binary Search
# on every individual row.
#
# For each row:
#     Binary Search for target.
#
# Time  : O(n * log m)
# Space : O(1)


def binary_search(row, target):
    low = 0
    high = len(row) - 1

    while low <= high:

        mid = low + (high - low) // 2

        if row[mid] == target:
            return True

        elif row[mid] < target:
            low = mid + 1

        else:
            high = mid - 1

    return False


def search_matrix_better(matrix, target):
    n = len(matrix)

    for i in range(n):

        if binary_search(matrix[i], target):
            return True

    return False


# ============================================================
# OPTIMAL
# ============================================================
#
# Start from the TOP-RIGHT corner.
#
# Example:
#
# [1   4   7   11  15]  <- start here
# [2   5   8   12  19]
# [3   6   9   16  22]
# [10 13  14  17  24]
# [18 21  23  26  30]
#
# At matrix[row][col]:
#
# If value == target:
#     Found it.
#
# If value < target:
#     Move DOWN.
#
# Why?
# The entire row to the LEFT is even smaller,
# so target cannot be there.
#
# If value > target:
#     Move LEFT.
#
# Why?
# The entire column BELOW is even larger,
# so target cannot be there.
#
# Every movement eliminates an entire row
# or an entire column.
#
# Time  : O(n + m)
# Space : O(1)


def search_matrix(matrix, target):
    n = len(matrix)
    m = len(matrix[0])

    # Start at top-right corner.
    row = 0
    col = m - 1

    while row < n and col >= 0:

        value = matrix[row][col]

        # Target found.
        if value == target:
            return True

        # Current value is smaller than target.
        # Everything to the left is even smaller,
        # so eliminate this entire row portion.
        elif value < target:
            row += 1

        # Current value is greater than target.
        # Everything below is even greater,
        # so eliminate this entire column portion.
        else:
            col -= 1

    return False


# ============================================================
# EXAMPLE
# ============================================================

matrix = [
    [1, 4, 7, 11, 15],
    [2, 5, 8, 12, 19],
    [3, 6, 9, 16, 22],
    [10, 13, 14, 17, 24],
    [18, 21, 23, 26, 30],
]

target = 14

print("Brute:", search_matrix_brute(matrix, target))
print("Better:", search_matrix_better(matrix, target))
print("Optimal:", search_matrix(matrix, target))

# Output:
# Brute: True
# Better: True
# Optimal: True