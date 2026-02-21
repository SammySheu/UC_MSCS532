"""
Empirical Analysis and Performance Comparison
Assignment 5 - Deterministic Quicksort vs Randomized Quicksort
"""
import random
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List

from quicksort import deterministic_quicksort, randomized_quicksort, measure_time


class QuicksortAnalyzer:
    """Analyzer for comparing Deterministic and Randomized Quicksort."""

    def __init__(self):
        self.detailed_results = []

    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        """
        Generate test data of a specified distribution.

        Args:
            size: Number of elements in the array
            data_type: One of 'random', 'sorted', 'reverse', 'nearly_sorted'

        Returns:
            List of integers with the requested distribution
        """
        if data_type == 'random':
            return [random.randint(1, 100000) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(size))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'nearly_sorted':
            arr = list(range(size))
            # Swap ~5% of elements to introduce slight disorder
            swaps = max(1, size // 20)
            for _ in range(swaps):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def run_comparison(self, sizes: List[int], data_types: List[str], trials: int = 5):
        """
        Run a comprehensive comparison of deterministic and randomized Quicksort.

        Args:
            sizes: List of array sizes to benchmark
            data_types: List of data distributions to test
            trials: Number of independent trials to average per configuration
        """
        algorithms = {
            'Deterministic Quicksort': deterministic_quicksort,
            'Randomized Quicksort': randomized_quicksort,
        }

        for data_type in data_types:
            print(f"\nAnalyzing {data_type} arrays...")

            for size in sizes:
                print(f"  Size {size}...", end='', flush=True)

                for algo_name, algo_func in algorithms.items():
                    times = []
                    for _ in range(trials):
                        data = self.generate_test_data(size, data_type)
                        t = measure_time(algo_func, data)
                        times.append(t)

                    # Use nanmean so RecursionError-caused NaNs are excluded gracefully
                    avg_time = float(np.nanmean(times)) if times else float('nan')

                    self.detailed_results.append({
                        'Algorithm': algo_name,
                        'Data Type': data_type,
                        'Size': size,
                        'Execution Time (s)': avg_time,
                    })

                print(" Done")

    def plot_results(self, sizes: List[int], data_types: List[str]):
        """
        Plot the performance comparison as a 2x2 grid of subplots.

        Args:
            sizes: List of array sizes that were benchmarked
            data_types: List of data distributions that were benchmarked
        """
        colors = {
            'Deterministic Quicksort': '#E53935',
            'Randomized Quicksort':    '#1E88E5',
        }
        markers = {
            'Deterministic Quicksort': 's',
            'Randomized Quicksort':    'o',
        }

        df = pd.DataFrame(self.detailed_results)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Quicksort Comparison: Deterministic vs Randomized',
                     fontsize=18, fontweight='bold', y=0.995)

        for idx, data_type in enumerate(data_types):
            ax = axes[idx // 2, idx % 2]
            subset = df[df['Data Type'] == data_type]

            for algo_name in colors:
                algo_data = subset[subset['Algorithm'] == algo_name]
                # Drop NaN rows (RecursionError cases) before plotting
                valid = algo_data.dropna(subset=['Execution Time (s)'])
                ax.plot(valid['Size'], valid['Execution Time (s)'],
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
        plt.savefig('quicksort_comparison.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()
        print("Chart saved to 'quicksort_comparison.png'")

    def export_to_csv(self, filename: str = 'quicksort_results.csv'):
        """Export benchmark results to a CSV file."""
        df = pd.DataFrame(self.detailed_results)
        df = df.sort_values(['Data Type', 'Size', 'Algorithm'])
        df.to_csv(filename, index=False)
        print(f"Results saved to '{filename}'")

    def print_summary_table(self):
        """Print a formatted summary table of average execution times."""
        df = pd.DataFrame(self.detailed_results)
        print("\n" + "=" * 70)
        print("SUMMARY: Average Execution Time (seconds)")
        print("=" * 70)

        for data_type in df['Data Type'].unique():
            print(f"\n--- {data_type.replace('_', ' ').title()} Arrays ---")
            subset = df[df['Data Type'] == data_type]
            pivot = subset.pivot(index='Size', columns='Algorithm',
                                 values='Execution Time (s)')
            print(pivot.to_string(float_format=lambda x: f"{x:.6f}"))


def main():
    # Increase recursion limit to handle sorted/reverse inputs without crashing
    sys.setrecursionlimit(100000)

    print("QUICKSORT PERFORMANCE COMPARISON")
    print("Deterministic Quicksort vs Randomized Quicksort")
    print("=" * 55)

    analyzer = QuicksortAnalyzer()

    sizes = [100, 500, 1000, 2000, 5000, 10000]
    data_types = ['random', 'sorted', 'reverse', 'nearly_sorted']

    analyzer.run_comparison(sizes, data_types, trials=5)
    analyzer.print_summary_table()
    analyzer.plot_results(sizes, data_types)
    analyzer.export_to_csv('quicksort_results.csv')


if __name__ == "__main__":
    main()
