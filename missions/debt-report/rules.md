# Quy tắc làm việc

Luôn lấy kỳ báo cáo từ ô E7/G7 của sheet `DEBT` tại thời điểm tải file — không tự đặt kỳ khác, không tự đoán kỳ nếu người dùng không nói rõ (mặc định dùng đúng kỳ đang thiết lập sẵn).

AI **không có quyền và không được tự ý sửa** ô E7/G7 hoặc bất kỳ ô nào khác trên Google Sheet gốc — Mission chỉ đọc dữ liệu. Nếu người dùng muốn đổi kỳ, hướng dẫn họ tự sửa trên Sheet rồi yêu cầu chạy lại.

Luôn tự tính lại số liệu tổng hợp từ dữ liệu chi tiết bằng `analyze_debt.py`, không lấy trực tiếp các ô Tổng cộng có sẵn trên sheet, do đã ghi nhận lỗi công thức (xem `mapping.md`). Nếu phát hiện chênh lệch, phải nêu rõ trong báo cáo, không bỏ qua.

Không tự sửa công thức trên sheet gốc — Mission chỉ đọc và nêu khuyến nghị, việc sửa file gốc do người quản lý sheet quyết định.

Không tự đổi tên cột "Phải trả" trên sheet gốc dù đã xác định là gây hiểu nhầm — chỉ nêu khuyến nghị trong báo cáo (xem `mapping.md`).

Giữ đúng layout báo cáo đã chốt tại `mapping.md` mục "Layout báo cáo Word" cho mọi lần chạy — không tự ý đổi màu, bố cục, hay nội dung mở đầu mà không có yêu cầu mới từ người dùng. Nếu người dùng yêu cầu thay đổi layout, cập nhật cả `mapping.md` lẫn `scripts/build_report.js` để đồng bộ cho các lần chạy sau.

Số lượng Top N khách hàng và ngưỡng cảnh báo tập trung lấy theo tham số `TOP_N` / `CONCENTRATION_THRESHOLD` trong `analyze_debt.py` (mặc định 10 và 20%) — chỉ đổi khi người dùng yêu cầu rõ ràng.

Luôn render thử báo cáo ra PDF/ảnh để kiểm tra bố cục trước khi giao cho người dùng (xem `workflow.md` Bước 5).

Nếu dữ liệu nguồn thiếu hoặc không xác định được (vd không đọc được E7/G7, sheet `DEBT` không tồn tại, file không mở được), báo lại rõ ràng cho người dùng — không tự tạo báo cáo với dữ liệu giả định.

## Quy ước đặt tên Artifact

```
missions/debt-evaluation/output/BaoCaoDanhGiaCongNo_<tuKy>-<denKy>_<yyyyMMdd_HHmm>.docx
```

Trong đó `<tuKy>` và `<denKy>` lấy từ E7/G7, định dạng `ddMMyyyy`. Ví dụ:

```
missions/debt-evaluation/output/BaoCaoDanhGiaCongNo_01012026-31052026_20260725_1730.docx
```

## Quy tắc chuẩn hóa tên

- Không sử dụng khoảng trắng, ký tự đặc biệt.
- Chỉ sử dụng chữ cái, số và dấu gạch ngang/gạch dưới (`-`, `_`).
- Thời gian tạo Artifact lấy thời điểm hiện tại lúc chạy Mission.
