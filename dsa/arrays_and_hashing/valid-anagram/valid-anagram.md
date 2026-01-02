

````md
## Valid Anagram

### 📝 Problem
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, otherwise return `False`.

An **anagram** is a string that contains the **same characters with the same frequencies**, but possibly in a different order.

---

## 🧠 Key Insight (Most Important)
Two strings are anagrams **if and only if**:
- They have the **same length**
- They contain the **same characters**
- Each character appears the **same number of times**

Order **does not matter** — only **frequency** does.

---

## ⚠️ Always Check Constraints First
The problem statement **does NOT specify**:
- lowercase only
- uppercase allowed
- Unicode allowed

Because of this:
- A **hash map solution is the safest default**
- Array-based optimizations are only valid **if constraints allow them**

> **Never assume constraints that are not explicitly stated.**

---

## 🛠️ Solution 1: Brute Force (Baseline)

### Idea
- For each character in `s`, try to remove it from `t`
- If a character can’t be found, the strings aren’t anagrams

### Implementation
```python
def valid_anagram_bruteForce(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    t_list = list(t)
    for char in s:
        if char in t_list:
            t_list.remove(char)
        else:
            return False

    return True
````

### Complexity

* **Time:** `O(n²)` (search + remove in list)
* **Space:** `O(n)`

✅ Easy to understand
❌ Too slow for large inputs

---

## 🛠️ Solution 2: Sorting-Based

### Idea

* If two strings are anagrams, their **sorted versions will be identical**

### Implementation

```python
def valid_anagram_sort(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)
```

### Complexity

* **Time:** `O(n log n)`
* **Space:** `O(n)`

✅ Simple
❌ Sorting is unnecessary work

---

## 🛠️ Solution 3: Frequency Map (Optimal & General)

### Idea

* Count how many times each character appears
* Compare character frequencies

This solution:

* Works for **any characters**
* Does **not depend on constraints**
* Is the **recommended interview solution**

### Implementation

```python
def valid_anagram_frequencyMap(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    countS, countT = {}, {}
    for i in range(len(s)):
        countS[s[i]] = countS.get(s[i], 0) + 1
        countT[t[i]] = countT.get(t[i], 0) + 1

    return countS == countT
```

### Complexity

* **Time:** `O(n)`
* **Space:** `O(n)` (or `O(k)` unique characters)

✅ Optimal
✅ Safe default
✅ Interview-ready

---

## 🛠️ Solution 4: Frequency Array (Constraint-Based Optimization)

### ⚠️ When This Is Allowed

This solution is **ONLY valid if**:

* Characters are guaranteed to be `'a'` through `'z'`

If the problem **does not say this explicitly**, do **NOT** use this approach.

---

### Why an Array Works Here

* There are exactly **26 lowercase English letters**
* We map:

  ```
  'a' → index 0
  'b' → index 1
  ...
  'z' → index 25
  ```

### How the Mapping Works

* `ord(char)` returns the Unicode value of a character
* Subtracting `ord('a')` converts it to an index

Example:

```
ord('c') - ord('a') = 99 - 97 = 2
```

---

### Key Invariant

Each index stores:

```
(# occurrences in s) − (# occurrences in t)
```

If all values end at `0`, the strings are anagrams.

---

### Implementation

```python
def valid_anagram_frequencyMap_array(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False

    count = [0] * 26
    for i in range(len(s)):
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1

    for val in count:
        if val != 0:
            return False
    return True
```

### Complexity

* **Time:** `O(n)`
* **Space:** `O(1)` (fixed size array)

✅ Fast
❌ Only valid under strict constraints

---

## 🧠 Interview Strategy (What to Say)

> “I’ll start with a hash map solution since the problem doesn’t specify character constraints.
> If the input were guaranteed to be lowercase English letters, we could optimize further using a fixed-size frequency array.”

This shows:

* Correctness
* Awareness of constraints
* Optimization skill

---

## ✅ Summary Table

| Approach    | Time       | Space | Constraint Safe       |
| ----------- | ---------- | ----- | --------------------- |
| Brute Force | O(n²)      | O(n)  | ✅                     |
| Sorting     | O(n log n) | O(n)  | ✅                     |
| Hash Map    | O(n)       | O(n)  | ✅                     |
| Array       | O(n)       | O(1)  | ❌ (needs constraints) |

---

## 📌 Final Takeaways

* **Always listen for constraints**
* Hash maps are the **default optimal solution**
* Array solutions are **optional optimizations**
* Never assume input restrictions unless stated

---

**You didn’t just solve the problem — you learned how to reason about solutions.**

```