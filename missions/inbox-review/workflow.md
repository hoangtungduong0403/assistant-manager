# Quy trình thực hiện

## Bước 1

Đọc các email mới kể từ lần kiểm tra gần nhất, trạng thái kiểm tra gần nhất được lưu trong state.json, và xác định phạm vi, thời gian kiểm tra 

## Bước 2

Loại bỏ

- Spam
- Quảng cáo
- Newsletter
- Thông báo hệ thống

(trừ khi được yêu cầu)

## Bước 3

Phân loại email theo 7 nhóm sau:

### Client
Mục đích: Xử lý công việc và doanh thu (thu) của SGA.
Ưu tiên mặc định: Cao

### Government
Mục đích: Tuân thủ pháp lý, tránh trễ hạn/phạt.
Bao gồm: Công văn thuế, Thông báo BHXH, Thông báo từ cơ quan ban ngành,
Yêu cầu bổ sung hồ sơ, Quyết định xử phạt, Giấy mời làm việc.
Ưu tiên mặc định: Khẩn cấp

### Partner
Mục đích: Duy trì vận hành và công nợ — tiền chi của SGA.
Bao gồm: Hóa đơn, Hợp đồng nhà cung cấp, Đề nghị thanh toán, Báo giá đầu vào.
Ưu tiên mặc định: Trung bình

### Internal
Mục đích: Vận hành nội bộ SGA.
Bao gồm: Báo cáo công việc, Xin nghỉ phép, Thông báo nội bộ.
Ưu tiên mặc định: Trung bình

### Khác_SGA
Mục đích: Lưu trữ email liên quan đến SGA nhưng không thuộc các nhóm trên.
Ưu tiên mặc định: Xác định theo nội dung cụ thể (không có mức mặc định cố định).

### Project
Mục đích: Các email liên quan đến dự án/công việc ngoài SGA.
Ưu tiên mặc định: Cao

### Spam
Mục đích: Loại bỏ khỏi báo cáo.
Bao gồm: Quảng cáo, Newsletter, Email không rõ nguồn gốc, Nghi ngờ lừa đảo.
Không báo cáo (theo rules.md hiện hành).

## Bước 4

Đánh giá mức độ ưu tiên

- Khẩn cấp
- Cao
- Trung bình
- Thấp

## Bước 5

Tóm tắt nội dung từng email.

## Bước 6

Trích xuất các công việc cần thực hiện.

## Bước 7

Xác định người phụ trách.

## Bước 8

Đề xuất bước tiếp theo.

## Bước 9

Sinh báo cáo Inbox Review.