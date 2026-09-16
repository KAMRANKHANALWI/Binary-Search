"""
Painter's Partition
Pattern: Binary Search on Answer — Minimize the Maximum

Same template as book_allocation.py and split_array_largest_sum.py —
see 11_painters_partition.md.
"""


def count_painters(boards, max_work):
    """How many painters it takes if none may be assigned more than max_work."""
    painters = 1
    current_work = 0

    for board in boards:
        if current_work + board <= max_work:
            current_work += board
        else:
            painters += 1
            current_work = board

    return painters


def brute_force(boards, k):
    """Linear scan over every possible max_work, reusing count_painters."""
    if k > len(boards):
        return -1

    low, high = max(boards), sum(boards)
    for max_work in range(low, high + 1):
        if count_painters(boards, max_work) <= k:
            return max_work
    return -1


def painters_partition(boards, k):
    """Minimum possible value of the maximum work assigned to any painter."""
    if k > len(boards):
        return -1

    low, high = max(boards), sum(boards)
    ans = high  # sum(boards) always works: one painter, k=1

    while low <= high:
        mid = (low + high) // 2
        if count_painters(boards, mid) <= k:
            ans = mid       # mid works, record it
            high = mid - 1  # keep looking for something smaller
        else:
            low = mid + 1   # too small, need more capacity per painter

    return ans


if __name__ == "__main__":
    tests = [
        (([10, 20, 30, 40], 2), 60),
        (([10, 10, 10, 10], 2), 20),
        (([1, 2, 3, 4, 5], 1), 15),
        (([1, 2, 3, 4, 5], 5), 5),
        (([5, 5, 5, 5, 5], 3), 10),
    ]

    for (boards, k), expected in tests:
        results = (brute_force(boards, k), painters_partition(boards, k))
        status = "PASS" if all(r == expected for r in results) else "FAIL"
        print(f"{status}: boards={boards}, k={k} -> {results} (expected {expected})")