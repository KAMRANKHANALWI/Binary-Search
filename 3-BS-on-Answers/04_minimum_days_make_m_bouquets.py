"""
Minimum Days to Make M Bouquets
Pattern: Binary Search on Answer

See 04_minimum_days_make_m_bouquets.md for the full walkthrough.
"""

def possible(arr, day, m, k):
    """Can we make at least m bouquets by the given day?"""
    run = 0
    bouquets = 0

    for bloom_day in arr:
        if bloom_day <= day:
            run += 1
        else:
            bouquets += run // k
            run = 0

    bouquets += run // k
    return bouquets >= m


def min_days(arr, m, k):
    """Minimum day by which m bouquets of k adjacent flowers can be made.

    Returns -1 if it's impossible.
    """
    if m * k > len(arr):
        return -1

    low, high = min(arr), max(arr)

    while low <= high:
        mid = (low + high) // 2
        if possible(arr, mid, m, k):
            high = mid - 1
        else:
            low = mid + 1

    return low


if __name__ == "__main__":
    tests = [
        (([1, 10, 3, 10, 2], 3, 1), 3),
        (([1, 10, 3, 10, 2], 3, 2), -1),
        (([7, 7, 7, 7, 12, 7, 7], 2, 3), 12),
        (([1000000000, 1000000000], 1, 1), 1000000000),
        (([1, 2, 3, 4, 5], 5, 1), 5),
        (([1, 2, 3, 4, 5], 1, 5), 5),
    ]

    for (arr, m, k), expected in tests:
        result = min_days(arr, m, k)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: min_days({arr}, m={m}, k={k}) = {result} (expected {expected})")