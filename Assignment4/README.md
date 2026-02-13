# Assignment 4: Heap Data Structures - Implementation, Analysis, and Applications

This assignment implements the Heapsort algorithm and a priority queue using a binary heap, then empirically compares Heapsort with Quicksort and Merge Sort.

## Setup
Remember to use Python3.8+ and create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

We use `matplotlib`, `numpy` and `pandas` for visualizing the data. Those are listed in [requirements.txt](./requirements.txt) 

```bash
pip install -r requirements.txt
```

## Running the Code

### Heapsort

```bash
python3 heapsort.py
```

### Priority Queue

```bash
python3 priority_queue.py
```

### Empirical Analysis (Heapsort vs Quicksort vs Merge Sort)

This script requires `Assignment3/quicksort.py` to be present in the parent directory.

```bash
python3 analysis.py
```

This will generate:
- `sorting_comparison.png` - Performance comparison chart
- `sorting_results.csv` - Raw timing data

## Running Tests

```bash
python3 -m unittest test_heapsort test_priority_queue -v
```

## Summary

We now inplemented **Quicksort**, **Mergesort** and **Heapsort**. **Heapsort** is typically the fastest in practice on random data due to better cache locality and smaller constant factors. **Merge Sort** offers stable sorting but requires O(n) auxiliary space. As for **Heapsort**, it provides guaranteed O(n log n) performance across all input and with only O(1) auxiliary space. Please see [REPORT.md](REPORT.md) for further analysis.
