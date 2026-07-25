# Các file cấp gốc cần cập nhật để hoàn thiện Mission "Đánh giá công nợ"

## 1. `README.md` (cấp gốc)

Thêm "Đánh giá công nợ (Debt Evaluation)" vào mục "Danh sách Mission":

```
## Danh sách Mission

Communication
Planning
Reporting
Knowledge
Báo giá (Quotation)
Revenue Notification Message
Đánh giá công nợ (Debt Evaluation)
...
```

## 2. `CLAUDE.md`

Thêm vào danh sách ví dụ Stateless Mission (mỗi lần chạy xử lý trọn vẹn 1 kỳ báo cáo hiện hành trên sheet, không phụ thuộc lần chạy trước):

```
## Stateless Mission

Không lưu trạng thái.

Ví dụ:

Meeting Note
Financial Analysis
Báo giá (Quotation)
Revenue Notification Message
Đánh giá công nợ (Debt Evaluation)
...
```

## 3. `shared/naming-convention.md`

Thêm quy ước đặt tên mới:

```
## Debt Evaluation

missions/debt-evaluation/output/BaoCaoDanhGiaCongNo_<tuKy>-<denKy>_<yyyyMMdd_HHmm>.docx
```

## 4. Thư mục Mission

Tạo thư mục `missions/debt-evaluation/` gồm:

- `mission.md`, `workflow.md`, `rules.md`, `mapping.md`, `examples.md`, `checklist.md`, `definition-of-done.md`
- `scripts/analyze_debt.py`, `scripts/build_report.js`
- `assets/sga_logo.png`
- `output/` (rỗng, chứa Artifact mỗi lần chạy)

## 5. Việc cần xác nhận thêm

- File ID Google Sheet "SGA_Revenue & Debt" đang hard-code trong `mission.md` (`18XReM8TVfivbddC1UAAKSJhhzVCSBhzeZdkY1qn5ZX4`) — xác nhận đây là file chính thức duy nhất, hay có thể thay đổi/có nhiều bản sao cần chọn.
- Cân nhắc báo cáo lại với người quản lý sheet về lỗi công thức và nhãn cột "Phải trả" sai bản chất đã phát hiện (xem `mapping.md`) — Mission chỉ nêu khuyến nghị trong báo cáo, việc sửa sheet gốc nằm ngoài phạm vi Mission này.
