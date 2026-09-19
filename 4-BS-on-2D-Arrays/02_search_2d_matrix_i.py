# Search in a 2D Matrix - I
#
# Given a matrix where:
# - Each row is sorted.
# - The first element of each row is greater
#   than the last element of the previous row.
#
# Return True if target exists, otherwise False.
#
# Example:
#
# [
#     [3,  4,  7,  9],
#     [12, 13, 16, 18],
#     [20, 21, 23, 29]
# ]
#
# We can imagine the matrix as:
#
# [3, 4, 7, 9, 12, 13, 16, 18, 20, 21, 23, 29]
#
# without actually creating this 1D array.
#
# ------------------------------------------------------------
# BRUTE FORCE
# ------------------------------------------------------------
#
# Visit every element.
#
# Time  : O(n * m)
# Space : O(1)
#
#
# ------------------------------------------------------------
# BETTER
# ------------------------------------------------------------
#
# Search each row using Binary Search.
#
# Time  : O(n * log m)
# Space : O(1)
#
#
# ------------------------------------------------------------
# OPTIMAL
# ------------------------------------------------------------
#
# Treat the entire matrix as a virtual sorted 1D array.
#
# For a virtual 1D index mid:
#
#     row = mid // m
#     col = mid % m
#
# This lets us perform Binary Search over all n * m elements.
#
# Time  : O(log(n * m))
# Space : O(1)


# ============================================================
# BRUTE FORCE
# ============================================================

def search_matrix_brute(matrix, target):
    n = len(matrix)
    m = len(matrix[0])

    for i in range(n):
        for j in range(m):

            if matrix[i][j] == target:
                return True

    return False


# ============================================================
# BINARY SEARCH ON EACH ROW
# ============================================================

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
    m = len(matrix[0])

    for i in range(n):

        # Target can only exist in this row if
        # it lies between the first and last element.
        if matrix[i][0] <= target <= matrix[i][m - 1]:

            return binary_search(matrix[i], target)

    return False


# ============================================================
# OPTIMAL - VIRTUAL 1D BINARY SEARCH
# ============================================================

def search_matrix(matrix, target):
    n = len(matrix)
    m = len(matrix[0])

    # Imagine the matrix as one sorted 1D array.
    #
    # Number of elements = n * m
    # Last virtual index = n * m - 1
    low = 0
    high = n * m - 1

    while low <= high:

        mid = low + (high - low) // 2

        # Convert virtual 1D index into
        # actual 2D coordinates.
        row = mid // m
        col = mid % m

        value = matrix[row][col]

        if value == target:
            return True

        elif value < target:

            # Target must be on the right.
            low = mid + 1

        else:

            # Target must be on the left.
            high = mid - 1

    return False


# ============================================================
# EXAMPLE
# ============================================================

matrix = [
    [3, 4, 7, 9],
    [12, 13, 16, 18],
    [20, 21, 23, 29],
]

target = 23

print("Brute:", search_matrix_brute(matrix, target))
print("Better:", search_matrix_better(matrix, target))
print("Optimal:", search_matrix(matrix, target))

# Output:
# Brute: True
# Better: True
# Optimal: True