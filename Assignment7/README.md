# Assignment 7: Exploring Hash Tables and Their Practical Applications

This assignment implements two hash table collision-resolution strategies — Separate Chaining and Open Addressing (linear probing) — along with two hash functions, and empirically compares their performance across different key distributions and table sizes.

## Setup

Remember to use Python 3.8+ and create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

We use `matplotlib`, `numpy`, and `pandas` for visualization. Install them with:

```bash
pip install -r requirements.txt
```

## Running the Code

### Hash Table (quick demonstration)

```bash
python3 hash_table.py
```

### Empirical Analysis (Separate Chaining vs Open Addressing)

```bash
python3 analysis.py
```

This will generate:
- `hashtable_comparison.png` - Performance comparison chart across four key distributions
- `hashtable_results.csv` - Raw timing data for all configurations

## Running Tests

```bash
python3 -m unittest test_hash_table -v
```

## Summary

This assignment implements two hash table variants:

- **Separate Chaining** stores colliding keys in a linked list (Python list) at each bucket. It degrades gracefully under high load factors and is O(1 + α) average for search, insert, and delete.
- **Open Addressing (Linear Probing)** stores all entries in the table array itself. Collisions are resolved by stepping forward until an empty slot is found. Performance degrades sharply as the load factor approaches 1.0 due to primary clustering.

Two hash functions are provided:
- **Division hash** `h(k) = k mod m` — fast but sensitive to key patterns that share a common factor with the table capacity.
- **Multiply hash** `h(k) = floor(m * frac(k * A))` — more uniform distribution, not sensitive to capacity choice.

For full analysis, please see [REPORT.md](REPORT.md)
