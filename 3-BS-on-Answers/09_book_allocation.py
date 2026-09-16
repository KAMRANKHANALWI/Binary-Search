"""
Book Allocation
Pattern: Binary Search on Answer — Minimize the Maximum

See 09_book_allocation.md for the full walkthrough.
"""


def brute_force(arr, m):
    """Try every possible page limit from low to high, reusing the same
    feasibility check the binary search uses. Returns the first (smallest)
    limit that works.
    """
    n = len(arr)
    if m > n:
        return -1

    low, high = max(arr), sum(arr)

    for limit in range(low, high + 1):
        if students_required(arr, limit) <= m:
            return limit

    return -1  # unreachable given the search space, but kept for safety


def students_required(arr, limit):
    """How many students it takes if no one can hold more than `limit` pages."""
    students = 1
    pages_used = 0

    for pages in arr:
        if pages_used + pages <= limit:
            pages_used += pages
        else:
            students += 1
            pages_used = pages

    return students


def find_pages(arr, m):
    """Minimum possible value of the maximum pages assigned to any student."""
    n = len(arr)
    if m > n:
        return -1

    low, high = max(arr), sum(arr)
    ans = high  # sum(arr) always works: one student takes everything

    while low <= high:
        mid = (low + high) // 2
        if students_required(arr, mid) <= m:
            ans = mid        # mid works, record it
            high = mid - 1   # but keep looking for something smaller
        else:
            low = mid + 1    # too small, need a bigger limit

    return ans


if __name__ == "__main__":
    tests = [
        (([25, 46, 28, 49, 24], 4), 71),
        (([12, 34, 67, 90], 2), 113),
        (([10, 20, 30, 40], 5), -1),
        (([5, 5, 5, 5], 4), 5),
        (([100], 1), 100),
    ]

    for (arr, m), expected in tests:
        results = (brute_force(arr, m), find_pages(arr, m))
        status = "PASS" if all(r == expected for r in results) else "FAIL"
        print(f"{status}: arr={arr}, m={m} -> {results} (expected {expected})")