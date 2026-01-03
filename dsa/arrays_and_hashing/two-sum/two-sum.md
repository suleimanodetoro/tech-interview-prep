# Two Sum — Logic, Intuition, and Implementations

This repository explores multiple solutions to the classic **Two Sum** problem, starting from intuition and building toward optimal approaches.

---

## Problem Statement

Given an integer array `nums` and an integer `target`, return **indices** of the two numbers such that:

```
nums[i] + nums[j] == target
```

Constraints:

* Each input has **exactly one solution**
* You **may not use the same element twice**
* Indices can be returned in any order

---

## Core Insight (The Key Idea)

Instead of checking **every possible pair** (which is slow), we can ask a better question:

> “For the current number, what value would I need to see elsewhere to reach the target?”

Mathematically:

```
needed = target - current
```

If we can remember values we’ve already seen (or values we are waiting for), we can solve the problem in **one pass**.

This leads directly to using a **hash map (dictionary)**.

---

## 1. One-Pass Remainder Map (Your Core Logic)

### Intuition

As we scan the array from left to right:

* For each number `num`
* Compute what value would complete the sum:

  ```
  remainder = target - num
  ```
* Store that remainder in a map **with the index of `num`**
* If we later see a number that exists in the map, we’re done

The map answers the question:

> “Have I already seen a number that pairs with this one?”

### Why it works

At any index `i`:

* Either `nums[i]` completes a previous number
* Or it becomes a number that needs a future partner

You never need to look backward more than one step.

### Complexity

* Time: **O(n)**
* Space: **O(n)**

---

## 2. Popular One-Pass Hash Map (Same Idea, Flipped)

### Difference from your version

Instead of storing:

```
needed value → index
```

This version stores:

```
seen value → index
```

Then for each number:

* Compute `diff = target - num`
* Check if `diff` has already been seen

### Important note

This is **not a different algorithm** — it’s the same logic expressed from the opposite direction.

Both rely on:

```
num + diff == target
```

### Why this version is common

* Reads naturally: “have I seen the complement?”
* Often preferred in interviews
* Slightly easier to explain verbally

### Complexity

* Time: **O(n)**
* Space: **O(n)**

---

## 3. Two-Pass Hash Map

### Intuition

Break the problem into two steps:

1. First pass: store every value with its index
2. Second pass: for each value, check if its complement exists somewhere else

Extra care is taken to ensure we don’t reuse the same index.

### Why include this

* Easier to understand conceptually
* Good stepping stone before the one-pass solution
* Useful for learning, less optimal in practice

### Complexity

* Time: **O(n)**
* Space: **O(n)**

---

## 4. Sorting + Two Pointers

### Intuition

If the array were sorted:

* Start with the smallest and largest values
* Move pointers inward based on whether the sum is too small or too large

Since sorting destroys indices, we:

* Pair each value with its original index
* Sort those pairs by value

### When this is useful

* Learning the two-pointer pattern
* When hashing is unavailable
* When asked specifically about pointer techniques

### Tradeoff

Sorting costs extra time.

### Complexity

* Time: **O(n log n)**
* Space: **O(n)**

---

## 5. Brute Force (Baseline)

### Intuition

Check every possible pair:

```
nums[i] + nums[j]
```

### Why include it

* Conceptually simple
* Good for verifying correctness
* Shows why better solutions matter

### Complexity

* Time: **O(n²)**
* Space: **O(1)**

---

## Final Comparison

| Approach               | Time       | Space | Notes               |
| ---------------------- | ---------- | ----- | ------------------- |
| Brute Force            | O(n²)      | O(1)  | Simple, slow        |
| Hash Map (1-pass)      | O(n)       | O(n)  | Optimal, preferred  |
| Hash Map (2-pass)      | O(n)       | O(n)  | Educational         |
| Sorting + Two Pointers | O(n log n) | O(n)  | Alternative pattern |

---

## Key Takeaway

The heart of Two Sum is this realization:

> “Every number defines what it needs to succeed.”

Once you understand that, the optimal solution becomes natural — not memorized.

This repository shows that idea from multiple angles so the concept sticks, not just the code.

