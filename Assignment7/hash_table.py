"""
Hash Table Implementations — Separate Chaining and Open Addressing
Assignment 7 - Exploring Hash Tables and Their Practical Applications
"""
import time
from typing import Any, Callable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Hash functions
# ---------------------------------------------------------------------------

def division_hash(key: int, capacity: int) -> int:
    """
    Division-method hash function: h(k) = k mod m.

    Fast and simple, but sensitive to the relationship between the key
    distribution and the capacity. When many keys share a common factor
    with the capacity, they all land in the same bucket (clustering).

    Args:
        key: Integer key to hash
        capacity: Number of buckets in the table

    Returns:
        Bucket index in [0, capacity)
    """
    return key % capacity


def multiply_hash(key: int, capacity: int) -> int:
    """
    Multiplication-method hash function using Knuth's constant.

    Multiplies the key by A = (sqrt(5) - 1) / 2, takes the fractional
    part, and scales to [0, capacity). Spreads keys more uniformly than
    the division method and is not sensitive to the choice of capacity.

    Args:
        key: Integer key to hash
        capacity: Number of buckets in the table

    Returns:
        Bucket index in [0, capacity)
    """
    A = 0.6180339887  # (sqrt(5) - 1) / 2 — Knuth's constant
    return int(capacity * ((key * A) % 1))


# ---------------------------------------------------------------------------
# Separate Chaining
# ---------------------------------------------------------------------------

