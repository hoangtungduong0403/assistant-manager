# Mission: Báo giá (Quotation)

## Giới thiệu

Mission này hỗ trợ giám đốc tự động cập nhật Summary Quotation cho danh sách khách hàng mới, dựa trên dữ liệu khách hàng có sẵn (Client Information) và Summary Quotation gốc của SGA.

> **Cập nhật quy trình (2026-07-24):** Mission được đơn giản hóa — chỉ cập nhật Summary Quotation, không còn sinh Single Quotation riêng cho từng khách hàng. Xem `project-updates-needed.md` / phần "Lịch sử thay đổi" bên dưới.

## Cấu trúc Mission

- `mission.md` — Mục tiêu, trigger, input/output.
- `workflow.md` — Quy trình thực hiện từng bước (file này).
- `rules.md` — Quy tắc làm việc và quy ước đặt tên Artifact.
- `mapping.md` — Mapping giữa Client Information và các cột trong Summary Quotation (đã đối chiếu với file thật).
- `scripts/update_summary_quotation.py` — Script tái sử dụng, tự động hóa Bước 1–6 bên dưới.
- `checklist.md` — Checklist kiểm tra trước khi hoàn thành.
- `definition-of-done.md` — Điều kiện hoàn thành Mission.
- `examples.md` — Ví dụ input/output.

## Phân loại Mission

Stateless Mission — không lưu trạng thái giữa các lần chạy. Mỗi lần chạy xử lý trọn vẹn 1 file Client Information được cung cấp, không phụ thuộc lần chạy trước. Việc chống trùng khách hàng (theo `MÃ CÔNG TY`) được thực hiện bằng cách so khớp trực tiếp với dữ liệu đã có trong file Summary Quotation được cung cấp ở mỗi lần chạy — không cần state.json.

## Vị trí Template / Nguồn dữ liệu thật

File Summary Quotation gốc được lưu **cục bộ trong mission**:

- Đường dẫn: `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`
- Đây là bản export .xlsx của file Google Sheets "SGA_Summary Quotation_2025" trên Drive, giữ nguyên toàn bộ style (font, màu fill theo nhóm cột, viền, freeze pane) và dropdown/data validation. Dùng file này làm nguồn đọc/ghi mặc định — **không cần gọi Google Drive connector mỗi lần chạy Mission**.
- Nếu người dùng yêu cầu đồng bộ lại với bản mới nhất trên Drive: dùng Google Drive connector (`search_files` → `download_file_content` với `exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`) để tải bản mới, rồi ghi đè vào đúng đường dẫn template cục bộ ở trên. Nếu có nhiều bản trên Drive (vd "Bản sao của SGA_Summary Quotation_2025"), xác nhận với người dùng đang đồng bộ từ bản nào.
- **Không còn sinh Single Quotation riêng theo từng khách hàng.** (Xem "Lịch sử thay đổi" bên dưới.)

# Quy trình thực hiện

## Bước 1

Đọc file Client Information (Excel), sheet `Information`, dữ liệu bắt đầu từ hàng 4.

Xác định với mỗi khách hàng:

- `MÃ CÔNG TY` (cột B) — khóa nối.
- `MÃ SỐ THUẾ` (cột E).
- `LOẠI` (cột N) — "Long-term 1/2" hoặc "Short-term".
- `Dịch vụ phân tích thống kê` (cột O) - Thuộc Long Term - bao gồm các lựa chọn: "Standard" hoặc "Premium" hoặc "Platinum", tương ứng với các gói. Chỉ dùng với mục đích để xác định gói mà doanh nghiệp đã chọn
- `Dịch vụ nhân sự` (cột P) - Thuộc Short Term, bao gồm các lựa chọn: "Standard" hoặc "Premium" hoặc "Platinum", tương ứng với các gói. Chỉ dùng với mục đích để xác định gói mà doanh nghiệp đã chọn
- `Dịch vụ pháp chế doanh nghiệp` (cột Q) - Thuộc Short Term, bao gồm các lựa chọn: "Standard" hoặc "Premium" hoặc "Platinum", tương ứng với các gói. Chỉ dùng với mục đích để xác định gói mà doanh nghiệp đã chọn

## Giải thích các lựa chọn ở cột N, O, P, Q:
- Công ty SGA cung cấp rất nhiều dịch vụ, mỗi loại dịch vụ sẽ thuộc Long term hoặc Short term, mỗi loại dịch vụ sẽ có thêm các lựa chọn "Standard" hoặc "Premium" hoặc "Platinum" để phân loại các tính năng có được cung cấp, tùy chọn vào gói Standard, Premium, Platinum
- Khách hàng có thể mua cả các gói long-term lẫn short term cùng 1 thời điểm.

