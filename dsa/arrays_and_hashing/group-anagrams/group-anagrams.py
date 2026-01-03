from typing import List
from collections import defaultdict

sample = ["act", "pots", "tops", "cat", "stop", "hat"]


# frequency-count solution (explicit / step-by-step)
def group_anagrams_by_count(strs: List[str]) -> List[List[str]]:
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


# frequency-count solution (compact / pythonic)
def group_anagrams_by_count_compact(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)

    for word in strs:
        char_count = [0] * 26
        for ch in word:
            char_count[ord(ch) - ord('a')] += 1

        groups[tuple(char_count)].append(word)

    return list(groups.values())


# sorting-based solution (simplest to understand, less optimal)
def group_anagrams_by_sorting(strs: List[str]) -> List[List[str]]:
    groups = defaultdict(list)

    for word in strs:
        key = ''.join(sorted(word))
        groups[key].append(word)

    return list(groups.values())
