from typing import List
from collections import defaultdict

def longestConsecutive(nums: List[int]) -> int:
    """
    Video explanation: https://www.youtube.com/watch?v=P6RZZMu_maU
    
    Problem: Find the length of the longest consecutive elements sequence.
    Must run in O(n) time.
    
    Example:
    nums = [100, 4, 200, 1, 3, 2]
    Output: 4 (the sequence is [1, 2, 3, 4])
    
    HASH MAP APPROACH:
    ==================
    Key insight: Instead of sorting or scanning sequences, we use a hash map
    to track the LENGTH of sequences at their BOUNDARY positions.
    
    When we encounter a new number:
    1. Check its left neighbor (num - 1) for existing sequence length
    2. Check its right neighbor (num + 1) for existing sequence length
    3. Merge them: new_length = left_length + right_length + 1
    4. Update ONLY the boundaries of this new sequence
    
    Why only update boundaries?
    - Interior values don't matter - we only need boundary lengths
    - When extending later, we'll look at boundaries again
    
    Visual example with [1, 2, 4, 3]:
    
    Step 1: Add 1
    mp = {1: 1}  # Sequence of length 1
    
    Step 2: Add 2
    - left = mp[1] = 1 (sequence ending at 1)
    - right = mp[3] = 0 (nothing starting at 3)
    - new_length = 1 + 0 + 1 = 2
    - Update left boundary: mp[2-1] = mp[1] = 2
    - Update right boundary: mp[2+0] = mp[2] = 2
    mp = {1: 2, 2: 2}
    
    Step 3: Add 4
    mp = {1: 2, 2: 2, 4: 1}
    
    Step 4: Add 3 (connects [1,2] and [4])
    - left = mp[2] = 2 (sequence ending at 2)
    - right = mp[4] = 1 (sequence starting at 4)
    - new_length = 2 + 1 + 1 = 4
    - Update left boundary: mp[3-2] = mp[1] = 4
    - Update right boundary: mp[3+1] = mp[4] = 4
    mp = {1: 4, 2: 2, 3: 4, 4: 4}
         ^left          ^right
    """
    
    # Hash map to store sequence lengths at boundary positions
    mp = defaultdict(int)
    res = 0  # Track the longest sequence found
    
    # Process each number
    for num in nums:
        # Skip if we've already processed this number
        if mp[num]:
            continue
        
        # Get lengths of adjacent sequences
        left_length = mp[num - 1]   # Length of sequence ending at num-1
        right_length = mp[num + 1]  # Length of sequence starting at num+1
        
        # Calculate new merged sequence length
        # (left sequence) + (current number) + (right sequence)
        new_length = left_length + right_length + 1
        
        # Store length at current position (marks it as visited)
        mp[num] = new_length
        
        # Update the LEFT boundary of the merged sequence
        # The left boundary is at position: num - left_length
        mp[num - left_length] = new_length
        
        # Update the RIGHT boundary of the merged sequence
        # The right boundary is at position: num + right_length
        mp[num + right_length] = new_length
        
        # Update result if this is the longest sequence so far
        res = max(res, new_length)
    
    return res


# ============================================================
# VISUAL: Boundary Update Logic
# ============================================================
#
# Example: nums = [1, 2, 4, 3]
#
# After adding 1, 2:
#   Sequence [1, 2] with length 2
#   mp[1] = 2 (left boundary)
#   mp[2] = 2 (right boundary)
#
# After adding 4:
#   Sequence [4] with length 1
#   mp[4] = 1
#
# Adding 3 connects them:
#   - num = 3
#   - left_length = mp[2] = 2 (sequence [1,2])
#   - right_length = mp[4] = 1 (sequence [4])
#   - new_length = 2 + 1 + 1 = 4
#
#   Update boundaries:
#   - Left boundary at: 3 - 2 = 1
#     mp[1] = 4
#   - Right boundary at: 3 + 1 = 4
#     mp[4] = 4
#
#   Final: [1, 2, 3, 4] all connected, length 4 stored at boundaries


# ============================================================
# Alternative approach: HashSet (for comparison)
# ============================================================

def longestConsecutive_set(nums: List[int]) -> int:
    """
    Classic NeetCode approach using a set.
    
    Strategy:
    1. Put all numbers in a set for O(1) lookup
    2. For each number, check if it's the START of a sequence
       (i.e., num-1 is NOT in the set)
    3. If it's a start, count forward until sequence breaks
    """
    if not nums:
        return 0
    
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Only start counting if this is the beginning of a sequence
        if num - 1 not in num_set:
            current_num = num
            current_length = 1
            
            # Count forward
            while current_num + 1 in num_set:
                current_num += 1
                current_length += 1
            
            longest = max(longest, current_length)
    
    return longest


# ============================================================
# TEST CASES
# ============================================================

if __name__ == "__main__":
    test_cases = [
        ([100, 4, 200, 1, 3, 2], 4),           # [1,2,3,4]
        ([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], 9),   # [0,1,2,3,4,5,6,7,8]
        ([9, 1, 4, 7, 3, 2, 8, 5, 6], 9),      # [1,2,3,4,5,6,7,8,9]
        ([], 0),                                # Empty
        ([1], 1),                               # Single element
        ([1, 2, 0, 1], 3),                      # Duplicates [0,1,2]
    ]
    
    for nums, expected in test_cases:
        result_map = longestConsecutive(nums)
        result_set = longestConsecutive_set(nums)
        print(f"nums: {nums}")
        print(f"  HashMap approach: {result_map} (expected: {expected})")
        print(f"  HashSet approach: {result_set}")
        print(f"  {'✓' if result_map == expected else '✗'}")
        print()