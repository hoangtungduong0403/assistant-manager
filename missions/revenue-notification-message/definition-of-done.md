# Điều kiện hoàn thành Mission

Mission chỉ được xem là hoàn thành khi:

- Đã xác định đúng công ty và đúng kỳ theo yêu cầu người dùng.
- Đã lọc đúng toàn bộ dòng dữ liệu khớp trong `DATA Revenue` (không bỏ sót dịch vụ nào của công ty trong kỳ đó).
- Nếu có nhiều dịch vụ trong cùng kỳ, đã tạo đúng số email tương ứng (1 email / dịch vụ, không gộp, không thiếu).
- Nếu không tìm thấy dữ liệu khớp, đã báo lại rõ ràng cho người dùng thay vì tạo email với dữ liệu giả định.
- Nội dung mỗi email chỉ dùng dữ liệu đã xác nhận (không dùng các cột "chưa xác nhận" tại `mapping.md`).
- Email không đề cập trạng thái thanh toán / hạn thu / số tiền còn lại phải thu.
- Không còn trường thông tin bắt buộc bị bỏ trống mà không ghi rõ "Chưa được cung cấp".
- Mỗi email đã được lưu thành Artifact riêng theo đúng quy ước đặt tên.
- Email chỉ ở dạng bản nháp — Mission không tự gửi đi.

Nếu bất kỳ điều kiện nào chưa đạt, Mission chưa được coi là hoàn thành.
