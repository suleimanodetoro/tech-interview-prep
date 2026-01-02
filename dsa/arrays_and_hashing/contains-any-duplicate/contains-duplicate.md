# Contains Duplicate

**Difficulty:** Easy  
**Topic:** Arrays, Hash Table  
**Date Solved:** January 1, 2026  
**LeetCode:** [Problem #217](https://leetcode.com/problems/contains-duplicate/)

---

## Problem Statement

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

### Examples

**Example 1:**
```
Input: nums = [1, 2, 3, 1]
Output: true
Explanation: The value 1 appears at indices 0 and 3
```

**Example 2:**
```
Input: nums = [1, 2, 3, 4]
Output: false
Explanation: All elements are unique
```

**Example 3:**
```
Input: nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
Output: true
Explanation: Multiple values appear more than once
```

### Constraints
- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## Initial Thought Process

When I first encountered this problem, I asked myself:

1. **What am I looking for?** Any two elements that are equal.
2. **What's the simplest approach?** Compare every element with every other element.
3. **Can I do better?** Yes, by using additional data structures or preprocessing.

The key insight is recognizing this as a **lookup problem** - we need to quickly check if we've "seen" a number before.

---

## Solution 1: Brute Force (Nested Loops)

### Intuition
The most straightforward approach: compare each element with every element that comes after it. If we find any match, we've found a duplicate.

### Why This Works
- For each position `i`, we check all positions `j` where `j > i`
- We use `j = i + 1` to avoid comparing an element with itself
- This ensures we check every unique pair exactly once
- As soon as we find a match, we can return `true` immediately

### Code
```python
from typing import List

def hasDuplicate(nums: List[int]) -> bool:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):  # Start from i+1 to skip self-comparison
            if nums[i] == nums[j]:
                return True
    return False
```

### How It Works (Walkthrough)

For `nums = [1, 2, 3, 3]`:
```
i=0 (nums[0]=1): Compare with j=1,2,3 → 1 vs [2,3,3] → No match
i=1 (nums[1]=2): Compare with j=2,3   → 2 vs [3,3]   → No match
i=2 (nums[2]=3): Compare with j=3     → 3 vs [3]     → MATCH! Return True
```

### Complexity Analysis

**Time Complexity: O(n²)**
- Outer loop runs `n` times
- Inner loop runs `(n-1) + (n-2) + ... + 1` times
- Total comparisons: `n(n-1)/2` which simplifies to O(n²)

**Space Complexity: O(1)**
- Only using two variables `i` and `j`
- No extra data structures

### Pros and Cons

✅ **Pros:**
- Very simple to understand and implement
- No extra memory needed
- Works for any input size

❌ **Cons:**
- Extremely slow for large arrays (10^5 elements = 5 billion comparisons!)
- Not practical for real-world use
- Better as a baseline to understand the problem

---

## Solution 2: Sorting First

### Intuition
If we sort the array first, any duplicate values will end up next to each other. Then we only need to check adjacent elements instead of all pairs.

### Why This Works
- Sorting groups identical values together
- After sorting `[3, 1, 2, 3]` becomes `[1, 2, 3, 3]`
- Now duplicates are adjacent, so one pass through is enough
- Compare `nums[i]` with `nums[i+1]` for all valid indices

### Code
```python
from typing import List

def hasDuplicateSort(nums: List[int]) -> bool:
    nums.sort()  # Sort the array in-place
    
    for i in range(len(nums) - 1):  # Stop at len-1 to avoid index error
        if nums[i] == nums[i + 1]:
            return True
    
    return False
```

### How It Works (Walkthrough)

For `nums = [3, 1, 2, 3]`:
```
Step 1: Sort → [1, 2, 3, 3]
Step 2: Check adjacent pairs:
  i=0: nums[0] vs nums[1] → 1 vs 2 → No match
  i=1: nums[1] vs nums[2] → 2 vs 3 → No match
  i=2: nums[2] vs nums[3] → 3 vs 3 → MATCH! Return True
```

### Complexity Analysis

**Time Complexity: O(n log n)**
- Sorting takes O(n log n) using efficient algorithms like mergesort or timsort
- Single pass through array takes O(n)
- Overall: O(n log n) + O(n) = O(n log n)

**Space Complexity: O(1) or O(n)**
- O(1) if we modify the input array in place
- O(n) if the sorting algorithm requires extra space (depends on implementation)
- Most Python sorting uses Timsort which may use O(n) extra space

### Pros and Cons

✅ **Pros:**
- Much faster than brute force for large inputs
- Can be done in-place to save memory
- Good middle-ground solution

❌ **Cons:**
- Slower than hash set approach (O(n log n) vs O(n))
- Modifies the input array (unless we make a copy)
- Still not optimal for very large datasets

### When to Use This
- When space is extremely limited
- When the input can be modified
- When the array is already sorted or nearly sorted

---

## Solution 3: Hash Set (Optimal)

### Intuition
As we iterate through the array, we keep track of numbers we've "seen" before. If we encounter a number already in our "seen" set, we've found a duplicate.

### Why This Works
- A hash set provides O(1) average lookup time
- For each number, we check: "Have I seen this before?"
- If yes → duplicate found!
- If no → add it to the set and continue
- This is the classic "tracking seen elements" pattern

### Code
```python
from typing import List

def hasDuplicateHashSet(nums: List[int]) -> bool:
    seen = set()
    
    for num in nums:
        if num in seen:  # O(1) lookup
            return True
        seen.add(num)     # O(1) insertion
    
    return False
```

### How It Works (Walkthrough)

For `nums = [1, 2, 3, 3]`:
```
num=1: Check seen={} → Not found → Add → seen={1}
num=2: Check seen={1} → Not found → Add → seen={1,2}
num=3: Check seen={1,2} → Not found → Add → seen={1,2,3}
num=3: Check seen={1,2,3} → FOUND! Return True
```

For `nums = [1, 2, 3, 4]`:
```
num=1: seen={} → Add → seen={1}
num=2: seen={1} → Add → seen={1,2}
num=3: seen={1,2} → Add → seen={1,2,3}
num=4: seen={1,2,3} → Add → seen={1,2,3,4}
End of loop → No duplicates found → Return False
```

### Complexity Analysis

**Time Complexity: O(n)**
- Single pass through the array: O(n)
- Each set operation (lookup and insert) is O(1) average case
- Overall: O(n) × O(1) = O(n)

**Space Complexity: O(n)**
- In the worst case (no duplicates), we store all `n` elements in the set
- Best case (duplicate found early): O(k) where k < n

### Pros and Cons

✅ **Pros:**
- **Fastest solution** - linear time complexity
- Returns immediately when duplicate found (early exit)
- Clean and Pythonic code
- This is the expected solution in interviews

❌ **Cons:**
- Uses extra memory proportional to input size
- Not suitable if memory is severely constrained

### When to Use This
- **Almost always!** This is the standard solution
- When you need the best time complexity
- When space complexity of O(n) is acceptable (which it usually is)

---

## Python One-Liner Bonus

```python
def hasDuplicateOneLiner(nums: List[int]) -> bool:
    return len(nums) != len(set(nums))
```

**How it works:**
- `set(nums)` removes all duplicates
- If lengths differ, duplicates existed

**Pros:** Concise and readable  
**Cons:** Always processes entire array, even if duplicate is at index 0 and 1

---

## Comparison of All Solutions

| Approach | Time | Space | When to Use |
|----------|------|-------|-------------|
| **Brute Force** | O(n²) | O(1) | Learning/understanding only |
| **Sorting** | O(n log n) | O(1)* | Space-constrained environments |
| **Hash Set** | O(n) | O(n) | Default choice (best performance) |
| **One-liner** | O(n) | O(n) | Code golf, but less efficient in practice |

*O(n) if sorting algorithm needs extra space

---

## Key Takeaways & Patterns

### The "Seen Elements" Pattern
This problem demonstrates a fundamental pattern in DSA:
- **Use a hash set when you need to track "have I seen this before?"**
- Common in problems like: Two Sum, Longest Substring, Valid Anagram

### Trade-offs Understanding
1. **Time vs Space:** Hash set trades space for speed
2. **Early Exit:** Hash set can return immediately; one-liner cannot
3. **Input Modification:** Sorting changes the array; hash set doesn't

### Interview Tips
- Start with brute force to show you understand the problem
- Then immediately suggest the hash set optimization
- Discuss trade-offs if asked
- Mention sorting approach as an alternative for space-constrained scenarios

---

## Common Mistakes I Made

1. **Forgot `i + 1` in brute force:** Used `range(len(nums))` instead of `range(i + 1, len(nums))`, causing elements to compare with themselves
2. **Off-by-one error in sorting:** Used `range(len(nums))` instead of `range(len(nums) - 1)`, causing index out of bounds
3. **Didn't consider early exit:** First wrote one-liner without realizing hash set approach is more efficient for early duplicates

---

## Related Problems

Once you understand this pattern, try these:
- **Two Sum** - Uses hash map to track complements
- **Valid Anagram** - Frequency counting with hash map
- **Longest Substring Without Repeating Characters** - Sliding window with set
- **First Unique Character** - Hash map for frequency

---

## Follow-Up Questions

**Q: What if we could only use O(1) extra space?**  
A: Use the sorting approach (modifying input in-place)

**Q: What if the numbers are in a limited range (e.g., 1-100)?**  
A: Could use a boolean array of size 100 instead of a set

**Q: What if we need to find ALL duplicates, not just detect if they exist?**  
A: Use a hash map to count frequencies: `{num: count}`

**Q: Can this be solved in-place without modifying the input?**  
A: Not in O(n) time with O(1) space - you need either extra space or more time

---

## Test Cases to Consider

```python
# Edge cases
[1]                    # Single element → False
[1, 1]                 # Smallest duplicate → True
[]                     # Empty (not in constraints, but good to think about)

# Normal cases
[1, 2, 3, 4]          # No duplicates → False
[1, 2, 3, 1]          # Duplicate at start and end → True
[1, 1, 1, 1]          # All same → True

# Large numbers
[1000000, 1000000]    # Large values → True
[-1, -1]              # Negative duplicates → True
[0, 0]                # Zero duplicates → True
```

---

## Complete Test File

```python
if __name__ == "__main__":
    # Test all three implementations
    
    test_cases = [
        ([1, 2, 3, 3], True),
        ([1, 2, 3, 4], False),
        ([1, 1, 1, 3, 3, 4], True),
        ([1], False),
        ([1, 1], True),
    ]
    
    for nums, expected in test_cases:
        # Test brute force
        result_brute = hasDuplicate(nums)
        assert result_brute == expected, f"Brute force failed for {nums}"
        
        # Test sorting
        result_sort = hasDuplicateSort(nums.copy())  # Copy to avoid modifying
        assert result_sort == expected, f"Sort failed for {nums}"
        
        # Test hash set
        result_hash = hasDuplicateHashSet(nums)
        assert result_hash == expected, f"Hash set failed for {nums}"
        
        print(f"✓ All methods passed for {nums} → {expected}")
    
    print("\n🎉 All tests passed!")
```

---

## Final Thoughts

This problem is a perfect introduction to DSA because it teaches:
- The importance of algorithm analysis (O(n²) vs O(n))
- Time-space trade-offs
- The power of hash-based data structures
- The value of preprocessing (sorting)

**Remember:** The hash set solution is what you should know by heart. It's the optimal solution for 90% of interview scenarios.