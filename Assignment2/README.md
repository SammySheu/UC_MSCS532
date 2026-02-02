# Assignment 2: Divide-and-Conquer Algorithms - Quick Sort and Merge Sort

This repository contains a comprehensive implementation and analysis of two fundamental divide-and-conquer sorting algorithms: **Quick Sort** and **Merge Sort**.

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
Could refer to [REPO_README.md](../README.md) if Python hasn't set up. 

### Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/SammySheu/UC_MSCS532/
   cd UC_MSCS532/Assignmen2
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running Individual Algorithm Tests

#### Test Quick Sort:
```bash
python quick_sort.py
```

#### Test Merge Sort:
```bash
python merge_sort.py
```

Both scripts will show `Execution time` and `Memory usage`. 


### Run Analysis

```bash
python performance_comparison.py
```
This script run Quick Sort and Merge Sort and compare them with different testset.
**Size**
- 100
- 500
- 1000
- 5000

**Type of Testset**
- sorted
- reverse_sorted
- random
- nearly_sorted
- many_duplicates


**Output Files:**
- `performance_results.csv` - results stored in tabular format
- `performance_comparison.png` - Visualization with 4 subplots:
  - Execution time vs array size
  - Memory usage vs array size
  - Execution time by data type
  - Performance summary statistics

### Running Unit Tests

```bash
python test_algorithms.py
```

## Complexity Summary

| Algorithm | Best Case | Average Case | Worst Case | Space Complexity |
|-----------|-----------|--------------|------------|------------------|
| **Quick Sort (Standard)** | Ω(n log n) | Θ(n log n) | O(n²) | O(log n) |
| **Quick Sort (Randomized)** | Ω(n log n) | Θ(n log n) | O(n log n) | O(log n) |
| **Merge Sort** | Ω(n log n) | Θ(n log n) | O(n log n) | O(n) |


### Results and Summary
[Comparison](./graph.png)

1. **Random Data**: All algorithms perform similarly, with O(n log n) behavior
2. **Sorted Data**: Standard Quick Sort may show degraded performance (O(n²)), while randomized Quick Sort and Merge Sort maintain O(n log n)
3. **Reverse Sorted Data**: Similar to sorted data
4. **Nearly Sorted Data**: Quick Sort variants perform well; Merge Sort remains consistent
5. **Many Duplicates**: Algorithms show varying efficiency based on pivot selection strategy

**Key Observations:**

1. **Merge Sort Consistency**: Maintains consistent O(n log n) performance across all dataset types
2. **Quick Sort Variance**: Standard Quick Sort shows worst-case behavior on sorted/reverse-sorted data
3. **Randomized Quick Sort**: Effectively avoids worst-case scenarios
4. **Memory Usage**: Merge Sort uses approximately 2-3x more memory than Quick Sort
5. **Small Arrays**: Performance differences are minimal; overhead dominates
6. **Large Arrays**: Theoretical predictions become more evident