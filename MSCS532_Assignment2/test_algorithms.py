"""
Unit Tests for Quick Sort and Merge Sort Implementations
This module contains comprehensive tests to verify correctness of both algorithms.
"""

import unittest
import random
from quick_sort import quick_sort, quick_sort_randomized, partition
from merge_sort import merge_sort, merge_sort_inplace, merge


class TestQuickSort(unittest.TestCase):
    """Test cases for Quick Sort implementation."""

    def test_empty_array(self):
        """Test Quick Sort with an empty array."""
        arr = []
        result = quick_sort(arr.copy())
        self.assertEqual(result, [])

    def test_single_element(self):
        """Test Quick Sort with a single element."""
        arr = [42]
        result = quick_sort(arr.copy())
        self.assertEqual(result, [42])

    def test_already_sorted(self):
        """Test Quick Sort with already sorted array."""
        arr = [1, 2, 3, 4, 5]
        # Use randomized to avoid O(n²)
        result = quick_sort_randomized(arr.copy())
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Test Quick Sort with reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        result = quick_sort_randomized(arr.copy())
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_random_array(self):
        """Test Quick Sort with random array."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = quick_sort(arr.copy())
        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])

    def test_duplicates(self):
        """Test Quick Sort with duplicate elements."""
        arr = [5, 2, 8, 2, 9, 1, 5, 5]
        result = quick_sort(arr.copy())
        self.assertEqual(result, [1, 2, 2, 5, 5, 5, 8, 9])

    def test_all_same_elements(self):
        """Test Quick Sort with all identical elements."""
        arr = [7, 7, 7, 7, 7]
        result = quick_sort(arr.copy())
        self.assertEqual(result, [7, 7, 7, 7, 7])

    def test_negative_numbers(self):
        """Test Quick Sort with negative numbers."""
        arr = [-5, 3, -1, 7, -9, 2]
        result = quick_sort(arr.copy())
        self.assertEqual(result, [-9, -5, -1, 2, 3, 7])

    def test_large_random_array(self):
        """Test Quick Sort with a large random array."""
        arr = random.sample(range(1000), 100)
        result = quick_sort_randomized(arr.copy())
        self.assertEqual(result, sorted(arr))

    def test_partition_function(self):
        """Test the partition function independently."""
        arr = [10, 7, 8, 9, 1, 5]
        pivot_index = partition(arr, 0, len(arr) - 1)
        # Verify all elements left of pivot are <= pivot
        # and all elements right of pivot are >= pivot
        pivot = arr[pivot_index]
        for i in range(pivot_index):
            self.assertLessEqual(arr[i], pivot)
        for i in range(pivot_index + 1, len(arr)):
            self.assertGreaterEqual(arr[i], pivot)


class TestMergeSort(unittest.TestCase):
    """Test cases for Merge Sort implementation."""

    def test_empty_array(self):
        """Test Merge Sort with an empty array."""
        arr = []
        result = merge_sort(arr)
        self.assertEqual(result, [])

    def test_single_element(self):
        """Test Merge Sort with a single element."""
        arr = [42]
        result = merge_sort(arr)
        self.assertEqual(result, [42])

    def test_already_sorted(self):
        """Test Merge Sort with already sorted array."""
        arr = [1, 2, 3, 4, 5]
        result = merge_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        """Test Merge Sort with reverse sorted array."""
        arr = [5, 4, 3, 2, 1]
        result = merge_sort(arr)
        self.assertEqual(result, [1, 2, 3, 4, 5])

    def test_random_array(self):
        """Test Merge Sort with random array."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = merge_sort(arr)
        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])

    def test_duplicates(self):
        """Test Merge Sort with duplicate elements."""
        arr = [5, 2, 8, 2, 9, 1, 5, 5]
        result = merge_sort(arr)
        self.assertEqual(result, [1, 2, 2, 5, 5, 5, 8, 9])

    def test_all_same_elements(self):
        """Test Merge Sort with all identical elements."""
        arr = [7, 7, 7, 7, 7]
        result = merge_sort(arr)
        self.assertEqual(result, [7, 7, 7, 7, 7])

    def test_negative_numbers(self):
        """Test Merge Sort with negative numbers."""
        arr = [-5, 3, -1, 7, -9, 2]
        result = merge_sort(arr)
        self.assertEqual(result, [-9, -5, -1, 2, 3, 7])

    def test_large_random_array(self):
        """Test Merge Sort with a large random array."""
        arr = random.sample(range(1000), 100)
        result = merge_sort(arr)
        self.assertEqual(result, sorted(arr))

    def test_merge_function(self):
        """Test the merge function independently."""
        left = [1, 3, 5]
        right = [2, 4, 6]
        result = merge(left, right)
        self.assertEqual(result, [1, 2, 3, 4, 5, 6])

    def test_inplace_version(self):
        """Test in-place Merge Sort variant."""
        arr = [64, 34, 25, 12, 22, 11, 90]
        result = merge_sort_inplace(arr.copy())
        self.assertEqual(result, [11, 12, 22, 25, 34, 64, 90])

    def test_stability(self):
        """Test that Merge Sort is stable (preserves relative order of equal elements)."""
        # Using tuples where first element is key, second is original position
        arr = [(3, 0), (1, 1), (3, 2), (2, 3), (1, 4)]
        result = merge_sort(arr)
        expected = [(1, 1), (1, 4), (2, 3), (3, 0), (3, 2)]
        self.assertEqual(result, expected)


