"""
Performance Comparison of Quick Sort and Merge Sort
This script compares the two divide-and-conquer sorting algorithms across different datasets.
"""

import random
import time
import tracemalloc
import matplotlib.pyplot as plt
import pandas as pd
from quick_sort import quick_sort, quick_sort_randomized
from merge_sort import merge_sort, merge_sort_inplace


def generate_datasets(sizes):
    """
    Generates different types of datasets for testing.

    Args:
        sizes: List of dataset sizes to generate

    Returns:
        Dictionary of datasets organized by type and size
    """
    datasets = {}

    for size in sizes:
        datasets[size] = {
            'random': random.sample(range(size * 10), size),
            'sorted': list(range(size)),
            'reverse_sorted': list(range(size, 0, -1)),
            'nearly_sorted': list(range(size)),
            'many_duplicates': [random.randint(1, 10) for _ in range(size)]
        }

        # Create nearly sorted array (90% sorted with 10% random swaps)
        nearly_sorted = datasets[size]['nearly_sorted']
        num_swaps = max(1, size // 10)
        for _ in range(num_swaps):
            i, j = random.randint(0, size-1), random.randint(0, size-1)
            nearly_sorted[i], nearly_sorted[j] = nearly_sorted[j], nearly_sorted[i]

    return datasets


def measure_algorithm(algorithm, arr, algorithm_name=""):
    """
    Measures execution time and memory usage for a sorting algorithm.

    Args:
        algorithm: Sorting function to test
        arr: Array to sort
        algorithm_name: Name of the algorithm (for error reporting)

    Returns:
        Tuple of (sorted_array, execution_time, peak_memory, success)
    """
    test_arr = arr.copy()

    try:
        # Start memory tracking
        tracemalloc.start()

        # Measure execution time
        start_time = time.perf_counter()
        sorted_arr = algorithm(test_arr)
        end_time = time.perf_counter()

        # Get peak memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        execution_time = end_time - start_time
        peak_memory = peak / 1024  # Convert to KB

        return sorted_arr, execution_time, peak_memory, True

    except RecursionError:
        tracemalloc.stop()
        print(f"RecursionError in {algorithm_name} - stack overflow")
        return None, float('inf'), 0, False
    except Exception as e:
        tracemalloc.stop()
        print(f"Error in {algorithm_name}: {str(e)}")
        return None, float('inf'), 0, False


def compare_algorithms(datasets, algorithms):
    """
    Compares multiple sorting algorithms across different datasets.

    Args:
        datasets: Dictionary of test datasets
        algorithms: Dictionary of {name: function} for algorithms to test

    Returns:
        DataFrame with performance results
    """
    results = []

    for size, data_types in datasets.items():
        print(f"\nTesting with array size: {size}")

        for data_type, arr in data_types.items():
            print(f"  {data_type}...", end=" ")

            for algo_name, algo_func in algorithms.items():
                sorted_arr, exec_time, memory, success = measure_algorithm(
                    algo_func, arr, algo_name
                )

                results.append({
                    'Algorithm': algo_name,
                    'Size': size,
                    'Data Type': data_type,
                    'Execution Time (s)': exec_time if success else None,
                    'Memory (KB)': memory if success else None,
                    'Success': success
                })

            print("Done")

    return pd.DataFrame(results)


def visualize_results(df):
    """
    Creates visualizations for the performance comparison.

    Args:
        df: DataFrame containing performance results
    """
    # Filter out failed runs
    df_success = df[df['Success'] == True].copy()

    if df_success.empty:
        print("No successful runs to visualize")
        return

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Quick Sort vs Merge Sort Performance Comparison',
                 fontsize=16, fontweight='bold')

    # 1. Execution Time by Size (for random data)
    ax1 = axes[0, 0]
    random_data = df_success[df_success['Data Type'] == 'random']
    for algo in random_data['Algorithm'].unique():
        algo_data = random_data[random_data['Algorithm'] == algo]
        ax1.plot(algo_data['Size'], algo_data['Execution Time (s)'],
                 marker='o', label=algo, linewidth=2)
    ax1.set_xlabel('Array Size', fontsize=12)
    ax1.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax1.set_title('Execution Time vs Array Size (Random Data)',
                  fontsize=13, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Memory Usage by Size (for random data)
    ax2 = axes[0, 1]
    for algo in random_data['Algorithm'].unique():
        algo_data = random_data[random_data['Algorithm'] == algo]
        ax2.plot(algo_data['Size'], algo_data['Memory (KB)'],
                 marker='s', label=algo, linewidth=2)
    ax2.set_xlabel('Array Size', fontsize=12)
    ax2.set_ylabel('Memory Usage (KB)', fontsize=12)
    ax2.set_title('Memory Usage vs Array Size (Random Data)',
                  fontsize=13, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Execution Time by Data Type (for a specific size)
    ax3 = axes[1, 0]
    # Use the largest size for this comparison
    largest_size = df_success['Size'].max()
    size_data = df_success[df_success['Size'] == largest_size]

    data_types = size_data['Data Type'].unique()
    algorithms = size_data['Algorithm'].unique()
    x = range(len(data_types))
    width = 0.8 / len(algorithms)

    for i, algo in enumerate(algorithms):
        algo_data = size_data[size_data['Algorithm'] == algo]
        times = [algo_data[algo_data['Data Type'] == dt]['Execution Time (s)'].values[0]
                 if len(algo_data[algo_data['Data Type'] == dt]) > 0 else 0
                 for dt in data_types]
        ax3.bar([xi + i * width for xi in x],
                times, width, label=algo, alpha=0.8)

    ax3.set_xlabel('Data Type', fontsize=12)
    ax3.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax3.set_title(
        f'Execution Time by Data Type (Size={largest_size})', fontsize=13, fontweight='bold')
    ax3.set_xticks([xi + width * (len(algorithms)-1) / 2 for xi in x])
    ax3.set_xticklabels(data_types, rotation=45, ha='right')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # 4. Performance Comparison Table (smallest and largest sizes)
    ax4 = axes[1, 1]
    ax4.axis('tight')
    ax4.axis('off')

    # Create summary statistics
    summary_data = []
    for algo in df_success['Algorithm'].unique():
        algo_df = df_success[df_success['Algorithm'] == algo]
        summary_data.append([
            algo,
            f"{algo_df['Execution Time (s)'].mean():.6f}",
            f"{algo_df['Execution Time (s)'].std():.6f}",
            f"{algo_df['Memory (KB)'].mean():.2f}"
        ])

    table = ax4.table(cellText=summary_data,
                      colLabels=[
                          'Algorithm', 'Avg Time (s)', 'Std Dev (s)', 'Avg Memory (KB)'],
                      cellLoc='center',
                      loc='center',
                      colWidths=[0.25, 0.25, 0.25, 0.25])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style the header row
    for i in range(4):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')

    ax4.set_title('Performance Summary Statistics',
                  fontsize=13, fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    print("\nVisualization saved as 'performance_comparison.png'")
    plt.show()


def print_detailed_results(df):
    """
    Prints detailed results in a formatted table.

    Args:
        df: DataFrame containing performance results
    """
    print("\n" + "="*100)
    print("DETAILED PERFORMANCE RESULTS")
    print("="*100)

    for size in sorted(df['Size'].unique()):
        print(f"\n{'─'*100}")
        print(f"Array Size: {size}")
        print(f"{'─'*100}")

        size_df = df[df['Size'] == size]

        for data_type in size_df['Data Type'].unique():
            print(f"\n  Data Type: {data_type}")
            print(f"  {'-'*90}")

            type_df = size_df[size_df['Data Type'] == data_type]

            for _, row in type_df.iterrows():
                if row['Success']:
                    print(
                        f"    {row['Algorithm']:25} | Time: {row['Execution Time (s)']:10.6f}s | Memory: {row['Memory (KB)']:8.2f} KB")
                else:
                    print(f"    {row['Algorithm']:25} | FAILED")


def analyze_complexity(df):
    """
    Analyzes and prints the empirical complexity of each algorithm.

    Args:
        df: DataFrame containing performance results
    """
    print("\n" + "="*100)
    print("EMPIRICAL COMPLEXITY ANALYSIS")
    print("="*100)

    df_success = df[df['Success'] == True]

    for algo in df_success['Algorithm'].unique():
        print(f"\n{algo}:")
        print(f"{'-'*90}")

        algo_data = df_success[df_success['Algorithm'] == algo]

        for data_type in algo_data['Data Type'].unique():
            type_data = algo_data[algo_data['Data Type']
                                  == data_type].sort_values('Size')

            if len(type_data) >= 2:
                sizes = type_data['Size'].values
                times = type_data['Execution Time (s)'].values

                # Calculate growth rate between consecutive sizes
                growth_rates = []
                for i in range(1, len(sizes)):
                    if times[i-1] > 0:
                        size_ratio = sizes[i] / sizes[i-1]
                        time_ratio = times[i] / times[i-1]
                        growth_rates.append((size_ratio, time_ratio))

                if growth_rates:
                    avg_size_ratio = sum(
                        sr for sr, _ in growth_rates) / len(growth_rates)
                    avg_time_ratio = sum(
                        tr for _, tr in growth_rates) / len(growth_rates)

                    # Estimate complexity (rough approximation)
                    import math
                    if avg_size_ratio > 1:
                        empirical_power = math.log(
                            avg_time_ratio) / math.log(avg_size_ratio)

                        print(
                            f"  {data_type:20} | Empirical growth: O(n^{empirical_power:.2f})", end="")

                        # Interpret the complexity
                        if empirical_power < 1.2:
                            print(" ≈ O(n log n)")
                        elif empirical_power < 1.6:
                            print(" ≈ O(n^1.5)")
                        elif empirical_power < 2.2:
                            print(" ≈ O(n²)")
                        else:
                            print()


def main():
    """
    Main function to run the performance comparison.
    """
    print("="*100)
    print("DIVIDE-AND-CONQUER SORTING ALGORITHMS: PERFORMANCE COMPARISON")
    print("Quick Sort vs Merge Sort")
    print("="*100)

    # Define test sizes
    sizes = [100, 500, 1000, 2000, 5000]

    print(f"\nGenerating test datasets with sizes: {sizes}")
    datasets = generate_datasets(sizes)

    # Define algorithms to compare
    algorithms = {
        'Quick Sort (Standard)': lambda arr: quick_sort(arr.copy()),
        'Quick Sort (Randomized)': lambda arr: quick_sort_randomized(arr.copy()),
        'Merge Sort (Standard)': lambda arr: merge_sort(arr),
        'Merge Sort (In-place)': lambda arr: merge_sort_inplace(arr.copy())
    }

    print("\nRunning performance comparison...")
    results_df = compare_algorithms(datasets, algorithms)

    # Save results to CSV
    results_df.to_csv('performance_results.csv', index=False)
    print("\nResults saved to 'performance_results.csv'")

    # Print detailed results
    print_detailed_results(results_df)

    # Analyze complexity
    analyze_complexity(results_df)

    # Create visualizations
    print("\nGenerating visualizations...")
    visualize_results(results_df)

    print("\n" + "="*100)
    print("Performance comparison completed!")
    print("="*100)


if __name__ == "__main__":
    main()
