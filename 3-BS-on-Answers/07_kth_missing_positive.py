"""
Kth Missing Positive Number
Pattern: Binary Search on Index

See 07_kth_missing_positive.md for the full walkthrough and derivation of `low + k`.
"""


def brute_force(arr, k):
    """Check every positive integer one by one. O(n * answer)."""
    missing_count = 0
    number = 1

    while True:
        if number not in arr:
            missing_count += 1
        if missing_count == k:
            return number
        number += 1


def better(arr, k):
    """Linear scan using the missing-count formula. O(n)."""
    for i in range(len(arr)):
        missing = arr[i] - (i + 1)
        if missing >= k:
            return k + i
    return k + len(arr)


def optimal(arr, k):
    """Binary search on index. O(log n)."""
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        missing = arr[mid] - (mid + 1)

        if missing < k:
            low = mid + 1   # not enough missing numbers yet
        else:
            high = mid - 1  # already enough, look left

    return low + k


if __name__ == "__main__":
    tests = [
        (([2, 3, 4, 7, 11], 5), 9),
        (([1, 2, 3, 4], 2), 6),
        (([1, 2, 3, 4], 100), 104),
        (([2], 1), 1),
        (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 1), 11),
    ]

    for (arr, k), expected in tests:
        results = (brute_force(arr, k), better(arr, k), optimal(arr, k))
        status = "PASS" if all(r == expected for r in results) else "FAIL"
        print(f"{status}: arr={arr}, k={k} -> {results} (expected {expected})")