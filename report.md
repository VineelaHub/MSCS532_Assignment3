# Assignment 3 - Understanding Algorithm Efficiency and Scalability
---

## Part 1: Randomized Quicksort Analysis

### 1. Implementation
I implemented **two in-place Quicksort variants**:

1) **Deterministic Quicksort**: pivot is always the first element of the subarray.  
2) **Randomized Quicksort**: pivot is chosen uniformly at random from the current subarray.

To handle common edge cases efficiently, my partition logic uses a 3-way partition:
- elements `< pivot`
- elements `== pivot`
- elements `> pivot`

This is helpful when the input contains many repeated values, because duplicates do not keep getting pushed into recursive calls.

To avoid Python recursion-depth issues, I used an explicit stack and I always process the smaller side first to keep the stack small.

**Edge cases handled**
- Empty list: returns immediately  
- Already sorted / reverse sorted: deterministic version degrades (as expected), randomized stays near \(O(n \log n)\)  
- Repeated elements: 3-way partition reduces wasted work  

---

### 2. Analysis

Let the input size be \(n\). Randomized Quicksort picks the pivot uniformly from the subarray, so every element is equally likely to be the pivot.

A clean way to show expected \(O(n \log n)\) is with indicator random variables on comparisons.

#### Key idea
Quicksort’s running time is dominated by the number of comparisons.

Consider two distinct elements \(x_i\) and \(x_j\) (assume \(i < j\) in sorted order).  
They get compared at most once during the algorithm, and they are compared only if one of them becomes the first pivot chosen from the set \(\{x_i, x_{i+1}, \dots, x_j\}\).

Define an indicator variable:

\[
X_{ij} =
\begin{cases}
1 & \text{if } x_i \text{ and } x_j \text{ are compared} \\
0 & \text{otherwise}
\end{cases}
\]

Then the total number of comparisons is:

\[
X = \sum_{i<j} X_{ij}
\]

So the expected number of comparisons is:

\[
\mathbb{E}[X] = \sum_{i<j} \mathbb{E}[X_{ij}] = \sum_{i<j} \Pr(X_{ij}=1)
\]

#### Probability that \(x_i\) and \(x_j\) are compared
They are compared iff the first pivot chosen from the range \(\{x_i, \dots, x_j\}\) is either \(x_i\) or \(x_j\).  
There are \((j - i + 1)\) elements in that range, and the pivot is uniform.

\[
\Pr(X_{ij} = 1) = \frac{2}{j - i + 1}
\]

So:

\[
\mathbb{E}[X] = \sum_{i<j} \frac{2}{j - i + 1}
\]

We can rewrite by grouping on distance \(k = j - i\):

\[
\mathbb{E}[X] = \sum_{k=1}^{n-1} \sum_{i=1}^{n-k} \frac{2}{k+1}
= \sum_{k=1}^{n-1} (n-k)\frac{2}{k+1}
\]

This is bounded by a constant times:

\[
n \sum_{k=1}^{n-1}\frac{1}{k} = n \cdot H_{n} = O(n\log n)
\]

So the expected comparisons is \(O(n\log n)\), and therefore the average running time is:

\[
\boxed{\mathbb{E}[T(n)] = O(n\log n)}
\]

---

### 3. Empirical Comparison

#### Method
I compared the runtime in seconds for:
- Random arrays
- Sorted arrays
- Reverse-sorted arrays
- Arrays with repeated elements

I measured time using `time.perf_counter()` and averaged across multiple trials.

> Note: results depend on hardware and Python runtime, but the trend is what matters.

---

#### Runtime Comparison of Quicksort Variants

**Table 1**  
*Mean runtime (seconds) for Deterministic vs Randomized Quicksort across input types and sizes.*

| Input distribution | n     | Deterministic QS (s) | Randomized QS (s) | Det/Rand time ratio |
|---|---:|---:|---:|---:|
| random   | 1000  | 0.001782 | 0.002403 | 0.742 |
| random   | 2000  | 0.004351 | 0.004505 | 0.966 |
| random   | 5000  | 0.007703 | 0.009813 | 0.785 |
| random   | 8000  | 0.017660 | 0.013858 | 1.274 |
| random   | 10000 | 0.013948 | 0.027577 | 0.506 |
| sorted   | 1000  | 0.003844 | 0.001182 | 3.253 |
| sorted   | 2000  | 0.007035 | 0.002722 | 2.585 |
| sorted   | 5000  | 0.056939 | 0.008792 | 6.476 |
| sorted   | 8000  | 0.068047 | 0.013730 | 4.956 |
| sorted   | 10000 | 0.072400 | 0.028965 | 2.500 |
| reversed | 1000  | 0.037852 | 0.001225 | 30.906 |
| reversed | 2000  | 0.152257 | 0.002648 | 57.497 |
| reversed | 5000  | 0.999545 | 0.008593 | 116.319 |
| reversed | 8000  | 2.559995 | 0.013075 | 195.789 |
| reversed | 10000 | 4.054403 | 0.015774 | 257.028 |
| repeated | 1000  | 0.000425 | 0.000498 | 0.853 |
| repeated | 2000  | 0.000885 | 0.000900 | 0.984 |
| repeated | 5000  | 0.002034 | 0.002206 | 0.922 |
| repeated | 8000  | 0.003465 | 0.003760 | 0.922 |
| repeated | 10000 | 0.004464 | 0.004228 | 1.056 |

