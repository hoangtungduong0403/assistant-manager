# Quy tắc làm việc

Luôn sử dụng dữ liệu từ file Client Information do người dùng cung cấp. Không tự suy diễn hoặc tự bổ sung thông tin khách hàng không có trong dữ liệu nguồn.

Mỗi dòng trong Client Information tương ứng đúng 1 dòng trong Summary Quotation và đúng 1 file Single Quotation — không gộp, không bỏ sót, không tạo thêm khách hàng không có trong dữ liệu nguồn.

Không tự ý thay đổi cấu trúc cột của Template Summary Quotation hoặc Template Single Quotation (không thêm/xoá/đổi tên cột).

Nếu một trường dữ liệu bắt buộc bị thiếu trong Client Information, ghi rõ "Chưa được cung cấp" tại ô tương ứng. Không tự suy diễn hoặc tự điền giá trị thay thế.

Nếu có bảng giá chuẩn hoặc đơn giá mặc định cần áp dụng, chỉ sử dụng khi được xác nhận rõ nguồn (ví dụ: được nêu trong Client Information hoặc được người dùng cung cấp trực tiếp trong yêu cầu). Không tự đặt đơn giá.

Không tự ý gửi báo giá cho khách hàng qua Email hoặc kênh khác — Mission chỉ tạo Artifact, việc gửi đi do giám đốc quyết định.

Nếu chạy lại Mission trên cùng file Client Information, tạo Artifact mới (Summary Quotation mới), không ghi đè lên Summary Quotation đã sinh trước đó (theo nguyên tắc "Không chỉnh sửa Artifact đã sinh" tại `CLAUDE.md`).

## Quy ước đặt tên Artifact

### Summary Quotation

`SummaryQuotation_<yyyyMMdd_HHmm>.xlsx`

Ví dụ:

- `SummaryQuotation_20260723_1430.xlsx`

### Single Quotation (theo từng khách hàng)

`Quotation_<TênKháchHàng>_<yyyyMMdd_HHmm>.xlsx`

Ví dụ:

- `Quotation_Toyota_20260723_1430.xlsx`
- `Quotation_FPT_20260723_1430.xlsx`

## Quy tắc chuẩn hóa tên

- Không sử dụng khoảng trắng.
- Không sử dụng ký tự đặc biệt.
- Chỉ sử dụng chữ cái, số và dấu gạch dưới (_).
- Nếu tên khách hàng có khoảng trắng thì loại bỏ khoảng trắng (ví dụ "Toyota Việt Nam" → "ToyotaVietNam").
- Nếu không có giờ/phút cụ thể trong yêu cầu, lấy thời gian hiện tại tại thời điểm sinh Artifact.
- Toàn bộ N file Single Quotation sinh trong cùng 1 lần chạy dùng chung 1 mốc thời gian `<yyyyMMdd_HHmm>` để dễ nhóm theo đợt.
