# Runs quicksort benchmarks and hash table sanity benchmarks.

from __future__ import annotations
import random
import time
import statistics
from quicksort import deterministic_quicksort, randomized_quicksort
from hashtable import HashTableChaining

def is_sorted(a) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

def gen_array(n: int, kind: str, rng: random.Random):
    if kind == "random":
        return [rng.randint(0, 10 * n) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    if kind == "repeated":
        return [rng.randint(0, 50) for _ in range(n)]
    raise ValueError("Unknown distribution")

def bench_quicksort(sizes, kinds, trials=3, seed=42):
    rng = random.Random(seed)
    out = []
    for kind in kinds:
        for n in sizes:
            det_times = []
            rand_times = []
            for _ in range(trials):
                base = gen_array(n, kind, rng)
                a1 = base.copy()
                a2 = base.copy()

                t0 = time.perf_counter()
                deterministic_quicksort(a1)
                t1 = time.perf_counter()
                randomized_quicksort(a2, rng)
                t2 = time.perf_counter()

                assert is_sorted(a1) and is_sorted(a2)

                det_times.append(t1 - t0)
                rand_times.append(t2 - t1)

            det_mean = statistics.mean(det_times)
            rand_mean = statistics.mean(rand_times)
            ratio = det_mean / rand_mean if rand_mean > 0 else float("inf")

            out.append((kind, n, det_mean, rand_mean, ratio))
    return out

def hash_experiment(n: int, trials: int = 2000, seed: int = 1):
    rng = random.Random(seed)
    ht = HashTableChaining(capacity=8)

    keys = [rng.randrange(1, 10**9) for _ in range(n)]

    t0 = time.perf_counter()
    for k in keys:
        ht.insert(k, k * 2)
    t1 = time.perf_counter()

    sample_keys = [keys[rng.randrange(0, n)] for _ in range(trials)]
    t2 = time.perf_counter()
    for k in sample_keys:
        assert ht.search(k) is not None
    t3 = time.perf_counter()

    miss_keys = [rng.randrange(1, 10**9) for _ in range(trials)]
    t4 = time.perf_counter()
    for k in miss_keys:
        _ = ht.search(k)
    t5 = time.perf_counter()

    stats = ht.bucket_stats()
    return {
        "n": n,
        "capacity": ht.capacity,
        "load_factor": ht.load_factor,
        "insert_total_s": t1 - t0,
        "search_hit_avg_us": (t3 - t2) / trials * 1e6,
        "search_miss_avg_us": (t5 - t4) / trials * 1e6,
        "avg_chain_len": stats["avg_chain_len"],
        "max_chain_len": stats["max_chain_len"],
    }

def main():
    sizes = [1000, 2000, 5000, 8000, 10000]
    kinds = ["random", "sorted", "reversed", "repeated"]

    print("\n=== Quicksort Benchmark ===")
    results = bench_quicksort(sizes, kinds, trials=3, seed=42)
    print("distribution,n,det_s,rand_s,det/rand")
    for row in results:
        print(f"{row[0]},{row[1]},{row[2]:.6f},{row[3]:.6f},{row[4]:.3f}")

    print("\n=== Hash Table Benchmark ===")
    for n in [2000, 8000, 32000]:
        r = hash_experiment(n)
        print(r)

if __name__ == "__main__":
    main()
