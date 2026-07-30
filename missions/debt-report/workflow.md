# Quy trình thực hiện

## Bước 1 — Xác nhận kỳ báo cáo

Nguồn dữ liệu là JSON do người dùng cung cấp

## Bước 2 — Nhận dữ liệu JSON

Lưu dữ liệu JSON người dùng cung cấp (dán trong chat hoặc đính kèm file `.json`) vào thư mục làm việc tạm, ví dụ `<thư_mục_tạm>/debt_data.json`. Dữ liệu là mảng object, mỗi object là 1 dòng công ty — xem mapping field JSON ↔ cột sheet gốc tại `mapping.md`. Bỏ qua các dòng rác cuối bảng (dòng chữ ký, ngày lập, dòng trống — nhận diện bằng "Mã công ty" rỗng hoặc field chứa văn bản không phải số liệu công ty).

*(Quy trình cũ dùng Google Drive connector tải file `.xlsx` từ Google Sheet đã ngừng dùng — xem lịch sử ở cuối file này nếu cần khôi phục.)*

## Bước 3 — Phân tích dữ liệu

Chạy:

```
python3 scripts/analyze_debt_json.py <thư_mục_tạm>/debt_data.json "<kỳ_từ_ddMMyyyy>" "<kỳ_đến_ddMMyyyy>" <thư_mục_tạm>
```

Script tự động:

- Nhận kỳ báo cáo từ tham số dòng lệnh (do người dùng cung cấp ở Bước 1) — không tự đọc từ file.
- Đọc toàn bộ dòng dữ liệu công ty trong JSON, bỏ qua dòng không có "Mã công ty".
- Tự cộng tay toàn bộ số liệu tổng hợp (Đầu kỳ/Trong kỳ/Cuối kỳ, cả 2 cột Phải thu và Phải trả).
- Nguồn JSON **không có dòng Tổng cộng gốc** để đối chiếu → mục kiểm tra chéo (`discrepancies`) để trống và đánh dấu `reconciliation_available: false` thay vì tự bịa số so sánh.
- Tính Top 10 khách nợ nhiều nhất, Top 10 khách trả trước nhiều nhất, % tập trung, danh sách khách hàng vượt ngưỡng cảnh báo tập trung (>20%/khách hàng).
- Nếu JSON có field tương đương cột "Khó đòi" thì tính danh sách còn hiệu lực/hết hiệu lực như cũ; nếu không có field này, đánh dấu `kho_doi_data_available: false` thay vì mặc định bằng 0.
- Liệt kê mọi dòng có ghi chú đặc biệt (field "Ghi chú").
- Tính % số dòng có dữ liệu "Thời hạn thanh toán" (đánh giá mức đủ để làm báo cáo tuổi nợ).
- Xuất `analysis.json` + 4 biểu đồ PNG (`reconciliation.png`, `top_debtors.png`, `top_credit.png`, `concentration.png`) vào `<thư_mục_tạm>/charts/`.

## Bước 4 — Build báo cáo Word

Chạy:

```
node scripts/build_report.js <thư_mục_tạm>/analysis.json <thư_mục_tạm>/charts assets/sga_logo.png output/BaoCaoDanhGiaCongNo_<kỳ>_<yyyyMMdd_HHmm>.docx
```

Script tự động dựng báo cáo theo đúng layout đã chốt (xem `mapping.md` mục "Layout báo cáo"), với nội dung động theo `analysis.json`:

- Nếu `reconciliation_available: false` (nguồn JSON không có số liệu Tổng cộng gốc để đối chiếu) → mục 2 đổi thành "Kiểm tra chéo số liệu báo cáo" với nội dung ghi rõ "Chưa được cung cấp — không có số liệu Tổng cộng gốc để đối chiếu", **không** được diễn giải thành "số liệu khớp".
- Nếu `reconciliation_available: true` và không có chênh lệch (`discrepancies` rỗng) → mục 2 xác nhận số liệu khớp như quy trình cũ.
- Nếu không có khách hàng nào vượt ngưỡng tập trung → không hiển thị callout cảnh báo tập trung ở mục 3.
- Nếu `kho_doi_data_available: false` → mục 4 ghi rõ "Chưa được cung cấp" thay vì "0 khách hàng khó đòi".
- Nếu không có ghi chú đặc biệt nào → bỏ hẳn mục 7, đánh lại số mục Kết luận thành mục 7.
- Danh sách khuyến nghị ở mục cuối chỉ liệt kê các hành động thực sự cần thiết cho kỳ đó (vd chỉ nhắc "sửa công thức" nếu kỳ đó thực sự phát hiện chênh lệch, chỉ nhắc bổ sung cột "Khó đòi" nếu `kho_doi_data_available: false`).

## Bước 5 — Kiểm tra trước khi giao

Render thử file `.docx` ra PDF/ảnh (`soffice.py --convert-to pdf` rồi `pdftoppm`) và xem qua để đảm bảo không lỗi bố cục (bảng bể trang, biểu đồ không hiển thị, chữ tràn khung...) trước khi giao cho người dùng.

## Bước 6 — Lưu Artifact và báo cáo kết quả

Lưu file `.docx` vào `missions/debt-report/output/` theo đúng quy ước đặt tên tại `rules.md`. Báo cáo lại cho người dùng:

- Kỳ báo cáo đã xử lý (do người dùng cung cấp ở Bước 1).
- Có đối chiếu được số liệu Tổng cộng gốc hay không, và nếu có thì có phát hiện chênh lệch hay không (số tiền lệch nếu có).
- Số khách hàng vượt ngưỡng cảnh báo tập trung.
- Đường dẫn Artifact đã lưu.
