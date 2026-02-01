import random
import time
import tracemalloc


def quick_sort(arr, low=0, high=None):

    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition(arr, low, high)

        quick_sort(arr, low, pivot_index - 1)
        quick_sort(arr, pivot_index + 1, high)

    return arr


def partition(arr, low, high):

    pivot = arr[high]

    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_randomized(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition_randomized(arr, low, high)

        quick_sort_randomized(arr, low, pivot_index - 1)
        quick_sort_randomized(arr, pivot_index + 1, high)

    return arr


def partition_randomized(arr, low, high):
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]

    return partition(arr, low, high)


def measure_quick_sort_performance(arr, randomized=False):
    """
    Measures execution time and memory usage for Quick Sort.

    Args:
        arr: List to sort
        randomized: If True, uses randomized pivot selection

    Returns:
        Tuple of (sorted_array, execution_time, peak_memory)
    """
    # Create a copy to avoid modifying original
    test_arr = arr.copy()

    # Start memory tracking
    tracemalloc.start()

    # Measure execution time
    start_time = time.perf_counter()

    if randomized:
        sorted_arr = quick_sort_randomized(test_arr)
    else:
        sorted_arr = quick_sort(test_arr)

    end_time = time.perf_counter()

    # Get peak memory usage
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    peak_memory = peak / 1024  # Convert to KB

    return sorted_arr, execution_time, peak_memory


# Example usage and testing
if __name__ == "__main__":
    # Test with different data types
    test_arrays = {
        "Random": [64, 34, 25, 12, 22, 11, 90, 88, 45, 50],
        "Sorted": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Reverse Sorted": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Duplicates": [5, 2, 8, 2, 9, 1, 5, 5, 3, 2]
    }

    print("Quick Sort Implementation Test\n" + "="*50)

    for data_type, arr in test_arrays.items():
        print(f"\n{data_type} Array: {arr}")

        # Standard Quick Sort
        sorted_arr, exec_time, memory = measure_quick_sort_performance(arr)
        print(f"Standard Quick Sort: {sorted_arr}")
        print(f"Time: {exec_time:.6f} seconds, Memory: {memory:.2f} KB")

        # Randomized Quick Sort
        sorted_arr_rand, exec_time_rand, memory_rand = measure_quick_sort_performance(
            arr, randomized=True)
        print(f"Randomized Quick Sort: {sorted_arr_rand}")
        print(
            f"Time: {exec_time_rand:.6f} seconds, Memory: {memory_rand:.2f} KB")
