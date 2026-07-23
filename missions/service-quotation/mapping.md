# Mapping giữa Client Information và Summary Quotation

## File thực tế đang dùng

- Client Information: `SGA_Client_information.xlsx` — sheet `Information`
- Summary Quotation: `SGA_Summary Quotation_2025.xlsx` — workbook nhiều sheet, không phải 1 bảng đơn

## Cấu trúc thật của Summary Quotation

| Sheet | Vai trò | Có nên ghi dữ liệu mới vào không |
|---|---|---|
| DATA LONG-TERM | Log báo giá/hợp đồng khách Long-term | Có — đích chính khi LOẠI = Long-term 1/2 |
| DATA SHORT-TERM | Log báo giá/hợp đồng khách Short-term | Có — đích chính khi LOẠI = Short-term |
| DATA FEE SERVICE | Log dịch vụ tính phí riêng | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| LT 2025 / ST 2025 | Bảng báo giá gọn theo năm | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| OR 2025 / REPORT | Báo cáo tổng hợp | Chỉ đọc, không ghi |

Một số cột trong DATA LONG-TERM dùng công thức `IMPORTRANGE` trỏ tới Google Sheets ngoài — các công thức này không tính lại được khi thao tác trên file Excel cục bộ, nên dùng giá trị tĩnh lấy trực tiếp từ Client Information thay cho công thức đó (ví dụ Mã số thuế).

## Khóa nối (join key)

`MÃ CÔNG TY` trong Client Information = `MÃ CÔNG TY` (DATA LONG-TERM, cột B) / `MÃ KH` (DATA SHORT-TERM, cột B). Đây là mã ngắn (vd "BRACON", "2CE"), **không phải** `MÃ KHÁCH HÀNG` dạng C0xx.

## Quy tắc phân loại

Dựa vào cột `LOẠI` trong Client Information:
- Chứa "Long-term" (Long-term 1, Long-term 2) → ghi vào sheet **DATA LONG-TERM**
- Chứa "Short-term" → ghi vào sheet **DATA SHORT-TERM**
- Trống hoặc không xác định → **không ghi**, liệt kê riêng để người dùng xác nhận thủ công

## Mapping cột — DATA LONG-TERM

| Cột đích | Nguồn | Ghi chú |
|---|---|---|
| A - STT | Công thức subtotal theo cột B | Theo đúng pattern có sẵn trong sheet |
| B - MÃ CÔNG TY | Client Information > MÃ CÔNG TY | Khóa nối |
| C - Mã số thuế | Client Information > MÃ SỐ THUẾ | Giá trị tĩnh, không dùng công thức IMPORTRANGE cũ |
| D - GHI CHÚ | Ghép từ 3 cột dịch vụ (phân tích-thống kê / nhân sự / pháp chế) + cấp độ (Standard/Premium/Platinum) | Theo đúng format text đang dùng trong sheet |
| E - Số hợp đồng | "CHUA CO" | Giá trị mặc định khớp pattern có sẵn |
| G - Số thứ tự | Tiếp nối chuỗi số hiện có (3 chữ số, vd 101 -> 102) | Không được trùng |
| H - Số hiệu | Công thức nối Số thứ tự với "/LT/2025" | |
| I - ĐVT | "Quý" | Mặc định, có thể cần xác nhận lại theo từng khách hàng |
| J -> N (Hóa đơn, Ngày thực hiện, Ngày hiệu lực, Tình trạng) | -- | Để trống, nhân sự SGA điền tay sau |

## Mapping cột — DATA SHORT-TERM

| Cột đích | Nguồn | Ghi chú |
|---|---|---|
| A - STT | Công thức subtotal theo cột D | |
| B - MÃ KH | Client Information > MÃ CÔNG TY | Khóa nối |
| C - MÃ SỐ THUẾ | Client Information > MÃ SỐ THUẾ | Giá trị tĩnh |
| D - NO. | Tiếp nối chuỗi số hiện có (4 chữ số, vd 0111 -> 0112) | |
| E - SỐ HIỆU | Công thức nối NO. với "/ST/2025" | |
| G - DIỄN GIẢI | Ghép từ 3 cột dịch vụ + cấp độ | Cùng format với DATA LONG-TERM |
| H - ĐƠN GIÁ | -- | Không tự điền, chưa có nguồn giá xác nhận, để trống + tô vàng |
| I - VAT | 0.08 (8%) | Mặc định theo pattern hiện có trong sheet |
| J - TIỀN THUẾ | Công thức = ĐƠN GIÁ x VAT | |
| K - TỔNG TIỀN | Công thức = ĐƠN GIÁ + TIỀN THUẾ | |
| L - NGÀY ĐẾN HẠN | Công thức = Ngày thực hiện + 15 | |

## Nguyên tắc bắt buộc khi ghi vào file thật

- Không chỉnh sửa các dòng đã có sẵn trong DATA LONG-TERM / DATA SHORT-TERM -- chỉ thêm dòng mới cho khách hàng chưa từng xuất hiện (so khớp theo MÃ CÔNG TY).
- Không tự tạo dữ liệu cho sheet DATA FEE SERVICE, LT 2025, ST 2025, OR 2025, REPORT trừ khi được yêu cầu riêng.
- Không tự điền ĐƠN GIÁ khi chưa có nguồn giá xác nhận.
- Khách hàng có LOẠI trống/không xác định -> liệt kê riêng, không tự đoán phân loại.