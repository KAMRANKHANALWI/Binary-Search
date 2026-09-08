"""
Find Floor Square Root

Given a non-negative integer n, return floor(sqrt(n)).

Example:
    n = 28
    sqrt(28) ≈ 5.29
    answer = 5
"""

# ---------------------------------------------------------
# Brute Force
# ---------------------------------------------------------


def floor_sqrt_brute(n):
    if n < 2:
        return n

    i = 1

    while i * i <= n:
        i += 1

    return i - 1


# ---------------------------------------------------------
# Optimal: Binary Search
# ---------------------------------------------------------


def floor_sqrt(n):
    if n < 2:
        return n

    low = 1
    high = n
    answer = 1

    while low <= high:
        mid = (low + high) // 2

        if mid * mid <= n:
            answer = mid
            low = mid + 1
        else:
            high = mid - 1

    return answer


# ---------------------------------------------------------
# Examples
# ---------------------------------------------------------

print(floor_sqrt_brute(28))  # 5
print(floor_sqrt(28))  # 5
