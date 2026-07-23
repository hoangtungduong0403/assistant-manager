# Các file cấp gốc cần cập nhật để hoàn thiện Mission "Báo giá"

Mission mới không tự động xuất hiện trong các file cấu hình cấp gốc — cần bổ sung thủ công như sau:

## 1. `README.md` (cấp gốc)

Thêm "Báo giá" vào mục "Danh sách Mission":

```
## Danh sách Mission

Communication
Planning
Reporting
Knowledge
Báo giá (Quotation)
...
```

## 2. `CLAUDE.md`

Thêm "Báo giá" vào danh sách ví dụ Stateless Mission:

```
## Stateless Mission

Không lưu trạng thái.

Ví dụ:

Meeting Note
Financial Analysis
Báo giá (Quotation)
...
```

## 3. `shared/naming-convention.md`

Thêm 2 quy ước đặt tên mới:

```
## Summary Quotation

SummaryQuotation_<yyyyMMdd_HHmm>.xlsx

## Single Quotation

Quotation_<TênKháchHàng>_<yyyyMMdd_HHmm>.xlsx
```

## 4. Thư mục Template

Cần tạo thư mục `missions/quotation/templates/` và đặt vào đó:

- `SummaryQuotation_Template.xlsx`
- `SingleQuotation_Template.xlsx`

Sau khi có 2 file Template thật, cần đọc lại cấu trúc cột thực tế và cập nhật `mapping.md` trong mission này cho khớp (mapping hiện tại là mapping đề xuất, dựa trên mô tả nghiệp vụ, chưa đối chiếu với Template thật).
