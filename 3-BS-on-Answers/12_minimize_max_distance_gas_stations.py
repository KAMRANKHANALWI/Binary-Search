"""
Problem: Minimize Maximum Distance Between Gas Stations

Pattern: Binary Search on Answer — Minimize the Maximum (continuous version)
See 12_minimize_max_distance_gas_stations.md for the full walkthrough.

Given sorted coordinates of existing gas stations,
we have to place k new gas stations such that the
maximum distance between any two consecutive gas
stations is minimized.

Example:

arr = [1, 13, 17, 23]
k = 5

Answer = 3.0


Pattern:
    Binary Search on Answer
"""


import heapq
import math


# ============================================================
# Helper
# ============================================================

def number_of_gas_stations_required(arr, distance):
    """
    How many NEW gas stations are required if the maximum
    allowed distance between consecutive stations is 'distance'?
    """

    count = 0

    for i in range(len(arr) - 1):

        gap = arr[i + 1] - arr[i]

        # Number of stations needed in this gap.
        stations = math.floor(gap / distance)

        # Exact divisibility correction.
        #
        # Example:
        #
        # gap = 6
        # distance = 2
        #
        # floor(6 / 2) = 3
        #
        # But:
        #
        # 1 -- 3 -- 5 -- 7
        #
        # needs only 2 new stations.
        #
        # Why math.isclose() instead of just checking
        # "gap == stations * distance"?
        #
        # Because 'distance' is a decimal, and computer decimals
        # aren't always perfectly exact. A division that SHOULD
        # come out even, like 6 / 2, can sometimes land as
        # 2.9999999999998 instead of a clean 3.0. A plain ==
        # check could wrongly say "not equal" even when the two
        # numbers really should match. math.isclose() checks
        # "close enough to count as the same" instead of demanding
        # a bit-for-bit exact match, which is the safe way to
        # compare two floats.
        if math.isclose(
            gap,
            stations * distance,
            rel_tol=1e-12,
            abs_tol=1e-12
        ):
            stations -= 1

        count += stations

    return count


# ============================================================
# Approach 1: Brute Force
# ============================================================

def minimise_max_distance_brute(arr, k):
    """
    Brute Force

    Try possible answers linearly.

    Time:
        Extremely large for high precision.

    Space:
        O(1)
    """

    max_gap = 0

    for i in range(len(arr) - 1):
        max_gap = max(
            max_gap,
            arr[i + 1] - arr[i]
        )

    # Step size for how finely we scan candidate distances.
    #
    # NOTE: this must NOT start at 0.0 — number_of_gas_stations_required()
    # divides by 'distance', so a distance of exactly 0 would cause a
    # ZeroDivisionError. Starting at 'step' instead of 0.0 avoids that.
    #
    # We also use a slightly bigger step (1e-3) than the precision the
    # binary search version uses (1e-6). A brute force that checks every
    # 0.000001 units would take millions of iterations even for small
    # gaps -- far too slow for a demo. 1e-3 keeps this fast while still
    # showing the same idea: "try every candidate distance in order".
    step = 1e-3
    distance = step

    while distance <= max_gap:

        count = number_of_gas_stations_required(
            arr,
            distance
        )

        if count <= k:
            return distance

        distance += step

    return max_gap


# ============================================================
# Approach 2: Greedy + Max Heap
# ============================================================

def minimise_max_distance_heap(arr, k):
    """
    Better Approach:
    Greedy + Max Heap

    At every step:
        Pick the largest current section
        and split it by adding one station.

    Time:
        O(N log N + K log N)

    Space:
        O(N)
    """

    n = len(arr)

    # Number of stations placed inside each original gap
    how_many = [0] * (n - 1)

    # Python's heapq module only ever gives you the SMALLEST item,
    # but we need the LARGEST gap each time. The standard trick:
    # store every gap length as its negative. The most negative
    # number corresponds to the largest original number (-12 is
    # "smaller" than -4), so asking the heap for its smallest entry
    # now correctly hands us the largest gap. We just remember to
    # flip the sign back with a leading '-' whenever we read a value out.
    pq = []

    # Initially every gap has one section.
    for i in range(n - 1):

        gap = arr[i + 1] - arr[i]

        heapq.heappush(
            pq,
            (-gap, i)
        )

    # Place K stations
    for _ in range(k):

        # heappop always returns the smallest item -- since we stored
        # negated lengths, "smallest negative" means "largest gap",
        # so this pulls out whichever gap currently has the worst piece.
        # The index travels alongside the length so we still know
        # WHICH gap this came from, since the length alone doesn't say.
        negative_length, index = heapq.heappop(pq)

        # Add one station to this original gap
        how_many[index] += 1

        gap = arr[index + 1] - arr[index]

        # After x stations:
        #
        # number of sections = x + 1
        #
        # current largest section =
        # original gap / (x + 1)

        new_length = gap / (
            how_many[index] + 1
        )

        heapq.heappush(
            pq,
            (-new_length, index)
        )

    # Largest current section is sitting at the top of the heap.
    # pq[0] peeks without removing it; negate to undo the earlier flip.
    negative_length, _ = pq[0]

    return -negative_length


# ============================================================
# Approach 3: Binary Search on Answer
# ============================================================

def minimise_max_distance(arr, k):
    """
    Optimal Approach:
    Binary Search on Answer

    Time:
        O(N * log(max_gap / epsilon))

    Space:
        O(1)
    """

    low = 0.0

    # Answer cannot exceed the largest existing gap.
    high = 0.0

    for i in range(len(arr) - 1):

        gap = arr[i + 1] - arr[i]

        high = max(high, gap)

    epsilon = 1e-6

    while high - low > epsilon:

        mid = (low + high) / 2.0

        count = number_of_gas_stations_required(
            arr,
            mid
        )

        if count > k:

            # Too many stations required.
            # Candidate distance is too small.
            low = mid

        else:

            # Possible answer.
            # Try a smaller distance.
            high = mid

    return high


# ============================================================
# Example
# ============================================================

if __name__ == "__main__":
    arr = [1, 13, 17, 23]
    k = 5

    print("Brute:", minimise_max_distance_brute(arr, k))
    print("Heap :", minimise_max_distance_heap(arr, k))
    print("BS   :", minimise_max_distance(arr, k))