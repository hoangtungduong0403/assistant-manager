# Quy trình thực hiện

## Bước 1

Xác định yêu cầu từ người dùng:

- Công ty (mã hoặc tên) — bắt buộc.
- Kỳ: loại kỳ (Tháng / Quý / Năm / Lần) + giá trị kỳ (vd Tháng 6, Quý 1, Năm 2026) — bắt buộc.
- Dịch vụ cụ thể (nếu người dùng chỉ muốn thông báo 1 dịch vụ nhất định thay vì tất cả dịch vụ trong kỳ đó) — tùy chọn.

Nếu thiếu công ty hoặc kỳ, hỏi lại người dùng trước khi tiếp tục — không tự đoán.

## Bước 2

Đọc sheet `DATA Revenue` của file "SGA_Revenue & Debt" (dữ liệu từ hàng 10, header hàng 9 — xem `mapping.md`).

Lọc các dòng khớp:

- Cột B (Mã công ty) = công ty được yêu cầu (so khớp không phân biệt hoa/thường).
- Cột M (Phân loại doanh thu) = đúng loại kỳ được yêu cầu.
- Cột N (Kỳ) = đúng giá trị kỳ được yêu cầu.
- Nếu người dùng chỉ định dịch vụ cụ thể, lọc thêm theo cột H (Loại dịch vụ) và/hoặc cột L (Chi tiết dịch vụ).

## Bước 3

Nếu không có dòng nào khớp → dừng lại, báo cho người dùng là không tìm thấy dữ liệu phí cho công ty/kỳ đó, gợi ý kiểm tra lại mã công ty hoặc kỳ. Không tự tạo email với dữ liệu giả định.

Nếu có ≥ 1 dòng khớp → với mỗi dòng, coi là 1 dịch vụ riêng cần thông báo (xem `mapping.md` mục "Xử lý khi công ty có nhiều dịch vụ trong cùng kỳ").

## Bước 4

Với mỗi dòng dữ liệu khớp, trích xuất các trường theo `mapping.md` (chỉ dùng cột đã xác nhận, bỏ qua cột "chưa xác nhận"):

- Tên/Mã công ty, MST.
- Loại dịch vụ, cấp độ gói tương ứng, chi tiết dịch vụ.
- Kỳ (loại kỳ + giá trị kỳ), ngày chốt kỳ.
- Các khoản phí có giá trị (Kế toán / HCNS / Pháp lý / Phụ phí hóa đơn).
- Thành tiền trước VAT, % VAT, tiền VAT, thành tiền sau VAT (tổng cần thông báo).

Nếu 1 trường bắt buộc bị thiếu dữ liệu (vd MST rỗng), ghi "Chưa được cung cấp" trong email — không tự suy diễn hoặc điền thay.

## Bước 5

Soạn nội dung email theo mẫu (xem `examples.md`):

- Văn phong: trang trọng, đầy đủ chi tiết (email).
- Không đề cập trạng thái thanh toán, hạn thu, hay số tiền còn lại phải thu — chỉ thông báo phí phát sinh trong kỳ (theo xác nhận của người dùng).
- Dùng công cụ soạn message (`message_compose_v1`, kind = "email") để tạo bản nháp — **không tự gửi email**.

## Bước 6

Lưu nội dung từng email đã soạn thành 1 Artifact riêng (file `.md`), theo đúng quy ước đặt tên tại `rules.md`.

## Bước 7

Tổng hợp kết quả trả lời người dùng:

- Công ty, kỳ đã xử lý.
- Số lượng email đã tạo (tương ứng số dịch vụ tìm thấy).
- Danh sách Artifact đã lưu.
- Các trường bị thiếu dữ liệu (nếu có), đã ghi "Chưa được cung cấp".
- Nếu có cột dữ liệu "chưa xác nhận" (xem `mapping.md`) liên quan trực tiếp đến công ty/kỳ đang xử lý, nhắc người dùng biết là các cột này chưa được đưa vào email do chưa xác nhận ý nghĩa.
