# Product of Array Except Self — From Confused to Clear (My Learning Path)

> This is written for **past me** and **future students**: the exact points I tripped over, what clicked, and how to go from "I can multiply" → "I can solve this without division" confidently.

---

## Problem (what it *actually* asks)

Given:
- an integer array `nums` of length `n` (where `n > 1`)

Return an array `output` where:
- `output[i]` = product of all elements in `nums` **except** `nums[i]`

✅ Example: `nums = [1,2,3,4]`  
- For index 0: `2 × 3 × 4 = 24`
- For index 1: `1 × 3 × 4 = 12`
- For index 2: `1 × 2 × 4 = 8`
- For index 3: `1 × 2 × 3 = 6`

Answer: `[24, 12, 8, 6]`

### The tempting "easy" solution (that's banned):

> "Calculate total product, then divide by current element at each index."

**Problem says:** Solve it **without division**.

That forces you to think differently.

---

## Constraints

- `n >= 2` (at least 2 elements)
- `-30 <= nums[i] <= 30`
- Product of any prefix/suffix is guaranteed to fit in a 32-bit integer

---

## The Core Insight (the "click" moment)

For any index `i`, the product of everything except `nums[i]` is:

> **Everything to the LEFT of i** × **Everything to the RIGHT of i**

### Visual example:

```
nums = [4, 5, 1, 8, 2]
         ↑
       index 2

Left of index 2:  4 × 5 = 20
Right of index 2: 8 × 2 = 16

Product except self: 20 × 16 = 320
```

That's the whole algorithm.

---

## The Two-Pass Strategy

### Pass 1: Calculate all left products

Go **left to right**, accumulating products as you go.

For each index, store "product of everything before this index."

### Pass 2: Calculate all right products

Go **right to left**, accumulating products as you go.

For each index, store "product of everything after this index."

### Pass 3: Multiply them together

At each index: `output[i] = left[i] × right[i]`

---

# Approach A: Using Two Extra Arrays (clearest to understand)

This is the version that makes the logic crystal clear.

```python
def productExceptSelf_twoArrays(nums: list[int]) -> list[int]:
    n = len(nums)
    
    left = [0] * n
    right = [0] * n
    output = [0] * n
    
    # Build left products
    left[0] = 1  # nothing to the left of index 0
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]
    
    # Build right products
    right[n - 1] = 1  # nothing to the right of last index
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]
    
    # Combine
    for i in range(n):
        output[i] = left[i] * right[i]
    
    return output
```

### Step-by-step walkthrough

**Input:** `nums = [4, 5, 1, 8, 2]`

**After left pass:**
```
left = [1, 4, 20, 20, 160]
```
- `left[0] = 1` (nothing before)
- `left[1] = 1 × 4 = 4`
- `left[2] = 4 × 5 = 20`
- `left[3] = 20 × 1 = 20`
- `left[4] = 20 × 8 = 160`

**After right pass:**
```
right = [80, 16, 16, 2, 1]
```
- `right[4] = 1` (nothing after)
- `right[3] = 1 × 2 = 2`
- `right[2] = 2 × 8 = 16`
- `right[1] = 16 × 1 = 16`
- `right[0] = 16 × 5 = 80`

**Final output:**
```
output = [80, 64, 320, 40, 160]
```
- `output[0] = 1 × 80 = 80`
- `output[1] = 4 × 16 = 64`
- `output[2] = 20 × 16 = 320`
- etc.

---

## Where I stumbled initially

### 1) The loop ranges

```python
for i in range(1, n):  # starts at 1, not 0
```

Why? Because `left[0]` is already set to 1.

```python
for i in range(n - 2, -1, -1):  # ends at 0 (inclusive)
```

Reading `range(start, stop, step)` when `step = -1`:
- `n - 2` = second-to-last index
- `-1` = stop before reaching -1 (so includes index 0)

### 2) The multiplication logic

```python
left[i] = left[i - 1] * nums[i - 1]
```

