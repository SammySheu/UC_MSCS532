"""
Selection Algorithms - Deterministic and Randomized Implementations
Assignment 6 - Medians and Order Statistics & Elementary Data Structures
"""
import random
import time
from typing import List, Callable


# ---------------------------------------------------------------------------
# Helpers shared by both algorithms
# ---------------------------------------------------------------------------

def _insertion_sort(arr: List[int], left: int, right: int) -> None:
    """
    Sort arr[left..right] in-place using insertion sort.

    Used internally by Median of Medians to sort small groups of 5.

    Args:
        arr: The list (modified in-place)
        left: Start index (inclusive)
        right: End index (inclusive)
    """
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def _partition_around(arr: List[int], left: int, right: int, pivot_val: int) -> int:
    """
    Three-way partition arr[left..right] around pivot_val.

    Rearranges elements so that all values < pivot_val are to the left,
    then pivot_val itself, then all values > pivot_val to the right.

    Args:
        arr: The list (modified in-place)
        left: Start index (inclusive)
        right: End index (inclusive)
        pivot_val: The value to partition around

    Returns:
        The final index where pivot_val is placed
    """
    # Find pivot_val and move it to the end
    for idx in range(left, right + 1):
        if arr[idx] == pivot_val:
            arr[idx], arr[right] = arr[right], arr[idx]
            break

    pivot = arr[right]
    i = left - 1

    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def _randomized_partition(arr: List[int], left: int, right: int) -> int:
    """
    Lomuto partition with a uniformly random pivot.

    Args:
        arr: The list (modified in-place)
        left: Start index (inclusive)
        right: End index (inclusive)

    Returns:
        The final index of the pivot element
    """
    random_index = random.randint(left, right)
    arr[random_index], arr[right] = arr[right], arr[random_index]

    pivot = arr[right]
    i = left - 1

    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# Part 1: Deterministic Selection — Median of Medians
# ---------------------------------------------------------------------------

