````md
# Top K Frequent Elements — From Confused to Clear (My Learning Path)

> This is written for **past me** and **future students**: the exact points I tripped over, what clicked, and how to go from “I can count” → “I can solve Top K” confidently.

---

## Problem (what it *actually* asks)

Given:
- an integer array `nums`
- an integer `k`

Return the **k most frequent elements** in `nums`.

✅ Example: `nums = [1,2,2,3,3,3], k = 2`  
Frequencies: `1→1, 2→2, 3→3`  
Answer: `[3, 2]` (order doesn’t matter)

### The confusing question I asked:
> “If nums=[7,5] and k=1, what happens?”

Answer: both have frequency 1 → there’s a tie.  
But the problem says: **“test cases are generated such that the answer is always unique”** → they won’t give you a tie case that makes multiple correct answers.

---

## Constraints (how to read them without pain)

- `1 <= nums.length <= 10^4`
  - length is at least 1, at most 10,000
- `-1000 <= nums[i] <= 1000`
  - numbers can be negative too
- `1 <= k <= number of distinct elements in nums`
  - k is always valid (you won’t get k bigger than unique values)

### Reading trick for `a <= x <= b`
Just read it as:
> “x is between a and b, inclusive.”

---

## The core plan (two steps)

Top K Frequent is always:

1. **Count** how often each number appears  
2. **Extract** the top `k` numbers from those counts

Step 1 is easy.
Step 2 is where all the choices are.

---

# Step 1 — Counting (frequency map)

### Why a dictionary instead of an array?
Because numbers can be negative and not dense.
A dict maps: `number → frequency`.

### The clean counting pattern

```python
from collections import defaultdict

freq = defaultdict(int)
for n in nums:
    freq[n] += 1
````

✅ `defaultdict(int)` starts missing keys at 0
So you don’t need `if key in dict`.

### My early mistake (important)

Don’t create `freq` *inside* the loop.
That resets it every iteration.

---

# Step 2 — Extract the Top K (3 main approaches)

You’ve counted. Now you decide:

## Approach A: Sort by frequency (simplest)

### Idea

* Convert dict to list of pairs `(num, count)`
* Sort by count descending
* Take first `k`

```python
from collections import defaultdict

def topKFrequent_sort(nums: list[int], k: int) -> list[int]:
    freq = defaultdict(int)
    for n in nums:
        freq[n] += 1

    sorted_items = sorted(freq.items(), key=lambda pair: pair[1], reverse=True)
    return [num for num, _count in sorted_items[:k]]
```

### Where I stumbled:

* I sorted **inside** the counting loop (wastes time)
* I didn’t understand what `lambda` was

#### What `lambda pair: pair[1]` means

It’s just a small function:

```python
def f(pair):
    return pair[1]
```

### Complexity

* Counting: `O(n)`
* Sorting distinct items: `O(d log d)`
* Total: `O(n + d log d)`
  (where `d` is number of distinct elements)

---

## Approach B: Min-Heap of size k (optimized + very common)

This is where I struggled the most, so I’m going to explain it in the same “tree → code collapse” way.

### The Key Heap Idea (the real “click”)

We don’t want to store everything.

We maintain a rule:

> **The heap never holds more than k elements.**

That means the heap is a **filter**:

* it keeps only the best `k` candidates
* throws away the rest early

### Python `heapq` facts

* `heapq` uses a **list** as the heap container
* the list is rearranged internally to maintain heap rules
* it’s always a **min-heap**
* heap levels can change as Python rebalances (normal)

---

## Heap Construction: why tuples?

This was a big confusion point.

### Does heapq “require” tuples?

No.

### What it requires:

* a list container
* elements that are comparable via `<`

### Why we use tuples anyway:

We need to store:

* `count` (priority)
* `num` (payload)

So we push:

```python
(count, num)
```

Why this works:

* Python compares tuples left-to-right
* so the heap prioritizes the **first item** (`count`)
* `num` is carried along

If we pushed `(num, count)` it would order by `num` (wrong).

---

## Min-Heap Algorithm (the actual loop)

```python
import heapq
from collections import defaultdict

