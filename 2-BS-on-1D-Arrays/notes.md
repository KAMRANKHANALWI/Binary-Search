# Binary Search on 1D Arrays

## Core Patterns

### 1. Standard Binary Search
Search for an exact target in a sorted array.

### 2. Bounds
- Lower Bound → first index where `arr[i] >= x`
- Upper Bound → first index where `arr[i] > x`

Useful for:
- First occurrence
- Last occurrence
- Count occurrences
- Search insert position

### 3. Rotated Sorted Array
At least one half is sorted.

Steps:
1. Find `mid`
2. Identify sorted half
3. Check whether target lies there
4. Eliminate the other half

Duplicates:
- If `arr[low] == arr[mid] == arr[high]`
- Shrink both ends

### 4. Minimum in Rotated Sorted Array
If:

`arr[mid] > arr[high]`
→ minimum is on the right

Else:
→ minimum is at `mid` or on the left

### 5. Single Element
Use XOR-style pairing / binary-search parity pattern.

### 6. Peak Element
Peak condition:

`arr[i-1] < arr[i] > arr[i+1]`

Brute:
- Check every element → `O(n)`

Optimal:
- If `arr[mid] < arr[mid+1]`
  → peak exists on the right
- Else
  → peak exists on the left including `mid`

Time: `O(log n)`
Space: `O(1)`