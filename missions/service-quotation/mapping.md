# Mapping giữa Client Information và Summary Quotation

> **Cập nhật 2026-07-24:** Mapping dưới đây đã được đối chiếu trực tiếp với file thật (`Bản_sao_của_SGA_Client_information.xlsx` và `SGA_Summary_Quotation_2025.xlsx`) và áp dụng cho cả `DATA LONG - TERM` lẫn `DATA SHORT - TERM` — mục "chưa đối chiếu" của `DATA SHORT - TERM` trong bản trước đã được thay thế bằng cấu trúc thật bên dưới.

## File thực tế đang dùng

- Client Information: sheet `Information`, dữ liệu bắt đầu từ **hàng 4**. Cột chính:
  - B = MÃ CÔNG TY (khóa nối)
  - E = MÃ SỐ THUẾ
  - F = TÊN CÔNG TY
  - N = LOẠI ("Long-term 1", "Long-term 2", "Short-term")
  - O = Dịch vụ phân tích - thống kê (cấp độ: Standard/Premium/Platinum)
  - P = Dịch vụ nhân sự (cấp độ)
  - Q = Dịch vụ pháp chế doanh nghiệp (cấp độ)
- Summary Quotation: **template cục bộ trong mission**
  - Đường dẫn: `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`
  - Bản export .xlsx từ Google Sheets gốc. Các công thức `IMPORTRANGE` gốc (trỏ tới sheet "Information" và "HD DAU RA" ngoài) hiện xuất hiện trong file cục bộ dưới dạng `=IFERROR(__xludf.DUMMYFUNCTION("..."),"")` — đây là placeholder do Google Sheets ghi lại khi export, **không phải công thức có thể tính toán được** trong Excel/LibreOffice cục bộ, và **không nên tái sử dụng cho dòng mới**.
  - **Với dòng mới do Mission tạo:** không viết công thức IMPORTRANGE/DUMMYFUNCTION — thay bằng giá trị tĩnh lấy trực tiếp từ Client Information (xem quy tắc cột C bên dưới). Các dòng cũ giữ nguyên, không sửa.

## Khóa nối (join key)

`MÃ CÔNG TY` trong Client Information = cột B của `DATA LONG - TERM` / `DATA SHORT - TERM` (cả 2 sheet dùng cùng tên cột `MÃ CÔNG TY` / `MÃ KH`). So khớp không phân biệt hoa/thường.

## Quy tắc phân loại

Dựa vào cột `LOẠI` trong Client Information:

- Chứa "Long-term" (Long-term 1, Long-term 2) → ghi vào sheet **DATA LONG - TERM**
- Chứa "Short-term" → ghi vào sheet **DATA SHORT - TERM**
- Trống hoặc không xác định → **không ghi**, liệt kê riêng để người dùng xác nhận thủ công

## Cấu trúc cột thật — Sheet DATA LONG - TERM

Header gồm **2 hàng** (hàng 1 = nhóm cột, hàng 2 = tên cột con), dữ liệu bắt đầu từ **hàng 4** (hàng 3 để trống).

| Cột | Tên cột | Nguồn dữ liệu cho dòng mới | Ghi chú |
|---|---|---|---|
| A | STT | Công thức `=IF(B{r}="","",SUBTOTAL(3,$B$4:B{r}))` | Tự tính, giữ công thức |
| B | MÃ CÔNG TY | Client Information > MÃ CÔNG TY | Khóa nối |
| C | Mã số thuế | Client Information > MÃ SỐ THUẾ | **Giá trị tĩnh** (không dùng IMPORTRANGE/DUMMYFUNCTION) |
| D | GHI CHÚ (cấp độ) | Client Information > cấp độ gói dịch vụ (lấy cấp độ đầu tiên có giá trị trong O/P/Q) | Dropdown gốc: Standard / Premium / Platinum |
| E | Số hợp đồng | Mặc định `"CHUA CO"` | Không có nguồn trong Client Information |
| F | Tình trạng hợp đồng | **Để trống** | Không có nguồn — không suy diễn |
| G | Số thứ tự | Tiếp nối số lớn nhất hiện có trong sheet (3 chữ số) | Tự sinh, không trùng |
| H | Số hiệu | Công thức `=IF(B{r}="","",(G{r}&"/LT/2025"))` | Tự tính, giữ công thức |
| I | ĐVT phụ phí | **Để trống** | Không có nguồn — cần người dùng xác nhận |
| J | Hóa đơn (checkbox) | **Để trống** | Không có nguồn |
| K | ĐVT (phụ phí, tự tính) | Công thức `=IF(J{r},"Quý","")` | Tự tính, giữ công thức |
| L | Ngày thực hiện | **Để trống** | Không có nguồn |
| M | Ngày hiệu lực | Công thức `=IF(B{r}="","",(L{r}+15))` | Tự tính. **Lưu ý:** khi L để trống, công thức gốc trả về ngày không có ý nghĩa (15/01/1900) — đây là hành vi vốn có của công thức gốc, không phải lỗi do Mission gây ra. Sẽ tự đúng khi người dùng điền Ngày thực hiện thật. |
| N | Tình trạng báo giá | **Để trống** | Không có nguồn — cần người dùng xác nhận (dropdown gốc: DONE / Progressing / Cancel) |

