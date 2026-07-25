# Mapping giữa DATA Revenue và nội dung Email thông báo phí

> Mapping dưới đây được đối chiếu với dữ liệu thật trong file "Bản sao của SGA_Revenue & Debt_2026", sheet `DATA Revenue` (đọc ngày 2026-07-25). **Một số cột có ý nghĩa chưa rõ ràng hoặc dữ liệu mẫu có dấu hiệu bất thường** — các cột này được liệt kê riêng ở mục "Cột chưa xác nhận" và **không được đưa vào nội dung email** cho đến khi người quản lý xác nhận lại ý nghĩa.

## Vị trí dữ liệu

- Sheet: `DATA Revenue`.
- Header nằm ở **hàng 9**, dữ liệu bắt đầu từ **hàng 10**.
- Khóa lọc: cột B (Mã công ty) + cột M (Phân loại doanh thu = loại kỳ: "Tháng" / "Quý" / "Năm" / "Lần") + cột N (Kỳ = giá trị kỳ, ví dụ 1–12 cho Tháng, 1–4 cho Quý, năm cho Năm).

## Cột dùng trong nội dung email

| Cột | Tên cột / ý nghĩa | Dùng vào |
|---|---|---|
| B | Mã công ty | Xác định đúng khách hàng, khóa lọc |
| C | Mã số thuế | Ghi trong email (đối chiếu khách hàng) |
| H | Loại dịch vụ (Long-term x / Short-term) | Ghi rõ loại dịch vụ trong email |
| I / J / K | Gói PT-TK / Gói nhân sự / Gói pháp chế (cấp độ dịch vụ) | Ghi cấp độ gói tương ứng với dịch vụ trong email (chỉ ghi cột có giá trị khớp dịch vụ ở cột H/L) |
| L | Chi tiết dịch vụ | Tên dịch vụ cụ thể trong email |
| M | Phân loại doanh thu (loại kỳ: Tháng/Quý/Năm/Lần) | Khóa lọc + ghi rõ kỳ trong email |
| N | Kỳ (giá trị kỳ) | Khóa lọc + ghi rõ kỳ trong email (vd "Tháng 6", "Quý 1", "Năm 2026") |
| O | Ngày (ngày chốt/kết thúc kỳ) | Ghi trong email làm mốc thời gian phát sinh phí |
| S | Phí dịch vụ Kế toán | Liệt kê trong bảng chi tiết phí (nếu có giá trị) |
| T | Phí dịch vụ HCNS | Liệt kê trong bảng chi tiết phí (nếu có giá trị) |
| U | Phí dịch vụ Pháp lý | Liệt kê trong bảng chi tiết phí (nếu có giá trị) |
| V | Phụ phí hóa đơn | Liệt kê trong bảng chi tiết phí (nếu có giá trị) |
| W | Thành tiền chi phí (trước VAT) | Ghi rõ "Tạm tính (chưa VAT)" |
| X | VAT (%) | Ghi rõ % VAT áp dụng |
| Y | Tiền VAT | Ghi rõ tiền VAT |
| Z | Thành tiền bao gồm VAT | Ghi rõ **Tổng cộng (đã gồm VAT)** — số tiền chính cần thông báo |

Chỉ liệt kê các dòng phí (S/T/U/V) có giá trị khác rỗng/0; dòng nào rỗng thì bỏ qua, không ghi "0đ" gây rối nội dung email.

## Cột KHÔNG dùng (theo yêu cầu người dùng — email chỉ thông báo phí phát sinh, không nêu trạng thái thanh toán)

- AC (Ngày phải thu), AD (Đã thanh toán), AE (Còn lại phải thu), AI (Tình trạng) — **không đưa vào email**, dù có dữ liệu.

## Cột chưa xác nhận (KHÔNG dùng cho đến khi được xác nhận ý nghĩa)