This means:
> "The product to the left of `i` is the product to the left of `i-1`, multiplied by `nums[i-1]`."

In other words: **we're building up accumulated products**.

---

## Complexity

- **Time:** `O(n)` — three separate passes
- **Space:** `O(n)` — two extra arrays

### Follow-up challenge:

> "Can you do this in `O(1)` extra space?"

(The output array doesn't count.)

---

# Approach B: Optimized (Constant Extra Space)

Instead of storing both `left` and `right` arrays, we:

1. Store **left products** directly in `output`
2. Calculate **right products on-the-fly** using a single variable

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    output = [0] * n
    
    # Build left products into output
    output[0] = 1
    for i in range(1, n):
        output[i] = output[i - 1] * nums[i - 1]
    
    # Now output = [1, 4, 20, 20, 160] for nums = [4,5,1,8,2]
    
    # Build right products with a running variable
    R = 1  # running product from the right
    for i in range(n - 1, -1, -1):
        output[i] = output[i] * R  # multiply left by right
        R = R * nums[i]  # update running product
    
    return output
```

---

## The tricky part: the second loop

This is where I got confused.

### What's happening:

```python
R = 1
for i in range(n - 1, -1, -1):
    output[i] = output[i] * R
    R = R * nums[i]
```

Let's trace it for `nums = [4, 5, 1, 8, 2]`:

**Before second loop:** `output = [1, 4, 20, 20, 160]` (left products)

| `i` | `output[i]` before | `R` before | `output[i] = output[i] * R` | `R = R * nums[i]` | `R` after |
|-----|-------------------|------------|----------------------------|------------------|-----------|
| 4   | 160               | 1          | 160 × 1 = **160**          | 1 × 2 = 2        | 2         |
| 3   | 20                | 2          | 20 × 2 = **40**            | 2 × 8 = 16       | 16        |
| 2   | 20                | 16         | 20 × 16 = **320**          | 16 × 1 = 16      | 16        |
| 1   | 4                 | 16         | 4 × 16 = **64**            | 16 × 5 = 80      | 80        |
| 0   | 1                 | 80         | 1 × 80 = **80**            | (loop ends)      | —         |

**Final output:** `[80, 64, 320, 40, 160]` ✅

---

## Why this works

At each index `i`:
- `output[i]` already holds the **left product**
- `R` holds the **right product** (accumulated from previous iterations)
- Multiplying them gives the final answer

Then we update `R` to include `nums[i]` for the next iteration.

---

## The "aha" moment for me

The variable `R` is doing the same job as the entire `right[]` array, but:
- Instead of storing all values upfront
- We calculate them **just in time** as we loop

That's why it's `O(1)` space.

---

# Pitfalls I hit (so you don't)

### 1) Off-by-one errors in loop ranges

I kept writing:
```python
for i in range(n - 1, 0, -1):  # WRONG
```

This stops at `i = 1`, skipping `i = 0`.

Correct:
```python
for i in range(n - 1, -1, -1):  # includes i = 0
```

### 2) Updating `R` before multiplying

I tried:
```python
R = R * nums[i]
output[i] = output[i] * R  # WRONG ORDER
```

This uses the **new** `R` value, which includes `nums[i]`.

But we want the **old** `R` value (product of everything to the right).

### 3) Thinking I needed division

Early on, I kept trying:
```python
total_product = product_of_all_elements
output[i] = total_product / nums[i]
```

This fails when `nums[i] = 0` and doesn't match the problem's restriction anyway.

---

# Final Understanding Summary

✅ The answer at index `i` is: **left product × right product**  
✅ We can store left products in the output array directly  
✅ We can calculate right products on-the-fly with a running variable  
✅ The order of operations in the second loop matters:
   1. Multiply current `output[i]` by `R`
   2. Update `R` to include `nums[i]`

---

# The "final reassurance"

If you can:

- Understand why "left × right" gives the product except self
- Trace through one example by hand
- Remember the loop direction and range syntax

You understand this problem enough to solve it in an interview.

That's the whole game.