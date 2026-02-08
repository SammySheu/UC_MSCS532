import random
from typing import Any, Optional, List


class Node:
    """Node for chaining in hash table."""

    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.next: Optional[Node] = None


class HashTable:
    """
    Hash Table implementation using chaining for collision resolution.
    Uses a universal hash function family.
    """

    def __init__(self, initial_capacity: int = 16, load_factor_threshold: float = 0.75):
        """
        Initialize hash table with chaining.

        Args:
            initial_capacity: Initial number of slots
            load_factor_threshold: Threshold for resizing (default: 0.75)
        """
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor_threshold = load_factor_threshold
        self.table: List[Optional[Node]] = [None] * self.capacity

        # Universal hash function parameters
        # Using h(k) = ((a * k + b) mod p) mod m
        # where p is a prime number larger than universe size
        self.prime = 2147483647  # Large prime (2^31 - 1)
        self.a = random.randint(1, self.prime - 1)
        self.b = random.randint(0, self.prime - 1)

    def _hash(self, key: Any) -> int:
        """
        Universal hash function.

        Args:
            key: Key to hash

        Returns:
            Hash value (index in table)
        """
        # Convert key to integer for hashing
        if isinstance(key, str):
            key_int = hash(key)
        elif isinstance(key, int):
            key_int = key
        else:
            key_int = hash(str(key))

        # Apply universal hash function: h(k) = ((a * k + b) mod p) mod m
        return ((self.a * key_int + self.b) % self.prime) % self.capacity

    def get_load_factor(self) -> float:
        """
        Calculate current load factor.

        Returns:
            Load factor (number of elements / number of slots)
        """
        return self.size / self.capacity

    def insert(self, key: Any, value: Any) -> None:
        """
        Insert a key-value pair into the hash table.
        If key exists, update its value.

        Args:
            key: Key to insert
            value: Value to associate with key
        """
        index = self._hash(key)

        # Check if key already exists in chain
        current = self.table[index]
        while current is not None:
            if current.key == key:
                # Update existing key
                current.value = value
                return
            current = current.next

        # Key doesn't exist, insert new node at head of chain
        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1

        # Check if resizing is needed
        if self.get_load_factor() > self.load_factor_threshold:
            self._resize()

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the hash table.

        Args:
            key: Key to search for

        Returns:
            Value associated with key, or None if not found
        """
        index = self._hash(key)

        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def delete(self, key: Any) -> bool:
        """
        Delete a key-value pair from the hash table.

        Args:
            key: Key to delete

        Returns:
            True if key was found and deleted, False otherwise
        """
        index = self._hash(key)

        current = self.table[index]
        prev = None

        while current is not None:
            if current.key == key:
                # Found the key, remove it
                if prev is None:
                    # Removing head of chain
                    self.table[index] = current.next
                else:
                    # Removing middle or end of chain
                    prev.next = current.next

                self.size -= 1
                return True

            prev = current
            current = current.next

        return False

    def _resize(self) -> None:
        """
        Resize the hash table to maintain low load factor.
        Doubles the capacity and rehashes all elements.
        """
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        # Rehash all elements
        for node in old_table:
            current = node
            while current is not None:
                self.insert(current.key, current.value)
                current = current.next

    def get_chain_lengths(self) -> List[int]:
        """
        Get lengths of all chains in the hash table.

        Returns:
            List of chain lengths
        """
        lengths = []
        for node in self.table:
            length = 0
            current = node
            while current is not None:
                length += 1
                current = current.next
            if length > 0:
                lengths.append(length)
        return lengths

    def get_statistics(self) -> dict:
        """
        Get statistics about the hash table.

        Returns:
            Dictionary with statistics
        """
        chain_lengths = self.get_chain_lengths()

        stats = {
            'capacity': self.capacity,
            'size': self.size,
            'load_factor': self.get_load_factor(),
            'num_chains': len(chain_lengths),
            'empty_slots': self.capacity - len(chain_lengths),
        }

        if chain_lengths:
            stats['avg_chain_length'] = sum(chain_lengths) / len(chain_lengths)
            stats['max_chain_length'] = max(chain_lengths)
            stats['min_chain_length'] = min(chain_lengths)
        else:
            stats['avg_chain_length'] = 0
            stats['max_chain_length'] = 0
            stats['min_chain_length'] = 0

        return stats

    def __str__(self) -> str:
        """String representation of hash table."""
        result = []
        for i, node in enumerate(self.table):
            if node is not None:
                chain = []
                current = node
                while current is not None:
                    chain.append(f"({current.key}: {current.value})")
                    current = current.next
                result.append(f"Slot {i}: {' -> '.join(chain)}")
        return '\n'.join(result) if result else "Empty hash table"


def main():

    ht = HashTable(initial_capacity=4)

    # Test insert
    ht.insert("apple", 5)
    ht.insert("banana", 7)
    ht.insert("cherry", 3)
    ht.insert("date", 9)

    # Test search
    print(f"apple: {ht.search('apple')}")  # Should return 5
    print(f"banana: {ht.search('banana')}")  # Should return 7
    print(f"cherry: {ht.search('cherry')}")  # Should return 3
    print(f"grape: {ht.search('grape')}")  # Should return None

    # Test update
    ht.insert("apple", 10)
    print(f"apple (updated): {ht.search('apple')}")

    # Test delete
    ht.delete("banana")
    # Should return None
    print(f"Search for banana after delete: {ht.search('banana')}")

    # Test statistics
    stats_old = ht.get_statistics()
    for key, value in stats_old.items():
        print(f"{key}: {value}")

    # Test resizing
    print("\nTesting automatic resizing...")
    for i in range(10):
        ht.insert(f"key_{i}", i)

    stats_new = ht.get_statistics()
    print(f"Capacity: {stats_old['capacity']} -> {stats_new['capacity']}")
    print(f"Size: {stats_old['size']} -> {stats_new['size']}")
    print(
        f"Load Factor: {stats_old['load_factor']:.2f} -> {stats_new['load_factor']:.2f}")


if __name__ == "__main__":
    main()
