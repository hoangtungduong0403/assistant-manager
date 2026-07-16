# Mission: Inbox Review

## Mục tiêu

Đóng vai trò là trợ lý giám đốc, giúp giám đốc nắm bắt nhanh tình hình email mà không cần tự đọc toàn bộ hộp thư.

Sau mỗi lần thực hiện, AI phải:

- Tóm tắt các email mới.
- Phân loại theo mức độ ưu tiên.
- Xác định email cần giám đốc xử lý.
- Trích xuất các công việc phát sinh.
- Đề xuất hành động tiếp theo.
- Không bỏ sót các email quan trọng.

## Tần suất

Tự động

- 08:00
- 14:00
- 18:00

Thủ công

Khi giám đốc yêu cầu.

Ví dụ:

- Kiểm tra email.
- Có email quan trọng không?
- Xem hộp thư giúp tôi.

## Trạng thái Mission

Mission phải lưu trạng thái thực thi vào `state.json`.

Sau mỗi lần hoàn thành cần cập nhật:

- Thời gian chạy
- Thời gian xử lý email gần nhất
- Trạng thái
- Artifact vừa tạo
- Thống kê