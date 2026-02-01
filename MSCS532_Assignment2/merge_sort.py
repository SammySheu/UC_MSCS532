import time
import tracemalloc


def merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return merge(left_half, right_half)


def merge(left, right):

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def merge_sort_inplace(arr, left=0, right=None):

    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2

        merge_sort_inplace(arr, left, mid)
        merge_sort_inplace(arr, mid + 1, right)

        # Merge the sorted halves
        merge_inplace(arr, left, mid, right)

    return arr


def merge_inplace(arr, left, mid, right):
    """
    Merges two sorted subarrays in-place.

    Args:
        arr: Array containing both subarrays
        left: Starting index of first subarray
        mid: Ending index of first subarray
        right: Ending index of second subarray
    """
    left_array = arr[left:mid + 1]
    right_array = arr[mid + 1:right + 1]

    i = j = 0  # Initial indexes for left_array and right_array
    k = left   # Initial index for merged array

    while i < len(left_array) and j < len(right_array):
        if left_array[i] <= right_array[j]:
            arr[k] = left_array[i]
            i += 1
        else:
            arr[k] = right_array[j]
            j += 1
        k += 1

    while i < len(left_array):
        arr[k] = left_array[i]
        i += 1
        k += 1

    while j < len(right_array):
        arr[k] = right_array[j]
        j += 1
        k += 1


def measure_merge_sort_performance(arr, inplace=False):
    test_arr = arr.copy()

    tracemalloc.start()

    start_time = time.perf_counter()

    if inplace:
        sorted_arr = merge_sort_inplace(test_arr)
    else:
        sorted_arr = merge_sort(test_arr)

    end_time = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end_time - start_time
    peak_memory = peak / 1024  # Convert to KB

    return sorted_arr, execution_time, peak_memory


def merge_sort_with_stats(arr):
    """
    Merge Sort with detailed statistics tracking.

    Args:
        arr: List to sort

    Returns:
        Tuple of (sorted_array, comparisons, recursive_calls)
    """
    stats = {'comparisons': 0, 'recursive_calls': 0}

    def merge_sort_tracked(arr):
        stats['recursive_calls'] += 1

        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2
        left_half = merge_sort_tracked(arr[:mid])
        right_half = merge_sort_tracked(arr[mid:])

        return merge_tracked(left_half, right_half)

    def merge_tracked(left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            stats['comparisons'] += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result

    sorted_arr = merge_sort_tracked(arr)
    return sorted_arr, stats['comparisons'], stats['recursive_calls']


# Example usage and testing
if __name__ == "__main__":
    test_arrays = {
        "Random": [64, 34, 25, 12, 22, 11, 90, 88, 45, 50],
        "Sorted": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Reverse Sorted": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1],
        "Duplicates": [5, 2, 8, 2, 9, 1, 5, 5, 3, 2]
    }

    print("Merge Sort Implementation Test\n" + "="*50)

    for data_type, arr in test_arrays.items():
        print(f"\n{data_type} Array: {arr}")

        # Standard Merge Sort
        sorted_arr, exec_time, memory = measure_merge_sort_performance(arr)
        print(f"Standard Merge Sort: {sorted_arr}")
        print(f"Time: {exec_time:.6f} seconds, Memory: {memory:.2f} KB")

        # In-place Merge Sort
        sorted_arr_ip, exec_time_ip, memory_ip = measure_merge_sort_performance(
            arr, inplace=True)
        print(f"In-place Merge Sort: {sorted_arr_ip}")
        print(f"Time: {exec_time_ip:.6f} seconds, Memory: {memory_ip:.2f} KB")

        # With statistics
        sorted_arr_stats, comparisons, calls = merge_sort_with_stats(arr)
        print(
            f"Statistics: {comparisons} comparisons, {calls} recursive calls")
