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

def cnt_sol(board, cnt):
    min_poss = 10
    min_r, min_c = -1, -1
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                poss = sum(1 for i in range(1, 10) if check(board, r, c, i))
                if poss == 0: return
                if poss < min_poss:
                    min_poss = poss
                    min_r, min_c = r, c
    if min_r == -1:
        cnt[0] += 1
        return
    for num in range(1, 10):
        if check(board, min_r, min_c, num):
            board[min_r][min_c] = num
            cnt_sol(board, cnt)
            board[min_r][min_c] = 0
            if cnt[0] > 1: 
                return

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
    solved_board = copy.deepcopy(board)
    if dif == "Easy":
        cnt = random.randint(30, 35)
    elif dif == "Medium":
        cnt = random.randint(40, 45)
    elif dif == "Hard":
        cnt = random.randint(50, 55)
    else:
        cnt = random.randint(30, 35)
    tmp = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(tmp)
    removed = 0
    for row, col in tmp:
        if removed >= cnt:
            break
        backup = board[row][col]
        board[row][col] = 0
        count = [0]
        board_copy = copy.deepcopy(board)
        cnt_sol(board_copy, count)
        if count[0] == 1:
            removed += 1
        else:
            board[row][col] = backup            
    return board, solved_board

def hint(cur, solved):
    empty_cells = [(r, c) for r in range(9) for c in range(9) if cur[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        return r, c, solved[r][c]
    return None
