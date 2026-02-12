import unittest
from heapsort import heapsort, build_max_heap, merge_sort


class TestHeapsort(unittest.TestCase):
    """Test cases for the Heapsort implementation."""

    def test_basic_sorting(self):
        """Test sorting a basic unsorted array."""
        arr = [12, 11, 13, 5, 6, 7]
        heapsort(arr)
        self.assertEqual(arr, [5, 6, 7, 11, 12, 13])

    def test_already_sorted(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5]
        heapsort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Test sorting a reverse-sorted array."""
        arr = [5, 4, 3, 2, 1]
        heapsort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_duplicates(self):
        """Test sorting with duplicate values."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        heapsort(arr)
        self.assertEqual(arr, [1, 1, 2, 3, 3, 4, 5, 5, 6, 9])

    def test_negative_numbers(self):
        """Test sorting with negative numbers."""
        arr = [-1, -3, -2, 0, 1, -4]
        heapsort(arr)
        self.assertEqual(arr, [-4, -3, -2, -1, 0, 1])

    def test_single_element(self):
        """Test sorting a single-element array."""
        arr = [42]
        heapsort(arr)
        self.assertEqual(arr, [42])

    def test_empty_list(self):
        """Test sorting an empty array."""
        arr = []
        heapsort(arr)
        self.assertEqual(arr, [])

    def test_two_elements(self):
        """Test sorting a two-element array."""
        arr = [2, 1]
        heapsort(arr)
        self.assertEqual(arr, [1, 2])

    def test_large_list(self):
        """Test sorting a larger list."""
        arr = list(range(100, 0, -1))
        heapsort(arr)
        self.assertEqual(arr, list(range(1, 101)))

    def test_in_place(self):
        """Test that heapsort modifies the list in-place."""
        arr = [3, 1, 2]
        original_id = id(arr)
        heapsort(arr)
        self.assertEqual(id(arr), original_id)


class TestBuildMaxHeap(unittest.TestCase):
    """Test cases for the build_max_heap function."""

    def test_max_heap_property(self):
        """Test that build_max_heap produces a valid max-heap."""
        arr = [4, 1, 3, 2, 16, 9, 10, 14, 8, 7]
        build_max_heap(arr)

        # Verify max-heap property: parent >= children
        n = len(arr)
        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n:
                self.assertGreaterEqual(arr[i], arr[left])
            if right < n:
                self.assertGreaterEqual(arr[i], arr[right])

    def test_root_is_maximum(self):
        """Test that root of max-heap is the maximum element."""
        arr = [3, 7, 1, 9, 2, 8, 4]
        build_max_heap(arr)
        self.assertEqual(arr[0], 9)


class TestMergeSort(unittest.TestCase):
    """Test cases for the Merge Sort implementation."""

    def test_basic_sorting(self):
        """Test sorting a basic unsorted array."""
        arr = [12, 11, 13, 5, 6, 7]
        merge_sort(arr)
        self.assertEqual(arr, [5, 6, 7, 11, 12, 13])

    def test_already_sorted(self):
        """Test sorting an already sorted array."""
        arr = [1, 2, 3, 4, 5]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Test sorting a reverse-sorted array."""
        arr = [5, 4, 3, 2, 1]
        merge_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5])

    def test_empty_and_single(self):
        """Test edge cases."""
        arr = []
        merge_sort(arr)
        self.assertEqual(arr, [])

        arr = [1]
        merge_sort(arr)
        self.assertEqual(arr, [1])


if __name__ == '__main__':
    unittest.main()
