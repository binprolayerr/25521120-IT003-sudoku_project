## 1. File `stack.py`

### Các hàm chính:

- **`create_stack()`**  
  Khởi tạo một ngăn xếp mới.

- **`is_empty(stack)`**  
  Kiểm tra xem ngăn xếp hiện tại có rỗng hay không.

- **`push(stack, item)`**  
  Thêm một phần tử mới vào đỉnh (cuối list) của ngăn xếp.

- **`peek(stack)`**  
  Trả về phần tử ở đỉnh của ngăn xếp mà không xóa nó khỏi ngăn xếp.

- **`pop(stack)`**  
  Lấy và xóa phần tử ở đỉnh của ngăn xếp.

## 2. File `sudoku_core.py`

### Các hàm chính:

- **`check(board, row, col, num)`**  
  Kiểm tra xem việc đặt số `num` vào vị trí `(row, col)` trên bảng có vi phạm luật Sudoku không.

- **`solve(board)`**  
  Giải bảng Sudoku sử dụng thuật toán đệ quy.  
  Hàm này sẽ sửa đổi trực tiếp trên biến `board` được truyền vào.

- **`gen_board()`**  
  Sinh ra một bảng Sudoku đã được giải hoàn chỉnh và hợp lệ.  
  Hàm sử dụng `random.shuffle()` để đảm bảo mỗi lần chạy sẽ sinh ra một bảng hoàn toàn khác nhau.

- **`gen_dif(dif="Easy")`**  
  Tạo đề bài Sudoku từ một bảng hoàn chỉnh bằng cách khoét lỗ ngẫu nhiên theo cấp độ khó.

- **`hint(cur)`**  
  Dùng thuật toán giải ngầm trên một bản sao của bảng hiện tại để tìm ra giá trị đúng cho một ô trống chưa điền.

- **`print_board(board)`**  
  Định dạng và in bảng Sudoku ra màn hình console để người chơi dễ quan sát,  
  bao gồm các đường gạch ngang `-` và dọc `|` để phân tách các khối 3x3.

## 3. File `main.py`

### Hàm chính: `main()`

Chạy vòng lặp chính của ứng dụng trên giao diện Pygame. Luồng hoạt động:

#### 1. Thiết lập ban đầu
- Khởi tạo bảng với độ khó mặc định thông qua `gen_dif()`
- Sao chép bảng gốc `org` để chặn người dùng ghi đè lên số của đề bài
- Khởi tạo:
  - `undo_stack`
  - `redo_stack` (từ module `stack.py`)
  - Cấu trúc dữ liệu `notes` để quản lý ghi chú nháp


#### 2. Render giao diện
Trong vòng lặp `while running`:
- Vẽ lưới Sudoku
- Hiển thị các con số:
  - Phân biệt màu sắc giữa số gốc và số người chơi nhập
- Hiển thị:
  - Số ghi chú
  - Các nút chức năng
  - Thông báo

#### 3. Xử lý Mouse Events
- **Click vào lưới:**  
  Cập nhật tọa độ ô đang được chọn

- **Click nút bấm:**  
  Kích hoạt các chức năng:
  - New Game
  - Đổi độ khó
  - Bật/Tắt chế độ Note
  - Undo / Redo
  - Hint

#### 4. Xử lý Keyboard Events (khi đã chọn ô trống)

- **Phím số (1–9):**
  - **Chế độ Note bật:**  
    Thêm hoặc xóa số nháp vào `notes`
  - **Chế độ Note tắt:**  
    - Gọi `check()` để kiểm tra hợp lệ
    - Nếu hợp lệ:
      - Cập nhật `board`
      - Lưu trạng thái vào `undo_stack`
      - Xóa `redo_stack`
    - Nếu không hợp lệ:
      - Từ chối nhập
      - Hiển thị thông báo lỗi

- **Phím Xóa (Backspace/Delete):**
  - Xóa số đã nhập
  - Đưa ô về trạng thái trống (`0`)
  - Lưu lịch sử vào `undo_stack`

#### 5. Logic các tính năng hỗ trợ

- **Undo:**
  - Lấy trạng thái gần nhất từ `undo_stack`
  - Khôi phục giá trị cũ trên `board`
  - Đưa trạng thái vào `redo_stack`

- **Redo:**
  - Lấy thao tác từ `redo_stack`
  - Áp dụng lại lên `board`
  - Đưa lại vào `undo_stack`

- **Hint:**
  - Gọi hàm `hint()`
  - Tự động chọn ô hợp lệ
  - Hiển thị gợi ý số đúng
