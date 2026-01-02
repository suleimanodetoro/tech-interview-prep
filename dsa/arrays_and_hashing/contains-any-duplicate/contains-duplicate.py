from typing import List 

# Most efficient: using hash set
def hasDuplicateHashSet(nums: List[int]) -> bool:
        seen = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False

# Sort first implementation
def hasDuplicateSort(nums: List[int])->bool:
    nums.sort()
    for i in range(len(nums)-1):
        if nums[i]==nums[i+1]:
            return True
    return False
# brute force implementation

def hasDuplicate(nums: List[int]) -> bool:
    for i in range(len(nums)):
        for j in range (i+1,len(nums)):
            if nums[i]==nums[j]:
                return True
    return False
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