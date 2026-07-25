# Quy trình thực hiện

## Bước 1 — Xác nhận kỳ báo cáo

Nếu người dùng nêu rõ muốn đánh giá theo 1 kỳ cụ thể (vd "Quý 2", "từ tháng 1 đến tháng 5"), hỏi/nhắc người dùng xác nhận đã cập nhật ô **E7** (từ ngày) và **G7** (đến ngày) trên sheet `DEBT` của Google Sheet gốc chưa — vì AI không có quyền tự sửa 2 ô này. Nếu người dùng chỉ nói "đánh giá công nợ" mà không nêu kỳ, mặc định dùng đúng kỳ đang thiết lập sẵn trên E7/G7 tại thời điểm đọc file.

## Bước 2 — Tải file

Dùng Google Drive connector: `download_file_content` với `fileId` của file "SGA_Revenue & Debt", `exportMimeType: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`. Giải mã base64, lưu file `.xlsx` vào thư mục làm việc tạm (không phải `output/`).

## Bước 3 — Phân tích dữ liệu

Chạy:

```
python3 scripts/analyze_debt.py <file_vừa_tải.xlsx> <thư_mục_tạm>
```

Script tự động:

- Đọc kỳ báo cáo từ E7/G7.
- Đọc toàn bộ dòng dữ liệu công ty từ hàng 14 (dừng khi gặp 3 dòng trống liên tiếp ở cột Mã công ty).
- Tự cộng tay toàn bộ số liệu tổng hợp (Đầu kỳ/Trong kỳ/Cuối kỳ, cả 2 cột Phải thu và Phải trả) — **không dùng trực tiếp các ô Tổng cộng có sẵn**, vì sheet gốc có lỗi vùng công thức đã biết (xem `mapping.md`).
- So sánh số tự tính với số hiển thị sẵn trên sheet (dòng 12) → ghi nhận mọi chênh lệch ≥ 1đ vào `discrepancies`.
- Tính Top 10 khách nợ nhiều nhất, Top 10 khách trả trước nhiều nhất, % tập trung, danh sách khách hàng vượt ngưỡng cảnh báo tập trung (>20%/khách hàng).
- Tính danh sách "Khó đòi" còn hiệu lực (còn dư nợ > 0) và số đã hết hiệu lực (dư nợ = 0 nhưng cờ chưa gỡ).
- Liệt kê mọi dòng có ghi chú đặc biệt (cột "GHI CHÚ").
- Tính % số dòng có dữ liệu "Thời hạn thanh toán" (đánh giá mức đủ để làm báo cáo tuổi nợ).
- Xuất `analysis.json` + 4 biểu đồ PNG (`reconciliation.png`, `top_debtors.png`, `top_credit.png`, `concentration.png`) vào `<thư_mục_tạm>/charts/`.

## Bước 4 — Build báo cáo Word

Chạy:

```
node scripts/build_report.js <thư_mục_tạm>/analysis.json <thư_mục_tạm>/charts assets/sga_logo.png output/BaoCaoDanhGiaCongNo_<kỳ>_<yyyyMMdd_HHmm>.docx
```

Script tự động dựng báo cáo theo đúng layout đã chốt (xem `mapping.md` mục "Layout báo cáo"), với nội dung động theo `analysis.json`:

- Nếu không có chênh lệch số liệu (`discrepancies` rỗng) → mục 2 đổi thành "Kiểm tra chéo số liệu báo cáo" với nội dung xác nhận số liệu khớp, thay vì cảnh báo lỗi.
- Nếu không có khách hàng nào vượt ngưỡng tập trung → không hiển thị callout cảnh báo tập trung ở mục 3.
- Nếu không có ghi chú đặc biệt nào → bỏ hẳn mục 7, đánh lại số mục Kết luận thành mục 7.
- Danh sách khuyến nghị ở mục cuối chỉ liệt kê các hành động thực sự cần thiết cho kỳ đó (vd chỉ nhắc "sửa công thức" nếu kỳ đó thực sự phát hiện chênh lệch).

## Bước 5 — Kiểm tra trước khi giao

Render thử file `.docx` ra PDF/ảnh (`soffice.py --convert-to pdf` rồi `pdftoppm`) và xem qua để đảm bảo không lỗi bố cục (bảng bể trang, biểu đồ không hiển thị, chữ tràn khung...) trước khi giao cho người dùng.

## Bước 6 — Lưu Artifact và báo cáo kết quả

Lưu file `.docx` vào `missions/debt-evaluation/output/` theo đúng quy ước đặt tên tại `rules.md`. Báo cáo lại cho người dùng:

- Kỳ báo cáo đã xử lý (lấy từ E7/G7).
- Có phát hiện chênh lệch số liệu hay không (và số tiền lệch nếu có).
- Số khách hàng vượt ngưỡng cảnh báo tập trung.
- Đường dẫn Artifact đã lưu.
