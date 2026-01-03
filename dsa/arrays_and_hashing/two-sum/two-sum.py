from typing import List, Dict


def twoSumMyOnePass(nums: List[int], target: int) -> List[int]:
    # map: needed value -> index
    remainder_map: Dict[int, int] = {}

    for i, num in enumerate(nums):
        if num in remainder_map:
            return [remainder_map[num], i]

        remainder = target - num
        remainder_map[remainder] = i

    raise ValueError("No two sum solution found")


# popular one-pass method (saw this after coming up with above solution)
def twoSumPopularOnePass(nums: List[int], target: int) -> List[int]:
    seen: Dict[int, int] = {}

    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i

    raise ValueError("No two sum solution found")


# two-pass method
def twoSumTwoPass(nums: List[int], target: int) -> List[int]:
    indices: Dict[int, int] = {}

    for i, num in enumerate(nums):
        indices[num] = i

    for i, num in enumerate(nums):
        diff = target - num
        if diff in indices and indices[diff] != i:
            return [i, indices[diff]]

    raise ValueError("No two sum solution found")

def twoSumSorting(nums: List[int], target: int) -> List[int]:
    pairs = []

    for i, num in enumerate(nums):
        pairs.append((num, i))

    pairs.sort()  # sort by value

    left, right = 0, len(pairs) - 1
    while left < right:
        cur = pairs[left][0] + pairs[right][0]

        if cur == target:
            return [pairs[left][1], pairs[right][1]]
        elif cur < target:
            left += 1
        else:
            right -= 1

    raise ValueError("No two sum solution found")

# brute force method (learning / baseline)
def twoSumBruteForce(nums: List[int], target: int) -> List[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

    raise ValueError("No two sum solution found")
