import copy
import random

def check(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    tmp_row = (row // 3) * 3
    tmp_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[tmp_row + i][tmp_col + j] == num:
                return False
    return True

def solve(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if check(board, row, col, num):
                        board[row][col] = num
                        if solve(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def gen_board():
    board = [[0] * 9 for _ in range(9)]
    def fill_board(b):
        for row in range(9):
            for col in range(9):
                if b[row][col] == 0:
                    num = list(range(1, 10))
                    random.shuffle(num) 
                    for i in num:
                        if check(b, row, col, i):
                            b[row][col] = i
                            if fill_board(b):
                                return True
                            b[row][col] = 0
                    return False
        return True
    fill_board(board)
    return board

def gen_dif(dif="Easy"):
    board = gen_board()
    if dif == "Easy":
        cnt = random.randint(30, 40)
    elif dif == "Medium":
        cnt = random.randint(45, 50)
    elif dif == "Hard":
        cnt = random.randint(55, 60)
    else:
        cnt = random.randint(30, 40)
    tmp = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(tmp)
    for i in range(cnt):
        row, col = tmp[i]
        board[row][col] = 0        
    return board

def hint(cur):
    tmp_board = copy.deepcopy(cur)
    if solve(tmp_board):
        for row in range(9):
            for col in range(9):
                if cur[row][col] == 0:
                    return row, col, tmp_board[row][col]
    return None

def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")