"""
Unit tests for all elementary data structures:
DynamicArray, Matrix, Stack, Queue, SinglyLinkedList, RootedTree
"""
import unittest
from data_structures import (
    DynamicArray,
    Matrix,
    Stack,
    Queue,
    SinglyLinkedList,
    RootedTree,
)


# ===========================================================================
# DynamicArray tests
# ===========================================================================

class TestDynamicArray(unittest.TestCase):
    """Tests for the DynamicArray class."""

    def test_append_and_get(self):
        """Appended elements are accessible by index."""
        da = DynamicArray()
        da.append(10)
        da.append(20)
        da.append(30)
        self.assertEqual(da.get(0), 10)
        self.assertEqual(da.get(1), 20)
        self.assertEqual(da.get(2), 30)

    def test_insert_middle(self):
        """insert() shifts subsequent elements right."""
        da = DynamicArray()
        for v in [1, 2, 3]:
            da.append(v)
        da.insert(1, 99)
        self.assertEqual(da.get(1), 99)
        self.assertEqual(da.get(2), 2)
        self.assertEqual(len(da), 4)

    def test_insert_front(self):
        """Insert at index 0 prepends an element."""
        da = DynamicArray()
        da.append(5)
        da.insert(0, 0)
        self.assertEqual(da.get(0), 0)
        self.assertEqual(da.get(1), 5)

    def test_insert_back(self):
        """Insert at len(da) is equivalent to append."""
        da = DynamicArray()
        da.append(1)
        da.insert(1, 2)
        self.assertEqual(da.get(1), 2)

    def test_delete(self):
        """delete() removes and returns the correct element."""
        da = DynamicArray()
        for v in [10, 20, 30]:
            da.append(v)
        removed = da.delete(1)
        self.assertEqual(removed, 20)
        self.assertEqual(len(da), 2)
        self.assertEqual(da.get(1), 30)

    def test_set(self):
        """set() overwrites an element without changing size."""
        da = DynamicArray()
        da.append(1)
        da.set(0, 42)
        self.assertEqual(da.get(0), 42)
        self.assertEqual(len(da), 1)

    def test_empty_length(self):
        """Empty array has length 0."""
        self.assertEqual(len(DynamicArray()), 0)

    def test_out_of_range_get(self):
        """get() with an invalid index raises IndexError."""
        da = DynamicArray()
        da.append(1)
        with self.assertRaises(IndexError):
            da.get(5)

    def test_out_of_range_insert(self):
        """insert() at a negative index raises IndexError."""
        da = DynamicArray()
        with self.assertRaises(IndexError):
            da.insert(-1, 0)

    def test_out_of_range_delete(self):
        """delete() on an empty array raises IndexError."""
        da = DynamicArray()
        with self.assertRaises(IndexError):
            da.delete(0)


# ===========================================================================
# Matrix tests
# ===========================================================================

class TestMatrix(unittest.TestCase):
    """Tests for the Matrix class."""

    def test_default_fill(self):
        """All cells are initialised to the default value."""
        m = Matrix(3, 4)
        for r in range(3):
            for c in range(4):
                self.assertEqual(m.get(r, c), 0)

    def test_set_and_get(self):
        """set() and get() round-trip correctly."""
        m = Matrix(2, 2)
        m.set(0, 0, 1)
        m.set(0, 1, 2)
        m.set(1, 0, 3)
        m.set(1, 1, 4)
        self.assertEqual(m.get(0, 0), 1)
        self.assertEqual(m.get(1, 1), 4)

    def test_identity_matrix(self):
        """Construct a 3×3 identity matrix and verify the diagonal."""
        m = Matrix(3, 3)
        for i in range(3):
            m.set(i, i, 1)
        for r in range(3):
            for c in range(3):
                expected = 1 if r == c else 0
                self.assertEqual(m.get(r, c), expected)

    def test_out_of_bounds(self):
        """get() outside bounds raises IndexError."""
        m = Matrix(2, 2)
        with self.assertRaises(IndexError):
            m.get(2, 0)
        with self.assertRaises(IndexError):
            m.get(0, 2)

    def test_invalid_dimensions(self):
        """Matrix with non-positive dimensions raises ValueError."""
        with self.assertRaises(ValueError):
            Matrix(0, 3)
        with self.assertRaises(ValueError):
            Matrix(3, -1)

    def test_non_integer_values(self):
        """Matrix cells can store arbitrary Python objects."""
        m = Matrix(2, 2, default=None)
        m.set(0, 0, "hello")
        self.assertEqual(m.get(0, 0), "hello")
        self.assertIsNone(m.get(0, 1))


