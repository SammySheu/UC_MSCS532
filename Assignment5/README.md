# Assignment 5: Quicksort Algorithm - Implementation, Analysis, and Randomization

This assignment implements both the deterministic and randomized Quicksort algorithms, analyzes their theoretical complexity, and empirically compares their performance across different input sizes and distributions.

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

### Quicksort (quick demonstration)

```bash
python3 quicksort.py
```

### Empirical Analysis (Deterministic vs Randomized Quicksort)

```bash
python3 analysis.py
```

This will generate:
- `quicksort_comparison.png` - Performance comparison chart across four input distributions
- `quicksort_results.csv` - Raw timing data for all configurations

## Running Tests

```bash
python3 -m unittest test_quicksort -v
```

## Summary

This assignment implements two variants of Quicksort:

- **Deterministic Quicksort** always picks the last element as the pivot (Lomuto partition scheme). It runs in O(n log n) on average but degrades to O(n²) on sorted or reverse-sorted input.
- **Randomized Quicksort** picks the pivot uniformly at random, which breaks any adversarial input pattern and achieves expected O(n log n) performance on all input distributions.

For full analysis, please see [REPORT.md](REPORT.md)
