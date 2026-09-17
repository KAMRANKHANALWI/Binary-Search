"""
Minimize Max Distance Between Gas Stations
Pattern: Binary Search on Answer — Minimize the Maximum (continuous version)

See 13_median_of_two_sorted_arrays.md for the full walkthrough.
"""

import heapq
import math


def stations_required(arr, dist):
    """How many NEW stations are needed so every gap's pieces are <= dist."""
    count = 0

    for i in range(len(arr) - 1):
        gap = arr[i + 1] - arr[i]
        sections = math.floor(gap / dist)

        # Exact-division correction: if gap divides evenly by dist,
        # one fewer new station is needed than floor() alone suggests.
        #
        # Why not just write "gap == sections * dist"?
        # Because dist is a float, and float math is not perfectly
        # exact. 6 / 2 might come out as 2.9999999999998 instead of
        # exactly 3, so a plain == check could wrongly say "not equal"
        # even when the two numbers really should be the same.
        # math.isclose() checks "close enough to count as equal"
        # instead of "bit-for-bit identical", which is the safe way
        # to compare floats.
        if math.isclose(gap, sections * dist, rel_tol=1e-9, abs_tol=1e-9):
            sections -= 1

        count += sections

    return count


def minimise_max_distance_brute(arr, k, step=1e-3):
    """Step through candidate distances linearly. Slow — for small demos only."""
    # step=1e-3 is a "default argument" -- if you call this function
    # without giving a step (e.g. minimise_max_distance_brute(arr, k)),
    # Python automatically uses 0.001. You only need to pass a step
    # explicitly if you want a different one.

    # This line computes every gap (arr[i+1] - arr[i]) and takes the
    # biggest one, all in a single expression -- called a "generator
    # expression". It's the same result as writing this longer version:
    #
    #     gaps = []
    #     for i in range(len(arr) - 1):
    #         gaps.append(arr[i + 1] - arr[i])
    #     max_gap = max(gaps)
    #
    # just written compactly. No square brackets needed since max()
    # can consume the values one at a time without building a full list.
    max_gap = max(arr[i + 1] - arr[i] for i in range(len(arr) - 1))

    dist = step
    while dist <= max_gap:
        if stations_required(arr, dist) <= k:
            return dist
        dist += step

    return max_gap


def minimise_max_distance_heap(arr, k):
    """Greedy: repeatedly split whichever gap currently has the worst piece."""
    # This function uses a "heap" (from Python's heapq module), which
    # is a data structure that always lets you grab the smallest item
    # very quickly. We need the LARGEST gap each time, not the
    # smallest -- Python's heapq only supports "smallest first", so
    # the standard trick is to store every value NEGATED. The smallest
    # negative number corresponds to the largest original number, so
    # "smallest negative" behaves exactly like "largest positive".
    # We just remember to flip the sign back (with a leading -) every
    # time we read a value out of the heap.

    n = len(arr)

    # how_many[i] = how many new stations we've placed inside gap i so far.
    how_many = [0] * (n - 1)

    # Build the starting heap: one entry per gap, storing
    # (negative gap length, which gap this is).
    # We need the index alongside the length because once we pop the
    # "largest" entry off the heap, the length alone doesn't tell us
    # WHICH gap it came from -- we need the index to update how_many
    # and to look up the gap's original length again.
    pq = [(-(arr[i + 1] - arr[i]), i) for i in range(n - 1)]
    heapq.heapify(pq)  # arranges the list into valid heap order in place

    # Place one new station at a time, k times total.
    for _ in range(k):
        # heappop always returns the smallest item in the heap.
        # Because we stored negated lengths, "smallest negative" is
        # really "largest gap" -- so this line pulls out whichever
        # gap currently has the worst (biggest) piece.
        neg_len, i = heapq.heappop(pq)  # unpack the (length, index) pair

        how_many[i] += 1  # one more station now lives inside gap i

        gap = arr[i + 1] - arr[i]  # the ORIGINAL length of this gap

        # After how_many[i] stations, gap i is split into
        # (how_many[i] + 1) equal pieces -- this is its new worst piece.
        new_len = gap / (how_many[i] + 1)

        # Push the updated (still negated) length back onto the heap
        # so it competes fairly against the other gaps next time.
        heapq.heappush(pq, (-new_len, i))

    # After placing all k stations, the heap's smallest (negated) entry
    # tells us the largest piece remaining anywhere -- that's our answer.
    # pq[0] peeks at the top of the heap without removing it.
    return -pq[0][0]


def minimise_max_distance(arr, k, epsilon=1e-6):
    """Binary search on the answer (a continuous distance)."""
    low = 0.0
    # Same "generator expression" pattern as in the brute force function
    # above: computes every gap and keeps the biggest one, without
    # building a separate list first.
    high = max(arr[i + 1] - arr[i] for i in range(len(arr) - 1))

    while high - low > epsilon:
        mid = (low + high) / 2
        if stations_required(arr, mid) > k:
            low = mid  # too many stations needed, dist too small
        else:
            high = mid  # feasible, keep looking for something smaller

    return high


if __name__ == "__main__":
    tests = [
        (([1, 13, 17, 23], 5), 3.0),
        (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 9), 0.5),
        (([1, 5], 1), 2.0),
        (([1, 10], 4), 1.8),
    ]

    for (arr, k), expected in tests:
        heap_result = minimise_max_distance_heap(list(arr), k)
        bs_result = minimise_max_distance(arr, k)
        ok = math.isclose(heap_result, expected, abs_tol=1e-6) and math.isclose(
            bs_result, expected, abs_tol=1e-6
        )
        status = "PASS" if ok else "FAIL"
        print(
            f"{status}: arr={arr}, k={k} -> heap={heap_result:.6f}, "
            f"bs={bs_result:.6f} (expected {expected})"
        )
