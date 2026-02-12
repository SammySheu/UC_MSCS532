import time
from typing import List, Callable


def max_heapify(arr: List[int], n: int, i: int) -> None:
    """
    Maintain the max-heap property for a subtree rooted at index i.

    Args:
        arr: The array representing the heap
        n: Size of the heap
        i: Index of the root of the subtree
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        max_heapify(arr, n, largest)


def build_max_heap(arr: List[int]) -> None:
    """
    Build a max-heap from an unordered array in-place.
    Starts from the last non-leaf node and heapifies downward.

    Args:
        arr: The array to transform into a max-heap
    """
    n = len(arr)
    # Start from the last non-leaf node (parent of the last element)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(arr, n, i)


def heapsort(arr: List[int]) -> List[int]:
    """
    Sort an array in ascending order using Heapsort.

    Args:
        arr: List of integers to sort

    Returns:
        The sorted list (sorted in-place)
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Step 1: Build a max-heap
    build_max_heap(arr)

    # Step 2: Repeatedly extract the maximum (root) and place it at the end.
    for i in range(n - 1, 0, -1):
        # Move current root (maximum) to the end
        arr[0], arr[i] = arr[i], arr[0]
        # Step 3: Reduce heap size and heapify the root.
        max_heapify(arr, i, 0)

    return arr


def merge_sort(arr: List[int]) -> List[int]:
    """
    Sort an array using Merge Sort.

    Args:
        arr: List of integers to sort

    Returns:
        The sorted list
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right, arr)


def _merge(left: List[int], right: List[int], arr: List[int]) -> List[int]:
    """
    Merge two sorted lists into the original array.

    Args:
        left: Left sorted sublist
        right: Right sorted sublist
        arr: Original array to write merged result into

    Returns:
        The merged sorted array
    """
    i = j = k = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1

    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1

    return arr


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
    test_arr = [12, 11, 13, 5, 6, 7]
    print(f"Original array: {test_arr}")

    sorted_arr = test_arr.copy()
    heapsort(sorted_arr)
    print(f"Heapsort result: {sorted_arr}")

    merge_arr = test_arr.copy()
    merge_sort(merge_arr)
    print(f"Merge Sort result: {merge_arr}")
