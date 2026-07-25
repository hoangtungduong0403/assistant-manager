# Quy tắc làm việc

Luôn sử dụng dữ liệu thật từ sheet `DATA Revenue`. Không tự tính toán lại số tiền, không tự suy diễn hoặc bổ sung dữ liệu không có trong nguồn.

Không tự ý gửi email — Mission chỉ tạo bản nháp (draft) bằng công cụ soạn message; việc gửi đi do người dùng quyết định (theo nguyên tắc chung tại `CLAUDE.md`: "Không tự ý gửi Email... trừ khi Mission hiện tại cho phép").

Email chỉ thông báo **phí phát sinh trong kỳ** — không đề cập trạng thái thanh toán, hạn thu, số tiền còn lại phải thu (cột AC/AD/AE/AI của `DATA Revenue`), theo xác nhận của người dùng khi thiết lập Mission này.

Nếu công ty có nhiều dịch vụ/dòng phí phát sinh trong cùng 1 kỳ được yêu cầu, luôn tách thành **email riêng cho từng dịch vụ** — không gộp nhiều dịch vụ vào 1 email.

Không sử dụng các cột dữ liệu chưa xác nhận ý nghĩa (xem `mapping.md` mục "Cột chưa xác nhận": Số hợp đồng/Số Báo giá, Doanh thu, Nhân sự, Số hóa đơn, cột "Số") trong nội dung email.

Nếu không tìm thấy dữ liệu khớp đúng công ty + kỳ được yêu cầu, không tự tạo email với dữ liệu giả định — báo lại cho người dùng.

Nếu một trường bắt buộc trong email bị thiếu dữ liệu nguồn, ghi rõ "Chưa được cung cấp", không tự suy diễn hoặc điền giá trị thay thế.

Văn phong và cấu trúc email: theo đúng **template thật** tại `examples.md` (đã xác nhận với người dùng 2026-07-25) — không dùng bảng markdown hay văn phong trang trọng kiểu công văn. Mỗi email luôn kèm khối "Quý Công ty thanh toán theo thông tin sau" với thông tin tài khoản nhận tiền.

## Thông tin tài khoản thanh toán

Chọn tài khoản theo loại dịch vụ, xem quy tắc và danh sách đầy đủ tại `templates/bank-accounts.md`. Nếu dịch vụ không khớp rõ ràng nhóm nào đã định nghĩa, hỏi lại người dùng — không tự đoán tài khoản.

Trường `{{noi_dung}}` (nội dung chuyển khoản) hiện **chưa xác định được công thức đầy đủ** (xem `mapping.md`) — để trống và ghi "Chưa được cung cấp — cần điền tay trước khi gửi" cho đến khi có xác nhận nguồn dữ liệu cho "tên viết tắt khách hàng".

## Quy ước đặt tên Artifact

`missions/revenue-notification/output/RevenueNotification_<MãCôngTy>_<MãKỳ>_<yyyyMMdd_HHmm>.md`

Trong đó `<MãKỳ>` được quy ước:

- Tháng: `T<n>` (vd Tháng 6 → `T6`)
- Quý: `Q<n>` (vd Quý 1 → `Q1`)
- Năm: `Nam<yyyy>` (vd Năm 2026 → `Nam2026`)
- Lần (dịch vụ phát sinh 1 lần, không theo kỳ cố định): `Lan_<ddMMyyyy>` (theo ngày phát sinh ở cột O)

Nếu 1 công ty có nhiều dịch vụ trong cùng kỳ (nhiều email), thêm hậu tố tên dịch vụ viết liền không dấu vào cuối tên file để phân biệt, ví dụ:

- `RevenueNotification_2CE_Q1_LongTerm_20260725_0930.md`
- `RevenueNotification_2CE_Q1_ShortTerm_20260725_0930.md`

## Quy tắc chuẩn hóa tên

- Không sử dụng khoảng trắng, ký tự đặc biệt.
- Chỉ sử dụng chữ cái, số và dấu gạch dưới (_).
- Nếu không có giờ/phút cụ thể trong yêu cầu, lấy thời gian hiện tại tại thời điểm sinh Artifact.