def _median_of_medians(arr: List[int], left: int, right: int) -> int:
    """
    Find a good pivot using the Median-of-Medians strategy.

    Splits arr[left..right] into groups of 5, sorts each group, collects
    their medians, then recursively finds the median of those medians.
    This guarantees the pivot lies between the 30th and 70th percentile,
    ensuring balanced partitions and O(n) worst-case selection.

    Args:
        arr: The list
        left: Start index (inclusive)
        right: End index (inclusive)

    Returns:
        The median-of-medians value (not its index)
    """
    n = right - left + 1

    # Base case: five or fewer elements — just sort and return median
    if n <= 5:
        _insertion_sort(arr, left, right)
        return arr[left + (n - 1) // 2]

    # Step 1: divide into groups of 5, sort each, collect medians
    medians = []
    i = left
    while i <= right:
        group_right = min(i + 4, right)
        _insertion_sort(arr, i, group_right)
        group_size = group_right - i + 1
        median_idx = i + (group_size - 1) // 2
        medians.append(arr[median_idx])
        i += 5

    # Step 2: recursively find the true median of the collected medians
    if len(medians) == 1:
        return medians[0]

    # Build a temporary subarray of medians and recurse
    pivot_val = _median_of_medians_select_helper(medians, 0, len(medians) - 1,
                                                 (len(medians) - 1) // 2)
    return pivot_val


def _median_of_medians_select_helper(arr: List[int], left: int, right: int,
                                     k: int) -> int:
    """
    Recursive helper for median-of-medians selection.

    Args:
        arr: The list (modified in-place)
        left: Start index (inclusive)
        right: End index (inclusive)
        k: 0-based rank of the desired element within arr[left..right]

    Returns:
        The k-th smallest value in arr[left..right]
    """
    if left == right:
        return arr[left]

    pivot_val = _median_of_medians(arr, left, right)
    pivot_idx = _partition_around(arr, left, right, pivot_val)

    rank = pivot_idx - left  # rank of pivot within the subarray
    if k == rank:
        return arr[pivot_idx]
    elif k < rank:
        return _median_of_medians_select_helper(arr, left, pivot_idx - 1, k)
    else:
        return _median_of_medians_select_helper(arr, pivot_idx + 1, right,
                                                k - rank - 1)


def median_of_medians_select(arr: List[int], k: int) -> int:
    """
    Find the k-th smallest element using Median of Medians.

    Guarantees O(n) worst-case time by always choosing a pivot that
    lies between the 30th and 70th percentile of the current subarray.

    Args:
        arr: List of integers (a copy is used internally; original unchanged)
        k: 1-based rank (k=1 returns the minimum, k=len(arr) the maximum)

    Returns:
        The k-th smallest integer in arr

    Raises:
        ValueError: If k is out of range [1, len(arr)]
    """
    if not arr:
        raise ValueError("Cannot select from an empty list")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range [1, {len(arr)}]")

    work = arr.copy()
    return _median_of_medians_select_helper(work, 0, len(work) - 1, k - 1)


# ---------------------------------------------------------------------------
# Part 1: Randomized Selection — Randomized Quickselect
# ---------------------------------------------------------------------------

def _randomized_select_helper(arr: List[int], left: int, right: int,
                               k: int) -> int:
    """
    Recursive helper for randomized quickselect.

    Args:
        arr: The list (modified in-place)
        left: Start index (inclusive)
        right: End index (inclusive)
        k: 0-based rank of the desired element within arr[left..right]

    Returns:
        The k-th smallest value in arr[left..right]
    """
    if left == right:
        return arr[left]

    pivot_idx = _randomized_partition(arr, left, right)
    rank = pivot_idx - left

    if k == rank:
        return arr[pivot_idx]
    elif k < rank:
        return _randomized_select_helper(arr, left, pivot_idx - 1, k)
    else:
        return _randomized_select_helper(arr, pivot_idx + 1, right, k - rank - 1)


def randomized_quickselect(arr: List[int], k: int) -> int:
    """
    Find the k-th smallest element using Randomized Quickselect.

    Uses a uniformly random pivot at each step, achieving expected O(n)
    time on any input distribution. No adversarial input can reliably
    force worst-case O(n²) behaviour.

    Args:
        arr: List of integers (a copy is used internally; original unchanged)
        k: 1-based rank (k=1 returns the minimum, k=len(arr) the maximum)

    Returns:
        The k-th smallest integer in arr

    Raises:
        ValueError: If k is out of range [1, len(arr)]
    """
    if not arr:
        raise ValueError("Cannot select from an empty list")
    if k < 1 or k > len(arr):
        raise ValueError(f"k={k} is out of range [1, {len(arr)}]")

    work = arr.copy()
    return _randomized_select_helper(work, 0, len(work) - 1, k - 1)


# ---------------------------------------------------------------------------
# Timing utility
# ---------------------------------------------------------------------------

def measure_time(select_func: Callable, arr: List[int], k: int) -> float:
    """
    Measure the wall-clock execution time of a selection function.

    Args:
        select_func: Selection function with signature f(arr, k) -> int
        arr: Input list (passed directly; function should copy internally)
        k: The 1-based rank to select

    Returns:
        Execution time in seconds
    """
    start = time.perf_counter()
    select_func(arr, k)
    end = time.perf_counter()
    return end - start


# ---------------------------------------------------------------------------
# Quick demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_arr = [7, 2, 10, 4, 3, 8, 1, 6, 5, 9]
    print(f"Array: {test_arr}")
    print(f"Sorted: {sorted(test_arr)}")
    print()

    for k in [1, 3, 5, 8, 10]:
        mom = median_of_medians_select(test_arr, k)
        rqs = randomized_quickselect(test_arr, k)
        print(f"k={k:2d}  Median-of-Medians: {mom}   Randomized Quickselect: {rqs}")
