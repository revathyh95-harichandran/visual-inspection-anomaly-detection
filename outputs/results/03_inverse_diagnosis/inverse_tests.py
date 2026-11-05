import csv
import sys
import time

import torch

RESULTS_FILE = "inverse_results.csv"
SEED = 42
PHOTO_DIFFERENCES = 7
# PaDiM adds these two values along the diagonal of each table
DIAGONAL_ADDITION = 0.01 + 0.00001
TABLES_CHECKED_FOR_ACCURACY = 16

if torch.cuda.is_available():
    TABLE_SIZES = [100, 550]
    COUNTS = [1, 16, 256, 1024, 4096]
    FULL_COUNT = 4096
    GROUPS = {100: [1024, 256, 64, 16, 1], 550: [1024, 256, 64]}
else:
    # The laptop only checks that the code runs
    TABLE_SIZES = [10, 20]
    COUNTS = [1, 4]
    FULL_COUNT = 8
    GROUPS = {10: [4, 1], 20: [4]}


def make_tables(count, size):
    """Build made-up symmetric tables resembling PaDiM's, repeatable with the seed."""
    generator = torch.Generator().manual_seed(SEED)
    random_numbers = torch.randn(count, size, PHOTO_DIFFERENCES, generator=generator)
    tables = torch.bmm(random_numbers, random_numbers.transpose(1, 2)) / PHOTO_DIFFERENCES
    return tables + DIAGONAL_ADDITION * torch.eye(size)


def wait_for_gpu(device):
    """Wait for the GPU to finish, so the timer does not stop early."""
    if device == "cuda":
        torch.cuda.synchronize()


def largest_error(tables, inverses):
    """Return how far table times inverse is from the identity table."""
    product = torch.bmm(tables, inverses)
    identity = torch.eye(tables.shape[1], device=tables.device)
    return float((product - identity).abs().max())


def record(part, size, count, group, outcome, seconds, peak_gb, error):
    """Save one test's result straight away, and print it."""
    with open(RESULTS_FILE, "a", newline="") as results_file:
        csv.writer(results_file).writerow([part, size, count, group, outcome, seconds, peak_gb, error])
    print(part, size, count, group, outcome, seconds, peak_gb, error, flush=True)


def run_test(part, size, count, group, device):
    """Invert the tables in groups. Return worked, out of memory or gpu error."""
    tables = make_tables(count, size)
    if device == "cuda":
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

    error = ""
    try:
        wait_for_gpu(device)
        started = time.perf_counter()
        for start in range(0, count, group):
            group_tables = tables[start:start + group].to(device)
            inverses = torch.linalg.inv(group_tables)
            wait_for_gpu(device)
            if start == 0:
                checked = TABLES_CHECKED_FOR_ACCURACY
                first_error = largest_error(group_tables[:checked], inverses[:checked])
                error = round(first_error, 6)
        seconds = round(time.perf_counter() - started, 3)
        peak_gb = ""
        if device == "cuda":
            peak_gb = round(torch.cuda.max_memory_allocated() / 1e9, 2)
        record(part, size, count, group, "worked", seconds, peak_gb, error)
        return "worked"
    except torch.cuda.OutOfMemoryError:
        record(part, size, count, group, "out of memory", "", "", "")
        return "out of memory"
    except torch.AcceleratorError as gpu_error:
        message = str(gpu_error).split("\n")[0]
        record(part, size, count, group, "gpu error: " + message, "", "", "")
        return "gpu error"


def part_a():
    """Whole tables at once, from small up to PaDiM's real size."""
    for size in TABLE_SIZES:
        for count in COUNTS:
            outcome = run_test("A", size, count, count, "cuda")
            if outcome == "gpu error":
                return
            if outcome == "out of memory":
                break


def part_b():
    """The full number of tables, split into smaller groups."""
    for size in TABLE_SIZES:
        for group in GROUPS[size]:
            outcome = run_test("B", size, FULL_COUNT, group, "cuda")
            if outcome == "gpu error":
                return


def part_c():
    """The full number of tables on the processor, which does not use the GPU."""
    for size in TABLE_SIZES:
        run_test("C", size, FULL_COUNT, FULL_COUNT, "cpu")


part_name = sys.argv[1]
if part_name == "A":
    if torch.cuda.is_available():
        part_a()
elif part_name == "B":
    if torch.cuda.is_available():
        part_b()
else:
    part_c()
