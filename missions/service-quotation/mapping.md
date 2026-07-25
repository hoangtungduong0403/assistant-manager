# Mapping giữa Client Information và Summary Quotation

> **Cập nhật 2026-07-24:** Mapping dưới đây đã được đối chiếu trực tiếp với file thật (`Bản_sao_của_SGA_Client_information.xlsx` và `SGA_Summary_Quotation_2025.xlsx`) và áp dụng cho cả `DATA LONG - TERM` lẫn `DATA SHORT - TERM` — mục "chưa đối chiếu" của `DATA SHORT - TERM` trong bản trước đã được thay thế bằng cấu trúc thật bên dưới.
>
> **Cập nhật 2026-07-25:** Thay đổi căn cứ phân loại Long-term / Short-term — không còn dùng cột `LOẠI` (N) làm căn cứ chính, mà dùng trực tiếp giá trị trong cột dịch vụ O/P/Q (xem mục "Quy tắc phân loại dịch vụ" bên dưới). `LOẠI` chỉ còn vai trò fallback. Một khách hàng có thể phát sinh **2 dòng** (1 ở mỗi sheet) nếu vừa dùng dịch vụ Long-term vừa dùng dịch vụ Short-term.

## File thực tế đang dùng

- Client Information: sheet `Information`, dữ liệu bắt đầu từ **hàng 4**. Cột chính:
  - B = MÃ CÔNG TY (khóa nối)
  - E = MÃ SỐ THUẾ
  - F = TÊN CÔNG TY
  - N = LOẠI ("Long-term 1", "Long-term 2", "Short-term") — **chỉ dùng làm fallback**, xem mục "Quy tắc phân loại dịch vụ" bên dưới.
  - O = Dịch vụ phân tích - thống kê (cấp độ: Standard/Premium/Platinum) — **thuộc nhóm Long-term**
  - P = Dịch vụ nhân sự (cấp độ: Standard/Premium/Platinum) — **thuộc nhóm Short-term**
  - Q = Dịch vụ pháp chế doanh nghiệp (cấp độ: Standard/Premium/Platinum) — **thuộc nhóm Short-term**
- Summary Quotation: **template cục bộ trong mission**
  - Đường dẫn: `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`
  - Bản export .xlsx từ Google Sheets gốc. Các công thức `IMPORTRANGE` gốc (trỏ tới sheet "Information" và "HD DAU RA" ngoài) hiện xuất hiện trong file cục bộ dưới dạng `=IFERROR(__xludf.DUMMYFUNCTION("..."),"")` — đây là placeholder do Google Sheets ghi lại khi export, **không phải công thức có thể tính toán được** trong Excel/LibreOffice cục bộ, và **không nên tái sử dụng cho dòng mới**.
  - **Với dòng mới do Mission tạo:** không viết công thức IMPORTRANGE/DUMMYFUNCTION — thay bằng giá trị tĩnh lấy trực tiếp từ Client Information (xem quy tắc cột C bên dưới). Các dòng cũ giữ nguyên, không sửa.

## Khóa nối (join key)

`MÃ CÔNG TY` trong Client Information = cột B của `DATA LONG - TERM` / `DATA SHORT - TERM` (cả 2 sheet dùng cùng tên cột `MÃ CÔNG TY` / `MÃ KH`). So khớp không phân biệt hoa/thường.

## Ý nghĩa cột O, P, Q

Công ty SGA cung cấp nhiều loại dịch vụ, mỗi dịch vụ thuộc nhóm Long-term hoặc Short-term, và mỗi dịch vụ có thêm cấp độ gói (Standard / Premium / Platinum) xác định các tính năng đi kèm. Khách hàng có thể mua **cả gói Long-term lẫn Short-term cùng một thời điểm**.

- **O — Dịch vụ phân tích thống kê**: thuộc nhóm **Long-term**. Giá trị (Standard/Premium/Platinum) chỉ dùng để xác định **gói** khách hàng đã chọn, không dùng để suy ra Long/Short — bản thân việc O có giá trị hay không mới là căn cứ phân loại.
- **P — Dịch vụ nhân sự**: thuộc nhóm **Short-term**. Tương tự, giá trị chỉ xác định gói.
- **Q — Dịch vụ pháp chế doanh nghiệp**: thuộc nhóm **Short-term**. Tương tự, giá trị chỉ xác định gói.

## Quy tắc phân loại dịch vụ (Long-term / Short-term)

Căn cứ chính là **giá trị thực tế trong cột O, P, Q**. Cột `LOẠI` (N) **không còn là căn cứ chính** — chỉ dùng làm fallback khi O, P, Q đều rỗng.

