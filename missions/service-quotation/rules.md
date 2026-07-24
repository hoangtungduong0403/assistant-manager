# Quy tắc làm việc

> **Cập nhật 2026-07-24:** Mission không còn sinh Single Quotation riêng theo từng khách hàng. Chỉ sinh/cập nhật Summary Quotation. Các quy tắc liên quan đến Single Quotation bên dưới đã được loại bỏ; xem "Lịch sử thay đổi" ở cuối file.

Luôn sử dụng dữ liệu từ file Client Information do người dùng cung cấp. Không tự suy diễn hoặc tự bổ sung thông tin khách hàng không có trong dữ liệu nguồn.

Mỗi dòng trong Client Information tương ứng đúng 1 dòng mới trong Summary Quotation — không gộp, không bỏ sót, không tạo thêm khách hàng không có trong dữ liệu nguồn.

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

Script `missions/service-quotation/scripts/update_summary_quotation.py` tự động hóa việc đọc Client Information, mapping, chống trùng khách hàng, và sinh Artifact Summary Quotation mới theo đúng các quy tắc trên. Xem chi tiết cách dùng trong `workflow.md`.

## Lịch sử thay đổi

**2026-07-24:**

- Loại bỏ toàn bộ quy tắc và quy ước đặt tên liên quan đến Single Quotation (trước đây: `Quotation_<TênKháchHàng>_<yyyyMMdd_HHmm>.xlsx`). Mission chỉ còn sinh Summary Quotation.
- Bổ sung quy tắc: mọi lần chạy đều sinh Artifact mới trong output, không có tùy chọn ghi đè trực tiếp vào template.
- Bổ sung quy tắc: giữ nguyên công thức gốc kể cả khi lỗi sẵn; chỉ ghi chú lại, không tự sửa.
