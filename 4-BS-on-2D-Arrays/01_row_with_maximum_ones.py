# Row With Maximum 1s
#
# Given a binary matrix where each row is sorted,
# find the index of the row containing the maximum number of 1s.
#
# If multiple rows have the same maximum number of 1s,
# return the index of the first such row.
#
# ------------------------------------------------------------
# BRUTE FORCE
# ------------------------------------------------------------
#
# Idea:
# - Traverse every element of every row.
# - Count the number of 1s in each row.
# - Keep track of the row with the maximum count.
#
# Time: O(n * m)
# Space: O(1)
#
#
# ------------------------------------------------------------
# OPTIMAL - BINARY SEARCH
# ------------------------------------------------------------
#
# Since every row is sorted:
#
#     [0, 0, 0, 1, 1, 1]
#                 ^
#             first 1
#
# We can use Binary Search to find the first 1.
#
# Number of 1s = m - index_of_first_1
#
# We use lower_bound(row, 1):
#     first index where row[index] >= 1
#
# Since the array contains only 0 and 1,
# this is exactly the first index containing 1.
#
# Time: O(n * log m)
# Space: O(1)


# ============================================================
# BRUTE FORCE
# ============================================================

def row_with_max_1s_brute(matrix):
    n = len(matrix)
    m = len(matrix[0])

    max_ones = 0
    row_index = -1

    for i in range(n):

        count_ones = 0

        # Count all 1s in the current row.
        for j in range(m):
            if matrix[i][j] == 1:
                count_ones += 1

        # Update only when we find MORE 1s.
        #
        # Using > instead of >= means that if two rows
        # have the same number of 1s, we keep the first row.
        if count_ones > max_ones:
            max_ones = count_ones
            row_index = i

    return row_index


# ============================================================
# OPTIMAL - BINARY SEARCH
# ============================================================

def lower_bound(row, x):
    """
    Return the first index where row[index] >= x.

    Example:
        row = [0, 0, 0, 1, 1]

        lower_bound(row, 1) -> 3

    Because index 3 is the first position
    where the value is >= 1.
    """

    low = 0
    high = len(row) - 1

    # If no valid position is found,
    # return len(row).
    ans = len(row)

    while low <= high:

        mid = low + (high - low) // 2

        if row[mid] >= x:

            # mid can be our answer.
            ans = mid

            # But there might be an earlier valid index.
            high = mid - 1

        else:

            # row[mid] < x
            # Therefore we need to search on the right.
            low = mid + 1

    return ans


def row_with_max_1s(matrix):
    n = len(matrix)
    m = len(matrix[0])

    max_ones = 0
    row_index = -1

    for i in range(n):

        # Find the first 1 in this row.
        first_one = lower_bound(matrix[i], 1)

        # Everything after first_one is 1.
        #
        # Example:
        # [0, 0, 1, 1, 1]
        #       ^
        #       first_one = 2
        #
        # m = 5
        # number of 1s = 5 - 2 = 3
        ones = m - first_one

        # Keep the first row in case of a tie.
        if ones > max_ones:
            max_ones = ones
            row_index = i

    return row_index


# ============================================================
# EXAMPLE
# ============================================================

matrix = [
    [0, 0, 1, 1, 1],  # 3 ones
    [0, 0, 0, 0, 0],  # 0 ones
    [0, 1, 1, 1, 1],  # 4 ones
    [0, 0, 0, 0, 0],  # 0 ones
    [0, 1, 1, 1, 1],  # 4 ones
]


# Brute Force
print("Brute:", row_with_max_1s_brute(matrix))

# Optimal - Binary Search
print("Optimal:", row_with_max_1s(matrix))


# Output:
# Brute: 2
# Optimal: 2