| # | Điều kiện | Kết luận | Hành động |
|---|---|---|---|
| 1 | O có giá trị; P và Q đều rỗng | Chỉ dùng **Long-term** | Thêm 1 dòng vào `DATA LONG - TERM`, gói (cột D) lấy từ O |
| 2 | O rỗng; (P hoặc Q) có giá trị | Chỉ dùng **Short-term** | Thêm 1 dòng vào `DATA SHORT - TERM`, DIỄN GIẢI ghép từ P/Q |
| 3 | O có giá trị **và** (P hoặc Q) có giá trị | Dùng **cả Long-term lẫn Short-term** | Thêm **2 dòng riêng**: 1 dòng `DATA LONG - TERM` (gói theo O) + 1 dòng `DATA SHORT - TERM` (DIỄN GIẢI ghép từ P/Q). Không gộp 2 dịch vụ vào chung 1 dòng. |
| 4 | O, P, Q đều rỗng; `LOẠI` (N) xác định được là "Long-term" hoặc "Short-term" | Fallback theo `LOẠI` | Thêm 1 dòng vào sheet tương ứng theo N; cột gói/DIỄN GIẢI để trống và ghi "Chưa được cung cấp" vì không có nguồn cấp độ dịch vụ |
| 5 | O, P, Q đều rỗng **và** `LOẠI` cũng rỗng/không xác định | Không đủ căn cứ phân loại | Bỏ qua, liệt kê riêng trong báo cáo để người dùng xác nhận thủ công, không tự đoán |

Ghi chú quan trọng cho trường hợp #3 (dùng cả 2 loại): DIỄN GIẢI ở sheet Short-term **chỉ chứa dịch vụ thuộc Short-term (P/Q)**, không lặp lại dịch vụ Long-term (O) đã được ghi riêng ở sheet Long-term.

## Quy tắc phân loại

Sheet đích được xác định theo bảng ở trên (không còn xác định trực tiếp theo `LOẠI` như trước).

## Cấu trúc cột thật — Sheet DATA LONG - TERM

Header gồm **2 hàng** (hàng 1 = nhóm cột, hàng 2 = tên cột con), dữ liệu bắt đầu từ **hàng 4** (hàng 3 để trống).

| Cột | Tên cột | Nguồn dữ liệu cho dòng mới | Ghi chú |
|---|---|---|---|
| A | STT | Công thức `=IF(B{r}="","",SUBTOTAL(3,$B$4:B{r}))` | Tự tính, giữ công thức |
| B | MÃ CÔNG TY | Client Information > MÃ CÔNG TY | Khóa nối |
| C | Mã số thuế | Client Information > MÃ SỐ THUẾ | **Giá trị tĩnh** (không dùng IMPORTRANGE/DUMMYFUNCTION) |
| D | GHI CHÚ (cấp độ) | Client Information > cột O (Dịch vụ phân tích - thống kê) | Dropdown gốc: Standard / Premium / Platinum. Nếu dòng được thêm theo fallback (#4) và O rỗng, để trống + ghi "Chưa được cung cấp" trong báo cáo |
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
| G | DIỄN GIẢI | Ghép các cặp `<Tên dịch vụ> - <Cấp độ>` **chỉ từ cột P và Q** có giá trị trong Client Information (không lấy từ O) | Vd: "Dịch vụ nhân sự - Premium". Nếu dòng thêm theo fallback (#4) và P, Q rỗng, ghi "Chưa được cung cấp" |
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

- Không chỉnh sửa các dòng đã có sẵn — chỉ thêm dòng mới cho khách hàng chưa từng xuất hiện trong sheet tương ứng (so khớp theo `MÃ CÔNG TY`).
- Phân loại Long-term / Short-term theo bảng ở mục "Quy tắc phân loại dịch vụ" — dựa vào O/P/Q trước, `LOẠI` (N) chỉ là fallback.
- Một khách hàng có thể tạo ra **2 dòng** (1 ở `DATA LONG - TERM`, 1 ở `DATA SHORT - TERM`) nếu thỏa điều kiện #3. Việc chống trùng (`MÃ CÔNG TY`) được kiểm tra **độc lập theo từng sheet** — khách hàng đã có ở 1 sheet nhưng chưa có ở sheet còn lại vẫn được thêm dòng mới ở sheet còn thiếu.
- Không tự tạo dữ liệu cho các sheet khác (`DATA FEE SERVICE`, `LT 2025`, `ST 2025`, `OR 2025`, `REPORT`...) trừ khi được yêu cầu riêng.
- Không tự điền ĐƠN GIÁ khi chưa có nguồn giá xác nhận.
- Khách hàng thuộc trường hợp #5 (O, P, Q, N đều rỗng/không xác định) → liệt kê riêng, không tự đoán phân loại.
- Không dùng công thức IMPORTRANGE/DUMMYFUNCTION cho dòng mới — luôn dùng giá trị tĩnh cho MÃ SỐ THUẾ.
- Không sửa các công thức gốc dù có lỗi sẵn (vd cột K của `DATA SHORT - TERM`) — giữ đúng quy ước file, chỉ ghi chú lại trong báo cáo kết quả.
