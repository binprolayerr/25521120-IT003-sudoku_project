import copy
from sudoku_core import gen_dif, hint, print_board
from stack import create_stack, push, pop, is_empty

def main():
    print("=== CHÀO MỪNG ĐẾN VỚI SUDOKU ===")
    print("Chọn cấp độ khó:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    choice = input("Nhập lựa chọn (1/2/3): ").strip()
    dif_map = {"1": "Easy", "2": "Medium", "3": "Hard"}
    dif = dif_map.get(choice, "Easy")
    print(f"\nĐang tạo bảng với độ khó: {dif}...")
    board = gen_dif(dif)
    org = copy.deepcopy(board) 
    undo_stack = create_stack()
    redo_stack = create_stack()
    while True:
        print("\n" + "="*30)
        print_board(board)
        print("="*30)
        print("HƯỚNG DẪN LỆNH:")
        print(" - Điền số: Nhập [Hàng] [Cột] [Số] (Ví dụ: 0 1 5 -> điền 5 vào hàng 0 cột 1)")
        print(" - Undo: Nhập 'u'")
        print(" - Redo: Nhập 'r'")
        print(" - Gợi ý: Nhập 'h'")
        print(" - Thoát: Nhập 'q'")
        cmd = input(">>> Nhập lệnh của bạn: ").strip().lower().split()
        if not cmd:
            continue
        action = cmd[0]
        if action == 'q':
            print("Cảm ơn bạn đã chơi!")
            break
        elif action == 'u':
            move = pop(undo_stack)
            if move:
                push(redo_stack,{
                    "row": move["row"], 
                    "col": move["col"], 
                    "old_val": board[move["row"]][move["col"]], 
                    "new_val": move["old_val"]
                })
                board[move["row"]][move["col"]] = move["old_val"]
                print(f"Đã Undo ô ({move['row']}, {move['col']}).")
            else:
                print("Không có bước đi nào để Undo.")
        elif action == 'r':
            move = pop(redo_stack)
            if move:
                push(undo_stack,{
                    "row": move["row"], 
                    "col": move["col"], 
                    "old_val": board[move["row"]][move["col"]], 
                    "new_val": move["new_val"]
                })
                board[move["row"]][move["col"]] = move["new_val"] 
                print(f"Đã Redo ô ({move['row']}, {move['col']}).")
            else:
                print("Không có bước đi nào để Redo.")
        elif action == 'h':
            get = hint(board)
            if get:
                r, c, val = get
                print(f"Gợi ý: Bạn có thể điền số {val} vào Hàng {r}, Cột {c}.")
        elif len(cmd) == 3:
            try:
                r, c, v = int(cmd[0]), int(cmd[1]), int(cmd[2])
                if r < 0 or r > 8 or c < 0 or c > 8 or v < 0 or v > 9:
                    print("Hàng, cột phải từ 0-8. Giá trị từ 1-9.")
                    continue             
                if org[r][c] != 0:
                    print("Bạn không thể sửa ô cố định của đề bài!")
                    continue
                old_val = board[r][c]
                if old_val != v:
                    push(undo_stack, {"row": r, "col": c, "old_val": old_val, "new_val": v})
                    while not is_empty(redo_stack):
                        pop(redo_stack)
                    board[r][c] = v
                    print(f"✅ Đã điền {v} vào ({r}, {c}).")
            except ValueError:
                print("Lệnh không hợp lệ. Vui lòng nhập số.")
        else:
            print("Lệnh không hợp lệ.")

if __name__ == "__main__":
    main()