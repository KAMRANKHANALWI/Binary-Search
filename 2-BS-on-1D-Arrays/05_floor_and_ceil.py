def floor_and_ceil(arr, x):
    """
    Return (floor, ceil) of x in a sorted array.

    Floor = largest value <= x
    Ceil  = smallest value >= x

    Returns -1 for either value if it doesn't exist.
    """

    low = 0
    high = len(arr) - 1

    floor = -1
    ceil = -1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] == x:
            return arr[mid], arr[mid]

        elif arr[mid] <= x:
            floor = arr[mid]
            low = mid + 1

        else:
            ceil = arr[mid]
            high = mid - 1

    return floor, ceil


if __name__ == "__main__":

    arr = [1, 3, 5, 7, 9]

    print(floor_and_ceil(arr, 6))  # (5, 7)
    print(floor_and_ceil(arr, 5))  # (5, 5)
    print(floor_and_ceil(arr, 0))  # (-1, 1)
    print(floor_and_ceil(arr, 10))  # (9, -1)
