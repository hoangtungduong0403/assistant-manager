# Danh sách tài khoản thanh toán

> **Nguồn:** người dùng cung cấp trực tiếp trong hội thoại thiết lập Mission (2026-07-25). **Chưa xác nhận vị trí lưu trữ chính thức** (Drive Sheet/Doc hay chỉ paste tay) — xem `mapping.md` mục "Vấn đề cần xác nhận".

## Tài khoản công ty

### 1. Dịch vụ cho thuê văn phòng

- Tên tài khoản: CT TNHH SAIGON ALH
- Số tài khoản: 1060869999
- Ngân hàng: Vietcombank - CN Tân Định
- Nội dung: `{{noi_dung}}`

### 2. Dịch vụ thanh toán công ty SGA

- Tên tài khoản: CONG TY TNHH SAIGON ALH
- Số tài khoản: 380226868
- Ngân hàng: MB - PGD Thủ Đức
- Nội dung: `{{noi_dung}}`

## Tài khoản cá nhân

### 3. Tài khoản thanh toán cá nhân và các dịch vụ riêng của Viettel

- Tên tài khoản: NGUYEN THI THUY HANG
- Số tài khoản: 0986197540
- Ngân hàng: VP BANK - CN TPHCM
- Nội dung: `{{noi_dung}}`

## Quy tắc chọn tài khoản theo dịch vụ (rút ra từ 3 ví dụ thật, đã đối chiếu khớp)

| Loại dịch vụ (theo `Chi tiết dịch vụ` / `Loại dịch vụ` trong `DATA Revenue`) | Tài khoản áp dụng |
|---|---|
| Dịch vụ cho thuê văn phòng / chỗ ngồi cố định | Tài khoản 1 (Vietcombank) |
| Dịch vụ hóa đơn điện tử (HDDT) / dịch vụ liên quan Viettel | Tài khoản 3 (VPBank cá nhân) |
| Các dịch vụ SGA thông thường khác (phí kế toán/HCNS/pháp lý theo gói Long-term/Short-term) | Tài khoản 2 (MB) |

Nếu dịch vụ không khớp rõ ràng với 1 trong 3 nhóm trên, **không tự đoán** — hỏi lại người dùng nên dùng tài khoản nào trước khi đưa vào email.

## Nội dung chuyển khoản (`{{noi_dung}}`)

**Chưa xác định công thức chính xác — cần xác nhận thêm.** Quan sát từ 3 ví dụ:

- `MIN HOME TT PHI THUE VP T6 T7.2026` (TK1, thuê VP, gộp 2 tháng)
- `Chuyen tien` (TK3, không theo pattern rõ ràng)
- `MIN HOME TT PHI DV` (TK2, phí dịch vụ thường)

Pattern quan sát được: `<Tên viết tắt khách hàng> TT <Loại phí viết tắt> [<Kỳ viết tắt>]`. Tuy nhiên **nguồn của "Tên viết tắt khách hàng" (vd "MIN HOME") chưa xác định** — không có trong `DATA Revenue` (chỉ có Mã công ty dạng "2CE", "2HITACHI"...). Không tự suy diễn tên viết tắt — để trống và hỏi người dùng cho đến khi có nguồn dữ liệu xác nhận.
