
# 你提供的数独字符串

sudoku ='''
x4x2x8xx7
862xx5x3x
xx7x6x1xx
xxxx3x96x
xxxxxxxxx
x26x4xxxx
xx4x5x2xx
x5x4xx391
2xx6x9x4x
'''

'''
3xxxx1xxx
xx89x35xx
x6xxxxx21
5x1xxxx8x
2x4x6x1x7
x8xxxx9x5
91xxxxx6x
xx65x27xx
xxx1xxxx3
'''

import numpy as np
import math

def convert_sudoku(sudoku):
    sudoku = sudoku.strip().split('\n')  # 去除首尾空白字符并按行分割
    board = []
    for row in sudoku:
        board_row = []
        for char in row:
            if char == 'x':
                board_row.append(0)  # 空位置用 0 表示
            else:
                board_row.append(int(char))  # 将数字字符转换为整数
        board.append(board_row)
    return board

def is_valid(board, row, col, num):
    N = len(board)
    box_size = int(math.sqrt(N))
    
    for x in range(N):
        if board[row][x] == num or board[x][col] == num:
            return False
    
    start_row = row - row % box_size
    start_col = col - col % box_size
    for i in range(box_size):
        for j in range(box_size):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):
    N = len(board)
    empty = find_empty_location(board)
    
    if not empty:
        return True
    else:
        row, col = empty

    for num in range(1, N + 1):
        if is_valid(board, row, col, num):
            board[row][col] = num
            
            if solve_sudoku(board):
                return True
            
            board[row][col] = 0
    return False

def find_empty_location(board):
    N = len(board)
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                return (i, j)
    return None

def print_board(board):
    N = len(board)
    for i in range(N):
        for j in range(N):
            print(board[i][j], end=" ")
        print()

# 示例，初始化一个 N*N 的数独板
N = 9 # 或者是任何其它合法的尺寸，比如 4x4, 16x16 等
#board = np.zeros((N,N), dtype=int)
# 填充一些初始数字...


# 转换数独
board = convert_sudoku(sudoku)

# 打印转换后的数独板
for row in board:
    print(row)


# 打印初始数独板
print_board(board)

# 尝试解决数独
if solve_sudoku(board):
    print("数独解决方案：")
    print_board(board)
else:
    print("无解")
