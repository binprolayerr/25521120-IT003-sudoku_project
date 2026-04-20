## 1. File `stack.py`
### `create_stack()`
Khởi tạo một ngăn xếp mới.
### `is_empty(stack)`
Kiểm tra xem ngăn xếp hiện tại có rỗng hay không.
### `push(stack, item)`
Thêm một phần tử mới vào đỉnh (cuối list) của ngăn xếp.
### `peek(stack)`
Trả về phần tử ở đỉnh của ngăn xếp mà không xóa nó khỏi ngăn xếp.
### `pop(stack)`
Lấy và xóa phần tử ở đỉnh của ngăn xếp.
## 2. File `sudoku_core.py`
### `check(board, row, col, num)`
Kiểm tra xem việc đặt số `num` vào vị trí `(row, col)` trên bảng có vi phạm luật sudoku không.
### `solve(board)`
Giải bảng sudoku sử dụng thuật toán đệ quy. Hàm này sẽ sửa đổi trực tiếp trên biến `board` được truyền vào.
### `gen_board()`
Sinh ra một bảng Sudoku đã được giải hoàn chỉnh và hợp lệ. Hàm sử dụng `random.shuffle()` để đảm bảo mỗi lần chạy sẽ sinh ra một bảng hoàn toàn khác nhau.
### `gen_dif(dif="Easy")`
Tạo đề bài Sudoku từ một bảng hoàn chỉnh bằng cách khoét lỗ ngẫu nhiên theo cấp độ khó.
### `hint(cur)`
Dùng thuật toán giải ngầm trên một bản sao của bảng hiện tại để tìm ra giá trị đúng cho một ô trống chưa điền.
### `print_board(board)`
Định dạng và in bảng Sudoku ra màn hình console để người chơi dễ quan sát bao gồm các đường gạch ngang `-` và dọc `|` để phân tách các khối 3x3.
## 3. File `main.py`
### `main()`
Chạy vòng lặp chính của ứng dụng.
**Luồng hoạt động:**
  1. Hiển thị menu chọn độ khó và khởi tạo bảng thông qua `gen_dif()`.
  2. Sao chép một bảng gốc `org` để chặn người dùng ghi đè lên số của đề bài.
  3. Khởi tạo 2 biến `undo_stack` và `redo_stack` từ module `stack.py`.
  4. Mở vòng lặp `while True` nhận input từ người dùng, xử lý các logic:
* Nhập số: Cập nhật biến `board`, ghi trạng thái vào `undo_stack` và xóa sạch `redo_stack`.
* `u` (Undo): Pop từ `undo_stack`, khôi phục số cũ, push trạng thái vào `redo_stack`.
* `r` (Redo): Pop từ `redo_stack`, cập nhật số mới, push trạng thái vào `undo_stack`.
* `h` (Hint): Gọi `hint()` và in ra màn hình vị trí có thể điền.
* `q` (Quit): Thoát game.
