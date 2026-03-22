"""
Empirical Analysis and Performance Comparison
Assignment 7 - Hash Table: Separate Chaining vs Open Addressing
"""
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List

from hash_table import (
    HashTableChaining,
    HashTableOpenAddressing,
    division_hash,
)


class HashTableAnalyzer:
    """Analyzer for comparing Separate Chaining vs Open Addressing hash tables."""

    def __init__(self):
        self.detailed_results = []

    def generate_keys(self, size: int, data_type: str) -> List[int]:
        """
        Generate a list of unique integer keys with the requested distribution.

        Args:
            size: Number of keys to generate
            data_type: One of 'random', 'sequential', 'clustered', 'nearly_sequential'

        Returns:
            List of unique integer keys
        """
        if data_type == 'random':
            # Uniform spread — keys drawn from a range 10x the table size
            return random.sample(range(1, size * 10 + 1), size)
        elif data_type == 'sequential':
            # Keys 0..n-1: each hashes to its own bucket with division_hash
            # and capacity = size * 2, so no collisions occur
            return list(range(size))
        elif data_type == 'clustered':
            # Multiples of 100: with capacity = size * 2,
            # gcd(100, size * 2) causes most keys to land in the same
            # ~(size * 2 / 100) buckets — e.g. 20 buckets for size=1000,
            # meaning ~50 keys per bucket on average.  This is the
            # "poor hash function design" scenario from the assignment prompt.
            return [i * 100 for i in range(size)]
        elif data_type == 'nearly_sequential':
            # Sequential with ~5% of positions randomly swapped
            arr = list(range(size))
            swaps = max(1, size // 20)
            for _ in range(swaps):
                i, j = random.randint(0, size - 1), random.randint(0, size - 1)
                arr[i], arr[j] = arr[j], arr[i]
            return arr
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def _benchmark_search(self, ht_class, keys: List[int], capacity: int) -> float:
        """
        Build a hash table, insert all keys, then time searching for all of them.

        Args:
            ht_class: HashTableChaining or HashTableOpenAddressing
            keys: Keys to insert and subsequently search for
            capacity: Table capacity to use

        Returns:
            Total wall-clock time (seconds) to complete all searches
        """
        ht = ht_class(capacity=capacity, hash_func=division_hash)
        for k in keys:
            ht.insert(k, k)

        start = time.perf_counter()
        for k in keys:
            ht.search(k)
        return time.perf_counter() - start

    def run_comparison(self, sizes: List[int], data_types: List[str], trials: int = 5):
        """
        Benchmark both hash table implementations across sizes and data types.

        The table capacity is set to size * 2 for every configuration,
        giving a steady load factor of ~0.5 across all tests.

        Args:
            sizes: List of table sizes to benchmark
            data_types: List of key distributions to test
            trials: Number of independent trials to average per configuration
        """
        algorithms = {
            'Separate Chaining': HashTableChaining,
            'Open Addressing':   HashTableOpenAddressing,
        }

        for data_type in data_types:
            print(f"\nAnalyzing {data_type} keys...")

            for size in sizes:
                print(f"  Size {size}...", end='', flush=True)
                capacity = size * 2  # Load factor ≈ 0.5

                for algo_name, ht_class in algorithms.items():
                    times = []
                    for _ in range(trials):
                        keys = self.generate_keys(size, data_type)
                        t = self._benchmark_search(ht_class, keys, capacity)
                        times.append(t)

                    avg_time = float(np.mean(times))

                    self.detailed_results.append({
                        'Algorithm':          algo_name,
                        'Data Type':          data_type,
                        'Size':               size,
                        'Execution Time (s)': avg_time,
                    })

                print(" Done")

    def plot_results(self, sizes: List[int], data_types: List[str]):
        """
        Plot the performance comparison as a 2×2 grid of subplots.

        Args:
            sizes: List of table sizes that were benchmarked
            data_types: List of key distributions that were benchmarked
        """
        colors = {
            'Separate Chaining': '#E53935',
            'Open Addressing':   '#1E88E5',
        }
        markers = {
            'Separate Chaining': 's',
            'Open Addressing':   'o',
        }

        df = pd.DataFrame(self.detailed_results)

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Hash Table Comparison: Separate Chaining vs Open Addressing',
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

            ax.set_xlabel('Number of Keys', fontsize=13, fontweight='bold')
            ax.set_ylabel('Search Time (seconds)', fontsize=13, fontweight='bold')
            ax.set_title(f'{data_type.replace("_", " ").title()} Keys',
                         fontsize=14, fontweight='bold', pad=12)
            ax.legend(fontsize=11, loc='best', framealpha=0.95, shadow=True)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_facecolor('#f8f9fa')
            ax.tick_params(labelsize=10)

        plt.tight_layout()
        plt.savefig('./Assignment7/hashtable_comparison.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()
        print("Chart saved to 'hashtable_comparison.png'")

    def export_to_csv(self, filename: str = 'hashtable_results.csv'):
        """Export benchmark results to a CSV file."""
        df = pd.DataFrame(self.detailed_results)
        df = df.sort_values(['Data Type', 'Size', 'Algorithm'])
        df.to_csv(filename, index=False)
        print(f"Results saved to '{filename}'")

    def print_summary_table(self):
        """Print a formatted summary table of average search times."""
        df = pd.DataFrame(self.detailed_results)
        print("\n" + "=" * 70)
        print("SUMMARY: Average Search Time (seconds)")
        print("=" * 70)

        for data_type in df['Data Type'].unique():
            print(f"\n--- {data_type.replace('_', ' ').title()} Keys ---")
            subset = df[df['Data Type'] == data_type]
            pivot = subset.pivot(index='Size', columns='Algorithm',
                                 values='Execution Time (s)')
            print(pivot.to_string(float_format=lambda x: f"{x:.6f}"))


def main():
    print("HASH TABLE PERFORMANCE COMPARISON")
    print("Separate Chaining vs Open Addressing")
    print("=" * 55)

    analyzer = HashTableAnalyzer()

    sizes = [100, 500, 1000, 2000, 5000, 10000]
    data_types = ['random', 'sequential', 'clustered', 'nearly_sequential']

    analyzer.run_comparison(sizes, data_types, trials=5)
    analyzer.print_summary_table()
    analyzer.plot_results(sizes, data_types)
    analyzer.export_to_csv('./Assignment7/hashtable_results.csv')


if __name__ == "__main__":
    main()
