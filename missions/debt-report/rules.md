# Quy tắc làm việc

**Từ 2026-07-30: nguồn dữ liệu là JSON do người dùng cung cấp, không còn dùng Google Drive.** Luôn lấy kỳ báo cáo do người dùng nêu rõ trong yêu cầu — nếu chưa nêu, phải hỏi lại trước khi phân tích, không tự đoán, không tái dùng kỳ của lần chạy trước.


Luôn tự tính lại số liệu tổng hợp từ dữ liệu chi tiết bằng `analyze_debt_json.py`, cộng tay từ toàn bộ dòng công ty trong JSON. Vì nguồn JSON không có dòng Tổng cộng gốc để đối chiếu, mục kiểm tra chéo số liệu phải ghi rõ "Chưa được cung cấp" (`reconciliation_available: false`) — không được tự suy diễn là "khớp" hay tự bịa số so sánh. Nếu về sau người dùng cung cấp thêm số liệu Tổng cộng gốc để đối chiếu, khôi phục logic phát hiện chênh lệch như quy trình cũ.

Nếu JSON không có field tương đương cột "Khó đòi", mục nợ khó đòi phải ghi "Chưa được cung cấp" (`kho_doi_data_available: false`), không mặc định là 0.

Không tự sửa công thức trên sheet gốc — Mission chỉ đọc và nêu khuyến nghị, việc sửa file gốc do người quản lý sheet quyết định.

Không tự đổi tên cột "Phải trả" trên sheet gốc dù đã xác định là gây hiểu nhầm — chỉ nêu khuyến nghị trong báo cáo (xem `mapping.md`).

Giữ đúng layout báo cáo đã chốt tại `mapping.md` mục "Layout báo cáo Word" cho mọi lần chạy — không tự ý đổi màu, bố cục, hay nội dung mở đầu mà không có yêu cầu mới từ người dùng. Nếu người dùng yêu cầu thay đổi layout, cập nhật cả `mapping.md` lẫn `scripts/build_report.js` để đồng bộ cho các lần chạy sau.

Số lượng Top N khách hàng và ngưỡng cảnh báo tập trung lấy theo tham số `TOP_N` / `CONCENTRATION_THRESHOLD` trong `analyze_debt.py` (mặc định 10 và 20%) — chỉ đổi khi người dùng yêu cầu rõ ràng.

Luôn render thử báo cáo ra PDF/ảnh để kiểm tra bố cục trước khi giao cho người dùng (xem `workflow.md` Bước 5).

Nếu dữ liệu nguồn thiếu hoặc không xác định được (vd không đọc được E7/G7, sheet `DEBT` không tồn tại, file không mở được), báo lại rõ ràng cho người dùng — không tự tạo báo cáo với dữ liệu giả định.

## Quy ước đặt tên Artifact

```
missions/debt-report/output/BaoCaoDanhGiaCongNo_<yyyyMMdd_HHmm>.docx

```
missions/debt-report/output/BaoCaoDanhGiaCongNo_20260725_1730.docx
```

## Quy tắc chuẩn hóa tên

- Không sử dụng khoảng trắng, ký tự đặc biệt.
- Chỉ sử dụng chữ cái, số và dấu gạch ngang/gạch dưới (`-`, `_`).
- Thời gian tạo Artifact lấy thời điểm hiện tại lúc chạy Mission.