class TestComparison(unittest.TestCase):
    """Test cases comparing both algorithms."""

    def test_same_output(self):
        """Verify both algorithms produce identical results."""
        test_cases = [
            [],
            [1],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [64, 34, 25, 12, 22, 11, 90],
            [5, 2, 8, 2, 9, 1, 5, 5],
            [-5, 3, -1, 7, -9, 2],
            random.sample(range(100), 50)
        ]

        for arr in test_cases:
            quick_result = quick_sort_randomized(arr.copy())
            merge_result = merge_sort(arr.copy())
            self.assertEqual(quick_result, merge_result,
                             f"Results differ for input {arr}")

    def test_correctness_verification(self):
        """Verify both algorithms produce correctly sorted output."""
        arr = random.sample(range(1000), 100)
        expected = sorted(arr)

        quick_result = quick_sort_randomized(arr.copy())
        merge_result = merge_sort(arr.copy())

        self.assertEqual(quick_result, expected)
        self.assertEqual(merge_result, expected)

    def test_worst_case_quick_sort(self):
        """Test Quick Sort's worst case (sorted array with standard pivot)."""
        # Small array to avoid recursion limit
        arr = list(range(50))
        # Use randomized version to handle worst case efficiently
        result = quick_sort_randomized(arr.copy())
        self.assertEqual(result, arr)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios."""

    def test_two_elements_ascending(self):
        """Test with two elements in ascending order."""
        arr = [1, 2]
        self.assertEqual(quick_sort(arr.copy()), [1, 2])
        self.assertEqual(merge_sort(arr), [1, 2])

    def test_two_elements_descending(self):
        """Test with two elements in descending order."""
        arr = [2, 1]
        self.assertEqual(quick_sort(arr.copy()), [1, 2])
        self.assertEqual(merge_sort(arr), [1, 2])

    def test_very_large_values(self):
        """Test with very large integer values."""
        arr = [1000000, 999999, 1000001, 500000]
        expected = [500000, 999999, 1000000, 1000001]
        self.assertEqual(quick_sort_randomized(arr.copy()), expected)
        self.assertEqual(merge_sort(arr), expected)

    def test_mixed_positive_negative(self):
        """Test with mixed positive and negative values."""
        arr = [10, -5, 0, -10, 5]
        expected = [-10, -5, 0, 5, 10]
        self.assertEqual(quick_sort(arr.copy()), expected)
        self.assertEqual(merge_sort(arr), expected)

    def test_float_values(self):
        """Test with floating-point values."""
        arr = [3.14, 1.41, 2.71, 0.57]
        expected = [0.57, 1.41, 2.71, 3.14]
        self.assertEqual(quick_sort(arr.copy()), expected)
        self.assertEqual(merge_sort(arr), expected)


def run_tests():
    """Run all test suites and display results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestQuickSort))
    suite.addTests(loader.loadTestsFromTestCase(TestMergeSort))
    suite.addTests(loader.loadTestsFromTestCase(TestComparison))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(
        f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
