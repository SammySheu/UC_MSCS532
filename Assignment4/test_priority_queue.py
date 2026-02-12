import unittest
from priority_queue import Task, MinHeapPriorityQueue


class TestTask(unittest.TestCase):
    """Test cases for the Task dataclass."""

    def test_task_creation(self):
        """Test creating a task with all fields."""
        task = Task(task_id=1, priority=3, arrival_time=1.0,
                    deadline=5.0, description="Test task")
        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.priority, 3)
        self.assertEqual(task.arrival_time, 1.0)
        self.assertEqual(task.deadline, 5.0)

    def test_task_comparison(self):
        """Test task comparison operators based on priority."""
        t1 = Task(task_id=1, priority=1)
        t2 = Task(task_id=2, priority=5)
        self.assertTrue(t1 < t2)
        self.assertTrue(t2 > t1)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t2 >= t1)


class TestMinHeapPriorityQueue(unittest.TestCase):
    """Test cases for the MinHeapPriorityQueue."""

    def setUp(self):
        """Set up a fresh priority queue for each test."""
        self.pq = MinHeapPriorityQueue()

    def test_is_empty_on_new_queue(self):
        """Test that a new queue is empty."""
        self.assertTrue(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 0)
        self.assertEqual(len(self.pq), 0)

    def test_insert_single(self):
        """Test inserting a single task."""
        task = Task(task_id=1, priority=5)
        self.pq.insert(task)
        self.assertFalse(self.pq.is_empty())
        self.assertEqual(self.pq.size(), 1)
        self.assertEqual(self.pq.peek().task_id, 1)

    def test_insert_multiple_maintains_min_heap(self):
        """Test that insert maintains the min-heap property."""
        tasks = [
            Task(task_id=1, priority=5),
            Task(task_id=2, priority=1),
            Task(task_id=3, priority=3),
        ]
        for t in tasks:
            self.pq.insert(t)

        # The minimum priority should be at the top
        self.assertEqual(self.pq.peek().task_id, 2)
        self.assertEqual(self.pq.peek().priority, 1)

    def test_extract_min_returns_lowest_priority(self):
        """Test that extract_min returns tasks in priority order."""
        self.pq.insert(Task(task_id=1, priority=5))
        self.pq.insert(Task(task_id=2, priority=1))
        self.pq.insert(Task(task_id=3, priority=3))

        t1 = self.pq.extract_min()
        self.assertEqual(t1.priority, 1)

        t2 = self.pq.extract_min()
        self.assertEqual(t2.priority, 3)

        t3 = self.pq.extract_min()
        self.assertEqual(t3.priority, 5)

    def test_extract_min_from_empty_raises(self):
        """Test that extract_min raises IndexError on empty queue."""
        with self.assertRaises(IndexError):
            self.pq.extract_min()

    def test_peek_from_empty_raises(self):
        """Test that peek raises IndexError on empty queue."""
        with self.assertRaises(IndexError):
            self.pq.peek()

    def test_decrease_key(self):
        """Test decreasing the priority of a task."""
        self.pq.insert(Task(task_id=1, priority=10))
        self.pq.insert(Task(task_id=2, priority=5))
        self.pq.insert(Task(task_id=3, priority=8))

        # Task 2 is currently at the top (priority 5)
        self.assertEqual(self.pq.peek().task_id, 2)

        # Decrease task 3's priority from 8 to 1 -> it should become the new min
        self.pq.decrease_key(task_id=3, new_priority=1)
        self.assertEqual(self.pq.peek().task_id, 3)
        self.assertEqual(self.pq.peek().priority, 1)

    def test_decrease_key_invalid_task(self):
        """Test decrease_key with non-existent task raises KeyError."""
        with self.assertRaises(KeyError):
            self.pq.decrease_key(task_id=999, new_priority=1)

    def test_decrease_key_higher_value_raises(self):
        """Test decrease_key with higher value raises ValueError."""
        self.pq.insert(Task(task_id=1, priority=5))
        with self.assertRaises(ValueError):
            self.pq.decrease_key(task_id=1, new_priority=10)

    def test_increase_key(self):
        """Test increasing the priority of a task."""
        self.pq.insert(Task(task_id=1, priority=1))
        self.pq.insert(Task(task_id=2, priority=5))
        self.pq.insert(Task(task_id=3, priority=3))

        # Task 1 is at the top (priority 1)
        self.assertEqual(self.pq.peek().task_id, 1)

        # Increase task 1's priority from 1 to 10 -> task 3 should be new min
        self.pq.increase_key(task_id=1, new_priority=10)
        self.assertEqual(self.pq.peek().task_id, 3)
        self.assertEqual(self.pq.peek().priority, 3)

    def test_increase_key_invalid_task(self):
        """Test increase_key with non-existent task raises KeyError."""
        with self.assertRaises(KeyError):
            self.pq.increase_key(task_id=999, new_priority=10)

    def test_increase_key_lower_value_raises(self):
        """Test increase_key with lower value raises ValueError."""
        self.pq.insert(Task(task_id=1, priority=5))
        with self.assertRaises(ValueError):
            self.pq.increase_key(task_id=1, new_priority=2)

    def test_many_inserts_and_extracts(self):
        """Test with many tasks to verify correctness at scale."""
        import random
        priorities = random.sample(range(1, 101), 50)

        for i, p in enumerate(priorities):
            self.pq.insert(Task(task_id=i, priority=p))

        extracted = []
        while not self.pq.is_empty():
            extracted.append(self.pq.extract_min().priority)

        # Extracted priorities should be in non-decreasing order
        self.assertEqual(extracted, sorted(extracted))

    def test_size_after_operations(self):
        """Test that size is correctly maintained through operations."""
        self.pq.insert(Task(task_id=1, priority=3))
        self.pq.insert(Task(task_id=2, priority=1))
        self.assertEqual(self.pq.size(), 2)

        self.pq.extract_min()
        self.assertEqual(self.pq.size(), 1)

        self.pq.extract_min()
        self.assertEqual(self.pq.size(), 0)
        self.assertTrue(self.pq.is_empty())


if __name__ == '__main__':
    unittest.main()
