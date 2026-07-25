# Mission: Đánh giá công nợ (Debt Evaluation)

## Mục tiêu

Đóng vai trò chuyên gia tài chính, đọc dữ liệu công nợ trong sheet `DEBT` của file "SGA_Revenue & Debt" (Google Sheet) và tạo **báo cáo đánh giá công nợ** dạng Word — có letterhead công ty, metric card tóm tắt, cảnh báo rủi ro tập trung, bảng số liệu và biểu đồ — theo đúng layout đã được xác nhận với người dùng (2026-07-25).

Kỳ báo cáo được xác định hoàn toàn bởi 2 ô **E7** (từ ngày) và **G7** (đến ngày) trên chính sheet `DEBT`. Đổi kỳ báo cáo cho lần chạy sau = đổi 2 ô này trên Google Sheet gốc rồi chạy lại Mission — **không cần sửa bất kỳ script hay tài liệu nào** trong Mission.

Sau mỗi lần thực hiện, AI phải:

- Đọc đúng kỳ báo cáo hiện hành từ E7/G7.
- Tự tính lại toàn bộ số liệu tổng hợp từ dữ liệu chi tiết (không tin tưởng mù quáng các ô Tổng cộng có sẵn — sheet gốc có lỗi công thức đã biết, xem `mapping.md`).
- Phát hiện và nêu rõ mọi chênh lệch giữa số hiển thị trên sheet và số tính đúng.
- Phân tích rủi ro tập trung công nợ, nợ khó đòi, mức đầy đủ dữ liệu tuổi nợ, khoản trả trước.
- Sinh đủ 4 biểu đồ và báo cáo Word theo đúng layout đã chốt.
- Lưu Artifact theo đúng quy ước đặt tên.

## Trigger

### Thủ công

Ví dụ:

- "Đánh giá công nợ giúp tôi."
- "Tạo báo cáo công nợ theo kỳ mới." (sau khi người dùng đã tự đổi E7/G7 trên Sheet)
- "Cập nhật lại báo cáo đánh giá công nợ."

## Input

- File Google Sheet "SGA_Revenue & Debt" — File ID: `18XReM8TVfivbddC1UAAKSJhhzVCSBhzeZdkY1qn5ZX4` (xác nhận lại với người dùng nếu link thay đổi).
- Sheet `DEBT`, ô E7 (từ ngày) / G7 (đến ngày) xác định kỳ báo cáo, dữ liệu chi tiết từ hàng 14.
- Logo công ty: đã trích xuất sẵn và lưu tại `assets/sga_logo.png` (không cần trích xuất lại mỗi lần chạy, trừ khi công ty đổi logo).

## Output

- 1 file Word (`.docx`) — báo cáo đánh giá công nợ đầy đủ 8 mục (hoặc 7 mục nếu kỳ đó không có ghi chú đặc biệt cần đối chiếu — xem `mapping.md`), lưu theo quy ước đặt tên tại `rules.md`.

## Giới hạn quan trọng

Mission này **không có quyền ghi/sửa trực tiếp vào Google Sheet gốc** (connector Google Drive hiện chỉ hỗ trợ đọc/tải file, không hỗ trợ chỉnh sửa cell). Vì vậy:

- Nếu người dùng muốn đổi kỳ báo cáo, họ cần **tự sửa ô E7/G7 trên Google Sheet** (hoặc AI hướng dẫn thao tác), sau đó mới yêu cầu AI chạy lại Mission.
- AI không tự ý bịa kỳ báo cáo hoặc tự chạy với kỳ khác kỳ đang được thiết lập trên sheet.