---

#### Observations
- **Random arrays:** both versions are generally near \(O(n\log n)\). Random pivot adds slight overhead, so it is not always faster on random data.
- **Sorted arrays:** deterministic pivot (first element) is consistently slower because partitions become highly unbalanced.
- **Reverse-sorted arrays:** deterministic Quicksort becomes extremely slow (worst-case behavior). Randomized Quicksort stays fast because it avoids consistently bad pivots.
- **Repeated values:** 3-way partition helps a lot for both; performance is stable and close.

#### Why the results match theory
- Deterministic first-pivot Quicksort has a well-known \(O(n^2)\) worst case on sorted/reversed inputs due to unbalanced partitions.
- Randomization makes it very unlikely to repeatedly pick extreme pivots, so the expected recursion depth stays near \(\log n\), leading to \(O(n\log n)\) expected time.

#### Small discrepancies
- Sometimes deterministic wins on random, because random number generation costs time.
- Python overhead (function calls, list operations) can hide small theoretical differences when \(n\) is not huge.

---

## Part 2: Hashing with Chaining

### 1. Implementation
I implemented a hash table with chaining using a Python list of buckets, where each bucket is a list of `(key, value)` pairs.

Supported operations:
- **Insert(key, value)**: adds or updates a key-value pair
- **Search(key)**: returns value or `None`
- **Delete(key)**: removes key if present and returns True/False

To reduce collisions, I used a universal hashing style function:

\[
h(k) = ((a \cdot k + b) \bmod p) \bmod m
\]

- \(p\) is a large prime
- \(a\) is chosen from \(\{1, \dots, p-1\}\)
- \(b\) is chosen from \(\{0, \dots, p-1\}\)
- \(m\) is the table size

For non-integer keys (like strings), I convert the key into a stable integer using a simple polynomial rolling method.

I also implemented dynamic resizing:
- If load factor \( \alpha > 0.75 \): resize up (double capacity)
- If load factor \( \alpha < 0.15 \): resize down (halve capacity, but not below a minimum)

---

### 2. Analysis

Let:
- \(n\) = number of stored elements
- \(m\) = number of buckets (slots)
- \(\alpha = \frac{n}{m}\) = load factor

Under simple uniform hashing, each key is equally likely to hash into any bucket, so the expected chain length is about \(\alpha\).

#### Expected times
- **Search (successful):** expected \(O(1 + \alpha)\)
- **Search (unsuccessful):** expected \(O(1 + \alpha)\)
- **Insert:** expected \(O(1 + \alpha)\) (find spot/update + append)
- **Delete:** expected \(O(1 + \alpha)\)

So if \(\alpha\) is kept bounded (like \(\le 0.75\)), operations stay expected constant time.

---

### Load factor impact
- As \(\alpha\) increases, average chain length grows, so each operation scans more elements.
- If \(\alpha\) becomes large (say 5, 10, 20...), chaining still works, but performance starts to feel linear in \(\alpha\).

---

### Strategy to maintain low load factor
My solution uses dynamic resizing:
- When \(\alpha\) exceeds a threshold, allocate a larger table and rehash everything.
- Resizing is expensive in that moment, but amortized over many inserts, the expected per-insert cost stays near constant.

---

### Empirical sanity check
In my test run, the load factor stayed ~0.49 due to resizing, and average search time stayed around microseconds even as \(n\) increased.

**Table 2**  
*Hash table performance under resizing (chaining & universal hash).*

| n     | capacity | load factor | avg chain len | max chain len | avg search hit (µs) | avg search miss (µs) |
|---:|---:|---:|---:|---:|---:|---:|
| 2000  | 4096  | 0.488 | 0.488 | 5 | 0.416 | 0.702 |
| 8000  | 16384 | 0.488 | 0.488 | 6 | 0.845 | 0.675 |
| 32000 | 65536 | 0.488 | 0.488 | 6 | 0.934 | 0.716 |

---

## Conclusion

### Randomized Quicksort
**Advantages**
- Random pivot selection prevents consistent bad splits
- 3-way partition makes repeated elements efficient
- Iterative stack avoids recursion-depth failures

**Disadvantages**
- Deterministic first pivot is fragile on sorted/reversed inputs
- Random pivot adds small overhead (RNG cost), so not always fastest on already-random data

### Hashing with Chaining
**Advantages**
- Keeping load factor bounded using resizing keeps operations near constant time
- Universal hashing reduces collision patterns (more even distribution)

**Disadvantages**
- Allowing load factor to grow unchecked increases chain length and slows operations
- Poor hash functions can create clustering even with chaining

---

## Files included in repo
- `quicksort.py`
- `hashtable.py`
- `comparision.py`
- `README.md`
- `REPORT.md`
