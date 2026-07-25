# Các file cấp gốc cần cập nhật để hoàn thiện Mission "Revenue Notification Message"

Mission mới không tự động xuất hiện trong các file cấu hình cấp gốc — cần bổ sung thủ công như sau:

## 1. `README.md` (cấp gốc)

Thêm "Revenue Notification Message" vào mục "Danh sách Mission":

```
## Danh sách Mission

Communication
Planning
Reporting
Knowledge
Báo giá (Quotation)
Revenue Notification Message
...
```

## 2. `CLAUDE.md`

Thêm vào danh sách ví dụ Stateless Mission (Mission này không lưu trạng thái — mỗi lần chạy xử lý trọn vẹn 1 yêu cầu công ty + kỳ, không phụ thuộc lần chạy trước):

```
## Stateless Mission

Không lưu trạng thái.

Ví dụ:

Meeting Note
Financial Analysis
Báo giá (Quotation)
Revenue Notification Message
...
```

## 3. `shared/naming-convention.md`

Thêm quy ước đặt tên mới:

```
## Revenue Notification

missions/revenue-notification/output/RevenueNotification_<MãCôngTy>_<MãKỳ>_<yyyyMMdd_HHmm>.md
```

(Chi tiết quy tắc `<MãKỳ>` xem `missions/revenue-notification/rules.md`.)

## 4. Thư mục Mission

Tạo thư mục `missions/revenue-notification/` gồm các file đã soạn:

- `mission.md`
- `workflow.md`
- `rules.md`
- `mapping.md`
- `examples.md`
- `checklist.md`
- `definition-of-done.md`

Và thư mục `missions/revenue-notification/output/` để lưu Artifact (email draft).

## 5. Vấn đề cần xác nhận thêm trước khi đưa Mission vào sử dụng chính thức

`mapping.md` của Mission này đang đánh dấu 5 cột trong `DATA Revenue` là "chưa xác nhận ý nghĩa" (Số hợp đồng/Số Báo giá, Doanh thu, Nhân sự, Số hóa đơn, cột "Số") và tạm thời loại các cột này khỏi nội dung email. Nếu về sau cần dùng các cột này (ví dụ để trích dẫn số hợp đồng/báo giá trong email cho khách hàng), cần người quản lý file "SGA_Revenue & Debt" xác nhận lại ý nghĩa từng cột và cập nhật `mapping.md` cho khớp.
