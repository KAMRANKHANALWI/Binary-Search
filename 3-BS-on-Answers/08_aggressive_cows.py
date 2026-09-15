"""
Aggressive Cows
Pattern: Binary Search on Answer — Maximize the Minimum

See 08_aggressive_cows.md for the full walkthrough.
"""


def can_place(stalls, dist, cows):
    """Can we place `cows` cows so every pair is at least `dist` apart?"""
    count = 1
    last = stalls[0]  # first cow always goes in the first stall

    for i in range(1, len(stalls)):
        if stalls[i] - last >= dist:
            count += 1
            last = stalls[i]
        if count >= cows:
            return True

    return False


def aggressive_cows(stalls, cows):
    """Maximum possible minimum distance between any two placed cows."""
    stalls.sort()
    low, high = 1, stalls[-1] - stalls[0]
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        if can_place(stalls, mid, cows):
            ans = mid       # mid works, record it
            low = mid + 1   # but keep looking for something bigger
        else:
            high = mid - 1  # too far apart, need a smaller distance

    return ans


if __name__ == "__main__":
    tests = [
        (([0, 3, 4, 7, 9, 10], 4), 3),
        (([1, 2, 4, 8, 9], 3), 3),
        (([1, 2, 3, 4, 5], 2), 4),
        (([10, 1, 2, 7, 5], 3), 4),
        (([1, 5], 2), 4),
    ]

    for (stalls, cows), expected in tests:
        result = aggressive_cows(list(stalls), cows)
        status = "PASS" if result == expected else "FAIL"
        print(f"{status}: aggressive_cows({stalls}, cows={cows}) = {result} (expected {expected})")