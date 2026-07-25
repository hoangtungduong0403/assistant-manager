# Mẫu email (Template thật, xác nhận 2026-07-25)

> Template dưới đây thay thế bản nháp email trang trọng dạng bảng đã soạn ban đầu — đây là văn phong thật SGA đang dùng, dựa trên 3 ví dụ thật do người dùng cung cấp.

```
Kính gửi Anh/Chị! [@<Người liên hệ, nếu có>]
Em gửi Anh/Chị thông tin phí dịch vụ [tính đến <Tháng X (+ Tháng Y...)> năm <yyyy>] như sau:
Tổng số tiền: <Tổng cộng>đ

* <Tên khoản phí 1 (kèm kỳ nếu có nhiều kỳ)>: <Số tiền>đ
* <Tên khoản phí 2>: <Số tiền>đ

(Nếu có bất kỳ sự nhầm lẫn nào về thông tin trên, Anh/Chị phản hồi lại thông báo này)
Quý Công ty thanh toán theo thông tin sau:
Thanh toán từ <Tài khoản công ty / Tài khoản cá nhân>
Tên tài khoản: <...>
Số tài khoản: <...>
Ngân hàng: <...> - <Chi nhánh>
Nội dung: <{{noi_dung}} — xem templates/bank-accounts.md>

Trân trọng!
```

Ghi chú áp dụng:

- Dòng "tính đến ... như sau" chỉ liệt kê nếu có ≥ 2 kỳ trong 1 email (gộp nhiều tháng của cùng 1 dịch vụ); nếu chỉ 1 kỳ, có thể bỏ cụm "tính đến..." hoặc ghi rõ đúng 1 kỳ đó.
- Danh sách tài khoản + quy tắc chọn theo dịch vụ: xem `templates/bank-accounts.md`.
- Nếu không xác định được `{{noi_dung}}` (xem `mapping.md`), để trống và ghi "Chưa được cung cấp — cần điền tay trước khi gửi".

---

# Ví dụ

## Input

Yêu cầu người dùng: "Tạo message thông báo phí cho công ty 2CE, Tháng 5 và Tháng 6/2026, dịch vụ Dịch vụ hỗ trợ hồ sơ HCNS."

2 dòng dữ liệu khớp trong `DATA Revenue` (Mã công ty = 2CE, Chi tiết dịch vụ = "Dịch vụ hỗ trợ hồ sơ HCNS", Phân loại doanh thu = Tháng, Kỳ = 5 và 6):

| Kỳ | Thành tiền bao gồm VAT |
|---|---|
| Tháng 5/2026 | 2.160.000 đ |
| Tháng 6/2026 | 2.160.000 đ |

Dịch vụ này thuộc nhóm "Dịch vụ SGA thông thường khác" → dùng Tài khoản 2 (MB).

## Output

> Kính gửi Anh/Chị!
> Em gửi Anh/Chị thông tin phí dịch vụ tính đến Tháng 06 năm 2026 như sau:
> Tổng số tiền: 4.320.000 đ
>
> * Dịch vụ hỗ trợ hồ sơ HCNS Tháng 05/2026: 2.160.000đ
> * Dịch vụ hỗ trợ hồ sơ HCNS Tháng 06/2026: 2.160.000đ
>
> (Nếu có bất kỳ sự nhầm lẫn nào về thông tin trên, Anh/Chị phản hồi lại thông báo này)
> Quý Công ty thanh toán theo thông tin sau:
> Thanh toán từ Tài khoản công ty
> Tên tài khoản: CONG TY TNHH SAIGON ALH
> Số tài khoản: 380226868
> Ngân hàng: MB - PGD Thủ Đức
> Nội dung: **Chưa được cung cấp — cần điền tay trước khi gửi**
>
> Trân trọng!

Artifact được lưu: `missions/revenue-notification/output/RevenueNotification_2CE_T5T6_20260725_1030.md`

---

# Ví dụ flow (công ty có nhiều dịch vụ trong cùng kỳ → tách email riêng)

Yêu cầu: "Thông báo phí Quý 1 cho công ty XYZ" — XYZ có 2 dòng khớp Quý 1: 1 dòng Long-term, 1 dòng Short-term.

↓

Đọc `DATA Revenue`, lọc Mã công ty = XYZ, Phân loại doanh thu = Quý, Kỳ = 1

↓

Tìm thấy 2 dòng khớp (Long-term + Short-term)

↓

Xác định tài khoản cho từng dịch vụ (theo `templates/bank-accounts.md`)

↓

Tách thành 2 email riêng theo template thật ở trên, mỗi email 1 dịch vụ

↓

Lưu 2 Artifact:
- `RevenueNotification_XYZ_Q1_LongTerm_<yyyyMMdd_HHmm>.md`
- `RevenueNotification_XYZ_Q1_ShortTerm_<yyyyMMdd_HHmm>.md`

↓

Báo cáo: đã tạo 2/2 email cho công ty XYZ, Quý 1/2026
