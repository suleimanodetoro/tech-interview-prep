from typing import List
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


def valid_anagram_sort(s: str, t:str)->bool:
    # no point checking anagram for unequal lengths no?
    if len(s) != len(t):
        return False
    return sorted(s) == sorted(t)

# next is using a frequency map
def valid_anagram_frequencyMap(s:str, t:str)->bool:
    # no point checking anagram for unequal lengths no?
    if len(s) != len(t):
        return False
    countS,countT={},{}
    for i in range(len(s)):
        countS[s[i]] = countS.get(s[i], 0) + 1
        countT[t[i]] = countT.get(t[i], 0) + 1
    return countT == countS


def valid_anagram_frequencyMap_array(s:str, t:str)->bool:
    # no point checking anagram for unequal lengths no?
    if len(s) != len(t):
        return False
    count = [0]*26
    for i in range(len(s)):
        # use built in function to return unicode
        count[ord(s[i]) - ord('a')] += 1
        count[ord(t[i]) - ord('a')] -= 1

    for val in count:
        if val != 0:
            return False
    return True



    
    