def topKFrequent_heap(nums: list[int], k: int) -> list[int]:
    freq = defaultdict(int)
    for n in nums:
        freq[n] += 1

    heap: list[tuple[int, int]] = []  # (count, num)

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)  # removes smallest count (worst candidate)

    return [num for _count, num in heap]
```

---

## The two lines that confused me

### 1) The condition

```python
if len(heap) > k:
    heapq.heappop(heap)
```

Meaning:

* After pushing a new candidate, heap might have `k+1` elements
* We must remove **one**
* Since it’s a min-heap, popping removes the **smallest frequency**
* That’s the “worst among our kept candidates”

🔒 After this runs, the heap size returns to `k`.
So at the end of the loop, the heap contains **exactly k winners**.

### 2) The return line

```python
return [num for _count, num in heap]
```

This is a list comprehension.

Read it literally:

> “For each `(count, num)` in heap, collect `num` into a list.”

`_count` is not magic — it’s just a variable name meaning:

> “I’m ignoring this value on purpose.”

Equivalent long version:

```python
result = []
for count, num in heap:
    result.append(num)
return result
```

---

## Common “WTF” moment: `.items()`

### What does `freq.items()` return?

It returns an iterable of `(key, value)` tuples:

```python
for num, count in freq.items():
    ...
```

Each iteration:

* `num` = key
* `count` = value

### Is it sorted?

No.
Dicts preserve insertion order in modern Python, but **not sorted by frequency**.
The heap handles ordering for you.

---

## Complexity (why heap is “optimized”)

* Counting: `O(n)`
* Heap ops: pushing `d` items, each `O(log k)`
* Total: `O(n + d log k)`

Better than sorting when:

* `k` is small
* `d` is large

---

## Approach C: Bucket Sort (fastest big-O, more complex)

This exists because counts range from `1..n`.

```python
from collections import defaultdict

def topKFrequent_bucket(nums: list[int], k: int) -> list[int]:
    freq = defaultdict(int)
    for n in nums:
        freq[n] += 1

    buckets = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    res = []
    for count in range(len(buckets) - 1, 0, -1):
        for num in buckets[count]:
            res.append(num)
            if len(res) == k:
                return res
```

* Time: `O(n)`
* Space: `O(n)`

---

# How to choose the approach (decision rule)

### Use sorting if:

* you want the simplest, clearest solution
* performance is fine

### Use heap if:

* problem says **Top K**
* `k` is small compared to distinct values
* you want an interview-strong optimization

### Use buckets if:

* you want linear time and don’t mind extra memory / complexity

---

# The “final understanding” summary

✅ We count with a dict because keys can be anything and values are counts.
✅ We extract Top K using either sorting or a min-heap.
✅ A heap in Python is a list managed by `heapq`.
✅ We store tuples `(count, num)` because the heap compares the first value.
✅ The `len(heap) > k` pop keeps only the best `k` candidates.
✅ The return comprehension extracts only the `num` from each tuple.

---

# Pitfalls I hit (so you don’t)

* Creating the dict inside the loop (resets counts)
* Sorting inside the counting loop (wastes time)
* Thinking `.items()` is sorted (it’s not)
* Confusing “heap is a tree” with “tree structure matters”

  * heap levels can change; only the heap property matters
* Not understanding `_count`

  * it’s just “unused variable”

---

# Final reassurance

If you can:

* build `freq`
* understand why `(count, num)` is pushed
* understand why we pop when size exceeds `k`

You understand heaps enough to solve **Top K** problems repeatedly.

That’s the whole game.

```

If you want, paste your current `top-k-frequent-elements.md` and I’ll align this markdown to match your repo style exactly (headings, spacing, links to `notes/heaps.md`, etc.).
```
