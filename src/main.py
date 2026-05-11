import pygame
import sys
import copy
import time
from sudoku_core import gen_dif, hint
from stack import create_stack, push, pop, is_empty

pygame.init()
WIDTH, HEIGHT = 600, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 150, 0)

font_name = "tahoma" 
font = pygame.font.SysFont(font_name, 40)
note_font = pygame.font.SysFont(font_name, 15)
btn_font = pygame.font.SysFont(font_name, 20)
msg_font = pygame.font.SysFont(font_name, 25)
info_font = pygame.font.SysFont(font_name, 22)

def draw_grid():
    """
    Vẽ lưới Sudoku 9x9 lên màn hình.
    """
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (30, 40 + i * 60), (570, 40 + i * 60), thick)
        pygame.draw.line(screen, BLACK, (30 + i * 60, 40), (30 + i * 60, 580), thick)

def draw_board(board, org, selected):
    """
    Hiển thị trạng thái hiện tại của bảng Sudoku bao gồm các con số và ô đang được chọn.
    Args:
        board (list of list of int): Bảng Sudoku hiện tại.
        org (list of list of int): Bảng gốc chứa đề bài.
        selected (tuple or None): Tọa độ của ô đang được chọn. Nếu có ô này sẽ được tô màu nền xanh nhạt.
    """
    if selected:
        r, c = selected
        pygame.draw.rect(screen, LIGHT_BLUE, (30 + c * 60, 40 + r * 60, 60, 60))
    draw_grid()
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = BLACK if org[i][j] != 0 else BLUE
                text = font.render(str(board[i][j]), True, color)
                rect = text.get_rect(center=(30 + j * 60 + 30, 40 + i * 60 + 30))
                screen.blit(text, rect)

