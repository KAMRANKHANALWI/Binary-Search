"""
Smallest Divisor Given a Threshold
Pattern: Binary Search on Answer

See 05_smallest_divisor.md for the full walkthrough.
"""


def possible(arr, divisor, threshold):
    """Does this divisor keep the sum of ceil(x/divisor) under threshold?"""
    total = 0

    for x in arr:
        total += (x + divisor - 1) // divisor  # ceil(x / divisor)
        if total > threshold:
            return False

    return True


def smallest_divisor(arr, threshold):
    """Smallest positive divisor such that sum(ceil(x/divisor)) <= threshold."""
    low, high = 1, max(arr)
    ans = high  # max(arr) always works, so it's a safe starting fallback

    while low <= high:
        mid = (low + high) // 2
        if possible(arr, mid, threshold):
            ans = mid       # mid works, record it
            high = mid - 1  # but keep looking for something smaller
        else:
            low = mid + 1

    return ans


if __name__ == "__main__":
    tests = [
        (([1, 2, 5, 9], 6), 5),
        (([44, 22, 33, 11, 1], 5), 44),
        (([1, 2, 3, 4, 5], 15), 1),
        (([1, 2, 3, 4, 5], 5), 5),
        (([2, 3, 5, 7, 11], 11), 3),
    ]

    for (arr, threshold), expected in tests:
        result = smallest_divisor(arr, threshold)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: smallest_divisor({arr}, threshold={threshold}) = {result} (expected {expected})")