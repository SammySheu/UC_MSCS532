"""
Quicksort Algorithm - Deterministic and Randomized Implementations
Assignment 5 - Quicksort Algorithm: Implementation, Analysis, and Randomization
"""
import random
import time
from typing import List, Callable


# ---------------------------------------------------------------------------
# Partition helpers
# ---------------------------------------------------------------------------

def partition(arr: List[int], left: int, right: int) -> int:
    """
    Lomuto partition scheme using the rightmost element as pivot.

    Rearranges elements so that all values <= pivot are to its left
    and all values > pivot are to its right, then places the pivot
    at its final sorted position.

    Args:
        arr: The list to partition (modified in-place)
        left: Starting index of the subarray
        right: Ending index of the subarray (pivot is arr[right])

    Returns:
        The final index of the pivot element
    """
    pivot = arr[right]
    i = left - 1  # index of the last element <= pivot

    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    # Place the pivot in its correct sorted position
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def randomized_partition(arr: List[int], left: int, right: int) -> int:
    """
    Partition using a uniformly random pivot chosen from [left, right].

    Swaps a randomly chosen element to the rightmost position, then
    delegates to the standard Lomuto partition.

    Args:
        arr: The list to partition (modified in-place)
        left: Starting index of the subarray
        right: Ending index of the subarray

    Returns:
        The final index of the pivot element
    """
    random_index = random.randint(left, right)
    # Swap the randomly chosen element to the rightmost position
    arr[random_index], arr[right] = arr[right], arr[random_index]
    return partition(arr, left, right)


# ---------------------------------------------------------------------------
# Deterministic Quicksort
# ---------------------------------------------------------------------------

def deterministic_quicksort(arr: List[int], left: int = None, right: int = None) -> List[int]:
    """
    Sort an array in ascending order using deterministic Quicksort.

    Always selects the last element as the pivot. This is optimal on
    random data but degrades to O(n^2) on already-sorted or
    reverse-sorted input.

    Args:
        arr: List of integers to sort (modified in-place)
        left: Starting index (default: 0)
        right: Ending index (default: len(arr) - 1)

    Returns:
        The sorted list (sorted in-place)
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    if left < right:
        pivot_index = partition(arr, left, right)
        # Recursively sort the two partitions
        deterministic_quicksort(arr, left, pivot_index - 1)
        deterministic_quicksort(arr, pivot_index + 1, right)

    return arr


# ---------------------------------------------------------------------------
# Randomized Quicksort
# ---------------------------------------------------------------------------

def randomized_quicksort(arr: List[int], left: int = None, right: int = None) -> List[int]:
    """
    Sort an array in ascending order using randomized Quicksort.

    Selects a uniformly random pivot at each recursive call, which
    eliminates any adversarial input pattern and guarantees expected
    O(n log n) performance regardless of input distribution.

    Args:
        arr: List of integers to sort (modified in-place)
        left: Starting index (default: 0)
        right: Ending index (default: len(arr) - 1)

    Returns:
        The sorted list (sorted in-place)
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    if left < right:
        pivot_index = randomized_partition(arr, left, right)
        # Recursively sort the two partitions
        randomized_quicksort(arr, left, pivot_index - 1)
        randomized_quicksort(arr, pivot_index + 1, right)

    return arr


# ---------------------------------------------------------------------------
# Timing utility
# ---------------------------------------------------------------------------

def measure_time(sort_func: Callable, arr: List[int]) -> float:
    """
    Measure the wall-clock execution time of a sorting function.

    Args:
        sort_func: Sorting function to time; must accept a list and sort in-place
        arr: Input list (a copy is made so the original is not modified)

    Returns:
        Execution time in seconds, or float('nan') if a RecursionError occurs
    """
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    try:
        sort_func(arr_copy)
    except RecursionError:
        return float('nan')
    end_time = time.perf_counter()
    return end_time - start_time


# ---------------------------------------------------------------------------
# Quick demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array:          {test_arr}")

    det_arr = test_arr.copy()
    deterministic_quicksort(det_arr)
    print(f"Deterministic Quicksort: {det_arr}")

    rand_arr = test_arr.copy()
    randomized_quicksort(rand_arr)
    print(f"Randomized Quicksort:    {rand_arr}")
