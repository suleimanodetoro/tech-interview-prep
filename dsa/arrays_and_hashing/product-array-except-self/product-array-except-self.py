from typing import List

def productExceptSelf(nums: List[int]) -> List[int]:
    """
    Video explanation: https://www.youtube.com/watch?v=tSRFtR3pv74
    
    Example walkthrough: nums = [1, 2, 3, 4]
    
    VIDEO'S EXPLANATION (3 arrays):
    ================================
    Step 1: Build LEFT products
    left = [1, 1, 2, 6]
           ↑  ↑  ↑  ↑
           |  |  |  1*2*3
           |  |  1*2
           |  1
           nothing before
    
    Step 2: Build RIGHT products  
    right = [24, 12, 4, 1]
            ↑   ↑   ↑  ↑
            |   |   |  nothing after
            |   |   4
            |   3*4
            2*3*4
    
    Step 3: Multiply them
    output[i] = left[i] * right[i]
    output = [1*24, 1*12, 2*4, 6*1]
           = [24, 12, 8, 6]
    
    
    OUR OPTIMIZED APPROACH (reuse same array):
    ==========================================
    Instead of 3 arrays, we use 1 array and do it in 2 passes:
    
    Pass 1: Store LEFT products in resultArray
    Pass 2: Multiply by RIGHT products on-the-fly (no extra array!)
    """
    
    arrayLength = len(nums)
    resultArray = [1] * arrayLength
    
    # ========== PASS 1: Build PREFIX (LEFT) products ==========
    # Think of it like this: 1[1, 2, 3, 4]1
    #                        ^ we start from this invisible 1 on the left
    
    prefix = 1  # this represents "everything we've multiplied so far from the left"
    for i in range(arrayLength):
        # At each position, store the product of EVERYTHING BEFORE this index
        # 1[1, 2, 3, 4]1
        #   ^              i=0: prefix=1 (the invisible 1 before the array)
        # 1[1, 2, 3, 4]1
        #      ^           i=1: prefix=1 (just 1 from left side)
        # 1[1, 2, 3, 4]1
        #         ^        i=2: prefix=1*2=2 (accumulated 1*2 from left)
        # 1[1, 2, 3, 4]1
        #            ^     i=3: prefix=1*2*3=6 (accumulated 1*2*3 from left)
        resultArray[i] = prefix
        prefix *= nums[i]  # now include current element for next iteration
    
    # After Pass 1: resultArray = [1, 1, 2, 6]
    # This matches the video's "left" array!
    
    
    # ========== PASS 2: Multiply by SUFFIX (RIGHT) products ==========
    # Think of it like this: 1[1, 2, 3, 4]1
    #                                      ^ we start from this invisible 1 on the right
    
    suffix = 1  # this represents "everything we've multiplied so far from the right"
    for i in range(arrayLength - 1, -1, -1):
        # At each position, multiply by the product of EVERYTHING AFTER this index
        # 1[1, 2, 3, 4]1
        #            ^     i=3: suffix=1 (the invisible 1 after the array)
        #                      resultArray[3] = 6*1 = 6
        # 1[1, 2, 3, 4]1
        #         ^        i=2: suffix=4 (accumulated 4 from right)
        #                      resultArray[2] = 2*4 = 8
        # 1[1, 2, 3, 4]1
        #      ^           i=1: suffix=3*4=12 (accumulated 3*4 from right)
        #                      resultArray[1] = 1*12 = 12
        # 1[1, 2, 3, 4]1
        #   ^              i=0: suffix=2*3*4=24 (accumulated 2*3*4 from right)
        #                      resultArray[0] = 1*24 = 24
        resultArray[i] *= suffix
        suffix *= nums[i]  # now include current element for next iteration
    
    # Final: resultArray = [24, 12, 8, 6] 
    
    return resultArray


# ============================================================
# VISUAL: What "everything before/after" means
# ============================================================
# 
# Think of the array as: 1[1, 2, 3, 4]1
#                        ^           ^
#                   invisible 1s on both sides
# 
# For index 0 (value=1):
#   Everything BEFORE: 1
#   Everything AFTER:  2*3*4 = 24
#   Answer: 1 * 24 = 24
# 
# For index 1 (value=2):
#   Everything BEFORE: 1*1 = 1
#   Everything AFTER:  3*4 = 12
#   Answer: 1 * 12 = 12
# 
# For index 2 (value=3):
#   Everything BEFORE: 1*1*2 = 2
#   Everything AFTER:  4
#   Answer: 2 * 4 = 8
# 
# For index 3 (value=4):
#   Everything BEFORE: 1*1*2*3 = 6
#   Everything AFTER:  1
#   Answer: 6 * 1 = 6