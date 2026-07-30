# Mission: Đánh giá công nợ (Debt Evaluation)

## Mục tiêu

Đóng vai trò chuyên gia tài chính, đọc dữ liệu công nợ (JSON do người dùng cung cấp, tương đương sheet `DEBT` của file "SGA_Revenue & Debt") và tạo **báo cáo đánh giá công nợ** dạng Word — có letterhead công ty, metric card tóm tắt, cảnh báo rủi ro tập trung, bảng số liệu và biểu đồ — theo đúng layout đã được xác nhận với người dùng

Sau mỗi lần thực hiện, AI phải:

- Xác nhận đúng kỳ báo cáo do người dùng cung cấp.
- Tự tính lại toàn bộ số liệu tổng hợp từ dữ liệu chi tiết trong JSON.
- Nếu có số liệu Tổng cộng để đối chiếu thì nêu rõ chênh lệch; nếu nguồn JSON không có số liệu đối chiếu thì ghi "Chưa được cung cấp" cho mục kiểm tra chéo (xem `mapping.md`).
- Phân tích rủi ro tập trung công nợ, nợ khó đòi (nếu có dữ liệu), mức đầy đủ dữ liệu tuổi nợ, khoản trả trước.
- Sinh đủ 4 biểu đồ và báo cáo Word theo đúng layout đã chốt.
- Lưu Artifact theo đúng quy ước đặt tên.

## Trigger

### Thủ công

Ví dụ:

- "Đánh giá công nợ giúp tôi."
- "Tạo báo cáo công nợ theo kỳ mới."
- "Cập nhật lại báo cáo đánh giá công nợ."

## Input

Nguồn dữ liệu bây giờ là JSON do người dùng cung cấp trực tiếp (dán trong chat hoặc file `.json`), đại diện cho các dòng dữ liệu công ty của sheet `DEBT` (tương đương hàng 14 trở đi). Xem mapping cột JSON ↔ cột sheet gốc tại `mapping.md`.

  - Mục "2. Kiểm tra chéo số liệu" (so sánh số tự tính với số hiển thị sẵn trên sheet) **không thực hiện được** khi dùng nguồn JSON — báo cáo sẽ nêu rõ "Chưa được cung cấp" thay vì mục cảnh báo/kiểm tra chéo (xem `mapping.md`).
  - Nếu JSON không có cột "Khó đòi" (cột L gốc), mục 4 cũng ghi rõ "Chưa được cung cấp" thay vì suy diễn bằng 0.
- Logo công ty: đã trích xuất sẵn và lưu tại `sga_logo.png` trong thư mục Mission (không cần trích xuất lại mỗi lần chạy, trừ khi công ty đổi logo).


## Output

- 1 file Word (`.docx`) — báo cáo đánh giá công nợ đầy đủ 8 mục (hoặc 7 mục nếu kỳ đó không có ghi chú đặc biệt cần đối chiếu — xem `mapping.md`), lưu theo quy ước đặt tên tại `rules.md`.

## Giới hạn quan trọng

Toàn bộ dữ liệu đầu vào do người dùng cung cấp trực tiếp dưới dạng JSON. Vì vậy:

- AI không tự bịa hoặc suy diễn kỳ báo cáo — luôn hỏi lại người dùng nếu chưa nêu rõ.
- AI không tự bịa số liệu đối chiếu (dòng Tổng cộng gốc) hay cột "Khó đòi" nếu JSON không cung cấp — ghi rõ "Chưa được cung cấp" theo đúng nguyên tắc ở `CLAUDE.md`.
- Nếu người dùng muốn dùng lại quy trình Google Sheet cũ, cần nêu rõ yêu cầu — quy trình đó vẫn còn trong lịch sử `workflow.md` nhưng không phải mặc định nữa.
