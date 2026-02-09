# Hash Table with Chaining & Universal Hashing & Dynamic Resizing

from __future__ import annotations
import random
from typing import Any, List, Optional, Tuple

class HashTableChaining:
    def __init__(self, capacity: int = 8, max_load: float = 0.75, min_load: float = 0.15):
        self._m = max(8, self._next_pow2(capacity))
        self._n = 0
        self._max_load = max_load
        self._min_load = min_load
        self._table: List[List[Tuple[Any, Any]]] = [[] for _ in range(self._m)]

        # Universal hash parameters
        self._p = 2_147_483_647  # prime
        rng = random.Random(12345)
        self._a = rng.randrange(1, self._p)
        self._b = rng.randrange(0, self._p)

    def _next_pow2(self, x: int) -> int:
        p = 1
        while p < x:
            p *= 2
        return p

    def _key_to_int(self, key: Any) -> int:
        # Converting key -> int
        if isinstance(key, int):
            return key & 0x7fffffff

        data = (key if isinstance(key, bytes) else str(key).encode("utf-8"))
        h = 0
        for b in data:
            h = (h * 257 + b) & 0x7fffffff
        return h

    def _hash(self, key: Any) -> int:
        x = self._key_to_int(key)
        return ((self._a * x + self._b) % self._p) % self._m

    @property
    def size(self) -> int:
        return self._n

    @property
    def capacity(self) -> int:
        return self._m

    @property
    def load_factor(self) -> float:
        return self._n / self._m

    def _resize(self, new_capacity: int) -> None:
        old_items: List[Tuple[Any, Any]] = []
        for bucket in self._table:
            old_items.extend(bucket)

        self._m = self._next_pow2(new_capacity)
        self._table = [[] for _ in range(self._m)]
        self._n = 0

        for k, v in old_items:
            self.insert(k, v)

    def insert(self, key: Any, value: Any) -> None:
        idx = self._hash(key)
        bucket = self._table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._n += 1

        if self.load_factor > self._max_load:
            self._resize(self._m * 2)

    def search(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        for k, v in self._table[idx]:
            if k == key:
                return v
        return None

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        bucket = self._table[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._n -= 1
                if self._m > 8 and self.load_factor < self._min_load:
                    self._resize(self._m // 2)
                return True
        return False

    def bucket_stats(self) -> dict:
        lens = [len(b) for b in self._table]
        return {
            "avg_chain_len": sum(lens) / len(lens),
            "max_chain_len": max(lens),
            "nonempty_buckets": sum(1 for x in lens if x > 0),
        }

if __name__ == "__main__":
    ht = HashTableChaining()
    ht.insert("apple", 10)
    ht.insert("banana", 20)
    print("apple ->", ht.search("apple"))
    print("delete apple:", ht.delete("apple"))
    print("apple ->", ht.search("apple"))
    print("stats:", ht.bucket_stats())