class HashTableChaining:
    """
    Hash table using separate chaining for collision resolution.

    Each bucket holds a list of (key, value) pairs. Collisions are handled
    by appending to the bucket's list, so the table never becomes "full"
    and degrades gracefully under high load factors. Average-case search,
    insert, and delete are all O(1 + alpha) where alpha is the load factor.
    """

    def __init__(self, capacity: int = 16,
                 hash_func: Callable[[int, int], int] = None):
        """
        Initialise the hash table.

        Args:
            capacity: Number of buckets (slots) in the table
            hash_func: Hash function to use; defaults to division_hash
        """
        self.capacity = capacity
        self.hash_func = hash_func if hash_func is not None else division_hash
        self._buckets: List[List[Tuple[int, Any]]] = [[] for _ in range(capacity)]
        self._size = 0

    @property
    def load_factor(self) -> float:
        """Ratio of stored entries to total bucket count."""
        return self._size / self.capacity

    def _hash(self, key: int) -> int:
        return self.hash_func(key, self.capacity)

    def insert(self, key: int, value: Any) -> None:
        """
        Insert a key-value pair, or update the value if the key already exists.

        Args:
            key: Integer key
            value: Associated value
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def search(self, key: int) -> Optional[Any]:
        """
        Search for a key and return its value, or None if not found.

        Args:
            key: Integer key to look up

        Returns:
            Associated value, or None if the key is absent
        """
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """
        Delete a key-value pair from the table.

        Args:
            key: Integer key to remove

        Returns:
            True if the key was found and removed, False otherwise
        """
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return True
        return False

    def avg_chain_length(self) -> float:
        """
        Average length of non-empty chains.

        Returns:
            Mean chain length across occupied buckets, or 0.0 if the table is empty
        """
        occupied = [b for b in self._buckets if b]
        return sum(len(b) for b in occupied) / len(occupied) if occupied else 0.0

    def max_chain_length(self) -> int:
        """Return the length of the longest chain in the table."""
        return max((len(b) for b in self._buckets), default=0)


# ---------------------------------------------------------------------------
# Open Addressing (Linear Probing)
# ---------------------------------------------------------------------------

class HashTableOpenAddressing:
    """
    Hash table using open addressing with linear probing.

    All key-value pairs are stored directly in the table array. Collisions
    are resolved by stepping forward one slot at a time (h(k), h(k)+1,
    h(k)+2, ...) until an empty slot is found. Performance degrades
    sharply as the load factor approaches 1.0 due to primary clustering.
    """

    _DELETED = object()  # Tombstone sentinel for lazy deletion

    def __init__(self, capacity: int = 16,
                 hash_func: Callable[[int, int], int] = None):
        """
        Initialise the hash table.

        Args:
            capacity: Number of slots in the table
            hash_func: Hash function to use; defaults to division_hash
        """
        self.capacity = capacity
        self.hash_func = hash_func if hash_func is not None else division_hash
        self._keys: List[Optional[Any]] = [None] * capacity
        self._values: List[Optional[Any]] = [None] * capacity
        self._size = 0

    @property
    def load_factor(self) -> float:
        """Ratio of stored entries to total slot count."""
        return self._size / self.capacity

    def _hash(self, key: int) -> int:
        return self.hash_func(key, self.capacity)

    def insert(self, key: int, value: Any) -> None:
        """
        Insert a key-value pair using linear probing to resolve collisions.

        Args:
            key: Integer key
            value: Associated value

        Raises:
            RuntimeError: If every slot is occupied and no room remains
        """
        if self._size >= self.capacity:
            raise RuntimeError("Hash table is full")

        idx = self._hash(key)
        for _ in range(self.capacity):
            slot = self._keys[idx]
            if slot is None or slot is self._DELETED:
                self._keys[idx] = key
                self._values[idx] = value
                self._size += 1
                return
            if slot == key:
                self._values[idx] = value  # Update existing key
                return
            idx = (idx + 1) % self.capacity

        raise RuntimeError("Hash table is full")

    def search(self, key: int) -> Optional[Any]:
        """
        Search for a key using linear probing.

        Args:
            key: Integer key to look up

        Returns:
            Associated value, or None if the key is absent
        """
        idx = self._hash(key)
        for _ in range(self.capacity):
            slot = self._keys[idx]
            if slot is None:
                return None
            if slot == key:
                return self._values[idx]
            idx = (idx + 1) % self.capacity
        return None

    def delete(self, key: int) -> bool:
        """
        Delete a key-value pair using a tombstone marker.

        The slot is replaced with a sentinel rather than cleared so that
        subsequent linear probes for other keys are not prematurely
        terminated.

        Args:
            key: Integer key to remove

        Returns:
            True if the key was found and removed, False otherwise
        """
        idx = self._hash(key)
        for _ in range(self.capacity):
            slot = self._keys[idx]
            if slot is None:
                return False
            if slot == key:
                self._keys[idx] = self._DELETED
                self._values[idx] = None
                self._size -= 1
                return True
            idx = (idx + 1) % self.capacity
        return False

    def avg_probe_length(self, keys: List[int]) -> float:
        """
        Compute the average number of probes required to find each key.

        Args:
            keys: List of keys that are present in the table

        Returns:
            Mean probe count across all supplied keys, or 0.0 if empty
        """
        total, found = 0, 0
        for key in keys:
            idx = self._hash(key)
            for probes in range(1, self.capacity + 1):
                if self._keys[idx] == key:
                    total += probes
                    found += 1
                    break
                idx = (idx + 1) % self.capacity
        return total / found if found else 0.0


# ---------------------------------------------------------------------------
# Timing utility
# ---------------------------------------------------------------------------

def measure_time(operation: Callable, *args: Any) -> float:
    """
    Measure the wall-clock execution time of an operation.

    Args:
        operation: Callable to time
        *args: Positional arguments forwarded to the callable

    Returns:
        Execution time in seconds
    """
    start = time.perf_counter()
    operation(*args)
    return time.perf_counter() - start


# ---------------------------------------------------------------------------
# Quick demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    keys = [10, 22, 37, 47, 49, 89]

    print("=== Separate Chaining ===")
    ht_chain = HashTableChaining(capacity=10)
    for k in keys:
        ht_chain.insert(k, f"val_{k}")
    print(f"Keys inserted:     {keys}")
    print(f"Load factor:       {ht_chain.load_factor:.2f}")
    print(f"Max chain length:  {ht_chain.max_chain_length()}")
    print(f"Avg chain length:  {ht_chain.avg_chain_length():.2f}")
    print(f"Search 37:         {ht_chain.search(37)}")
    print(f"Search 99:         {ht_chain.search(99)}")

    print("\n=== Open Addressing (Linear Probing) ===")
    ht_open = HashTableOpenAddressing(capacity=10)
    for k in keys:
        ht_open.insert(k, f"val_{k}")
    print(f"Keys inserted:     {keys}")
    print(f"Load factor:       {ht_open.load_factor:.2f}")
    print(f"Avg probe length:  {ht_open.avg_probe_length(keys):.2f}")
    print(f"Search 37:         {ht_open.search(37)}")
    print(f"Search 99:         {ht_open.search(99)}")

    print("\n=== Hash Function Comparison ===")
    test_keys = [0, 16, 32, 48, 64, 80]
    cap = 16
    print(f"Capacity: {cap}, Keys: {test_keys}")
    print("Division hash:  ", [division_hash(k, cap) for k in test_keys])
    print("Multiply hash:  ", [multiply_hash(k, cap) for k in test_keys])
