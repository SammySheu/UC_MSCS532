"""
Empirical Analysis and Performance Comparison
Assignment 3 - Comprehensive Analysis Script
"""
import random
import time
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from quicksort import (
    randomized_quicksort,
    deterministic_quicksort,
    measure_time
)
from hash_table import HashTable

# Increase recursion limit to handle worst-case deterministic quicksort
sys.setrecursionlimit(50000)


class QuicksortAnalyzer:
    """Analyzer for Quicksort algorithm performance."""

    def __init__(self):
        self.results = {
            'randomized': {},
            'deterministic': {}
        }
        self.detailed_results = []  # For CSV export

    def generate_test_data(self, size: int, data_type: str) -> List[int]:
        """
        Generate test data of specified type.

        Args:
            size: Size of array
            data_type: Type of data ('random', 'sorted', 'reverse', 'repeated')

        Returns:
            List of integers
        """
        if data_type == 'random':
            return [random.randint(1, 10000) for _ in range(size)]
        elif data_type == 'sorted':
            return list(range(size))
        elif data_type == 'reverse':
            return list(range(size, 0, -1))
        elif data_type == 'repeated':
            # Array with many repeated elements (only 10 unique values)
            return [random.randint(1, 10) for _ in range(size)]
        else:
            raise ValueError(f"Unknown data type: {data_type}")

    def run_comparison(self, sizes: List[int], data_types: List[str], trials: int = 10):
        """
        Run comprehensive comparison of quicksort algorithms.

        Args:
            sizes: List of array sizes to test
            data_types: List of data types to test
            trials: Number of trials per configuration
        """
        for data_type in data_types:
            print(f"\nAnalyzing {data_type} arrays...")

            randomized_times = []
            deterministic_times = []

            for size in sizes:
                print(f"  Size {size}...", end='', flush=True)

                rand_avg = 0
                det_avg = 0

                for _ in range(trials):
                    # Generate fresh data for each trial
                    data = self.generate_test_data(size, data_type)

                    # Measure randomized quicksort
                    rand_time = measure_time(randomized_quicksort, data)
                    rand_avg += rand_time

                    # Measure deterministic quicksort
                    # Note: This will be very slow on sorted/reverse arrays (O(n²))
                    det_time = measure_time(deterministic_quicksort, data)
                    det_avg += det_time

                rand_avg /= trials
                det_avg /= trials

                randomized_times.append(rand_avg)
                deterministic_times.append(det_avg)

                # Store detailed results for CSV
                self.detailed_results.append({
                    'Algorithm': 'Randomized Quicksort',
                    'Data Type': data_type,
                    'Size': size,
                    'Execution Time (s)': rand_avg,
                    'Speedup': det_avg / rand_avg if rand_avg > 0 else 0
                })
                self.detailed_results.append({
                    'Algorithm': 'Deterministic Quicksort',
                    'Data Type': data_type,
                    'Size': size,
                    'Execution Time (s)': det_avg,
                    'Speedup': 1.0  # Baseline
                })

                print(f" Done (Rand: {rand_avg:.6f}s, Det: {det_avg:.6f}s)")

            self.results['randomized'][data_type] = randomized_times
            self.results['deterministic'][data_type] = deterministic_times

    def plot_results(self, sizes: List[int], data_types: List[str]):
        """
        Plot comparison results with beautiful styling.

        Args:
            sizes: List of array sizes tested
            data_types: List of data types tested
        """
        # Define color scheme
        colors = {
            'randomized': '#2196F3',  # Blue
            'deterministic': '#FF5722'  # Deep Orange
        }

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Randomized vs Deterministic Quicksort: Performance Comparison',
                     fontsize=18, fontweight='bold', y=0.995)

        for idx, data_type in enumerate(data_types):
            ax = axes[idx // 2, idx % 2]

            rand_times = self.results['randomized'][data_type]
            det_times = self.results['deterministic'][data_type]

            # Plot with enhanced styling
            ax.plot(sizes, rand_times, 'o-', label='Randomized Quicksort',
                    linewidth=2.5, markersize=10, color=colors['randomized'],
                    markeredgewidth=2, markeredgecolor='white', alpha=0.9)
            ax.plot(sizes, det_times, 's-', label='Deterministic Quicksort',
                    linewidth=2.5, markersize=10, color=colors['deterministic'],
                    markeredgewidth=2, markeredgecolor='white', alpha=0.9)

            ax.set_xlabel('Array Size', fontsize=13, fontweight='bold')
            ax.set_ylabel('Execution Time (seconds)',
                          fontsize=13, fontweight='bold')
            ax.set_title(f'{data_type.capitalize().replace("_", " ")} Arrays',
                         fontsize=14, fontweight='bold', pad=12)
            ax.legend(fontsize=11, loc='best', framealpha=0.95, shadow=True)
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
            ax.set_xscale('log')
            ax.set_yscale('log')

            # Add subtle background color
            ax.set_facecolor('#f8f9fa')

            # Format tick labels
            ax.tick_params(labelsize=10)

        plt.tight_layout()
        plt.savefig('quicksort_comparison.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()

    def export_to_csv(self, filename: str = 'quicksort_results.csv'):
        """
        Export results to CSV file.

        Args:
            filename: Output CSV filename
        """
        df = pd.DataFrame(self.detailed_results)
        df = df.sort_values(['Data Type', 'Size', 'Algorithm'])
        df.to_csv(filename, index=False)
        print(f"\n✅ Quicksort results saved to '{filename}'")


class HashTableAnalyzer:
    """Analyzer for Hash Table performance."""

    def __init__(self):
        self.results = {}
        self.detailed_results = []  # For CSV export

    def analyze_operations(self, sizes: List[int], trials: int = 100):
        """
        Analyze hash table operations at different load factors.

        Args:
            sizes: List of sizes to test
            trials: Number of operations per test
        """
        for size in sizes:
            print(f"\nTesting with {size} elements...")

            # Start with load factor ~2
            ht = HashTable(initial_capacity=size // 2)

            # Insert elements
            insert_times = []
            for i in range(size):
                start = time.perf_counter()
                ht.insert(f"key_{i}", i)
                end = time.perf_counter()
                insert_times.append(end - start)

            # Search operations
            search_times = []
            for _ in range(trials):
                key = f"key_{random.randint(0, size - 1)}"
                start = time.perf_counter()
                ht.search(key)
                end = time.perf_counter()
                search_times.append(end - start)

            # Delete operations
            delete_times = []
            for _ in range(min(trials, size // 2)):
                key = f"key_{random.randint(0, size - 1)}"
                start = time.perf_counter()
                ht.delete(key)
                end = time.perf_counter()
                delete_times.append(end - start)

            stats = ht.get_statistics()

            self.results[size] = {
                'insert_avg': np.mean(insert_times),
                'search_avg': np.mean(search_times),
                'delete_avg': np.mean(delete_times),
                'load_factor': stats['load_factor'],
                'avg_chain_length': stats['avg_chain_length'],
                'max_chain_length': stats['max_chain_length']
            }

            # Store detailed results for CSV
            self.detailed_results.append({
                'Size': size,
                'Insert Time (s)': np.mean(insert_times),
                'Search Time (s)': np.mean(search_times),
                'Delete Time (s)': np.mean(delete_times),
                'Load Factor': stats['load_factor'],
                'Avg Chain Length': stats['avg_chain_length'],
                'Max Chain Length': stats['max_chain_length'],
                'Capacity': stats['capacity']
            })

            print(
                f"  Average Insert Time: {self.results[size]['insert_avg']:.8f}s")
            print(
                f"  Average Search Time: {self.results[size]['search_avg']:.8f}s")
            print(
                f"  Average Delete Time: {self.results[size]['delete_avg']:.8f}s")
            print(f"  Load Factor: {stats['load_factor']:.2f}")
            print(f"  Average Chain Length: {stats['avg_chain_length']:.2f}")
            print(f"  Max Chain Length: {stats['max_chain_length']}")

    def analyze_load_factor_impact(self, base_size: int = 1000):
        """
        Analyze impact of load factor on performance.

        Args:
            base_size: Base size for testing
        """
        load_factors = []
        search_times = []
        chain_lengths = []

        # Test different initial capacities to get different load factors
        capacities = [base_size * 2, base_size,
                      base_size // 2, base_size // 4, base_size // 8]

        for capacity in capacities:
            ht = HashTable(initial_capacity=capacity,
                           load_factor_threshold=10.0)  # Disable auto-resize

            # Insert elements
            for i in range(base_size):
                ht.insert(f"key_{i}", i)

            # Measure search time
            trials = 1000
            total_time = 0
            for _ in range(trials):
                key = f"key_{random.randint(0, base_size - 1)}"
                start = time.perf_counter()
                ht.search(key)
                end = time.perf_counter()
                total_time += (end - start)

            avg_search_time = total_time / trials
            stats = ht.get_statistics()

            load_factors.append(stats['load_factor'])
            # Convert to microseconds
            search_times.append(avg_search_time * 1e6)
            chain_lengths.append(stats['avg_chain_length'])

            print(f"\nLoad Factor: {stats['load_factor']:.2f}")
            print(f"  Average Search Time: {avg_search_time * 1e6:.3f} μs")
            print(f"  Average Chain Length: {stats['avg_chain_length']:.2f}")

        # Plot results with enhanced styling
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        fig.suptitle('Hash Table Performance: Impact of Load Factor',
                     fontsize=18, fontweight='bold', y=0.98)

        # Search time vs load factor
        ax1.plot(load_factors, search_times, 'o-', linewidth=2.5, markersize=12,
                 color='#2196F3', markeredgewidth=2, markeredgecolor='white', alpha=0.9)
        ax1.set_xlabel('Load Factor (α)', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Average Search Time (μs)',
                       fontsize=13, fontweight='bold')
        ax1.set_title('Search Time vs Load Factor',
                      fontsize=14, fontweight='bold', pad=12)
        ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax1.set_facecolor('#f8f9fa')
        ax1.tick_params(labelsize=11)

        # Add annotation for optimal range
        ax1.axvspan(0, 0.75, alpha=0.1, color='green',
                    label='Optimal Range (α ≤ 0.75)')
        ax1.axvspan(0.75, max(load_factors), alpha=0.1,
                    color='red', label='High Load (α > 0.75)')
        ax1.legend(fontsize=10, loc='upper left', framealpha=0.95)

        # Chain length vs load factor
        ax2.plot(load_factors, chain_lengths, 's-', linewidth=2.5, markersize=12,
                 color='#FF5722', markeredgewidth=2, markeredgecolor='white', alpha=0.9)
        ax2.set_xlabel('Load Factor (α)', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Average Chain Length', fontsize=13, fontweight='bold')
        ax2.set_title('Chain Length vs Load Factor',
                      fontsize=14, fontweight='bold', pad=12)
        ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax2.set_facecolor('#f8f9fa')
        ax2.tick_params(labelsize=11)

        # Add reference line for y=x (theoretical expectation)
        ax2.plot([0, max(load_factors)], [0, max(load_factors)],
                 'k--', alpha=0.5, linewidth=1.5, label='Theoretical (α = chain length)')
        ax2.legend(fontsize=10, loc='upper left', framealpha=0.95)

        plt.tight_layout()
        plt.savefig('hash_table_load_factor.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        print("\nPlot saved as 'hash_table_load_factor.png'")
        plt.show()

    def plot_operation_times(self, sizes: List[int]):
        """
        Plot operation times across different sizes with beautiful styling.

        Args:
            sizes: List of sizes tested
        """
        insert_times = [self.results[s]['insert_avg'] * 1e6 for s in sizes]
        search_times = [self.results[s]['search_avg'] * 1e6 for s in sizes]
        delete_times = [self.results[s]['delete_avg'] * 1e6 for s in sizes]

        # Color scheme
        colors = {
            'insert': '#4CAF50',  # Green
            'search': '#2196F3',  # Blue
            'delete': '#FF5722'   # Deep Orange
        }

        _, ax = plt.subplots(figsize=(12, 7))

        ax.plot(sizes, insert_times, 'o-', label='Insert', linewidth=2.5,
                markersize=10, color=colors['insert'], markeredgewidth=2,
                markeredgecolor='white', alpha=0.9)
        ax.plot(sizes, search_times, 's-', label='Search', linewidth=2.5,
                markersize=10, color=colors['search'], markeredgewidth=2,
                markeredgecolor='white', alpha=0.9)
        ax.plot(sizes, delete_times, '^-', label='Delete', linewidth=2.5,
                markersize=10, color=colors['delete'], markeredgewidth=2,
                markeredgecolor='white', alpha=0.9)

        ax.set_xlabel('Number of Elements', fontsize=13, fontweight='bold')
        ax.set_ylabel('Average Time (μs)', fontsize=13, fontweight='bold')
        ax.set_title('Hash Table Operations: Performance vs Size',
                     fontsize=16, fontweight='bold', pad=15)
        ax.legend(fontsize=12, loc='best', framealpha=0.95, shadow=True)
        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_facecolor('#f8f9fa')
        ax.tick_params(labelsize=11)

        plt.tight_layout()
        plt.savefig('hash_table_operations.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()

    def create_visualization(self):
        """Create a single visualization of hash table analyses."""
        # Extract data from existing results
        if not self.results:
            print("No data available. Please run analyze_operations first.")
            return

        sizes = sorted(self.results.keys())
        insert_times = [self.results[s]['insert_avg'] * 1e6 for s in sizes]
        search_times = [self.results[s]['search_avg'] * 1e6 for s in sizes]
        delete_times = [self.results[s]['delete_avg'] * 1e6 for s in sizes]

        # Re-collect load factor data for combined plot
        base_size = 1000
        capacities = [base_size * 2, base_size,
                      base_size // 2, base_size // 4, base_size // 8]

        load_factors = []
        search_time_lf = []
        chain_lengths = []

        for capacity in capacities:
            ht = HashTable(initial_capacity=capacity,
                           load_factor_threshold=10.0)

            for i in range(base_size):
                ht.insert(f"key_{i}", i)

            trials = 1000
            total_time = 0
            for _ in range(trials):
                key = f"key_{random.randint(0, base_size - 1)}"
                start = time.perf_counter()
                ht.search(key)
                end = time.perf_counter()
                total_time += (end - start)

            stats = ht.get_statistics()
            load_factors.append(stats['load_factor'])
            search_time_lf.append((total_time / trials) * 1e6)
            chain_lengths.append(stats['avg_chain_length'])

        # Create combined figure with 3 subplots
        fig = plt.figure(figsize=(18, 6))

        colors = {
            'insert': '#4CAF50',
            'search': '#2196F3',
            'delete': '#FF5722'
        }

        # Subplot 1: Operations vs Size
        ax1 = plt.subplot(1, 3, 1)
        ax1.plot(sizes, insert_times, 'o-', label='Insert', linewidth=2.5,
                 markersize=10, color=colors['insert'], markeredgewidth=2,
                 markeredgecolor='white', alpha=0.9)
        ax1.plot(sizes, search_times, 's-', label='Search', linewidth=2.5,
                 markersize=10, color=colors['search'], markeredgewidth=2,
                 markeredgecolor='white', alpha=0.9)
        ax1.plot(sizes, delete_times, '^-', label='Delete', linewidth=2.5,
                 markersize=10, color=colors['delete'], markeredgewidth=2,
                 markeredgecolor='white', alpha=0.9)

        ax1.set_xlabel('Number of Elements', fontsize=13, fontweight='bold')
        ax1.set_ylabel('Average Time (μs)', fontsize=13, fontweight='bold')
        ax1.set_title('Operation Times vs Size',
                      fontsize=14, fontweight='bold', pad=12)
        ax1.legend(fontsize=11, loc='best', framealpha=0.95, shadow=True)
        ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_facecolor('#f8f9fa')
        ax1.tick_params(labelsize=10)

        # Subplot 2: Search Time vs Load Factor
        ax2 = plt.subplot(1, 3, 2)
        ax2.plot(load_factors, search_time_lf, 'o-', linewidth=2.5, markersize=12,
                 color='#2196F3', markeredgewidth=2, markeredgecolor='white', alpha=0.9)
        ax2.set_xlabel('Load Factor (α)', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Average Search Time (μs)',
                       fontsize=13, fontweight='bold')
        ax2.set_title('Search Time vs Load Factor',
                      fontsize=14, fontweight='bold', pad=12)
        ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax2.set_facecolor('#f8f9fa')
        ax2.tick_params(labelsize=10)

        ax2.axvspan(0, 0.75, alpha=0.1, color='green',
                    label='Optimal (α ≤ 0.75)')
        ax2.axvspan(0.75, max(load_factors), alpha=0.1,
                    color='red', label='High (α > 0.75)')
        ax2.legend(fontsize=10, loc='upper left', framealpha=0.95)

        # Subplot 3: Chain Length vs Load Factor
        ax3 = plt.subplot(1, 3, 3)
        ax3.plot(load_factors, chain_lengths, 's-', linewidth=2.5, markersize=12,
                 color='#FF5722', markeredgewidth=2, markeredgecolor='white', alpha=0.9)
        ax3.set_xlabel('Load Factor (α)', fontsize=13, fontweight='bold')
        ax3.set_ylabel('Average Chain Length', fontsize=13, fontweight='bold')
        ax3.set_title('Chain Length vs Load Factor',
                      fontsize=14, fontweight='bold', pad=12)
        ax3.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
        ax3.set_facecolor('#f8f9fa')
        ax3.tick_params(labelsize=10)

        ax3.plot([0, max(load_factors)], [0, max(load_factors)],
                 'k--', alpha=0.5, linewidth=1.5, label='Theoretical (α = length)')
        ax3.legend(fontsize=10, loc='upper left', framealpha=0.95)

        fig.suptitle('Hash Table with Chaining: Comprehensive Performance Analysis',
                     fontsize=18, fontweight='bold', y=1.00)

        plt.tight_layout()
        plt.savefig('hash_table_analysis.png', dpi=300, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.show()

    def export_to_csv(self, filename: str = 'hash_table_results.csv'):
        """
        Export results to CSV file.

        Args:
            filename: Output CSV filename
        """
        df = pd.DataFrame(self.detailed_results)
        df = df.sort_values('Size')
        df.to_csv(filename, index=False)
        print(f"\n✅ Hash table results saved to '{filename}'")


def main():

    # Part 1: Quicksort Analysis
    print("PART 1: RANDOMIZED QUICKSORT ANALYSIS")

    qs_analyzer = QuicksortAnalyzer()

    # Test sizes
    sizes = [100, 500, 1000, 2000, 5000, 10000]
    data_types = ['random', 'sorted', 'reverse', 'repeated']

    qs_analyzer.run_comparison(sizes, data_types, trials=5)
    qs_analyzer.plot_results(sizes, data_types)

    # Export quicksort results to CSV
    qs_analyzer.export_to_csv('quicksort_results.csv')

    # Part 2: Hash Table Analysis
    print("\nPART 2: HASH TABLE ANALYSIS")
    ht_analyzer = HashTableAnalyzer()

    # Test different sizes
    ht_sizes = [100, 500, 1000, 5000, 10000]
    ht_analyzer.analyze_operations(ht_sizes, trials=100)

    # Create hash table visualization
    ht_analyzer.create_visualization()

    # Export hash table results to CSV
    ht_analyzer.export_to_csv('hash_table_results.csv')


if __name__ == "__main__":
    main()
