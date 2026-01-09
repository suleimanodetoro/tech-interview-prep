from typing import List

def isValidSudoku(board: List[List[str]]) -> bool:
    """
    Video explanation: https://www.youtube.com/watch?v=TjFXEUCMqI8
    
    Problem: Determine if a 9x9 Sudoku board is valid.
    
    Rules:
    1. Each row must contain digits 1-9 without repetition
    2. Each column must contain digits 1-9 without repetition
    3. Each 3x3 sub-box must contain digits 1-9 without repetition
    
    Note: Empty cells are represented by '.'
    
    Example board:
    [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]
    
    NEETCODE'S APPROACH:
    ====================
    Use HashSets to track what we've seen:
    - rows: set for each row
    - cols: set for each column
    - boxes: set for each 3x3 sub-box
    
    Key insight for sub-boxes:
    Box index = (row // 3, col // 3)
    
    Visual of box indices:
    (0,0) (0,1) (0,2)
    (1,0) (1,1) (1,2)
    (2,0) (2,1) (2,2)
    """
    
    # Create sets to track seen numbers
    # We'll use defaultdict-like approach or manual initialization
    rows = [set() for _ in range(9)]     # 9 rows, each gets its own set
    cols = [set() for _ in range(9)]     # 9 columns, each gets its own set
    boxes = [set() for _ in range(9)]    # 9 boxes, each gets its own set
    
    # Scan through entire board
    for r in range(9):
        for c in range(9):
            cell = board[r][c]
            
            # Skip empty cells
            if cell == '.':
                continue
            
            # Calculate which 3x3 box this cell belongs to
            # Box numbering (left-to-right, top-to-bottom):
            # 0 1 2
            # 3 4 5
            # 6 7 8
            box_index = (r // 3) * 3 + (c // 3)
            
            # Check if number already exists in current row, column, or box
            if cell in rows[r]:
                return False  # duplicate in row
            if cell in cols[c]:
                return False  # duplicate in column
            if cell in boxes[box_index]:
                return False  # duplicate in box
            
            # Add number to the sets
            rows[r].add(cell)
            cols[c].add(cell)
            boxes[box_index].add(cell)
    
    # If we made it through without finding duplicates, board is valid
    return True


# ============================================================
# VISUAL: Understanding the 3x3 box indexing
# ============================================================
#
# Board positions to box index:
# 
# r=0,c=0 -> box = (0//3)*3 + (0//3) = 0*3 + 0 = 0
# r=0,c=3 -> box = (0//3)*3 + (3//3) = 0*3 + 1 = 1
# r=0,c=6 -> box = (0//3)*3 + (6//3) = 0*3 + 2 = 2
# r=3,c=0 -> box = (3//3)*3 + (0//3) = 1*3 + 0 = 3
# r=3,c=3 -> box = (3//3)*3 + (3//3) = 1*3 + 1 = 4
# r=3,c=6 -> box = (3//3)*3 + (6//3) = 1*3 + 2 = 5
# r=6,c=0 -> box = (6//3)*3 + (0//3) = 2*3 + 0 = 6
# r=6,c=3 -> box = (6//3)*3 + (3//3) = 2*3 + 1 = 7
# r=6,c=6 -> box = (6//3)*3 + (6//3) = 2*3 + 2 = 8
#
# Visual mapping:
#   Col: 0 1 2 | 3 4 5 | 6 7 8
#   Row
#    0   [  0  |   1   |   2  ]
#    1   [  0  |   1   |   2  ]
#    2   [  0  |   1   |   2  ]
#        ------+-------+-------
#    3   [  3  |   4   |   5  ]
#    4   [  3  |   4   |   5  ]
#    5   [  3  |   4   |   5  ]
#        ------+-------+-------
#    6   [  6  |   7   |   8  ]
#    7   [  6  |   7   |   8  ]
#    8   [  6  |   7   |   8  ]


# ============================================================
# Alternative approach using tuples as keys (also from NeetCode)
# ============================================================

def isValidSudoku_alternative(board: List[List[str]]) -> bool:
    """
    Same logic, but using a single set with tuple keys.
    
    Instead of separate lists of sets, we use one set containing tuples like:
    - ('row', row_number, value)
    - ('col', col_number, value)
    - ('box', box_index, value)
    """
    seen = set()
    
    for r in range(9):
        for c in range(9):
            cell = board[r][c]
            
            if cell == '.':
                continue
            
            box_index = (r // 3) * 3 + (c // 3)
            
            # Create unique identifiers for this number's position
            row_key = ('row', r, cell)
            col_key = ('col', c, cell)
            box_key = ('box', box_index, cell)
            
            # Check if any of these already exist
            if row_key in seen or col_key in seen or box_key in seen:
                return False
            
            # Add all three to the set
            seen.add(row_key)
            seen.add(col_key)
            seen.add(box_key)
    
    return True