## Quy tắc phân loại dịch vụ được chọn
- "Dịch vụ phân tích thống kê" có giá trị, nghĩa là có sử dụng dịch vụ long-term
- "Dịch vụ nhân sự" hoặc "Dịch vụ pháp chế doanh nghiệp" có giá trị, có nghĩa là khách hàng có sử dụng Short term
- "Dịch vụ phân tích thống kê" và "Dịch vụ nhân sự" hoặc "Dịch vụ pháp chế doanh nghiệp"
- Nếu Loại là Short term, và "Dịch vụ nhân sự" hoặc "Dịch vụ pháp chế doanh nghiệp" không có giá trị, nghĩa là khách hàng chỉ sử dụng dịch vụ Short-term
- Nếu Loại là Long term, và "Dịch vụ phân tích thống kê" có giá trị, nghĩa là khách hàng chỉ sử dụng dịch vụ Short-term
## Bước 2

Đọc file Summary Quotation gốc tại `missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx` (xem mục "Vị trí Template" ở trên).

Xác định:

- Sheet đích tùy thuộc vào lựa chọn mà file client-information cung cấp.
- AI cần xác định Khách hàng có dùng Long-term, Short-term hay ko, nếu chỉ có 1 trong 2 thì chỉ cần thêm ở sheet đích Long hoặc Short term tab , nếu có cả 2, thì cần thêm vào ở cả 2.
- Khách hàng có `LOẠI` trống hoặc không nhận diện được ("Long-term"/"Short-term") — liệt kê riêng để người dùng xác nhận thủ công, không tự đoán.

## Bước 3

Với mỗi khách hàng trong Client Information **chưa từng xuất hiện** trong Summary Quotation:

- Mapping dữ liệu khách hàng vào các cột tương ứng (tham khảo `mapping.md`).
- Thêm đúng 1 dòng mới, giữ nguyên các công thức tự tính (STT, Số hiệu, ĐVT phụ phí, Ngày hiệu lực) và copy style (font, fill, border, number format) từ dòng dữ liệu cuối cùng đang có.
- Số thứ tự / Số hiệu (G/H ở Long-term, D/E ở Short-term) tự động nối tiếp số lớn nhất đang có trong sheet.
- Các trường không có nguồn từ Client Information (giá, ngày thực hiện, tình trạng hợp đồng, tình trạng báo giá...) **để trống**, không tự suy diễn hoặc sao chép từ khách hàng khác.

Không gộp nhiều khách hàng vào 1 dòng. Không bỏ sót khách hàng nào trong Client Information.

## Bước 4

Lưu kết quả thành **1 file Summary Quotation mới** (Artifact) vào `missions/service-quotation/output/`, theo đúng quy ước đặt tên trong `rules.md`.

**Không ghi đè** vào file template cục bộ (`missions/service-quotation/templates/SGA_Summary Quotation_2025.xlsx`) và **không ghi đè** trực tiếp lên bản gốc trên Google Drive, trừ khi được yêu cầu rõ ràng và đã xác nhận với người dùng.

## Bước 5

Sau khi lưu file: chạy recalc (LibreOffice) để tính lại toàn bộ công thức trước khi bàn giao, đảm bảo không có lỗi công thức mới phát sinh (so sánh với baseline lỗi đã tồn tại sẵn trong file gốc, nếu có).

## Bước 6

Tổng hợp kết quả:

- Số lượng khách hàng đã xử lý (đã thêm dòng mới).
- Số lượng khách hàng bị bỏ qua vì đã tồn tại (trùng `MÃ CÔNG TY`).
- Số lượng khách hàng bị bỏ qua vì `LOẠI` trống/không xác định.
- Danh sách các trường bắt buộc còn thiếu, cần người dùng bổ sung thủ công (giá, ngày thực hiện, tình trạng...).
- Đường dẫn Artifact đã sinh.

## Công cụ hỗ trợ

Bước 1–4 và một phần Bước 6 có thể chạy tự động bằng script `missions/service-quotation/scripts/update_summary_quotation.py`:

```
python3 update_summary_quotation.py <client_information.xlsx> <summary_quotation_template.xlsx>
```

Script đọc trực tiếp 2 file Excel này và tự sinh file Summary Quotation mới vào `missions/service-quotation/output/` — không cần thao tác thủ công lặp lại các bước mapping mỗi lần có Client Information mới.

**Dùng output gần nhất làm nguồn cho lần chạy sau:** vì file mới nhất luôn nằm trong `missions/service-quotation/output/`, ở các lần chạy sau chỉ cần trỏ script tới file mới nhất trong thư mục này thay vì phải cung cấp lại từ nơi khác — miễn là thư mục này còn tồn tại trong ngữ cảnh làm việc hiện tại (xem lưu ý ở `rules.md` về việc file không tự lưu giữa các phiên hội thoại khác nhau).

---

## Lịch sử thay đổi

**2026-07-24** — Đơn giản hóa quy trình theo yêu cầu người dùng:

- Loại bỏ hoàn toàn bước sinh Single Quotation riêng theo từng khách hàng. Mission giờ chỉ sinh/cập nhật Summary Quotation.
- Chuẩn hóa: mọi lần chạy đều lưu ra file mới trong thư mục output; không còn tùy chọn ghi đè trực tiếp vào template cục bộ ở Bước 4 (trước đây `workflow.md` có nhánh cho phép ghi đè trực tiếp — nhánh này đã được gỡ bỏ).
- Thêm script tái sử dụng `scripts/update_summary_quotation.py` để tự động hóa toàn bộ luồng mapping + chống trùng + sinh Artifact.
