```markdown
# Group Anagrams

## Problem Statement

Given an array of strings `strs`, group all anagrams together into sublists.  
You may return the output in any order.

An **anagram** is a string that contains the exact same characters as another string, but the order of the characters can be different.

Example:

```

Input: ["act","pots","tops","cat","stop","hat"]
Output: [["act","cat"],["pots","tops","stop"],["hat"]]

```

---

## Core Insight

Two strings are anagrams **if and only if** they have:
- the same characters
- with the same frequencies

Order does **not** matter.  
Character **counts** do.

So the problem reduces to:
> “How do we give every word a representation that is identical for all its anagrams?”

That representation becomes the **key** we use to group words.

---

## Approach 1: Character Frequency Count (Optimal)

### Intuition

For each word:
1. Count how many times each character appears.
2. Use that count as a signature.
3. Group words that share the same signature.

Since the problem is constrained to lowercase English letters, we can use a fixed-size array of length 26.

Example:
```

"act" → [1,0,1,0,...,1,...]
"cat" → [1,0,1,0,...,1,...]

````

Same frequency array → same anagram group.

---

### Implementation (Explicit)

```python
def group_anagrams_by_count(strs: list[str]) -> list[list[str]]:
    groups = {}

    for word in strs:
        char_count = [0] * 26
        for i in range(len(word)):
            index = ord(word[i]) - ord('a')
            char_count[index] += 1

        key = tuple(char_count)

        if key not in groups:
            groups[key] = []
        groups[key].append(word)

    return list(groups.values())
````

---

### Implementation (Compact / Pythonic)

```python
from collections import defaultdict

def group_anagrams_by_count_compact(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        char_count = [0] * 26
        for ch in word:
            char_count[ord(ch) - ord('a')] += 1

        groups[tuple(char_count)].append(word)

    return list(groups.values())
```

---

### Complexity

Let:

* **N** = number of strings
* **K** = average length of a string

**Time:** `O(N · K)`
**Space:** `O(N · K)` (output storage)

This is **asymptotically optimal** — every character must be read at least once.

---

## Approach 2: Sorting (Simplest to Understand)

### Intuition

If two words are anagrams, then:

```
sorted(word1) == sorted(word2)
```

So:

1. Sort each word alphabetically.
2. Use the sorted word as the key.
3. Group words that share the same sorted form.

Example:

```
"pots" → "opst"
"tops" → "opst"
"stop" → "opst"
```

---

### Implementation (Sorting-Based)

```python
from collections import defaultdict

def group_anagrams_by_sorting(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)

    for word in strs:
        key = ''.join(sorted(word))
        groups[key].append(word)

    return list(groups.values())
```

---

### Complexity

**Time:** `O(N · K log K)`
**Space:** `O(N · K)`

Sorting makes this slower than the frequency-count approach, but it is very intuitive and often easier to reason about.

---

## Comparison Summary

| Approach        | Time Complexity  | Space Complexity | Notes           |
| --------------- | ---------------- | ---------------- | --------------- |
| Frequency Count | `O(N · K)`       | `O(N · K)`       | Optimal         |
| Sorting         | `O(N · K log K)` | `O(N · K)`       | Simpler, slower |

---

## Key Takeaways

* Different word lengths are allowed, but words of different lengths can **never** be anagrams.
* Character **frequency** is the true invariant for anagrams.
* Sorting works, but counting is faster.
* `defaultdict(list)` removes boilerplate when grouping.

Once the idea of a **canonical representation** clicks, Group Anagrams becomes a straightforward hashing problem.

```
```
