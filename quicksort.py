# Randomized Quicksort vs Deterministic Quicksort (first-element pivot)
# In-place, iterative, 3-way partition to handle duplicates efficiently.

from __future__ import annotations
import random
from typing import List, MutableSequence, TypeVar

T = TypeVar("T")

def _is_sorted(a: List[T]) -> bool:
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))

def deterministic_quicksort(a: MutableSequence[T]) -> MutableSequence[T]:
    """
    Deterministic in-place quicksort using the first element as the pivot.
    Uses 3-way partition and an explicit stack to avoid recursion depth issues.
    """
    n = len(a)
    if n < 2:
        return a

    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            pivot = a[lo]

            # 3-way partition: < pivot | == pivot | > pivot
            lt, i, gt = lo, lo + 1, hi
            while i <= gt:
                ai = a[i]
                if ai < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif ai > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1

            left = (lo, lt - 1)
            right = (gt + 1, hi)

            # Processing smaller side first to keep stack small
            if (left[1] - left[0]) < (right[1] - right[0]):
                if right[0] < right[1]:
                    stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                lo, hi = right

    return a

def randomized_quicksort(a: MutableSequence[T], rng: random.Random | None = None) -> MutableSequence[T]:
    """
    Randomized in-place quicksort choosing pivot uniformly at random from subarray.
    Uses 3-way partition and an explicit stack to avoid recursion depth issues.
    """
    if rng is None:
        rng = random.Random()

    n = len(a)
    if n < 2:
        return a

    stack = [(0, n - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            p = rng.randint(lo, hi)
            a[lo], a[p] = a[p], a[lo]
            pivot = a[lo]

            lt, i, gt = lo, lo + 1, hi
            while i <= gt:
                ai = a[i]
                if ai < pivot:
                    a[lt], a[i] = a[i], a[lt]
                    lt += 1
                    i += 1
                elif ai > pivot:
                    a[i], a[gt] = a[gt], a[i]
                    gt -= 1
                else:
                    i += 1

            left = (lo, lt - 1)
            right = (gt + 1, hi)

            if (left[1] - left[0]) < (right[1] - right[0]):
                if right[0] < right[1]:
                    stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                lo, hi = right

    return a

if __name__ == "__main__":
    data = [3, 1, 2, 5, 4, 3, 3]
    d1 = data.copy()
    d2 = data.copy()

    deterministic_quicksort(d1)
    randomized_quicksort(d2, random.Random(42))

    print("Deterministic:", d1)
    print("Randomized:   ", d2)
    print("Sorted OK:", _is_sorted(d1) and _is_sorted(d2))
