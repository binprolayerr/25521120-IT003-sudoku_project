# Đồ án: Phát triển ứng dụng game Sudoku

**Môn học:** Cấu trúc dữ liệu và Giải thuật (DSA)

**Trường:** Đại học Công nghệ Thông tin (UIT) - ĐHQG-HCM

**Sinh viên thực hiện:** Nguyễn Phúc Bình Minh

**MSSV:** 25521120

## Mô tả dự án
Trò chơi Sudoku truyền thống trên lưới 9x9 được phát triển bằng Python. Dự án tập trung vào việc áp dụng các cấu trúc dữ liệu (Mảng 2 chiều, stack cho Undo/Redo) và giải thuật (backtracking) để tạo ra các tính năng như sinh đề, kiểm tra tính hợp lệ và đặc biệt là hệ thống hỗ trợ gợi ý (Hint) thông minh cho người chơi.

## Tiến độ (Phase 1)
- Cài đặt CTDL Stack
- Thuật toán kiểm tra tính hợp lệ của Sudoku
- Thuật toán backtracking giải Sudoku
## Tiến độ (Phase 2)
- Hoàn thiện thuật toán sinh đề
- Tích hợp hệ thống Undo/Redo
- Phát triển tính năng Gợi ý
## Tiến độ (Phase 3)
- Xây dựng giao diện đồ họa tương tác trực quan bằng thư viện Pygame
- Xử lý các thao tác đầu vào của người chơi
- Phát triển tính năng Note mode hỗ trợ người chơi lưu nháp nhiều đáp án khả thi
- Tích hợp hệ thống cảnh báo lỗi hiển thị trên màn hình và tự động ngăn chặn các nước đi vi phạm luật Sudoku
## Tiến độ (Phase 4)
- Nâng cấp thuật toán đếm nghiệm để sinh đề Sudoku luôn đảm bảo tính duy nhất của lời giải
- Phát triển hệ thống đối chiếu đáp án trực tiếp, giới hạn tối đa 3 lần sai và xử lý logic kết thúc trò chơi (Game Over/Win)
- Bổ sung tính năng đồng hồ đếm thời gian giúp người chơi theo dõi thời gian giải
- Khắc phục lỗi hiển thị font chữ tiếng Việt trên Pygame và gỡ lỗi hoàn thiện logic luân chuyển dữ liệu của cấu trúc stack trong thao tác Undo/Redo.
