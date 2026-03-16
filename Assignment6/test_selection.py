"""
Unit tests for the deterministic (Median of Medians) and randomized
(Randomized Quickselect) selection algorithms.
"""
import random
import unittest
from selection import median_of_medians_select, randomized_quickselect


class _SelectionTestMixin:
    """
    Shared test logic for any selection algorithm.

    Subclasses must define self.select(arr, k) -> int.
    """

    # ---- Correctness tests -----------------------------------------------

    def test_minimum(self):
        """k=1 should return the smallest element."""
        arr = [5, 3, 1, 4, 2]
        self.assertEqual(self.select(arr, 1), 1)

    def test_maximum(self):
        """k=n should return the largest element."""
        arr = [5, 3, 1, 4, 2]
        self.assertEqual(self.select(arr, 5), 5)

    def test_median_odd(self):
        """k=(n+1)//2 on an odd-length array."""
        arr = [7, 2, 5, 1, 9, 3, 8]
        self.assertEqual(self.select(arr, 4), 5)

    def test_median_even(self):
        """k=n//2 on an even-length array."""
        arr = [4, 1, 7, 3, 8, 2]
        self.assertEqual(self.select(arr, 3), 3)

    def test_sorted_input(self):
        """Sorted array — k-th smallest is simply arr[k-1]."""
        arr = list(range(1, 11))  # [1..10]
        for k in range(1, 11):
            self.assertEqual(self.select(arr, k), k)

    def test_reverse_sorted_input(self):
        """Reverse-sorted array."""
        arr = list(range(10, 0, -1))  # [10, 9, ..., 1]
        for k in range(1, 11):
            self.assertEqual(self.select(arr, k), k)

    def test_duplicates(self):
        """Array with repeated values."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = sorted(arr)
        for k in range(1, len(arr) + 1):
            self.assertEqual(self.select(arr, k), expected[k - 1])

    def test_all_equal(self):
        """All elements are identical."""
        arr = [7] * 8
        for k in range(1, 9):
            self.assertEqual(self.select(arr, k), 7)

    def test_negative_numbers(self):
        """Array containing negative integers."""
        arr = [-3, -1, -4, -1, -5, -9, -2, -6]
        expected = sorted(arr)
        for k in range(1, len(arr) + 1):
            self.assertEqual(self.select(arr, k), expected[k - 1])

    def test_single_element(self):
        """Single-element array — only valid k is 1."""
        self.assertEqual(self.select([42], 1), 42)

    def test_two_elements(self):
        """Two-element array."""
        arr = [9, 3]
        self.assertEqual(self.select(arr, 1), 3)
        self.assertEqual(self.select(arr, 2), 9)

    def test_large_random(self):
        """Verify correctness on a large random array."""
        arr = [random.randint(-1000, 1000) for _ in range(500)]
        expected = sorted(arr)
        for k in [1, 50, 125, 250, 375, 499, 500]:
            self.assertEqual(self.select(arr, k), expected[k - 1])

    def test_original_array_unchanged(self):
        """The original array must not be mutated."""
        arr = [5, 3, 1, 4, 2]
        original = arr.copy()
        self.select(arr, 3)
        self.assertEqual(arr, original)

    # ---- Edge-case / error tests ----------------------------------------

    def test_k_out_of_range_low(self):
        """k=0 should raise ValueError."""
        with self.assertRaises(ValueError):
            self.select([1, 2, 3], 0)

    def test_k_out_of_range_high(self):
        """k > n should raise ValueError."""
        with self.assertRaises(ValueError):
            self.select([1, 2, 3], 4)

    def test_empty_array(self):
        """Empty array should raise ValueError."""
        with self.assertRaises(ValueError):
            self.select([], 1)

    # ---- Groups-of-5 boundary (Median of Medians specific) ---------------

    def test_exactly_5_elements(self):
        """Exactly one group of 5 — tests base case of _median_of_medians."""
        arr = [5, 1, 4, 2, 3]
        expected = sorted(arr)
        for k in range(1, 6):
            self.assertEqual(self.select(arr, k), expected[k - 1])

    def test_exactly_6_elements(self):
        """Six elements — two groups (5 + 1), tests split at boundary."""
        arr = [6, 2, 5, 1, 4, 3]
        expected = sorted(arr)
        for k in range(1, 7):
            self.assertEqual(self.select(arr, k), expected[k - 1])

    def test_exactly_10_elements(self):
        """Ten elements — two full groups of 5."""
        arr = [10, 1, 9, 2, 8, 3, 7, 4, 6, 5]
        expected = sorted(arr)
        for k in range(1, 11):
            self.assertEqual(self.select(arr, k), expected[k - 1])


class TestMedianOfMedians(_SelectionTestMixin, unittest.TestCase):
    """Tests for the deterministic Median-of-Medians algorithm."""

    def select(self, arr, k):
        return median_of_medians_select(arr, k)


class TestRandomizedQuickselect(_SelectionTestMixin, unittest.TestCase):
    """Tests for the randomized Quickselect algorithm."""

    def select(self, arr, k):
        return randomized_quickselect(arr, k)

    def test_randomness_does_not_affect_correctness(self):
        """Run randomized quickselect many times to confirm consistent results."""
        for _ in range(30):
            arr = [random.randint(-200, 200) for _ in range(40)]
            k = random.randint(1, len(arr))
            expected = sorted(arr)[k - 1]
            self.assertEqual(self.select(arr, k), expected)


if __name__ == '__main__':
    unittest.main()
