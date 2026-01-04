from collections import defaultdict

def topK_FrequentElement(nums: list[int], k: int) -> list[int]:
    """
    Returns the k most frequent elements in nums.
    Uses a frequency map followed by sorting.
    """

    # Step 1: Count frequency of each number
    frequency_counter = defaultdict(int)
    for number in nums:
        frequency_counter[number] += 1

    # Step 2: Sort elements by frequency (descending)
    # Each item is a (number, count) pair
    sorted_items = sorted(
        frequency_counter.items(),
        key=lambda pair: pair[1],
        reverse=True
    )

    # Step 3: Extract the top k elements
    return [num for num, count in sorted_items[:k]]
