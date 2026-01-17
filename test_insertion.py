import unittest
from insertion_sort import insertion_sort


class TestInsertionSort(unittest.TestCase):
    """Test cases for insertion_sort function that sorts in monotonically decreasing order."""

    def test_basic_sorting_ascending_input(self):
        """Test sorting when input is in ascending order (should reverse to descending)."""
        nums = [1, 2, 3, 4, 5]
        insertion_sort(nums)
        self.assertEqual(nums, [5, 4, 3, 2, 1])

    def test_basic_sorting_descending_input(self):
        """Test sorting when input is already in descending order (should remain unchanged)."""
        nums = [5, 4, 3, 2, 1]
        insertion_sort(nums)
        self.assertEqual(nums, [5, 4, 3, 2, 1])

    def test_random_order(self):
        """Test sorting with random order."""
        nums = [3, 1, 4, 1, 5, 9, 2, 6]
        insertion_sort(nums)
        self.assertEqual(nums, [9, 6, 5, 4, 3, 2, 1, 1])

    def test_duplicates(self):
        """Test sorting with duplicate values."""
        nums = [3, 3, 3, 1, 2, 2, 1]
        insertion_sort(nums)
        self.assertEqual(nums, [3, 3, 3, 2, 2, 1, 1])

    def test_negative_numbers(self):
        """Test sorting with negative numbers."""
        nums = [-1, -3, -2, 0, 1, -4]
        insertion_sort(nums)
        self.assertEqual(nums, [1, 0, -1, -2, -3, -4])

    def test_single_element(self):
        """Test sorting with single element."""
        nums = [42]
        insertion_sort(nums)
        self.assertEqual(nums, [42])

    def test_empty_list(self):
        """Test sorting with empty list."""
        nums = []
        insertion_sort(nums)
        self.assertEqual(nums, [])

    def test_two_elements_ascending(self):
        """Test sorting with two elements in ascending order."""
        nums = [1, 2]
        insertion_sort(nums)
        self.assertEqual(nums, [2, 1])

    def test_two_elements_descending(self):
        """Test sorting with two elements in descending order."""
        nums = [2, 1]
        insertion_sort(nums)
        self.assertEqual(nums, [2, 1])

    def test_large_list(self):
        """Test sorting with a larger list."""
        nums = list(range(10))
        insertion_sort(nums)
        self.assertEqual(nums, list(range(9, -1, -1)))

    def test_modified_in_place(self):
        """Test that the function modifies the list in-place."""
        nums = [1, 2, 3]
        original_id = id(nums)
        insertion_sort(nums)
        # Same object, modified in-place
        self.assertEqual(id(nums), original_id)


if __name__ == '__main__':
    unittest.main()
