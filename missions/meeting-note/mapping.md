# Mapping giữa Meeting Brief và Template

## Vị trí file template

File mẫu chính thức: `missions/meeting-note/templates/MeetingNote.docx`.

Ghi chú: `README.md` cấp gốc của dự án mô tả `templates/` là thư mục dùng chung ở cấp gốc dự án (ngang hàng với `missions/`, `artifacts/`...). Tuy nhiên, template của Mission Meeting Note thực tế được đặt trong thư mục con của Mission (`missions/meeting-note/templates/`), không phải ở `templates/` cấp gốc. Khi thực hiện Mission, luôn đọc file tại `missions/meeting-note/templates/MeetingNote.docx`; nếu cách tổ chức này áp dụng chung cho các Mission khác, nên cập nhật lại mục "Kiến trúc" trong `README.md` cho khớp với cách triển khai thực tế.

---

## Ngày

Nguồn

Ngày diễn ra cuộc họp.

Điền vào

Trường "Ngày".

---

## Đại diện

Nguồn

Tên khách hàng hoặc phòng ban.

Điền vào

Trường "Đại diện".

Ghi chú bổ sung

Nếu cuộc họp là nội bộ (không có công ty khách hàng/đối tác), điền "SGA (Họp nội bộ)", kèm bộ phận liên quan nếu xác định được. Không để trống, không tự suy diễn tên công ty nếu dữ liệu nguồn không nêu.

---

## Thời gian

Nguồn

Thời gian bắt đầu và kết thúc cuộc họp.

Điền vào

Trường "Thời gian".

Ghi chú bổ sung

Nếu dữ liệu nguồn chỉ nêu một trong hai mốc (ví dụ chỉ có giờ kết thúc), ghi rõ mốc còn lại là "Chưa được đề cập". Không suy diễn giờ bắt đầu từ giờ kết thúc hoặc ngược lại.

---

## Địa chỉ

Nguồn

Địa điểm họp hoặc đường link Microsoft Teams.

Điền vào

Trường "Địa chỉ".

---

## Người tham dự

Nguồn

Danh sách người tham gia.

Điền thành danh sách.

Ghi chú bổ sung

Nếu dữ liệu nguồn nêu rõ có bên/nhóm vắng mặt, thêm một dòng riêng trong danh sách: "Vắng mặt: …".

Quy tắc mặc định khi không có danh sách người tham dự cụ thể

- Cuộc họp nội bộ: mặc định là "SGA (nội bộ)".
- Cuộc họp khách hàng: mặc định là "SGA và <Tên khách hàng>".

Đây là mặc định khi ghi chú không liệt kê tên/chức danh người tham dự cụ thể — không phải suy diễn danh tính từng cá nhân, chỉ xác định phạm vi các bên tham gia (nội bộ SGA, hay SGA + khách hàng).

---

## Nội dung tư vấn

Nguồn

Meeting Brief.

Điền thành nội dung tóm tắt, tách rõ theo 4 nhóm:

- Chủ đề chính
- Các vấn đề được thảo luận
- Quyết định đã thống nhất
- Các vấn đề còn mở (bao gồm cả các trường hợp thiếu người phụ trách hoặc thiếu mốc thời gian)

---

## Thông tin công việc (Mục 2 của form)

Nguồn

Các công việc hoặc yêu cầu phát sinh từ cuộc họp (đối với họp khách hàng: yêu cầu của khách hàng; đối với họp nội bộ: các yêu cầu công việc được thống nhất cần triển khai).

Điền vào

Mục "2. THÔNG TIN CÔNG VIỆC" — liệt kê dạng gạch đầu dòng, ngắn gọn, làm tổng quan trước khi đi vào bảng Action Items chi tiết ở mục 3.

Vấn đề cần xác nhận

Tiêu đề mục 2 trong file `MeetingNote.docx` hiện trùng với tiêu đề mục 1 ("THÔNG TIN CÔNG VIỆC"). Cần xác nhận với người quản lý template xem đây có phải lỗi khi tạo file gốc hay không.

---

## Công việc thực hiện (Bảng ở Mục 3 của form)

Nguồn

Action Items.

Điền vào bảng cuối tài liệu — 4 cột: SGA | THỜI HẠN | TÊN CÔNG TY | THỜI HẠN.

Quy tắc điền

- Cột "SGA": Công việc + (Người phụ trách phía SGA). Nếu người phụ trách chưa xác định trong dữ liệu nguồn, ghi "(Người phụ trách: Chưa được đề cập)".
- Cột "TÊN CÔNG TY": chỉ điền khi cuộc họp có công ty khách hàng/đối tác với Action Item riêng cho họ. Với cuộc họp nội bộ, ghi "Không áp dụng (họp nội bộ)" và cột "THỜI HẠN" tương ứng ghi "—".
- Nếu số Action Item nhiều hơn số hàng có sẵn trong bảng mẫu, nhân bản thêm hàng theo đúng định dạng gốc (độ rộng cột, font chữ Palatino Linotype, màu 604412).
