# Quy tắc làm việc

> **Cập nhật 2026-07-24:** Mission không còn sinh Single Quotation riêng theo từng khách hàng. Chỉ sinh/cập nhật Summary Quotation. Các quy tắc liên quan đến Single Quotation bên dưới đã được loại bỏ; xem "Lịch sử thay đổi" ở cuối file.
>
> **Cập nhật 2026-07-25:** Căn cứ phân loại Long-term/Short-term đổi sang dựa vào cột O/P/Q (xem `mapping.md`, `workflow.md`). Vì vậy quy tắc "mỗi dòng Client Information tương ứng đúng 1 dòng mới" bên dưới đã được sửa lại để cho phép ngoại lệ khi khách hàng dùng cả 2 loại dịch vụ.

Luôn sử dụng dữ liệu từ file Client Information do người dùng cung cấp. Không tự suy diễn hoặc tự bổ sung thông tin khách hàng không có trong dữ liệu nguồn.

Mỗi khách hàng trong Client Information tương ứng với **1 dòng mới trong mỗi sheet mà khách hàng đó cần** (Long-term và/hoặc Short-term, xác định theo bảng quy tắc phân loại tại `mapping.md`). Với đa số khách hàng (chỉ dùng 1 loại dịch vụ) đây vẫn là đúng 1 dòng; **ngoại lệ**: khách hàng dùng cả dịch vụ Long-term (O có giá trị) lẫn Short-term (P hoặc Q có giá trị) sẽ tạo ra **2 dòng** — 1 dòng ở mỗi sheet. Không gộp 2 dịch vụ của cùng khách hàng vào chung 1 dòng, không bỏ sót khách hàng, không tạo thêm khách hàng không có trong dữ liệu nguồn.

Không tự ý thay đổi cấu trúc cột của Summary Quotation (không thêm/xoá/đổi tên cột).

Nếu một trường dữ liệu bắt buộc bị thiếu trong Client Information và không có quy tắc mặc định (xem `mapping.md`), để trống ô tương ứng và liệt kê trong báo cáo kết quả là "Chưa được cung cấp". Không tự suy diễn hoặc tự điền giá trị thay thế.

Nếu có bảng giá chuẩn hoặc đơn giá mặc định cần áp dụng, chỉ sử dụng khi được xác nhận rõ nguồn (ví dụ: được nêu trong Client Information hoặc được người dùng cung cấp trực tiếp trong yêu cầu). Không tự đặt đơn giá.

Không tự ý gửi báo giá cho khách hàng qua Email hoặc kênh khác — Mission chỉ tạo Artifact, việc gửi đi do giám đốc quyết định.

**Mọi lần chạy Mission đều lưu ra một file Summary Quotation mới vào `missions/service-quotation/output/`.** Đây là nơi lưu chính thức của mọi Artifact do Mission này sinh ra — lần chạy sau có thể lấy trực tiếp file mới nhất trong thư mục này làm nguồn, không cần cung cấp lại từ nơi khác (miễn thư mục này còn tồn tại trong ngữ cảnh làm việc hiện tại — file không tự lưu giữa các phiên hội thoại khác nhau nếu không thuộc Project knowledge). Không bao giờ ghi đè lên:

- File Summary Quotation đã sinh trước đó (theo nguyên tắc "Không chỉnh sửa Artifact đã sinh" tại `CLAUDE.md`).
- File template cục bộ tại `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`.
- Bản gốc trên Google Drive.

Việc ghi đè trực tiếp vào template cục bộ hoặc bản gốc trên Drive chỉ thực hiện khi được người dùng yêu cầu rõ ràng và đã xác nhận.

Khi thêm dòng mới, luôn copy style (font, fill, border, number format) từ dòng dữ liệu cuối cùng đang có trong sheet — không tự thiết kế lại định dạng.

Không tự sửa các công thức đã tồn tại sẵn trong template, kể cả khi công thức đó đang lỗi (xem ghi chú trong `mapping.md` về cột K của `DATA SHORT - TERM`) — chỉ ghi chú lại trong báo cáo kết quả để người dùng biết.

Phân loại Long-term / Short-term cho từng khách hàng thực hiện theo bảng quy tắc tại `mapping.md` (căn cứ chính là cột O/P/Q, `LOẠI` chỉ là fallback khi O/P/Q đều rỗng). Không tự đoán phân loại khi cả O, P, Q và `LOẠI` đều không xác định được — liệt kê riêng khách hàng đó để người dùng xác nhận thủ công.

## Quy ước đặt tên Artifact

### Summary Quotation

`missions/service-quotation/output/SummaryQuotation_<yyyyMMdd_HHmm>.xlsx`

Ví dụ:

- `missions/service-quotation/output/SummaryQuotation_20260723_1430.xlsx`

## Quy tắc chuẩn hóa tên

- Không sử dụng khoảng trắng.
- Không sử dụng ký tự đặc biệt.
- Chỉ sử dụng chữ cái, số và dấu gạch dưới (_).
- Nếu không có giờ/phút cụ thể trong yêu cầu, lấy thời gian hiện tại tại thời điểm sinh Artifact.

## Công cụ hỗ trợ

Script `missions/service-quotation/scripts/update_summary_quotation.py` tự động hóa việc đọc Client Information, mapping, chống trùng khách hàng (độc lập theo từng sheet), phân loại Long-term/Short-term theo O/P/Q, và sinh Artifact Summary Quotation mới theo đúng các quy tắc trên. Xem chi tiết cách dùng trong `workflow.md`.

## Lịch sử thay đổi

**2026-07-25:**

- Đổi căn cứ phân loại Long-term/Short-term từ cột `LOẠI` sang cột O (Long-term) / P, Q (Short-term); `LOẠI` chỉ còn là fallback.
- Sửa quy tắc "1 khách hàng = 1 dòng" thành "1 khách hàng = 1 dòng cho mỗi sheet cần thiết", cho phép sinh 2 dòng khi khách hàng dùng cả 2 loại dịch vụ.
- Bổ sung quy tắc: chống trùng khách hàng thực hiện độc lập theo từng sheet.

**2026-07-24:**

- Loại bỏ toàn bộ quy tắc và quy ước đặt tên liên quan đến Single Quotation (trước đây: `Quotation_<TênKháchHàng>_<yyyyMMdd_HHmm>.xlsx`). Mission chỉ còn sinh Summary Quotation.
- Bổ sung quy tắc: mọi lần chạy đều sinh Artifact mới trong output, không có tùy chọn ghi đè trực tiếp vào template.
- Bổ sung quy tắc: giữ nguyên công thức gốc kể cả khi lỗi sẵn; chỉ ghi chú lại, không tự sửa.
