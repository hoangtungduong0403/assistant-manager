# Mission: Báo giá (Quotation)

## Giới thiệu

Mission này hỗ trợ giám đốc tự động sinh báo giá cho danh sách khách hàng, dựa trên dữ liệu khách hàng có sẵn (Client Information) và các Template do SGA cung cấp (Summary Quotation, Single Quotation).

## Cấu trúc Mission

- `mission.md` — Mục tiêu, trigger, input/output.
- `workflow.md` — Quy trình thực hiện từng bước.
- `rules.md` — Quy tắc làm việc và quy ước đặt tên Artifact.
- `mapping.md` — Mapping giữa Client Information và các cột trong Template.
- `checklist.md` — Checklist kiểm tra trước khi hoàn thành.
- `definition-of-done.md` — Điều kiện hoàn thành Mission.
- `examples.md` — Ví dụ input/output.

## Phân loại Mission

Stateless Mission — không lưu trạng thái giữa các lần chạy. Mỗi lần chạy xử lý trọn vẹn 1 file Client Information được cung cấp, không phụ thuộc lần chạy trước.

## Vị trí Template

`missions/quotation/templates/SummaryQuotation_Template.xlsx`
`missions/quotation/templates/SingleQuotation_Template.xlsx`

*(Lưu ý: 2 file template này cần được giám đốc/nhân viên cung cấp và đặt đúng vị trí trên trước khi Mission có thể chạy. Khi có file thật, cần đọc lại và cập nhật `mapping.md` cho khớp với tên cột thực tế.)*

# Quy trình thực hiện

## Bước 1

Đọc file Client Information (Excel).

Xác định:

- Số lượng khách hàng (số dòng dữ liệu).
- Các trường thông tin có sẵn cho mỗi khách hàng (tên công ty, người liên hệ, sản phẩm/dịch vụ, số lượng, đơn giá, ghi chú...).

---

## Bước 2

Đọc Template Summary Quotation trong `missions/quotation/templates/`.

Xác định cấu trúc cột hiện có của Template (tên cột, thứ tự cột, định dạng).

---

## Bước 3

Với mỗi khách hàng trong Client Information:

- Mapping dữ liệu khách hàng vào các cột tương ứng trong Summary Quotation (tham khảo `mapping.md`).
- Thêm đúng 1 dòng mới vào Summary Quotation cho khách hàng đó.

Không gộp nhiều khách hàng vào 1 dòng. Không bỏ sót khách hàng nào trong Client Information.

---

## Bước 4

Sau khi hoàn tất mapping cho toàn bộ khách hàng, lưu file Summary Quotation đã cập nhật theo đúng quy ước đặt tên trong `rules.md`.

---

## Bước 5

Đọc Template Single Quotation trong `missions/quotation/templates/`.

Xác định cấu trúc của Template (các trường cần điền, vị trí điền).

---

## Bước 6

Với mỗi khách hàng:

- Mapping dữ liệu khách hàng (và dữ liệu báo giá tương ứng của khách hàng đó) vào Template Single Quotation.
- Sinh 1 file Quotation riêng cho khách hàng đó.

---

## Bước 7

Lưu từng file Single Quotation theo đúng quy ước đặt tên trong `rules.md` — 1 file cho mỗi khách hàng.

---

## Bước 8

Tổng hợp kết quả:

- Số lượng khách hàng đã xử lý.
- Danh sách Artifact đã sinh (1 Summary Quotation + N Single Quotation).
- Các trường thông tin bị thiếu (nếu có) cho từng khách hàng.
