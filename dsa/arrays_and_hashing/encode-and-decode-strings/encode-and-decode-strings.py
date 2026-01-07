def encode(strs: list) -> str:
    result = "" 
    
    for string in strs:
        # Format: LENGTH + DELIMITER + STRING
        # Example: "hello" becomes "5#hello"
        # The length prefix is the KEY - it tells us exactly how many chars to read
        result += str(len(string)) + "#" + string
    
    return result


def decode(encodedString: str) -> list:
    result = []  
    i = 0
    
    # WHY while loop? Because i jumps by VARIABLE amounts each iteration
    # (based on each string's length), not by 1 like a for loop would
    while i < len(encodedString):
        
        # PHASE 1: Find the delimiter to extract the LENGTH number
        j = i
        while encodedString[j] != '#':  
            j += 1
        # Now: i points to start of length, j points to the '#'
        
        # PHASE 2: Parse the length number
        length = int(encodedString[i:j])  
        # Example: if encoded is "5#hello", length becomes 5 (not "5")
        
        # PHASE 3: Extract exactly 'length' characters after the delimiter
        i = j + 1          # Move i to first char AFTER '#' (start of actual string)
        j = i + length     # Move j exactly 'length' positions forward (end of string)
        # At this point: i and j are DIFFERENT (j is 'length' ahead of i)
        # Example: if length=5, i points to 'h' in "hello", j points 5 chars later
        
        result.append(encodedString[i:j])  
        # This is WHY embedded '#' doesn't break us - we COUNT chars, don't search!
        
        # PHASE 4: Move to the start of next encoded segment
        i = j  # Now i and j are EQUAL again, both pointing to next length prefix
        # This equality resets at the start of each loop iteration
    
    return result