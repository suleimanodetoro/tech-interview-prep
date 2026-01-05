from collections import defaultdict
import heapq

def topK_FrequentElement_sort(nums: list[int], k: int) -> list[int]:
    """
    Approach 1: Count + sort by frequency.
    Time:  O(n + d log d)
    Space: O(d)
    """
    frequency_counter = defaultdict(int)
    for number in nums:
        frequency_counter[number] += 1

    sorted_items = sorted(
        frequency_counter.items(),
        key=lambda pair: pair[1],
        reverse=True
    )
    return [num for num, _count in sorted_items[:k]]


def topK_FrequentElement_heap(nums: list[int], k: int) -> list[int]:
    """
    Approach 2 (optimized): Count + min-heap of size k.
    Keep only the top k elements in the heap; pop when heap exceeds k.
    Time:  O(n + d log k)
    Space: O(d) for freq + O(k) for heap
    """
    frequency_counter = defaultdict(int)
    for number in nums:
        frequency_counter[number] += 1

    heap: list[tuple[int, int]] = []  # (count, num)

    for num, count in frequency_counter.items():
        heapq.heappush(heap, (count, num))
        if len(heap) > k:
            heapq.heappop(heap)  # removes smallest count

    return [num for _count, num in heap]
