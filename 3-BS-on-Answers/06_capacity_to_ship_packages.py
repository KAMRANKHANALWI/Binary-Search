"""
Capacity to Ship Packages Within D Days
Pattern: Binary Search on Answer

See 06_capacity_to_ship_packages.md for the full walkthrough.
"""


def days_required(weights, capacity):
    """How many days it takes to ship all packages at this capacity."""
    days = 1
    load = 0

    for weight in weights:
        if load + weight > capacity:
            days += 1
            load = weight
        else:
            load += weight

    return days


def ship_within_days(weights, days):
    """Minimum capacity needed to ship all packages within `days` days."""
    low, high = max(weights), sum(weights)
    ans = high  # sum(weights) always works: everything in 1 day

    while low <= high:
        mid = (low + high) // 2
        if days_required(weights, mid) <= days:
            ans = mid       # mid works, record it
            high = mid - 1  # but keep looking for something smaller
        else:
            low = mid + 1

    return ans


if __name__ == "__main__":
    tests = [
        (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15),
        (([3, 2, 2, 4, 1, 4], 3), 6),
        (([1, 2, 3, 1, 1], 4), 3),
        (([1, 2, 3, 4, 5], 1), 15),
        (([10, 10, 10, 10], 4), 10),
    ]

    for (weights, days), expected in tests:
        result = ship_within_days(weights, days)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: ship_within_days({weights}, days={days}) = {result} (expected {expected})")