def draw_notes(notes, board):
    """
    Vẽ các số nháp ở kích thước nhỏ vào các vị trí tương ứng trong những ô còn trống.
    Args:
        notes (list of list of set): Lưới 9x9 mỗi phần tử là một tập hợp chứa các số đã được nháp.
        board (list of list of int): Bảng Sudoku hiện tại.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for n in notes[i][j]:
                    r = (n - 1) // 3
                    c = (n - 1) % 3
                    text = note_font.render(str(n), True, DARK_GRAY)
                    screen.blit(text, (30 + j * 60 + 8 + c * 20, 40 + i * 60 + 5 + r * 20))

def draw_button(text, x, y, w, h, active=False):
    """
    Vẽ một nút bấm có thể tương tác trên màn hình và trả về đối tượng của nó.
    Args:
        text (str): Văn bản hiển thị trên nút.
        x (int): Tọa độ X góc trên bên trái của nút.
        y (int): Tọa độ Y góc trên bên trái của nút.
        w (int): Chiều rộng của nút.
        h (int): Chiều cao của nút.
        active (bool, optional): Cờ xác định trạng thái nút. 
                                 Nếu True, nút sẽ có màu xanh nhạt. 
                                 Mặc định là False (màu xám).
    Returns:
        pygame.Rect: Khung chứa nút bấm, dùng để kiểm tra click chuột.
    """
    color = LIGHT_BLUE if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
    txt_surf = btn_font.render(text, True, BLACK)
    txt_rect = txt_surf.get_rect(center=(x + w//2, y + h//2))
    screen.blit(txt_surf, txt_rect)
    return pygame.Rect(x, y, w, h)

def main():
    """
    Hàm chính điều khiển toàn bộ logic game và vòng lặp sự kiện của Pygame.
    Bao gồm các thao tác:
    - Khởi tạo trạng thái trò chơi.
    - Xử lý các sự kiện từ người dùng.
    - Quản lý logic thắng/thua.
    """
    dif_levels = ["Easy", "Medium", "Hard"]
    dif_idx = 0
    
    def init_game():
        """
        Khởi tạo lại trạng thái ban đầu của một ván chơi mới dựa trên độ khó hiện tại.
        Returns:
                - Bảng chơi hiện tại.
                - Bảng đáp án.
                - Bảng đề bài gốc. 
                - Ngăn xếp undo.
                - Ngăn xếp redo. 
                - Notes. 
                - Thời gian bắt đầu.
                - Số lỗi.
                - Cờ kết thúc game. 
                - Thông báo hệ thống. 
                - Thời điểm phát thông báo.
        """
        board, solved = gen_dif(dif_levels[dif_idx])
        return board, solved, copy.deepcopy(board), create_stack(), create_stack(), [[set() for _ in range(9)] for _ in range(9)], time.time(), 0, False, "Game mới bắt đầu!", time.time()

    board, solved_board, org, undo_stack, redo_stack, notes, start_time, mistakes, game_over, message, msg_time = init_game()
    selected = None
    note_mode = False
    final_time = 0
    running = True
    while running:
        screen.fill(WHITE)
        mistakes_surf = info_font.render(f"Lỗi: {mistakes}/3", True, RED if mistakes > 0 else BLACK)
        screen.blit(mistakes_surf, (30, 10))
        if not game_over:
            elapsed = int(time.time() - start_time)
        else:
            elapsed = final_time
        mins, secs = divmod(elapsed, 60)
        timer_surf = info_font.render(f"Thời gian: {mins:02d}:{secs:02d}", True, BLACK)
        screen.blit(timer_surf, (430, 10))
        draw_board(board, org, selected)
        draw_notes(notes, board)
        btn_new = draw_button("New Game", 30, 600, 120, 40)
        btn_dif = draw_button(f"Diff: {dif_levels[dif_idx]}", 160, 600, 140, 40)
        btn_note = draw_button("Note: ON" if note_mode else "Note: OFF", 310, 600, 120, 40, note_mode)
        btn_undo = draw_button("Undo", 30, 650, 100, 40)
        btn_redo = draw_button("Redo", 140, 650, 100, 40)
        btn_hint = draw_button("Hint", 250, 650, 100, 40)
        if message and time.time() - msg_time < 4:
            color = GREEN if "Chúc mừng" in message else RED
            msg_surf = msg_font.render(message, True, color)
            screen.blit(msg_surf, (30, 700))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 30 <= pos[0] <= 570 and 40 <= pos[1] <= 580:
                    c = (pos[0] - 30) // 60
                    r = (pos[1] - 40) // 60
                    selected = (r, c)
                elif btn_new.collidepoint(pos):
                    board, solved_board, org, undo_stack, redo_stack, notes, start_time, mistakes, game_over, message, msg_time = init_game()
                    selected = None
                elif btn_dif.collidepoint(pos):
                    dif_idx = (dif_idx + 1) % 3
                elif btn_note.collidepoint(pos):
                    note_mode = not note_mode
                elif btn_undo.collidepoint(pos) and not game_over:
                    move = pop(undo_stack)
                    if move:
                        push(redo_stack, move) 
                        board[move["row"]][move["col"]] = move["old_val"] 
                elif btn_redo.collidepoint(pos) and not game_over:
                    move = pop(redo_stack)
                    if move:
                        push(undo_stack, move)
                        board[move["row"]][move["col"]] = move["new_val"]
                elif btn_hint.collidepoint(pos) and not game_over:
                    get = hint(board, solved_board)
                    if get:
                        r, c, val = get
                        message = f"Gợi ý: Dòng {r+1}, Cột {c+1} là số {val}"
                        msg_time = time.time()
                        selected = (r, c)
                    else:
                        message = "Không tìm thấy gợi ý!"
                        msg_time = time.time()

            if event.type == pygame.KEYDOWN and selected and not game_over:
                r, c = selected
                if org[r][c] == 0:
                    if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                        val = int(event.unicode)
                        if note_mode:
                            if val in notes[r][c]:
                                notes[r][c].remove(val)
                            else:
                                notes[r][c].add(val)
                        else:
                            if val != solved_board[r][c]:
                                mistakes += 1
                                msg_time = time.time()
                                if mistakes >= 3:
                                    game_over = True
                                    final_time = int(time.time() - start_time)
                                    message = "Thua cuộc! Bạn đã nhập sai quá 3 lần."
                                else:
                                    message = f"Sai! Số {val} không đúng. Bạn còn {3 - mistakes} cơ hội."
                            else:
                                old_val = board[r][c]
                                if old_val != val:
                                    push(undo_stack, {"row": r, "col": c, "old_val": old_val, "new_val": val})
                                    while not is_empty(redo_stack):
                                        pop(redo_stack)
                                    board[r][c] = val
                                    if board == solved_board:
                                        game_over = True
                                        final_time = int(time.time() - start_time)
                                        message = "Chúc mừng! Bạn đã giải thành công!"
                                        msg_time = time.time()
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                        old_val = board[r][c]
                        if old_val != 0:
                            push(undo_stack, {"row": r, "col": c, "old_val": old_val, "new_val": 0})
                            while not is_empty(redo_stack):
                                pop(redo_stack)
                            board[r][c] = 0

if __name__ == "__main__":
    main()