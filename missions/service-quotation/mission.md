# Mission: Báo giá (Quotation)

## Mục tiêu

Đóng vai trò trợ lý giám đốc, tự động tạo báo giá cho khách hàng từ dữ liệu khách hàng có sẵn, giúp giảm thao tác thủ công khi cần báo giá cho nhiều khách hàng cùng lúc.

Sau khi thực hiện, AI phải:

- Đọc toàn bộ danh sách khách hàng từ file Client Information (Excel).
- Với mỗi khách hàng, thêm đúng 1 dòng tương ứng vào file Summary Quotation.
- Mapping dữ liệu khách hàng vào đúng cột theo Template Summary Quotation.
- Sinh ra 1 file Quotation riêng (Single Quotation) cho từng khách hàng, dựa trên Template Single Quotation.
- Lưu toàn bộ Artifact theo đúng quy ước đặt tên.
- Báo cáo lại số lượng khách hàng đã xử lý và danh sách Artifact đã sinh.

## Trigger

### Thủ công

Ví dụ:

- "Tạo báo giá cho danh sách khách hàng này."
- "Cập nhật Summary Quotation từ file Client Information."
- "Sinh báo giá cho các khách hàng trong file này."
- "Đây là file khách hàng, hãy tạo báo giá."

## Input

- File Client Information (Excel) — danh sách khách hàng cần báo giá. Mỗi dòng dữ liệu tương ứng 1 khách hàng.
- Template Summary Quotation — nằm trong `missions/quotation/templates/`.
- Template Single Quotation — nằm trong `missions/quotation/templates/`.

## Output

- 1 file Summary Quotation đã được cập nhật (thêm N dòng, N = số khách hàng trong Client Information).
- N file Quotation riêng lẻ (1 file / khách hàng).

## Quan hệ N khách hàng — N dòng — N file

Số khách hàng trong Client Information phải khớp chính xác với:

- Số dòng mới được thêm vào Summary Quotation.
- Số file Single Quotation được sinh ra.

Ví dụ: 3 khách hàng trong Client Information → 3 dòng mới trong Summary Quotation → 3 file Quotation riêng.
