# Top K Frequent Elements (Medium)

## Problem
Given an integer array `nums` and an integer `k`, return the **k most frequent** elements.

- The answer is guaranteed to be **unique**.
- You may return the output in **any order**.

### Example 1
Input: `nums = [1,2,2,3,3,3]`, `k = 2`  
Output: `[2,3]` (or `[3,2]`)

### Example 2
Input: `nums = [7,7]`, `k = 1`  
Output: `[7]`

### Constraints
- `1 <= nums.length <= 10^4`
- `-1000 <= nums[i] <= 1000`
- `1 <= k <= number of distinct elements in nums`

---

## Related Notes (recommended read)
- **Heaps (Tree → Code)**: [notes/heaps.md](../../../notes/heaps.md)

---

## Key Idea
This problem is two steps:

1) Build a frequency map: `number -> count`  
2) Extract the **top k** numbers based on that count

The only real decision is *how* we extract the top-k:
- Sort everything (simple)
- Min-heap of size k (optimized when k is small)

---

## Step 1: Frequency Map
Use a hash map / dictionary to count occurrences:

```python
from collections import defaultdict

freq = defaultdict(int)
for n in nums:
    freq[n] += 1
````

✅ `freq.items()` returns `(num, count)` pairs.
❌ It is **not** sorted by frequency. Dictionary iteration order is insertion order, not “highest count”.

---

## Approach 1: Sort by Frequency (Simple + readable)

### How it works

* Count all frequencies
* Sort `(num, count)` pairs by `count` descending
* Take the first `k`

### Python

```python
sorted_items = sorted(freq.items(), key=lambda pair: pair[1], reverse=True)
answer = [num for num, count in sorted_items[:k]]
```

### Complexity

Let:

* `n` = length of `nums`

* `d` = number of distinct elements

* Time: `O(n + d log d)`

* Space: `O(d)`

### When to use

* Great as a first solution
* Great when `d` is small enough
* Very easy to reason about in interviews

---

## Approach 2: Min-Heap of Size k (Optimized Top-K)

### Why a min-heap?

We want the **top k** most frequent, but we keep a **min-heap** so we can quickly remove the *worst* among our current top-k.

**Heap invariant:**

> The heap contains at most `k` elements.
> The root is the **smallest frequency** among those kept elements.

### How it works

1. Count frequencies
2. Push `(count, num)` into a min-heap
3. If heap grows larger than `k`, pop once (removes smallest count)
4. At the end, the heap contains exactly the top-k elements

### Important heap note (reassurance)

Python will **reorder internally** to maintain the heap property.

* Heap “levels” can change when inserting/removing
* That’s normal
* Only the heap property matters (root is smallest)

### Python

```python
import heapq

heap = []  # (count, num)

for num, count in freq.items():
    heapq.heappush(heap, (count, num))
    if len(heap) > k:
        heapq.heappop(heap)  # removes smallest frequency
```

Return values:

```python
answer = [num for count, num in heap]
```

### Complexity

* Time: `O(n + d log k)`
* Space: `O(d)` for the freq map + `O(k)` for the heap

### When to use

* Best when `k` is much smaller than `d`
* Common “Top K” pattern

---

## Walkthrough (Heap) on Example 1

`nums = [1,2,2,3,3,3]`, `k = 2`

Frequency:

* `1:1, 2:2, 3:3`

Heap process (store `(count,num)`):

* push (1,1) → heap = [(1,1)]
* push (2,2) → heap = [(1,1),(2,2)]
* push (3,3) → heap = [(1,1),(2,2),(3,3)] → too big → pop → removes (1,1)
  End heap contains: (2,2), (3,3) → answer `[2,3]`

---

## Common Mistakes / Gotchas

* Sorting inside the counting loop (wastes time)
* Assuming `freq.items()` is sorted (it isn’t)
* Thinking a heap is a “sorted structure” (it is not; only the root is guaranteed)
* Confusing **min-heap** vs **max-heap** in Python (`heapq` is min-heap)

---

## Final Takeaways

* Always start with the frequency map.
* If you want simplest: **sort by frequency**.
* If you want optimized top-k: **min-heap capped at k**.
* Heap levels can change — Python rebalances automatically.

```
