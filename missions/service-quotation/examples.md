# Ví dụ

## Input

Client Information (3 dòng):

| Tên công ty | Người liên hệ | Sản phẩm/Dịch vụ | Số lượng | Đơn giá |
|---|---|---|---|---|
| Toyota Việt Nam | Anh Phú | Dịch vụ kế toán trọn gói | 1 | 15.000.000đ |
| FPT Software | Chị Lan | Dịch vụ kế toán trọn gói | 1 | 12.000.000đ |
| Bracon | Anh Luong | Dịch vụ báo cáo thuế Quý | 1 | 5.000.000đ |

## Output

### Summary Quotation

1 file `SummaryQuotation_20260723_1430.xlsx` với 3 dòng mới, mỗi dòng tương ứng 1 khách hàng ở trên, dữ liệu được mapping đúng cột theo Template.

### Single Quotation

3 file riêng biệt:

- `Quotation_ToyotaVietNam_20260723_1430.xlsx`
- `Quotation_FPTSoftware_20260723_1430.xlsx`
- `Quotation_Bracon_20260723_1430.xlsx`

Mỗi file chỉ chứa thông tin báo giá của đúng 1 khách hàng tương ứng.

---

# Ví dụ flow

Nhận file Client Information (3 khách hàng)

↓

Đọc Template Summary Quotation

↓

Mapping + thêm 3 dòng vào Summary Quotation

↓

Lưu Summary Quotation

↓

Đọc Template Single Quotation

↓

Sinh 3 file Quotation riêng (1 file / khách hàng)

↓

Lưu 3 file theo quy ước đặt tên

↓

Báo cáo: đã xử lý 3/3 khách hàng, 4 Artifact đã sinh (1 Summary + 3 Single)
