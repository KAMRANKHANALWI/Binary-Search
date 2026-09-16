"""
Split Array Largest Sum
Pattern: Binary Search on Answer — Minimize the Maximum

Same template as 09_book_allocation.py — see 10_split_array_largest_sum.md
"""


def count_subarrays(arr, max_sum):
    """How many contiguous subarrays it takes if none may exceed max_sum."""
    subarrays = 1
    current_sum = 0

    for num in arr:
        if current_sum + num <= max_sum:
            current_sum += num
        else:
            subarrays += 1
            current_sum = num

    return subarrays


def brute_force(arr, k):
    """Linear scan over every possible max_sum, reusing count_subarrays."""
    if k > len(arr):
        return -1

    low, high = max(arr), sum(arr)
    for max_sum in range(low, high + 1):
        if count_subarrays(arr, max_sum) <= k:
            return max_sum
    return -1


def split_array(arr, k):
    """Minimum possible value of the largest subarray sum, split into k parts."""
    if k > len(arr):
        return -1

    low, high = max(arr), sum(arr)
    ans = high  # sum(arr) always works: one subarray, k=1

    while low <= high:
        mid = (low + high) // 2
        if count_subarrays(arr, mid) <= k:
            ans = mid       # mid works, record it
            high = mid - 1  # keep looking for something smaller
        else:
            low = mid + 1   # too small, need a bigger max_sum

    return ans


if __name__ == "__main__":
    tests = [
        (([10, 20, 30, 40], 2), 60),
        (([7, 2, 5, 10, 8], 2), 18),
        (([1, 2, 3, 4, 5], 1), 15),
        (([1, 2, 3, 4, 5], 5), 5),
        (([1, 4, 4], 3), 4),
    ]

    for (arr, k), expected in tests:
        results = (brute_force(arr, k), split_array(arr, k))
        status = "PASS" if all(r == expected for r in results) else "FAIL"
        print(f"{status}: arr={arr}, k={k} -> {results} (expected {expected})")