# Ví dụ

## Input

Yêu cầu người dùng: "Đánh giá công nợ giúp tôi."

Tại thời điểm đọc, sheet `DEBT` có E7 = 01/01/2026, G7 = 31/05/2026, 122 công ty có phát sinh dữ liệu từ hàng 14–135.

## Output (tóm tắt `analysis.json` do `analyze_debt.py` sinh ra)

```json
{
  "ky_tu": "01/01/2026",
  "ky_den": "31/05/2026",
  "n_companies_total": 122,
  "totals": {
    "dau_ky_thu": 196321066.0,
    "trong_ky_thu": 711673177.3,
    "trong_ky_tra": 845265500,
    "cuoi_ky_thu": 306905743.3,
    "cuoi_ky_tra": 226845000
  },
  "discrepancies": [
    { "field": "trong_ky_thu", "report_value": 609570927.3, "true_value": 711673177.3, "diff": 102102250.0, "diff_pct": 14.3 }
  ],
  "top_debtors_pct": 84.9,
  "concentrated_customers": [
    { "ma": "SAIGONLAND", "pct": 27.8 },
    { "ma": "H&P", "pct": 23.5 }
  ]
}
```

## Output (báo cáo Word)

`build_report.js` đọc file trên và tự sinh:

- Metric card "Số liệu báo cáo bị thiếu" = "-102,1 tr đ" (lấy từ `discrepancies`, không phải số cố định viết cứng).
- Mục 2 hiển thị callout đỏ nêu đúng cột bị lệch (`trong_ky_thu`) và số tiền/% lệch.
- Mục 3 liệt kê callout "SAIGONLAND (27,8%), H&P (23,5%) - vượt ngưỡng cảnh báo tập trung 20%/khách hàng" (lấy từ `concentrated_customers`, không viết cứng tên khách hàng).

Artifact được lưu: `missions/debt-evaluation/output/BaoCaoDanhGiaCongNo_01012026-31052026_20260725_1730.docx`

---

## Ví dụ flow (kỳ báo cáo không phát hiện chênh lệch — sau khi sheet gốc đã được sửa)

Giả sử sau này người quản lý sheet đã sửa đúng vùng công thức Tổng cộng, và người dùng chạy lại Mission cho kỳ mới (đã tự đổi E7/G7 = 01/06/2026 - 30/06/2026):

↓

`analyze_debt.py` tính lại, so sánh với dòng Tổng cộng → `discrepancies` rỗng

↓

`build_report.js` tự động đổi mục 2 thành "Kiểm tra chéo số liệu báo cáo" (xác nhận khớp), card "Số liệu báo cáo bị thiếu" hiển thị "Không lệch"

↓

Không cần sửa bất kỳ script nào — toàn bộ thay đổi là tự động theo dữ liệu
