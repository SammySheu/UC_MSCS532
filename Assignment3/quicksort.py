import random
import time
from typing import List, Callable


def randomized_quicksort(arr: List[int], left: int = None, right: int = None) -> List[int]:
    """
    Implements Randomized Quicksort where pivot is chosen uniformly at random.
    
    Args:
        arr: List of integers to sort
        left: Starting index (default: 0)
        right: Ending index (default: len(arr) - 1)
    
    Returns:
        Sorted list
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        # use the index to partition the array
        pivot_index = randomized_partition(arr, left, right)

        # quicksort from the left to the pivot index - 1
        randomized_quicksort(arr, left, pivot_index - 1)

        # quicksort from the pivot index + 1 to the right
        randomized_quicksort(arr, pivot_index + 1, right)
    
    return arr


def randomized_partition(arr: List[int], left: int, right: int) -> int:
    """
    Partition function that selects a random pivot.
    
    Args:
        arr: List to partition
        left: Starting index
        right: Ending index
    
    Returns:
        Final position of pivot element
    """
    # Choose random pivot uniformly
    random_index = random.randint(left, right)
    # Swap random element with rightmost element
    arr[random_index], arr[right] = arr[right], arr[random_index]
    
    return partition(arr, left, right)


def deterministic_quicksort(arr: List[int], left: int = None, right: int = None) -> List[int]:
    """
    Implements Deterministic Quicksort using first element as pivot.
    
    Args:
        arr: List of integers to sort
        left: Starting index (default: 0)
        right: Ending index (default: len(arr) - 1)
    
    Returns:
        Sorted list
    """
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1
    
    if left < right:
        pivot_index = deterministic_partition(arr, left, right)
        deterministic_quicksort(arr, left, pivot_index - 1)
        deterministic_quicksort(arr, pivot_index + 1, right)
    
    return arr


def deterministic_partition(arr: List[int], left: int, right: int) -> int:
    """
    Partition function using first element as pivot.
    
    Args:
        arr: List to partition
        left: Starting index
        right: Ending index
    
    Returns:
        Final position of pivot element
    """
    # Use first element as pivot (worst case for sorted arrays)
    pivot = arr[left]
    i = left
    
    for j in range(left + 1, right + 1):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[left], arr[i] = arr[i], arr[left]
    return i


def partition(arr: List[int], left: int, right: int) -> int:
    """
    Standard partition function using rightmost element as pivot.
    
    Args:
        arr: List to partition
        left: Starting index
        right: Ending index
    
    Returns:
        Final position of pivot element
    """
    pivot = arr[right]
    i = left - 1
    
    for j in range(left, right):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[right] = arr[right], arr[i + 1]
    return i + 1


def measure_time(sort_func: Callable, arr: List[int]) -> float:
    """
    Measures execution time of a sorting function.
    
    Args:
        sort_func: Sorting function to measure
        arr: List to sort
    
    Returns:
        Execution time in seconds
    """
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    end_time = time.perf_counter()
    return end_time - start_time



if __name__ == "__main__":
    
    # Quick demonstration
    test_arr = [64, 34, 25, 12, 22, 11, 90]
    print(f"Original array: {test_arr}")
    
    random_arr = test_arr.copy()
    randomized_quicksort(random_arr)
    print(f"Randomized Quicksort result: {random_arr}")
    
    determ_arr = test_arr.copy()
    deterministic_quicksort(determ_arr)
    print(f"Deterministic Quicksort result: {determ_arr}")
