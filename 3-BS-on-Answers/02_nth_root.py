"""
Find the integer nth root of m.

Return x if:
    x^n == m

Otherwise:
    return -1
"""


# ---------------------------------------------------------
# Brute Force
# ---------------------------------------------------------

def nth_root_brute(n, m):
    for x in range(1, m + 1):
        value = x ** n

        if value == m:
            return x

        if value > m:
            break

    return -1


# ---------------------------------------------------------
# Optimal: Binary Search
# ---------------------------------------------------------

def nth_root(n, m):
    low = 1
    high = m

    while low <= high:
        mid = (low + high) // 2
        value = mid ** n

        if value == m:
            return mid

        elif value < m:
            low = mid + 1

        else:
            high = mid - 1

    return -1


# ---------------------------------------------------------
# Examples
# ---------------------------------------------------------

print(nth_root_brute(3, 27))  # 3
print(nth_root_brute(3, 28))  # -1

print(nth_root(4, 16))        # 2
print(nth_root(3, 28))        # -1