| Cột | Tên cột theo header | Vấn đề quan sát được |
|---|---|---|
| E | Số hợp đồng | Trong dữ liệu mẫu luôn rỗng; giá trị dạng "001/LT/2025" lại nằm ở cột F ("Số Báo giá") — nghi ngờ 2 cột E/F bị lệch nhãn tiêu đề so với dữ liệu thực tế. Cần xác nhận trước khi dùng số hợp đồng/báo giá trong email. |
| P | Doanh thu | Giá trị trong dữ liệu mẫu lớn bất thường so với các khoản phí (hàng tỷ đồng so với vài triệu đồng phí dịch vụ) — nghi là dữ liệu tham chiếu/liên kết từ nguồn khác (không phải doanh thu của riêng dòng phí này). Không dùng cho đến khi xác nhận. |
| Q | Nhân sự | Chưa rõ đơn vị/ý nghĩa (số lượng nhân sự công ty khách hàng? số nhân sự SGA phụ trách?). Không dùng. |
| R | Số hóa đơn | Rỗng ở phần lớn dữ liệu mẫu đã xem — không chắc là số hóa đơn thực tế hay placeholder. Không dùng. |
| AG | Số | Tên cột chỉ ghi "Số", không rõ ý nghĩa (có thể là số ngày, xem cột AB "Số ngày thu" ở gần đó). Không dùng. |

## Xử lý khi công ty có nhiều dịch vụ trong cùng kỳ

Theo xác nhận của người dùng: **tách riêng 1 email / dịch vụ**. Nếu lọc theo (Mã công ty + Phân loại doanh thu + Kỳ) ra nhiều hơn 1 dòng dữ liệu (ví dụ công ty vừa có dòng Long-term vừa có dòng Short-term cùng rơi vào "Quý 1"), Mission tạo N email riêng biệt, mỗi email chỉ chứa đúng 1 dòng dịch vụ.

## Khi không tìm thấy dữ liệu khớp

Nếu không có dòng nào trong `DATA Revenue` khớp đúng (Mã công ty + Phân loại doanh thu + Kỳ) được yêu cầu, **không tự suy diễn hoặc tạo email giả định** — báo lại cho người dùng là không tìm thấy dữ liệu phí cho công ty/kỳ đó, và gợi ý kiểm tra lại chính tả mã công ty hoặc kỳ.

## Thông tin tài khoản thanh toán

> **Cập nhật 2026-07-25:** Mẫu email thật (do người dùng cung cấp, xem `examples.md`) luôn kèm khối "Quý Công ty thanh toán theo thông tin sau" — thông tin tài khoản nhận tiền, khác nhau tùy loại dịch vụ. Danh sách tài khoản và quy tắc chọn được lưu tại `templates/bank-accounts.md`.

Tóm tắt quy tắc chọn tài khoản theo dịch vụ:

| Loại dịch vụ | Tài khoản |
|---|---|
| Cho thuê văn phòng / chỗ ngồi cố định | TK1 — Vietcombank (CT TNHH SAIGON ALH) |
| Hóa đơn điện tử (HDDT) / dịch vụ liên quan Viettel | TK3 — VPBank cá nhân (NGUYEN THI THUY HANG) |
| Dịch vụ SGA thông thường khác (kế toán/HCNS/pháp lý) | TK2 — MB (CONG TY TNHH SAIGON ALH) |

Nếu dịch vụ không khớp rõ ràng nhóm nào ở trên, hỏi lại người dùng — không tự đoán tài khoản.

**Nội dung chuyển khoản (`{{noi_dung}}`) — CHƯA XÁC ĐỊNH được công thức đầy đủ**, đặc biệt là nguồn của "tên viết tắt khách hàng" xuất hiện trong nội dung mẫu (vd "MIN HOME") — không có trong `DATA Revenue`. Cho đến khi có xác nhận, để trống trường `{{noi_dung}}` trong email và ghi chú "Chưa được cung cấp — cần người dùng điền tay nội dung chuyển khoản trước khi gửi". Xem chi tiết quan sát tại `templates/bank-accounts.md`.