# ===========================================================================
# Stack tests
# ===========================================================================

class TestStack(unittest.TestCase):
    """Tests for the array-backed Stack class."""

    def test_push_and_peek(self):
        """Peek returns the most recently pushed element."""
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.peek(), 2)

    def test_pop_order(self):
        """Elements are popped in LIFO order."""
        s = Stack()
        for v in [1, 2, 3]:
            s.push(v)
        self.assertEqual(s.pop(), 3)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(s.pop(), 1)

    def test_is_empty(self):
        """is_empty() reflects the actual state."""
        s = Stack()
        self.assertTrue(s.is_empty())
        s.push(0)
        self.assertFalse(s.is_empty())
        s.pop()
        self.assertTrue(s.is_empty())

    def test_length(self):
        """len(stack) tracks the number of elements."""
        s = Stack()
        for i in range(5):
            s.push(i)
        self.assertEqual(len(s), 5)
        s.pop()
        self.assertEqual(len(s), 4)

    def test_pop_empty_raises(self):
        """pop() on an empty stack raises IndexError."""
        with self.assertRaises(IndexError):
            Stack().pop()

    def test_peek_empty_raises(self):
        """peek() on an empty stack raises IndexError."""
        with self.assertRaises(IndexError):
            Stack().peek()

    def test_mixed_types(self):
        """Stack can hold elements of different types."""
        s = Stack()
        s.push(1)
        s.push("two")
        s.push([3])
        self.assertEqual(s.pop(), [3])
        self.assertEqual(s.pop(), "two")


# ===========================================================================
# Queue tests
# ===========================================================================

class TestQueue(unittest.TestCase):
    """Tests for the array-backed Queue class."""

    def test_enqueue_and_front(self):
        """front() returns the oldest element without removing it."""
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        self.assertEqual(q.front(), "a")

    def test_dequeue_order(self):
        """Elements are dequeued in FIFO order."""
        q = Queue()
        for v in [1, 2, 3]:
            q.enqueue(v)
        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)

    def test_is_empty(self):
        """is_empty() reflects the actual state."""
        q = Queue()
        self.assertTrue(q.is_empty())
        q.enqueue(0)
        self.assertFalse(q.is_empty())
        q.dequeue()
        self.assertTrue(q.is_empty())

    def test_length(self):
        """len(queue) tracks the number of elements."""
        q = Queue()
        for i in range(4):
            q.enqueue(i)
        self.assertEqual(len(q), 4)
        q.dequeue()
        self.assertEqual(len(q), 3)

    def test_dequeue_empty_raises(self):
        """dequeue() on an empty queue raises IndexError."""
        with self.assertRaises(IndexError):
            Queue().dequeue()

    def test_front_empty_raises(self):
        """front() on an empty queue raises IndexError."""
        with self.assertRaises(IndexError):
            Queue().front()

    def test_interleaved_operations(self):
        """Interleaving enqueue and dequeue maintains FIFO order."""
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEqual(q.dequeue(), 1)
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(q.dequeue(), 3)


# ===========================================================================
# SinglyLinkedList tests
# ===========================================================================

