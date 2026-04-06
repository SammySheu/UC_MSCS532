"""
locality_benchmark.py
---------------------
Final Project: Data Locality and Cache Efficiency Optimization
Course: Algorithms and Data Structures (MSCS-532-M80)
Author: Sam Sheu (Chun-Shuo, Sheu)
Date: April 5, 2026

Demonstrates the performance impact of memory layout and data locality
using NumPy. Compares three configurations:
  1. C-contiguous array (row-major, locality-friendly row traversal)
  2. Non-contiguous transposed view (column-major strides, locality-unfriendly)
  3. Contiguous copy of the transposed view (locality restored via ascontiguousarray)

The benchmark sums each row in a Python loop so that traversal order is
visible to the profiler rather than hidden inside a single vectorized call.

Usage:
    python locality_benchmark.py

Requirements:
    numpy >= 1.20
    Python >= 3.8
"""

import time
from typing import Callable, Tuple

import numpy as np


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ROWS = 4000
COLS = 2000
DTYPE = np.float64
REPETITIONS = 5


# ---------------------------------------------------------------------------
# Core benchmark function
# ---------------------------------------------------------------------------

def row_loop_sum(arr: np.ndarray) -> np.ndarray:
    """
    Sum each row of a 2-D array using an explicit Python loop.

    Using a loop (rather than arr.sum(axis=1)) preserves the row-by-row
    access pattern and makes memory-layout differences observable at runtime.

    Args:
        arr: A 2-D NumPy array of shape (n_rows, n_cols).

    Returns:
        A 1-D array of length n_rows where element i is the sum of row i.
    """
    out = np.empty(arr.shape[0], dtype=np.float64)
    for i in range(arr.shape[0]):
        out[i] = arr[i].sum()
    return out


def time_function(func: Callable, arr: np.ndarray, reps: int = REPETITIONS) -> Tuple[float, float]:
    """
    Time a function call over multiple repetitions and return mean and std.

    Args:
        func:  Callable that accepts a single NumPy array.
        arr:   Input array to pass to func.
        reps:  Number of repetitions.

    Returns:
        Tuple of (mean_seconds, std_seconds).
    """
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        func(arr)
        end = time.perf_counter()
        times.append(end - start)
    arr_times = np.array(times)
    return float(arr_times.mean()), float(arr_times.std())


# ---------------------------------------------------------------------------
# Array construction helpers
# ---------------------------------------------------------------------------

def build_arrays(rows: int = ROWS, cols: int = COLS) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create the three array variants used in the benchmark.

    1. A   — C-contiguous (row-major) array.
    2. AT  — Non-contiguous transposed view of A (strides are column-major).
    3. AC  — Contiguous copy of AT, produced with np.ascontiguousarray.

    Args:
        rows: Number of rows for the base matrix.
        cols: Number of columns for the base matrix.

    Returns:
        Tuple (A, AT, AC).
    """
    rng = np.random.default_rng(seed=42)
    A: np.ndarray = rng.random((rows, cols)).astype(DTYPE)
    AT: np.ndarray = A.T          # view: shape (cols, rows), non-contiguous
    AC: np.ndarray = np.ascontiguousarray(AT)  # fresh contiguous copy
    return A, AT, AC


# ---------------------------------------------------------------------------
# Diagnostics: show memory layout metadata
# ---------------------------------------------------------------------------

def print_array_info(label: str, arr: np.ndarray) -> None:
    """
    Print shape, strides, dtype, and contiguity flags for a NumPy array.

    Args:
        label: Human-readable name for the array.
        arr:   Array to inspect.
    """
    print(f"  {label}:")
    print(f"    shape       = {arr.shape}")
    print(f"    strides     = {arr.strides}  (bytes between elements along each axis)")
    print(f"    dtype       = {arr.dtype}")
    print(f"    C-contiguous= {arr.flags['C_CONTIGUOUS']}")
    print(f"    F-contiguous= {arr.flags['F_CONTIGUOUS']}")
    size_mb = arr.nbytes / (1024 ** 2)
    print(f"    memory      ≈ {size_mb:.2f} MB")


# ---------------------------------------------------------------------------
# Main benchmark runner
# ---------------------------------------------------------------------------

def run_benchmark() -> None:
    """
    Build arrays, run the timed benchmark for each configuration, and
    print a formatted results table with relative speedups.
    """
    print("=" * 65)
    print("  Data Locality and Cache Efficiency Benchmark (NumPy)")
    print("=" * 65)

    # --- Array construction ---
    print(f"\nBuilding arrays: base shape ({ROWS}, {COLS}), dtype={DTYPE.__name__}")
    A, AT, AC = build_arrays(ROWS, COLS)

    print("\nArray memory layout details:")
    print_array_info("A   [C-contiguous, row-major]", A)
    print_array_info("A.T [non-contiguous view, column-major strides]", AT)
    print_array_info("AC  [ascontiguousarray(A.T), C-contiguous copy]", AC)

    # --- Warm-up pass (avoids cold-cache effects on first timed run) ---
    print("\nWarm-up pass (not timed)...")
    row_loop_sum(A)

    # --- Timed runs ---
    print(f"\nRunning row_loop_sum on each configuration ({REPETITIONS} repetitions)...\n")

    mean_A,  std_A  = time_function(row_loop_sum, A)
    mean_AT, std_AT = time_function(row_loop_sum, AT)
    mean_AC, std_AC = time_function(row_loop_sum, AC)

    # --- Results table ---
    baseline = mean_AT  # non-contiguous is the worst case / baseline

    col_w = [46, 22, 18]
    header = (
        f"{'Configuration':<{col_w[0]}}"
        f"{'Mean Time (s)':>{col_w[1]}}"
        f"{'Relative Speed':>{col_w[2]}}"
    )
    separator = "-" * sum(col_w)

    print(separator)
    print(header)
    print(separator)

    configs = [
        ("A — C-contiguous (row-major)",           mean_A,  std_A,  baseline / mean_A),
        ("A.T — non-contiguous view (baseline)",   mean_AT, std_AT, 1.0),
        ("ascontiguousarray(A.T) — contiguous copy", mean_AC, std_AC, baseline / mean_AC),
    ]
    for label, mean, std, rel in configs:
        rel_str = "1.00x (baseline)" if rel == 1.0 else f"{rel:.2f}x faster"
        time_str = f"{mean:.4f} +/- {std:.4f}"
        print(f"{label:<{col_w[0]}}{time_str:>{col_w[1]}}{rel_str:>{col_w[2]}}")
    print(separator)

    # --- Interpretation ---
    print("\nInterpretation:")
    print(f"  Non-contiguous A.T is {baseline/mean_A:.2f}× slower than A.")
    print(f"  Restoring contiguity (ascontiguousarray) yields a "
          f"{baseline/mean_AC:.2f}× speedup over A.T.")
    print(f"  This confirms that memory layout — not just arithmetic — "
          f"drives runtime in cache-sensitive workloads.")

    # --- NumPy / Python version info ---
    import sys
    print(f"\nEnvironment: Python {sys.version.split()[0]}, NumPy {np.__version__}")
    print("=" * 65)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    run_benchmark()
