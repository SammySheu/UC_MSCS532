"""
Empirical Analysis and Performance Comparison
Assignment 4 - Heapsort vs Quicksort vs Merge Sort
"""
import random
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List

from heapsort import heapsort, merge_sort, measure_time

# Add parent directory to path to import quicksort from Assignment3
sys.path.insert(0, '../Assignment3')
from quicksort import randomized_quicksort


class SortingAnalyzer:
    """Analyzer for comparing Heapsort, Quicksort, and Merge Sort."""

    def __init__(self):
        self.detailed_results = []

    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        """
        Generate test data of specified type.

        Args:
            size: Size of array
            data_type: Type of data ('random', 'sorted', 'reverse', 'nearly_sorted')

        Returns:
            List of integers
        """
        if data_type == 'random':
            return [random.randint(1, 100000) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(size))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'nearly_sorted':
            arr = list(range(size))
            # Swap ~5% of elements
            swaps = max(1, size // 20)
            for _ in range(swaps):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def run_comparison(self, sizes: List[int], data_types: List[str], trials: int = 5):
        """
        Run comprehensive comparison of sorting algorithms.

        Args:
            sizes: List of array sizes to test
            data_types: List of data types to test
            trials: Number of trials per configuration
        """
        algorithms = {
            'Heapsort': heapsort,
            'Quicksort (Randomized)': randomized_quicksort,
            'Merge Sort': merge_sort,
        }

        for data_type in data_types:
            print(f"\nAnalyzing {data_type} arrays...")

            for size in sizes:
                print(f"  Size {size}...", end='', flush=True)

                for algo_name, algo_func in algorithms.items():
                    total_time = 0
                    for _ in range(trials):
                        data = self.generate_test_data(size, data_type)
                        total_time += measure_time(algo_func, data)

                    avg_time = total_time / trials

                    self.detailed_results.append({
                        'Algorithm': algo_name,
                        'Data Type': data_type,
                        'Size': size,
                        'Execution Time (s)': avg_time,
                    })

                print(" Done")

    def plot_results(self, sizes: List[int], data_types: List[str]):
        """
        Plot comparison results.

        Args:
            sizes: List of array sizes tested
            data_types: List of data types tested
        """
        colors = {
            'Heapsort': '#2196F3',
            'Quicksort (Randomized)': '#FF5722',
            'Merge Sort': '#4CAF50',
        }
        markers = {
            'Heapsort': 'o',
            'Quicksort (Randomized)': 's',
            'Merge Sort': '^',
        }

        df = pd.DataFrame(self.detailed_results)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Sorting Algorithm Comparison: Heapsort vs Quicksort vs Merge Sort',
                     fontsize=18, fontweight='bold', y=0.995)

        for idx, data_type in enumerate(data_types):
            ax = axes[idx // 2, idx % 2]
            subset = df[df['Data Type'] == data_type]

            for algo_name in colors:
                algo_data = subset[subset['Algorithm'] == algo_name]
                ax.plot(algo_data['Size'], algo_data['Execution Time (s)'],
                        f'{markers[algo_name]}-', label=algo_name,
                        linewidth=2.5, markersize=10, color=colors[algo_name],
                        markeredgewidth=2, markeredgecolor='white', alpha=0.9)

            ax.set_xlabel('Array Size', fontsize=13, fontweight='bold')
            ax.set_ylabel('Execution Time (seconds)', fontsize=13, fontweight='bold')
            ax.set_title(f'{data_type.replace("_", " ").title()} Arrays',
                         fontsize=14, fontweight='bold', pad=12)
            ax.legend(fontsize=11, loc='best', framealpha=0.95, shadow=True)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_facecolor('#f8f9fa')
            ax.tick_params(labelsize=10)

        plt.tight_layout()
        plt.savefig('sorting_comparison.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()

    def export_to_csv(self, filename: str = 'sorting_results.csv'):
        """Export results to CSV file."""
        df = pd.DataFrame(self.detailed_results)
        df = df.sort_values(['Data Type', 'Size', 'Algorithm'])
        df.to_csv(filename, index=False)
        print(f"\nResults saved to '{filename}'")


def main():
    # Increase recursion limit for quicksort on sorted arrays
    sys.setrecursionlimit(50000)

    print("SORTING ALGORITHM COMPARISON")
    print("Heapsort vs Quicksort (Randomized) vs Merge Sort")
    print("=" * 55)

    analyzer = SortingAnalyzer()

    sizes = [100, 500, 1000, 2000, 5000, 10000]
    data_types = ['random', 'sorted', 'reverse', 'nearly_sorted']

    analyzer.run_comparison(sizes, data_types, trials=5)
    analyzer.plot_results(sizes, data_types)
    analyzer.export_to_csv('sorting_results.csv')


if __name__ == "__main__":
    main()