class TestSinglyLinkedList(unittest.TestCase):
    """Tests for the SinglyLinkedList class."""

    def test_insert_back_order(self):
        """insert_back maintains insertion order."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_back(v)
        self.assertEqual(ll.to_list(), [1, 2, 3])

    def test_insert_front_order(self):
        """insert_front prepends elements."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_front(v)
        self.assertEqual(ll.to_list(), [3, 2, 1])

    def test_insert_after(self):
        """insert_after places a node after the target."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_back(v)
        ll.insert_after(2, 99)
        self.assertEqual(ll.to_list(), [1, 2, 99, 3])

    def test_insert_after_not_found(self):
        """insert_after returns False when target is not present."""
        ll = SinglyLinkedList()
        ll.insert_back(1)
        self.assertFalse(ll.insert_after(99, 0))

    def test_delete_front(self):
        """Deleting the head element works correctly."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_back(v)
        self.assertTrue(ll.delete(1))
        self.assertEqual(ll.to_list(), [2, 3])

    def test_delete_middle(self):
        """Deleting a middle element links neighbours correctly."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_back(v)
        self.assertTrue(ll.delete(2))
        self.assertEqual(ll.to_list(), [1, 3])

    def test_delete_back(self):
        """Deleting the tail element works correctly."""
        ll = SinglyLinkedList()
        for v in [1, 2, 3]:
            ll.insert_back(v)
        self.assertTrue(ll.delete(3))
        self.assertEqual(ll.to_list(), [1, 2])

    def test_delete_not_found(self):
        """delete() returns False when the value is absent."""
        ll = SinglyLinkedList()
        ll.insert_back(1)
        self.assertFalse(ll.delete(99))

    def test_delete_empty(self):
        """delete() on an empty list returns False."""
        self.assertFalse(SinglyLinkedList().delete(1))

    def test_search_found(self):
        """search() returns True for an existing element."""
        ll = SinglyLinkedList()
        for v in [10, 20, 30]:
            ll.insert_back(v)
        self.assertTrue(ll.search(20))

    def test_search_not_found(self):
        """search() returns False for a missing element."""
        ll = SinglyLinkedList()
        ll.insert_back(1)
        self.assertFalse(ll.search(99))

    def test_length(self):
        """len(ll) tracks insertions and deletions."""
        ll = SinglyLinkedList()
        self.assertEqual(len(ll), 0)
        for v in [1, 2, 3]:
            ll.insert_back(v)
        self.assertEqual(len(ll), 3)
        ll.delete(2)
        self.assertEqual(len(ll), 2)

    def test_is_empty(self):
        """is_empty() reflects actual state."""
        ll = SinglyLinkedList()
        self.assertTrue(ll.is_empty())
        ll.insert_back(1)
        self.assertFalse(ll.is_empty())

    def test_to_list_empty(self):
        """to_list() on an empty list returns []."""
        self.assertEqual(SinglyLinkedList().to_list(), [])

    def test_single_element(self):
        """Single-element list behaves correctly for all operations."""
        ll = SinglyLinkedList()
        ll.insert_back(42)
        self.assertTrue(ll.search(42))
        self.assertTrue(ll.delete(42))
        self.assertTrue(ll.is_empty())


# ===========================================================================
# RootedTree tests
# ===========================================================================

class TestRootedTree(unittest.TestCase):
    """Tests for the RootedTree class."""

    def _build_sample_tree(self) -> RootedTree:
        """
        Build:
                root
               /    \\
              A      B
             / \\      \\
            C   D      E
        """
        tree = RootedTree("root")
        tree.add_child("root", "A")
        tree.add_child("root", "B")
        tree.add_child("A", "C")
        tree.add_child("A", "D")
        tree.add_child("B", "E")
        return tree

    def test_bfs_order(self):
        """BFS visits nodes level by level."""
        tree = self._build_sample_tree()
        self.assertEqual(tree.bfs_traversal(), ["root", "A", "B", "C", "D", "E"])

    def test_dfs_order(self):
        """DFS visits in pre-order (root, then children left-to-right)."""
        tree = self._build_sample_tree()
        self.assertEqual(tree.dfs_traversal(), ["root", "A", "C", "D", "B", "E"])

    def test_single_node(self):
        """A tree with only the root has singleton traversals."""
        tree = RootedTree(1)
        self.assertEqual(tree.bfs_traversal(), [1])
        self.assertEqual(tree.dfs_traversal(), [1])

    def test_add_child_returns_false_on_missing_parent(self):
        """add_child() returns False when the parent is not found."""
        tree = RootedTree("root")
        self.assertFalse(tree.add_child("nonexistent", "child"))

    def test_add_child_returns_true_on_success(self):
        """add_child() returns True when the parent exists."""
        tree = RootedTree("root")
        self.assertTrue(tree.add_child("root", "child"))

    def test_deep_tree(self):
        """Linear (chain) tree — each node has exactly one child."""
        tree = RootedTree(0)
        for i in range(1, 6):
            tree.add_child(i - 1, i)
        self.assertEqual(tree.bfs_traversal(), list(range(6)))
        self.assertEqual(tree.dfs_traversal(), list(range(6)))

    def test_wide_tree(self):
        """Star tree — root has many children, none have children."""
        tree = RootedTree("root")
        children = ["A", "B", "C", "D", "E"]
        for c in children:
            tree.add_child("root", c)
        bfs = tree.bfs_traversal()
        self.assertEqual(bfs[0], "root")
        self.assertEqual(sorted(bfs[1:]), sorted(children))


if __name__ == '__main__':
    unittest.main()
