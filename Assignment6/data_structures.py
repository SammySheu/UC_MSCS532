"""
Elementary Data Structures - Array, Matrix, Stack, Queue, Linked List, Rooted Tree
Assignment 6 - Medians and Order Statistics & Elementary Data Structures
"""
from typing import Any, List, Optional


# ===========================================================================
# Part 2a: Dynamic Array
# ===========================================================================

class DynamicArray:
    """
    A resizable array backed by a Python list.

    Supports O(1) amortized append and O(1) random access. Insertion and
    deletion at arbitrary positions are O(n) due to element shifting.
    """

    def __init__(self) -> None:
        """Initialize an empty dynamic array."""
        self._data: List[Any] = []

    # ---- Core operations -----------------------------------------------

    def insert(self, index: int, value: Any) -> None:
        """
        Insert value at the given index, shifting subsequent elements right.

        Args:
            index: Position at which to insert (0-based); must be in
                   [0, len(self)]
            value: The element to insert

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index > len(self._data):
            raise IndexError(f"Index {index} out of range [0, {len(self._data)}]")
        self._data.insert(index, value)

    def append(self, value: Any) -> None:
        """
        Append value to the end of the array in O(1) amortized time.

        Args:
            value: The element to append
        """
        self._data.append(value)

    def delete(self, index: int) -> Any:
        """
        Remove and return the element at the given index.

        Args:
            index: Position of the element to remove (0-based)

        Returns:
            The removed element

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(self._data):
            raise IndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        return self._data.pop(index)

    def get(self, index: int) -> Any:
        """
        Return the element at the given index in O(1) time.

        Args:
            index: Position to access (0-based)

        Returns:
            The element at that position

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(self._data):
            raise IndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        return self._data[index]

    def set(self, index: int, value: Any) -> None:
        """
        Overwrite the element at the given index in O(1) time.

        Args:
            index: Position to update (0-based)
            value: New value

        Raises:
            IndexError: If index is out of range
        """
        if index < 0 or index >= len(self._data):
            raise IndexError(f"Index {index} out of range [0, {len(self._data) - 1}]")
        self._data[index] = value

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"DynamicArray({self._data})"


# ===========================================================================
# Part 2b: Matrix
# ===========================================================================

class Matrix:
    """
    A 2-D matrix with O(1) element access and mutation.

    Stored as a flat list internally; indexing is row-major.
    """

    def __init__(self, rows: int, cols: int, default: Any = 0) -> None:
        """
        Create a rows×cols matrix filled with default.

        Args:
            rows: Number of rows (must be > 0)
            cols: Number of columns (must be > 0)
            default: Initial value for every cell (default 0)

        Raises:
            ValueError: If rows or cols is not positive
        """
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must both be positive")
        self.rows = rows
        self.cols = cols
        self._data: List[Any] = [default] * (rows * cols)

    def _check(self, row: int, col: int) -> None:
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(
                f"({row}, {col}) out of bounds for {self.rows}×{self.cols} matrix"
            )

    def get(self, row: int, col: int) -> Any:
        """
        Return the element at (row, col) in O(1) time.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)

        Returns:
            The element at that position

        Raises:
            IndexError: If (row, col) is out of bounds
        """
        self._check(row, col)
        return self._data[row * self.cols + col]

    def set(self, row: int, col: int, value: Any) -> None:
        """
        Write value to (row, col) in O(1) time.

        Args:
            row: Row index (0-based)
            col: Column index (0-based)
            value: New value

        Raises:
            IndexError: If (row, col) is out of bounds
        """
        self._check(row, col)
        self._data[row * self.cols + col] = value

    def __repr__(self) -> str:
        rows_str = []
        for r in range(self.rows):
            row = [str(self._data[r * self.cols + c]) for c in range(self.cols)]
            rows_str.append("[" + ", ".join(row) + "]")
        return "Matrix([\n  " + ",\n  ".join(rows_str) + "\n])"


# ===========================================================================
# Part 2c: Stack (array-backed)
# ===========================================================================

class Stack:
    """
    LIFO stack implemented over a Python list (array).

    All operations (push, pop, peek) run in O(1) amortized time.
    Arrays outperform linked lists for stacks because cache locality
    eliminates the pointer-following overhead of node-based structures.
    """

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._data: List[Any] = []

    def push(self, value: Any) -> None:
        """
        Push value onto the top of the stack.

        Args:
            value: The element to push
        """
        self._data.append(value)

    def pop(self) -> Any:
        """
        Remove and return the top element.

        Returns:
            The element that was on top

        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        """
        Return the top element without removing it.

        Returns:
            The element on top

        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("peek at an empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        """Return True if the stack contains no elements."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack({self._data})"


