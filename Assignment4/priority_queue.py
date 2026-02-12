from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    """
    Represents a task in the priority queue.

    Attributes:
        task_id: Unique identifier for the task
        priority: Priority level (lower value = higher priority)
        arrival_time: When the task arrived
        deadline: When the task must be completed
        description: Human-readable description
    """
    task_id: int
    priority: int
    arrival_time: float = 0.0
    deadline: float = float('inf')
    description: str = ""

    def __lt__(self, other: 'Task') -> bool:
        return self.priority < other.priority

    def __le__(self, other: 'Task') -> bool:
        return self.priority <= other.priority

    def __gt__(self, other: 'Task') -> bool:
        return self.priority > other.priority

    def __ge__(self, other: 'Task') -> bool:
        return self.priority >= other.priority

    def __repr__(self) -> str:
        return f"Task(id={self.task_id}, priority={self.priority}, desc='{self.description}')"


class MinHeapPriorityQueue:
    """
    Lower priority value means higher urgency.

    We use a list to represent the binary heap.
        - Parent of node at index i: (i - 1) // 2
        - Left child of node at index i: 2 * i + 1
        - Right child of node at index i: 2 * i + 2
    """

    def __init__(self):
        self._heap: list[Task] = []
        # This allows us to quickly find the index of a task in the heap.
        self._index_map: dict[int, int] = {}  # task_id -> heap index

    def _parent(self, i: int) -> int:
        return (i - 1) // 2

    def _left(self, i: int) -> int:
        return 2 * i + 1

    def _right(self, i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        """Swap two elements and update the index map."""
        self._index_map[self._heap[i].task_id] = j
        self._index_map[self._heap[j].task_id] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _sift_up(self, i: int) -> None:
        """
        Move an element up the heap to restore the min-heap property.
        """
        while i > 0 and self._heap[i] < self._heap[self._parent(i)]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _sift_down(self, i: int) -> None:
        """
        Move an element down the heap to restore the min-heap property.
        """
        n = len(self._heap)
        smallest = i

        left = self._left(i)
        if left < n and self._heap[left] < self._heap[smallest]:
            smallest = left

        right = self._right(i)
        if right < n and self._heap[right] < self._heap[smallest]:
            smallest = right

        if smallest != i:
            self._swap(i, smallest)
            self._sift_down(smallest)

    def insert(self, task: Task) -> None:
        """
        Insert a new task into the priority queue.

        Args:
            task: The Task object to insert
        """
        # Append the task to the end of the heap
        self._heap.append(task)
        idx = len(self._heap) - 1
        # Update the index map
        self._index_map[task.task_id] = idx
        # Maintain the min-heap property by sifting the task up to its correct position
        self._sift_up(idx)

    def extract_min(self) -> Task:
        """
        Remove and return the task with the highest priority (lowest value).

        Returns:
            The Task with the lowest priority value

        Raises:
            IndexError: If the priority queue is empty
        """
        if self.is_empty():
            raise IndexError("extract_min from an empty priority queue")

        # Swap the root with the last element
        self._swap(0, len(self._heap) - 1)

        # Remove the minimum (now at the end)
        min_task = self._heap.pop()
        # Remove the task from the index map
        del self._index_map[min_task.task_id]

        # Restore the min-heap property by sifting the new root down to its correct position
        if not self.is_empty():
            self._sift_down(0)

        return min_task

    def decrease_key(self, task_id: int, new_priority: int) -> None:
        """
        Decrease the priority value of an existing task (make it more urgent).

        Args:
            task_id: The ID of the task to modify
            new_priority: The new (lower) priority value

        Raises:
            KeyError: If task_id is not found
            ValueError: If new_priority is not less than current priority
        """
        if task_id not in self._index_map:
            raise KeyError(f"Task {task_id} not found in priority queue")

        # Get the index of the task in the heap
        idx = self._index_map[task_id]

        # Check if the new priority is less than the current priority
        if new_priority >= self._heap[idx].priority:
            raise ValueError(
                f"New priority ({new_priority}) must be less than "
                f"current priority ({self._heap[idx].priority})"
            )

        # Update the priority of the task
        self._heap[idx].priority = new_priority
        # Maintain the min-heap property by sifting the task up to its correct position
        self._sift_up(idx)

    def increase_key(self, task_id: int, new_priority: int) -> None:
        """
        Increase the priority value of an existing task (make it less urgent).

        Args:
            task_id: The ID of the task to modify
            new_priority: The new (higher) priority value

        Raises:
            KeyError: If task_id is not found
            ValueError: If new_priority is not greater than current priority
        """
        if task_id not in self._index_map:
            raise KeyError(f"Task {task_id} not found in priority queue")

        # Get the index of the task in the heap
        idx = self._index_map[task_id]

        # Check if the new priority is greater than the current priority
        if new_priority <= self._heap[idx].priority:
            raise ValueError(
                f"New priority ({new_priority}) must be greater than "
                f"current priority ({self._heap[idx].priority})"
            )

        # Update the priority of the task
        self._heap[idx].priority = new_priority
        # Maintain the min-heap property by sifting the task down to its correct position
        self._sift_down(idx)

    def peek(self) -> Task:
        """
        Return the task with the highest priority without removing it.

        Returns:
            The Task with the lowest priority value

        Raises:
            IndexError: If the priority queue is empty
        """
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        # Return the root of the heap
        return self._heap[0]

    def is_empty(self) -> bool:
        """
        Check if the priority queue is empty.
        Returns:
            True if the queue is empty, False otherwise
        """
        return len(self._heap) == 0

    def size(self) -> int:
        """Return the number of tasks in the priority queue."""
        return len(self._heap)

    def __len__(self) -> int:
        return self.size()

    def __repr__(self) -> str:
        return f"MinHeapPriorityQueue(size={self.size()}, heap={self._heap})"


def scheduler_simulation():
    """
    Simulate a simple task scheduler using the priority queue.

    Demonstrates how a priority queue can be used in an OS-like
    task scheduling scenario where tasks arrive with different
    priorities and are processed in priority order.
    """
    pq = MinHeapPriorityQueue()

    # Simulate tasks arriving
    tasks = [
        Task(task_id=1, priority=5, arrival_time=0.0, deadline=10.0,
             description="Low priority background job"),
        Task(task_id=2, priority=1, arrival_time=0.5, deadline=3.0,
             description="Critical system alert"),
        Task(task_id=3, priority=3, arrival_time=1.0, deadline=7.0,
             description="User request processing"),
        Task(task_id=4, priority=4, arrival_time=1.5, deadline=8.0,
             description="Data backup"),
        Task(task_id=5, priority=2, arrival_time=2.0, deadline=5.0,
             description="Network packet handling"),
    ]

    print("=== Task Scheduler Simulation ===\n")

    # Insert all tasks
    print("Inserting tasks:")
    for task in tasks:
        pq.insert(task)
        print(f"  Inserted: {task}")

    print(f"\nQueue size: {pq.size()}")
    print(f"Next task to process: {pq.peek()}")

    # Simulate a priority change: task 4 becomes more urgent
    print("\n--- Priority Update ---")
    print("Task 4 (Data backup) priority changed from 4 to 1 (urgent!)")
    pq.decrease_key(task_id=4, new_priority=1)

    # Process all tasks in priority order
    print("\n--- Processing Tasks in Priority Order ---")
    order = 1
    while not pq.is_empty():
        task = pq.extract_min()
        print(
            f"  {order}. [Priority {task.priority}] {task.description} (Task ID: {task.task_id})")
        order += 1


if __name__ == "__main__":
    scheduler_simulation()
