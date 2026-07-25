# Mission: Revenue Notification Message

## Mục tiêu

Đóng vai trò trợ lý giám đốc, soạn **email thông báo phí dịch vụ** phát sinh của 1 công ty khách hàng trong 1 kỳ cụ thể (Tháng / Quý / Năm / Lần), dựa trên dữ liệu thật trong sheet `DATA Revenue` của file "SGA_Revenue & Debt".

Sau khi thực hiện, AI phải:

- Xác định đúng công ty và đúng kỳ theo yêu cầu.
- Lọc đúng (các) dòng dữ liệu phí dịch vụ khớp công ty + kỳ trong `DATA Revenue`.
- Nếu công ty có nhiều dịch vụ phát sinh trong cùng kỳ đó, tách thành **nhiều email riêng, 1 email / dịch vụ**.
- Soạn nội dung email trang trọng, đầy đủ chi tiết khoản phí (không đề cập trạng thái thanh toán/hạn thu — xem `rules.md`).
- Không tự gửi email — chỉ tạo bản nháp (draft), việc gửi do người dùng quyết định (theo `CLAUDE.md`).
- Lưu Artifact (nội dung email đã soạn) theo đúng quy ước đặt tên.

## Trigger

### Thủ công

Ví dụ:

- "Tạo message thông báo phí cho công ty 2CE, Quý 1."
- "Soạn email thông báo phí dịch vụ tháng 6 cho khách hàng ABC."
- "Thông báo phí Long-term Quý 3 cho 2HITACHI."

Người dùng cần cung cấp tối thiểu:

- Công ty (mã hoặc tên).
- Kỳ: loại kỳ (Tháng / Quý / Năm / Lần) + giá trị kỳ (vd Tháng 6, Quý 1, Năm 2026).

Nếu thiếu 1 trong 2 thông tin trên, hỏi lại người dùng — không tự đoán.

## Input

- File "SGA_Revenue & Debt" (Google Sheet hoặc bản xuất `.xlsx`) — sheet `DATA Revenue`, dữ liệu bắt đầu từ hàng 10 (header ở hàng 9). Xem cấu trúc cột đầy đủ tại `mapping.md`.

## Output

- 1 email nháp (draft) cho mỗi dịch vụ phát sinh của công ty trong kỳ được yêu cầu — có thể là 1 hoặc nhiều email tùy số dịch vụ.
- Mỗi email lưu thành 1 Artifact riêng theo quy ước đặt tên tại `rules.md`.

## Quan hệ N dịch vụ — N email

Nếu công ty có N dòng dữ liệu (N dịch vụ) khớp đúng công ty + đúng kỳ trong `DATA Revenue`, Mission phải tạo ra đúng N email riêng biệt — không gộp nhiều dịch vụ vào 1 email, không bỏ sót dịch vụ nào.
