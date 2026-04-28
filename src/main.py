import pygame
import sys
import copy
import time
from sudoku_core import gen_dif, hint, check
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
LIGHT_BLUE = (173, 216, 230)

font = pygame.font.SysFont("arial", 40)
note_font = pygame.font.SysFont("arial", 15)
btn_font = pygame.font.SysFont("arial", 20)
msg_font = pygame.font.SysFont("arial", 25)

def draw_grid():
    for i in range(10):
        thick = 4 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (30, 30 + i * 60), (570, 30 + i * 60), thick)
        pygame.draw.line(screen, BLACK, (30 + i * 60, 30), (30 + i * 60, 570), thick)

def draw_board(board, org, selected):
    if selected:
        r, c = selected
        pygame.draw.rect(screen, LIGHT_BLUE, (30 + c * 60, 30 + r * 60, 60, 60))
    draw_grid()
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                color = BLACK if org[i][j] != 0 else BLUE
                text = font.render(str(board[i][j]), True, color)
                rect = text.get_rect(center=(30 + j * 60 + 30, 30 + i * 60 + 30))
                screen.blit(text, rect)

def draw_notes(notes, board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for n in notes[i][j]:
                    r = (n - 1) // 3
                    c = (n - 1) % 3
                    text = note_font.render(str(n), True, GRAY)
                    screen.blit(text, (30 + j * 60 + 8 + c * 20, 30 + i * 60 + 5 + r * 20))

def draw_button(text, x, y, w, h, active=False):
    color = LIGHT_BLUE if active else GRAY
    pygame.draw.rect(screen, color, (x, y, w, h))
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 2)
    txt_surf = btn_font.render(text, True, BLACK)
    txt_rect = txt_surf.get_rect(center=(x + w//2, y + h//2))
    screen.blit(txt_surf, txt_rect)
    return pygame.Rect(x, y, w, h)

def main():
    dif_levels = ["Easy", "Medium", "Hard"]
    dif_idx = 0
    board = gen_dif(dif_levels[dif_idx])
    org = copy.deepcopy(board)
    undo_stack = create_stack()
    redo_stack = create_stack()
    notes = [[set() for _ in range(9)] for _ in range(9)]
    selected = None
    note_mode = False
    message = ""
    msg_time = 0

    running = True
    while running:
        screen.fill(WHITE)
        draw_board(board, org, selected)
        draw_notes(notes, board)

        btn_new = draw_button("New Game", 30, 600, 120, 40)
        btn_dif = draw_button(f"Diff: {dif_levels[dif_idx]}", 160, 600, 140, 40)
        btn_note = draw_button("Note: ON" if note_mode else "Note: OFF", 310, 600, 120, 40, note_mode)
        
        btn_undo = draw_button("Undo", 30, 650, 100, 40)
        btn_redo = draw_button("Redo", 140, 650, 100, 40)
        btn_hint = draw_button("Hint", 250, 650, 100, 40)

        if message and time.time() - msg_time < 3:
            msg_surf = msg_font.render(message, True, RED)
            screen.blit(msg_surf, (30, 700))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 30 <= pos[0] <= 570 and 30 <= pos[1] <= 570:
                    c = (pos[0] - 30) // 60
                    r = (pos[1] - 30) // 60
                    selected = (r, c)
                elif btn_new.collidepoint(pos):
                    board = gen_dif(dif_levels[dif_idx])
                    org = copy.deepcopy(board)
                    undo_stack = create_stack()
                    redo_stack = create_stack()
                    notes = [[set() for _ in range(9)] for _ in range(9)]
                    selected = None
                    message = "New game started!"
                    msg_time = time.time()
                elif btn_dif.collidepoint(pos):
                    dif_idx = (dif_idx + 1) % 3
                elif btn_note.collidepoint(pos):
                    note_mode = not note_mode
                elif btn_undo.collidepoint(pos):
                    move = pop(undo_stack)
                    if move:
                        push(redo_stack, {"row": move["row"], "col": move["col"], "old_val": board[move["row"]][move["col"]], "new_val": move["old_val"]})
                        board[move["row"]][move["col"]] = move["old_val"]
                elif btn_redo.collidepoint(pos):
                    move = pop(redo_stack)
                    if move:
                        push(undo_stack, {"row": move["row"], "col": move["col"], "old_val": board[move["row"]][move["col"]], "new_val": move["new_val"]})
                        board[move["row"]][move["col"]] = move["new_val"]
                elif btn_hint.collidepoint(pos):
                    get = hint(board)
                    if get:
                        r, c, val = get
                        message = f"Gợi ý: ({r}, {c}) = {val}"
                        msg_time = time.time()
                        selected = (r, c)
                    else:
                        message = "Không tìm thấy gợi ý!"
                        msg_time = time.time()

            if event.type == pygame.KEYDOWN and selected:
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
                            old_val = board[r][c]
                            board[r][c] = 0
                            if not check(board, r, c, val):
                                message = f"Sai luật! Số {val} bị trùng."
                                msg_time = time.time()
                                board[r][c] = old_val 
                            else:
                                if old_val != val:
                                    push(undo_stack, {"row": r, "col": c, "old_val": old_val, "new_val": val})
                                    while not is_empty(redo_stack):
                                        pop(redo_stack)
                                    board[r][c] = val
                                else:
                                    board[r][c] = old_val 
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                        old_val = board[r][c]
                        if old_val != 0:
                            push(undo_stack, {"row": r, "col": c, "old_val": old_val, "new_val": 0})
                            while not is_empty(redo_stack):
                                pop(redo_stack)
                            board[r][c] = 0

if __name__ == "__main__":
    main()
