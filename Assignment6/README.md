# Assignment 6: Medians and Order Statistics & Elementary Data Structures

This assignment first showcase selection algorithms with empirical performance comparison. Then, implement elementary data structures from scratchis. For example, dynamic array, matrix, stack, queue, linked list and rooted tree.

## Setup

Requires Python 3.8+. Install dependencies with:

```bash
python3 -m venv venv
source venv/bin/activate
```
We use `matplotlib`, `numpy`, and `pandas` for visualization. Install them with:

```bash
pip install -r requirements.txt
```

## Running the Code

### Part 1 — Selection algorithms (quick demonstration)

```bash
python3 selection.py
```

### Part 1 — Empirical Analysis

In the analysis, I generate four dataset(random, sorted, reverse sorted, nearly sorted), and compare them in diagraph. Results stored in `selection_results.csv` and `selection_comparison.png`


### Part 2 — Data structures

```bash
python3 data_structures.py
```

## Running Tests

```bash
# Selection algorithms
python3 -m unittest test_selection -v

# Data structures
python3 -m unittest test_data_structures -v

# All tests at once
python3 -m unittest test_selection test_data_structures -v
```

## Summary

### Part 1

Two O(n) selection algorithms find the k-th smallest element in an unsorted array:

- **Median of Medians** (deterministic): guarantees O(n) worst-case by choosing a pivot that always lies between the 30th and 70th percentile. It divides the array into groups of 5, finds the median of each group, and recursively finds the median of those medians.
- **Randomized Quickselect** (randomized): uses a uniformly random pivot, achieving O(n) expected time on any input. Simpler to implement and faster in practice, but lacks the worst-case guarantee.

### Part 2

Five data structures are implemented from scratch using Python:

| Structure | Backing | Key Trade-off |
|---|---|---|
| Dynamic Array | Python list | O(1) access, O(n) insert/delete mid-array |
| Matrix | Flat list (row-major) | O(1) access and mutation |
| Stack | Array | O(1) amortized push/pop; better cache locality than linked list |
| Queue | Array | O(1) enqueue; O(n) dequeue (use deque for O(1) both) |
| Singly Linked List | Linked nodes | O(1) front insert; O(n) access; no shifting cost |
| Rooted Tree | Linked nodes (first-child/next-sibling) | Arbitrary branching factor without variable-size child arrays |

For full analysis see [REPORT.md](REPORT.md).
