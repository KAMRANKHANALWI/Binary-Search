"""
14 - K-th Element of Two Sorted Arrays

Pattern:
    Binary Search on Partition

Core idea:
    Do not merge the arrays.

    Create a partition with exactly k elements on the left.

    If we take:
        mid1 elements from A
        mid2 elements from B

    then:
        mid1 + mid2 = k
        mid2 = k - mid1

    Binary-search mid1 in the smaller array.
"""


def kth_element(a, b, k):
    n1 = len(a)
    n2 = len(b)

    # Binary-search the smaller array.
    if n1 > n2:
        return kth_element(b, a, k)

    # Valid range for elements taken from A.
    low = max(0, k - n2)
    high = min(k, n1)

    while low <= high:
        mid1 = (low + high) // 2
        mid2 = k - mid1

        # Elements immediately around the partition.
        l1 = float("-inf") if mid1 == 0 else a[mid1 - 1]
        r1 = float("inf") if mid1 == n1 else a[mid1]

        l2 = float("-inf") if mid2 == 0 else b[mid2 - 1]
        r2 = float("inf") if mid2 == n2 else b[mid2]

        # Correct partition.
        if l1 <= r2 and l2 <= r1:
            # Exactly k elements are on the left.
            # The k-th element is the largest element on the left.
            return max(l1, l2)

        # Too many elements taken from A.
        elif l1 > r2:
            high = mid1 - 1

        # Too few elements taken from A.
        else:
            low = mid1 + 1

    return -1


# Example
if __name__ == "__main__":
    a = [2, 3, 6, 7, 9]
    b = [1, 4, 8, 10]
    k = 4

    print(kth_element(a, b, k))  # 4
