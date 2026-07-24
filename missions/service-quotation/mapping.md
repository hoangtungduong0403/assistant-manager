# Mapping giữa Client Information và Summary Quotation

## File thực tế đang dùng

- Client Information: `SGA_Client_information.xlsx` — sheet `Information`
- Summary Quotation: **template cục bộ trong mission**
  - Đường dẫn: `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`
  - Đây là bản export .xlsx đầy đủ (giữ nguyên style, màu fill, dropdown/data validation) của file gốc trên Google Drive ("SGA_Summary Quotation_2025"), được đặt cố định trong mission để Mission luôn có sẵn 1 nguồn template nhất quán, không phụ thuộc kết nối Drive mỗi lần chạy.
  - Nếu file gốc trên Drive được cập nhật (thêm khách hàng mới, đổi cấu trúc cột...), cần đồng bộ lại thủ công: tải file mới từ Drive và ghi đè vào đúng đường dẫn trên.
  - Một số cột (C, E, F trong sheet DATA LONG - TERM) vốn là công thức `IMPORTRANGE` trỏ ra Google Sheets ngoài ở bản gốc trên Drive — trong bản template cục bộ này, các ô đó **đã được thay bằng giá trị tĩnh (cached value)** tại thời điểm tải về, vì công thức IMPORTRANGE không hoạt động khi mở như file Excel cục bộ (sẽ lỗi #REF). Khi dùng template này để mapping dữ liệu mới, giữ nguyên cách xử lý tĩnh này cho các cột đó — không cố khôi phục lại công thức IMPORTRANGE.

## Cấu trúc thật của Summary Quotation

| Sheet | Vai trò | Có nên ghi dữ liệu mới vào không |
|---|---|---|
| DATA LONG - TERM | Log báo giá/hợp đồng khách Long-term (lưu ý: tên sheet có khoảng trắng quanh dấu gạch ngang, không phải "DATA LONG-TERM") | Có — đích chính khi LOẠI = Long-term 1/2 |
| DATA SHORT - TERM | Log báo giá/hợp đồng khách Short-term | Có — đích chính khi LOẠI = Short-term |
| DATA OR | Báo giá cho thuê văn phòng | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| DATA FEE SERVICE | Log dịch vụ tính phí riêng | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| DATA HKD - LT / DATA HKD - ST | Log khách hộ kinh doanh | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| LT 2025 / ST 2025 / OR 2025 / 2024 | Bảng báo giá gọn theo năm | Không tự ý ghi, chỉ khi được yêu cầu cụ thể |
| REPORT | Báo cáo tổng hợp | Chỉ đọc, không ghi |

Trong file gốc trên Google Drive, nhiều cột ở DATA LONG - TERM / DATA SHORT - TERM dùng công thức `IMPORTRANGE` trỏ tới các Google Sheets ngoài (sheet "Information" và sheet "HD DAU RA" của các workbook khác). Trong **template cục bộ** (`missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`):
- Các cột từng là IMPORTRANGE (C, E, F ở DATA LONG - TERM) đã được **cố định thành giá trị tĩnh** — không còn công thức, không cần và không nên cố khôi phục lại IMPORTRANGE vì sẽ lỗi #REF khi không có kết nối tới Google Sheets ngoài.
- Các công thức nội bộ, không phụ thuộc external (STT bằng SUBTOTAL, Số hiệu bằng nối chuỗi, ĐVT phụ phí bằng IF, Ngày hiệu lực bằng cộng ngày) **vẫn được giữ nguyên dạng công thức** trong template, và tiếp tục dùng làm công thức khi thêm dòng mới.

## Khóa nối (join key)

`MÃ CÔNG TY` trong Client Information = cột B (MÃ CÔNG TY) của DATA LONG - TERM / DATA SHORT - TERM. Đây là mã ngắn (vd "BRACON", "2CE"), **không phải** `MÃ KHÁCH HÀNG` dạng C0xx.

## Quy tắc phân loại

Dựa vào cột `LOẠI` trong Client Information:
- Chứa "Long-term" (Long-term 1, Long-term 2) → ghi vào sheet **DATA LONG - TERM**
- Chứa "Short-term" → ghi vào sheet **DATA SHORT - TERM**
- Trống hoặc không xác định → **không ghi**, liệt kê riêng để người dùng xác nhận thủ công

## Cấu trúc cột thật — Sheet DATA LONG - TERM

Header gồm **2 hàng** (hàng 1 = nhóm cột, hàng 2 = tên cột con), dữ liệu bắt đầu từ **hàng 4** (hàng 3 để trống).

| Cột | Nhóm (hàng 1) | Tên cột (hàng 2) | Nguồn dữ liệu | Ghi chú |
|---|---|---|---|---|
| A | STT | (trống) | Công thức `=IF(B{r}="","",SUBTOTAL(3,$B$4:B{r}))` | Tự tính, giữ công thức |
| B | MÃ CÔNG TY | (trống) | Client Information > MÃ CÔNG TY | Khóa nối, nhập tay |
| C | THÔNG TIN KHÁCH HÀNG | Mã số thuế | IMPORTRANGE (sheet "Information" ngoài) | Khi export riêng: dùng cached value, không dùng công thức |
| D | GHI CHÚ | (trống) | Client Information > cấp độ gói dịch vụ | Dropdown: Standard / Premium / Platinum |
| E | DỊCH VỤ | Số hợp đồng | IMPORTRANGE (sheet "HD DAU RA" ngoài) | Mặc định "CHUA CO" nếu chưa có |
| F | DỊCH VỤ | Tình trạng | IMPORTRANGE (sheet "HD DAU RA" ngoài) | Cached value khi export riêng |
| G | DỊCH VỤ | Số thứ tự | Tiếp nối chuỗi số hiện có (3 chữ số, vd 101 → 102) | Không được trùng |
| H | DỊCH VỤ | Số hiệu | Công thức `=IF(B{r}="","",(G{r}&"/LT/2025"))` | Tự tính, giữ công thức |
| I | DỊCH VỤ | ĐVT | Nhập tay | Dropdown: Tháng / Quý / Năm / Khác |
| J | PHỤ PHÍ | Hóa đơn | Nhập tay (checkbox TRUE/FALSE) | Dropdown/checkbox: TRUE / FALSE |
| K | PHỤ PHÍ | ĐVT | Công thức `=IF(J{r},"Quý","")` | Tự tính, giữ công thức |
| L | PHỤ PHÍ | Ngày thực hiện | Nhập tay (ngày) | Định dạng `dd"/"mm"/"yyyy` |
| M | BÁO GIÁ | Ngày hiệu lực | Công thức `=IF(B{r}="","",(L{r}+15))` | Tự tính = Ngày thực hiện + 15 |
| N | BÁO GIÁ | Tình trạng | Nhập tay | Dropdown: DONE / Progressing / Cancel |

## Style chuẩn (áp dụng khi tạo báo giá theo đúng style file gốc)

- **Font:** Times New Roman, cỡ 11, header in đậm (bold).
- **Màu nền header (fill) theo nhóm cột:**
  - Vàng `FFD966`: STT, MÃ CÔNG TY, GHI CHÚ, BÁO GIÁ
  - Cam `F9CB9C`: THÔNG TIN KHÁCH HÀNG
  - Xanh lá `B6D7A8`: DỊCH VỤ, PHỤ PHÍ
  - Xám `D9D9D9`: các ô dữ liệu là công thức/IMPORTRANGE (không nhập tay)
- **Viền:** hair-line (mảnh), áp dụng toàn bộ vùng bảng.
- **Freeze pane:** tại ô `C4` (khóa 2 hàng tiêu đề + cột A, B).
- **Định dạng ngày:** `dd"/"mm"/"yyyy`.
- **Độ rộng cột (xấp xỉ):** A=7.4, B=18.9, C=20, D=19.5, E=38, F=14.75, G=8.9, H=17.25, I=7.9, J=8.6, K=6.6, L=14.6, M=14, N=14.9.

## Data Validation (Dropdown) cần tái tạo khi xuất báo giá

| Cột | Vùng áp dụng (file gốc) | Danh sách giá trị |
|---|---|---|
| D (GHI CHÚ) | D4:D1000 | Standard, Premium, Platinum |
| I, K (ĐVT) | I4:I501, K4:K501 | Tháng, Quý, Năm, Khác |
| J (Hóa đơn) | J4:J1000 | TRUE, FALSE (checkbox) |
| N (Tình trạng) | N4:N1000 | DONE, Progressing, Cancel |

## Mapping cột — DATA SHORT - TERM

*(giữ nguyên như đề xuất trước đây — chưa đối chiếu với file thật, cần cập nhật tương tự DATA LONG - TERM khi có yêu cầu xử lý khách Short-term.)*

| Cột đích | Nguồn | Ghi chú |
|---|---|---|
| A - STT | Công thức subtotal theo cột D | |
| B - MÃ KH | Client Information > MÃ CÔNG TY | Khóa nối |
| C - MÃ SỐ THUẾ | Client Information > MÃ SỐ THUẾ | Giá trị tĩnh |
| D - NO. | Tiếp nối chuỗi số hiện có (4 chữ số, vd 0111 → 0112) | |
| E - SỐ HIỆU | Công thức nối NO. với "/ST/2025" | |
| G - DIỄN GIẢI | Ghép từ 3 cột dịch vụ + cấp độ | |
| H - ĐƠN GIÁ | -- | Không tự điền, chưa có nguồn giá xác nhận, để trống + tô vàng |
| I - VAT | 0.08 (8%) | Mặc định theo pattern hiện có trong sheet |
| J - TIỀN THUẾ | Công thức = ĐƠN GIÁ x VAT | |
| K - TỔNG TIỀN | Công thức = ĐƠN GIÁ + TIỀN THUẾ | |
| L - NGÀY ĐẾN HẠN | Công thức = Ngày thực hiện + 15 | |

## Nguyên tắc bắt buộc khi ghi vào file thật

- Không chỉnh sửa các dòng đã có sẵn trong DATA LONG - TERM / DATA SHORT - TERM — chỉ thêm dòng mới cho khách hàng chưa từng xuất hiện (so khớp theo MÃ CÔNG TY).
- Không tự tạo dữ liệu cho sheet DATA OR, DATA FEE SERVICE, DATA HKD - LT/ST, LT 2025, ST 2025, OR 2025, 2024, REPORT trừ khi được yêu cầu riêng.
- Không tự điền ĐƠN GIÁ khi chưa có nguồn giá xác nhận.
- Khách hàng có LOẠI trống/không xác định → liệt kê riêng, không tự đoán phân loại.
- Khi xuất báo giá riêng cho 1 khách hàng (Single Quotation): giữ đúng style, dropdown, và định dạng như bảng trên; không dùng công thức IMPORTRANGE (sẽ lỗi #REF khi mất liên kết ngoài) — thay bằng giá trị tĩnh đã lấy từ file gốc.