## Cấu trúc cột thật — Sheet DATA SHORT - TERM

Header ở **hàng 2** (hàng 1 chỉ có tiêu đề gộp "BÁO GIÁ CHI TIẾT"), dữ liệu bắt đầu từ **hàng 4** (hàng 3 chứa công thức SUBTOTAL tổng).

| Cột | Tên cột | Nguồn dữ liệu cho dòng mới | Ghi chú |
|---|---|---|---|
| A | STT | Công thức `=IF(D{r}="","",SUBTOTAL(3,$D$4:D{r}))` | Tự tính, giữ công thức |
| B | MÃ KH | Client Information > MÃ CÔNG TY | Khóa nối |
| C | MÃ SỐ THUẾ | Client Information > MÃ SỐ THUẾ | **Giá trị tĩnh** |
| D | NO. | Tiếp nối số lớn nhất hiện có trong sheet (3 chữ số, vd 004 → 005) | Tự sinh, không trùng |
| E | SỐ HIỆU | Công thức `=IF(B{r}="","",(D{r}&"/ST/2025"))` | Tự tính, giữ công thức |
| F | NGÀY THỰC HIỆN | **Để trống** | Không có nguồn |
| G | DIỄN GIẢI | Ghép các cặp `<Tên dịch vụ> - <Cấp độ>` từ cột O/P/Q có giá trị trong Client Information | Vd: "Dịch vụ phân tích - thống kê - Standard" |
| H | ĐƠN GIÁ | **Để trống** | **Không tự đặt đơn giá** — chưa có nguồn giá xác nhận (theo `rules.md`) |
| I | VAT | Mặc định `0.08` (8%) | Theo pattern hiện có trong sheet |
| J | TIỀN THUẾ | Công thức `=H{r}*I{r}` | Tự tính |
| K | (nhãn header "TỔNG TIỀN" nhưng công thức thật trong file gốc là) `=IF(E{r}="","",(E{r}+15))` | Giữ nguyên công thức gốc | **Lưu ý:** công thức này vốn đã lỗi `#VALUE!` ở toàn bộ các dòng cũ (vì cộng chuỗi text với số) — đây là lỗi có sẵn trong file gốc, Mission giữ nguyên đúng quy ước, không tự sửa. |
| L | NGÀY ĐẾN HẠN | Công thức `=IF(F{r}="","",(F{r}+15))` | Tự tính |
| M | TÌNH TRẠNG | **Để trống** | Không có nguồn — cần người dùng xác nhận (dropdown gốc: DONE / Progressing / Cancel) |
| N | NGÀY HIỆU LỰC | Công thức `=IF(M{r}="Done",F{r},"")` | Tự tính |

## Style chuẩn (áp dụng khi thêm dòng mới)

Không tự thiết kế lại style — **copy toàn bộ style (font, fill, border, number format, alignment) từ dòng dữ liệu cuối cùng đang có** trong sheet tương ứng sang dòng mới, để đảm bảo khớp hoàn toàn với quy ước file gốc (Times New Roman cỡ 11, viền hair-line, màu fill theo nhóm cột...).

## Nguyên tắc bắt buộc khi thêm dòng mới

- Không chỉnh sửa các dòng đã có sẵn — chỉ thêm dòng mới cho khách hàng chưa từng xuất hiện (so khớp theo `MÃ CÔNG TY`).
- Không tự tạo dữ liệu cho các sheet khác (`DATA FEE SERVICE`, `LT 2025`, `ST 2025`, `OR 2025`, `REPORT`...) trừ khi được yêu cầu riêng.
- Không tự điền ĐƠN GIÁ khi chưa có nguồn giá xác nhận.
- Khách hàng có LOẠI trống/không xác định → liệt kê riêng, không tự đoán phân loại.
- Không dùng công thức IMPORTRANGE/DUMMYFUNCTION cho dòng mới — luôn dùng giá trị tĩnh cho MÃ SỐ THUẾ.
- Không sửa các công thức gốc dù có lỗi sẵn (vd cột K của `DATA SHORT - TERM`) — giữ đúng quy ước file, chỉ ghi chú lại trong báo cáo kết quả.
