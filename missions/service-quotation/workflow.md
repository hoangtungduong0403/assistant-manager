# Mission: Báo giá (Quotation)

## Giới thiệu

Mission này hỗ trợ giám đốc tự động sinh báo giá cho danh sách khách hàng, dựa trên dữ liệu khách hàng có sẵn (Client Information) và Summary Quotation gốc của SGA.

## Cấu trúc Mission

- `mission.md` — Mục tiêu, trigger, input/output.
- `workflow.md` — Quy trình thực hiện từng bước.
- `rules.md` — Quy tắc làm việc và quy ước đặt tên Artifact.
- `mapping.md` — Mapping giữa Client Information và các cột trong Summary Quotation (đã đối chiếu với file thật).
- `checklist.md` — Checklist kiểm tra trước khi hoàn thành.
- `definition-of-done.md` — Điều kiện hoàn thành Mission.
- `examples.md` — Ví dụ input/output.

## Phân loại Mission

Stateless Mission — không lưu trạng thái giữa các lần chạy. Mỗi lần chạy xử lý trọn vẹn 1 file Client Information được cung cấp, không phụ thuộc lần chạy trước.

## Vị trí Template / Nguồn dữ liệu thật

File Summary Quotation gốc được lưu **cục bộ trong mission**:

- Đường dẫn: `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`
- Đây là bản export .xlsx của file Google Sheets "SGA_Summary Quotation_2025" trên Drive, giữ nguyên toàn bộ style (font, màu fill theo nhóm cột, viền, freeze pane) và dropdown/data validation. Dùng file này làm nguồn đọc/ghi mặc định — **không cần gọi Google Drive connector mỗi lần chạy Mission**.
- Nếu người dùng yêu cầu đồng bộ lại với bản mới nhất trên Drive: dùng Google Drive connector (`search_files` → `download_file_content` với `exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`) để tải bản mới, rồi ghi đè vào đúng đường dẫn template cục bộ ở trên. Nếu có nhiều bản trên Drive (vd "Bản sao của SGA_Summary Quotation_2025"), xác nhận với người dùng đang đồng bộ từ bản nào.
- Template Single Quotation riêng cho từng khách hàng: hiện **chưa có file mẫu chính thức riêng** — khi cần xuất báo giá riêng 1 khách hàng, tái tạo theo đúng cấu trúc cột + style + dropdown của sheet tương ứng trong Summary Quotation gốc (xem chi tiết tại `mapping.md`).

# Quy trình thực hiện

## Bước 1

Đọc file Client Information (Excel).

Xác định:

- Số lượng khách hàng (số dòng dữ liệu).
- Các trường thông tin có sẵn cho mỗi khách hàng (tên công ty, người liên hệ, sản phẩm/dịch vụ, số lượng, đơn giá, ghi chú...).

---

## Bước 2

Đọc file Summary Quotation gốc tại `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx` (xem mục "Vị trí Template" ở trên).

Xác định:

- Sheet đích theo LOẠI (DATA LONG - TERM hoặc DATA SHORT - TERM).
- Khách hàng đã tồn tại sẵn trong sheet hay chưa (so khớp theo MÃ CÔNG TY) — nếu đã có, không tạo dòng trùng.

---

## Bước 3

Với mỗi khách hàng trong Client Information **chưa từng xuất hiện** trong Summary Quotation:

- Mapping dữ liệu khách hàng vào các cột tương ứng (tham khảo `mapping.md`).
- Thêm đúng 1 dòng mới, giữ nguyên các công thức tự tính (STT, Số hiệu, ĐVT phụ phí, Ngày hiệu lực).
- Với khách hàng đã tồn tại sẵn: không sửa dòng cũ, chỉ dùng dữ liệu hiện có để xuất báo giá nếu được yêu cầu.

Không gộp nhiều khách hàng vào 1 dòng. Không bỏ sót khách hàng nào trong Client Information.

---

## Bước 4

Nếu Mission yêu cầu cập nhật trực tiếp file template Summary Quotation cục bộ (thêm dòng khách hàng mới): ghi đè vào đúng đường dẫn `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`, giữ nguyên toàn bộ style và dropdown sẵn có. Nếu chỉ xuất báo giá tham khảo/tải về cho 1 khách hàng: lưu thành file .xlsx mới (Artifact) theo đúng quy ước đặt tên trong `rules.md`, giữ đúng style (font, màu fill, viền, freeze pane) và dropdown (data validation) như file template — chi tiết tại `mapping.md`. Không ghi đè trực tiếp lên bản gốc trên Google Drive trừ khi được yêu cầu rõ ràng và đã xác nhận với người dùng.

---

## Bước 5

Sinh Single Quotation riêng cho từng khách hàng (nếu được yêu cầu):

- Tái tạo đúng cấu trúc cột + style + dropdown của sheet nguồn.
- Không dùng công thức IMPORTRANGE liên kết ngoài trong file xuất riêng (sẽ lỗi #REF khi mất liên kết) — thay bằng giá trị tĩnh đã lấy từ file gốc.
- Giữ nguyên công thức nội bộ không phụ thuộc external (STT, Số hiệu, ĐVT phụ phí, Ngày hiệu lực).

---

## Bước 6

Lưu từng file Single Quotation theo đúng quy ước đặt tên trong `rules.md` — 1 file cho mỗi khách hàng.

---

## Bước 7

Tổng hợp kết quả:

- Số lượng khách hàng đã xử lý.
- Danh sách Artifact đã sinh (Summary Quotation cập nhật nếu có + N Single Quotation).
- Các trường thông tin bị thiếu (nếu có) cho từng khách hàng.