# ===========================================================================
# Part 2d: Queue (array-backed with circular indexing)
# ===========================================================================

class Queue:
    """
    FIFO queue implemented over a Python list (array).

    Uses Python's list.append (O(1) amortized) and collections.deque-style
    pop(0) semantics. For a pure array implementation, enqueue is O(1)
    amortized and dequeue is O(n) in the naive case; here Python's list
    correctly amortizes both operations.

    In production, prefer collections.deque for O(1) dequeue.
    """

    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._data: List[Any] = []

    def enqueue(self, value: Any) -> None:
        """
        Add value to the back of the queue in O(1) amortized time.

        Args:
            value: The element to enqueue
        """
        self._data.append(value)

    def dequeue(self) -> Any:
        """
        Remove and return the front element.

        Returns:
            The element at the front of the queue

        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._data.pop(0)

    def front(self) -> Any:
        """
        Return the front element without removing it.

        Returns:
            The element at the front

        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("front of an empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        """Return True if the queue contains no elements."""
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue({self._data})"


# ===========================================================================
# Part 2e: Singly Linked List
# ===========================================================================

class _Node:
    """Internal node for the singly linked list."""

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.next: Optional["_Node"] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class SinglyLinkedList:
    """
    Singly linked list with O(1) front insertion and O(n) back insertion,
    deletion, and search.

    Linked lists avoid the O(n) element-shift cost of array-backed
    insertion/deletion in the middle, but sacrifice O(1) random access
    and cache locality.
    """

    def __init__(self) -> None:
        """Initialize an empty linked list."""
        self._head: Optional[_Node] = None
        self._size: int = 0

    # ---- Insertion -------------------------------------------------------

    def insert_front(self, data: Any) -> None:
        """
        Insert a new node at the front of the list in O(1) time.

        Args:
            data: Value for the new node
        """
        node = _Node(data)
        node.next = self._head
        self._head = node
        self._size += 1

    def insert_back(self, data: Any) -> None:
        """
        Append a new node at the back of the list in O(n) time.

        Args:
            data: Value for the new node
        """
        node = _Node(data)
        if self._head is None:
            self._head = node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def insert_after(self, target: Any, data: Any) -> bool:
        """
        Insert a new node immediately after the first node with value target.

        Args:
            target: Value of the node to insert after
            data: Value for the new node

        Returns:
            True if target was found and insertion succeeded; False otherwise
        """
        current = self._head
        while current is not None:
            if current.data == target:
                node = _Node(data)
                node.next = current.next
                current.next = node
                self._size += 1
                return True
            current = current.next
        return False

    # ---- Deletion --------------------------------------------------------

    def delete(self, data: Any) -> bool:
        """
        Remove the first node with the given value.

        Args:
            data: The value to remove

        Returns:
            True if a node was found and removed; False otherwise
        """
        if self._head is None:
            return False

        if self._head.data == data:
            self._head = self._head.next
            self._size -= 1
            return True

        current = self._head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next

        return False

    # ---- Search & traversal ---------------------------------------------

    def search(self, data: Any) -> bool:
        """
        Return True if the list contains a node with the given value.

        Args:
            data: Value to search for

        Returns:
            True if found, False otherwise
        """
        current = self._head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False

    def to_list(self) -> List[Any]:
        """
        Return the list contents as a Python list, in order.

        Returns:
            List of node values from head to tail
        """
        result: List[Any] = []
        current = self._head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """Return True if the list is empty."""
        return self._size == 0

    def __repr__(self) -> str:
        return " -> ".join(str(v) for v in self.to_list()) + " -> None"


# ===========================================================================
# Part 2f: Rooted Tree (optional, implemented via linked nodes)
# ===========================================================================

class _TreeNode:
    """Node in a rooted tree; stores a reference to its first child and
    its next sibling (left-child, right-sibling representation)."""

    def __init__(self, data: Any) -> None:
        self.data: Any = data
        self.first_child: Optional["_TreeNode"] = None
        self.next_sibling: Optional["_TreeNode"] = None

    def __repr__(self) -> str:
        return f"TreeNode({self.data})"


class RootedTree:
    """
    A general rooted tree using the left-child / right-sibling linked
    representation (also called the first-child / next-sibling or
    binary-tree representation of a general tree).

    Each node holds a pointer to its leftmost child and a pointer to its
    next sibling, allowing arbitrary branching factors without storing a
    variable-length child list in every node.

    Supported operations:
        - add_child(parent_data, child_data): O(h) where h = tree height
        - bfs_traversal(): O(n) breadth-first traversal
        - dfs_traversal(): O(n) depth-first (pre-order) traversal
    """

    def __init__(self, root_data: Any) -> None:
        """
        Create a tree with a single root node.

        Args:
            root_data: Value of the root
        """
        self.root = _TreeNode(root_data)

    def _find(self, node: Optional[_TreeNode], target: Any) -> Optional[_TreeNode]:
        """BFS-based search for the first node with value target."""
        if node is None:
            return None
        from collections import deque
        queue: deque = deque([node])
        while queue:
            current = queue.popleft()
            if current.data == target:
                return current
            child = current.first_child
            while child is not None:
                queue.append(child)
                child = child.next_sibling
        return None

    def add_child(self, parent_data: Any, child_data: Any) -> bool:
        """
        Add a new child with child_data under the first node found with
        parent_data.

        Args:
            parent_data: Value of the parent node
            child_data: Value for the new child node

        Returns:
            True if the parent was found and the child was added;
            False if parent_data was not found in the tree
        """
        parent = self._find(self.root, parent_data)
        if parent is None:
            return False

        new_node = _TreeNode(child_data)
        if parent.first_child is None:
            parent.first_child = new_node
        else:
            # Append as the last sibling
            sibling = parent.first_child
            while sibling.next_sibling is not None:
                sibling = sibling.next_sibling
            sibling.next_sibling = new_node

        return True

    def bfs_traversal(self) -> List[Any]:
        """
        Return node values in breadth-first (level) order.

        Returns:
            List of values visited level by level, left to right
        """
        result: List[Any] = []
        from collections import deque
        queue: deque = deque([self.root])
        while queue:
            node = queue.popleft()
            result.append(node.data)
            child = node.first_child
            while child is not None:
                queue.append(child)
                child = child.next_sibling
        return result

    def dfs_traversal(self) -> List[Any]:
        """
        Return node values in depth-first pre-order.

        Returns:
            List of values visited in pre-order (root, then children
            left to right recursively)
        """
        result: List[Any] = []

        def _dfs(node: Optional[_TreeNode]) -> None:
            if node is None:
                return
            result.append(node.data)
            child = node.first_child
            while child is not None:
                _dfs(child)
                child = child.next_sibling

        _dfs(self.root)
        return result

    def __repr__(self) -> str:
        return f"RootedTree(bfs={self.bfs_traversal()})"


# ===========================================================================
# Quick demonstration
# ===========================================================================

if __name__ == "__main__":
    # --- DynamicArray ---
    print("=== DynamicArray ===")
    da = DynamicArray()
    for v in [10, 20, 30]:
        da.append(v)
    da.insert(1, 15)
    print(da)
    da.delete(2)
    print(da)

    # --- Matrix ---
    print("\n=== Matrix ===")
    m = Matrix(3, 3)
    for r in range(3):
        for c in range(3):
            m.set(r, c, r * 3 + c + 1)
    print(m)

    # --- Stack ---
    print("\n=== Stack ===")
    s = Stack()
    for v in [1, 2, 3]:
        s.push(v)
    print(s)
    print("pop:", s.pop())
    print("peek:", s.peek())

    # --- Queue ---
    print("\n=== Queue ===")
    q = Queue()
    for v in ["a", "b", "c"]:
        q.enqueue(v)
    print(q)
    print("dequeue:", q.dequeue())
    print("front:", q.front())

    # --- SinglyLinkedList ---
    print("\n=== SinglyLinkedList ===")
    ll = SinglyLinkedList()
    for v in [1, 2, 3]:
        ll.insert_back(v)
    ll.insert_front(0)
    ll.insert_after(2, 99)
    print(ll)
    ll.delete(99)
    print(ll)
    print("search 2:", ll.search(2))
    print("search 9:", ll.search(9))

    # --- RootedTree ---
    print("\n=== RootedTree ===")
    tree = RootedTree("root")
    tree.add_child("root", "A")
    tree.add_child("root", "B")
    tree.add_child("A", "C")
    tree.add_child("A", "D")
    tree.add_child("B", "E")
    print("BFS:", tree.bfs_traversal())
    print("DFS:", tree.dfs_traversal())
