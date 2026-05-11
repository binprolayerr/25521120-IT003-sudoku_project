import copy
import random

def check(board, row, col, num):
    """
    Kiểm tra xem việc đặt một số vào vị trí cụ thể có hợp lệ không.
    Luật Sudoku yêu cầu số không được trùng lặp trên cùng một hàng, một cột và trong cùng một khối 3x3 chứa ô đó.
    Args:
        board (list of list of int): Bảng Sudoku hiện tại.
        row (int): Chỉ số hàng của ô cần kiểm tra (0-8).
        col (int): Chỉ số cột của ô cần kiểm tra (0-8).
        num (int): Số cần điền thử vào ô (1-9).
    Returns:
        bool: True nếu số đặt vào hợp lệ, False nếu vi phạm luật.
    """
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

def cnt_sol(board, cnt):
    """
    Đếm số lượng nghiệm hợp lệ của bảng Sudoku hiện tại bằng thuật toán quay lui.
    Args:
        board (list of list of int): Bảng Sudoku cần giải.
        cnt (list of int): Danh sách chứa 1 phần tử dùng để lưu số lượng nghiệm tìm được.
    """
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
    """
    Tạo ra một bảng Sudoku 9x9 hoàn chỉnh.
    Returns:
        list of list of int: Bảng Sudoku 9x9 đã được điền đầy đủ số.
    """
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
    """
    Tạo ra một đề bài Sudoku mới dựa trên độ khó.
    Hàm hoạt động bằng cách lấy một bảng đã giải hoàn chỉnh, sau đó xóa dần các ô ngẫu nhiên. 
    Mỗi lần xóa nó kiểm tra xem bảng còn giữ được tính "nghiệm duy nhất" hay không. 
    Số lượng ô bị xóa phụ thuộc vào độ khó.
    Args:
        dif (str, optional): Mức độ khó của game ("Easy", "Medium", "Hard"). 
                             Mặc định là "Easy".
    Returns:
            - board (list of list of int): Bảng đề bài.
            - solved_board (list of list of int): Bảng kết quả hoàn chỉnh để đối chiếu.
    """
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
    """
    Cung cấp một gợi ý ngẫu nhiên cho người chơi bằng cách điền hộ một ô trống.
    Args:
        cur (list of list of int): Bảng Sudoku hiện tại của người chơi.
        solved (list of list of int): Bảng Sudoku kết quả hoàn chỉnh.
    Returns: 
            - (r, c, val): Chỉ số hàng, chỉ số cột và giá trị đúng của ô được gợi ý.
            - None: Nếu bảng đã được điền đầy.
    """
    empty_cells = [(r, c) for r in range(9) for c in range(9) if cur[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        return r, c, solved[r][c]
    return None