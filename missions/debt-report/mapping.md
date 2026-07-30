# Mapping dữ liệu và Layout báo cáo

## Nguồn dữ liệu JSON (từ 2026-07-30, thay cho Google Drive)

Người dùng cung cấp trực tiếp một mảng JSON, mỗi object là 1 dòng công ty. Mapping field JSON ↔ cột sheet gốc (dùng bởi `analyze_debt_json.py`):

| Field JSON | Cột sheet gốc | Ý nghĩa |
|---|---|---|
| `STT` | A | STT |
| `Mã công ty` | B | Mã công ty (khóa) |
| `Mã số thuế` | C | Mã số thuế |
| `Phải thu ĐẦU KỲ` | E | Đầu kỳ — Phải thu |
| `Phải trả ĐẦU KỲ` | F | Đầu kỳ — Phải trả |
| `Phải thu TRONG KỲ` | G | Trong kỳ — Phải thu |
| `Phải trả TRONG KỲ` | H | Trong kỳ — Phải trả (thực chất tiền khách đã thanh toán, xem mục "Lưu ý bản chất kế toán") |
| `Phải thu CUỐI kỳ` | I | Cuối kỳ — Phải thu (net dương) |
| `Phải trả CUỐI kỳ` | J | Cuối kỳ — Phải trả (net âm, hiển thị dương) |
| `Ghi chú` | K | Ghi chú |
| — (không có trong JSON quan sát 2026-07-30) | L | Khó đòi — nếu JSON không có field này, đánh dấu `kho_doi_data_available: false`, không suy diễn bằng 0 |
| `THỜI HẠN THANH TOÁN` | M | Thời hạn thanh toán |

Giá trị `""` (chuỗi rỗng) cho các field số tiền được hiểu là 0 khi cộng tổng, giống cách xử lý ô trống trên sheet gốc.

**Khác biệt quan trọng so với nguồn Google Sheet:**

- JSON không có ô E7/G7 → kỳ báo cáo phải do người dùng cung cấp qua tham số dòng lệnh (xem `workflow.md` Bước 1, 3), script không tự đọc được.
- JSON không có dòng Tổng cộng gốc (tương đương hàng 12) → không thể đối chiếu phát hiện lỗi công thức như quy trình cũ. `analysis.json` sẽ có `reconciliation_available: false` và mục 2 báo cáo ghi "Chưa được cung cấp" thay vì cảnh báo lệch hoặc xác nhận khớp.
- Dòng rác cuối bảng (chữ ký, ngày lập, ô kẹt công thức lạc chỗ...) phải được lọc bỏ trước khi phân tích — nhận diện bằng "Mã công ty" rỗng/None hoặc không phải tên công ty hợp lệ.

## Vị trí dữ liệu nguồn (quy trình Google Sheet cũ — không còn dùng mặc định)

- File: "SGA_Revenue & Debt" (Google Sheet), File ID `18XReM8TVfivbddC1UAAKSJhhzVCSBhzeZdkY1qn5ZX4`.
- Sheet: `DEBT` — "BÁO CÁO TỔNG HỢP CÔNG NỢ".
- Kỳ báo cáo: ô **E7** (từ ngày), **G7** (đến ngày).
- Header bảng: hàng 10–11. Dữ liệu công ty: từ hàng 14.

## Cấu trúc cột (hàng 14 trở đi)

| Cột | Ý nghĩa |
|---|---|
| A | STT (công thức SUBTOTAL, tự tính) |
| B | Mã công ty (khóa) |
| C | Mã số thuế |
| D | Tên công ty (IMPORTRANGE từ file ngoài — thường rỗng khi đọc bằng openpyxl, không dùng) |
| E | Đầu kỳ — Phải thu |
| F | Đầu kỳ — Phải trả |
| G | Trong kỳ — Phải thu (SUMIFS từ `DATA Revenue`, lọc theo kỳ E7:G7) |
| H | Trong kỳ — Phải trả (SUMIFS từ `DATA Pay` — **thực chất là tiền khách đã thanh toán/thu vào, không phải khoản SGA phải trả nhà cung cấp** — xem mục "Lưu ý bản chất kế toán" bên dưới) |
| I | Cuối kỳ — Phải thu (net dương) |
| J | Cuối kỳ — Phải trả (net âm, hiển thị dương) |
| K | Ghi chú |
| L | Khó đòi (giá trị quan sát được: "Khó đòi", "Nợ khó đòi", hoặc rỗng) |
| M | Thời hạn thanh toán |

## Lỗi công thức đã biết trên sheet gốc (tại thời điểm khảo sát 2026-07-25)

1. **G12 (Tổng cộng — Trong kỳ Phải thu)** dùng `SUM(G14:G108)`, trong khi các cột Tổng cộng khác (E,F,H,J) dùng `SUM(...14:473)` và cột I dùng đến `650`. Nếu dữ liệu thật vượt quá dòng 108 (rất dễ xảy ra khi có thêm khách hàng mới), tổng "Trong kỳ Phải thu" trên sheet sẽ **thiếu** so với thực tế. Đã ghi nhận thực tế thiếu 102.102.250đ (~14,3%) ở kỳ 01/01–31/05/2026, do 27 công ty nằm ngoài vùng SUM.
2. Công thức G14 (SUMIFS lọc theo kỳ + mã công ty từ `DATA Revenue`) có các vùng tham chiếu không cùng kích thước (`$Z$10:$Z$11015` và `$O$10:$O$11015` cho vùng tổng/điều kiện 1, nhưng `$O$10:$O$2015` và `$B$10:$B$2015` cho điều kiện 2–3) — rủi ro bỏ sót dữ liệu nằm sau dòng 2015 của `DATA Revenue`.
3. Cột E/F (Đầu kỳ) lấy qua `IMPORTRANGE` từ nhiều spreadsheet ngoài khác nhau, bọc trong `IFERROR(...,"")` — lỗi truy cập sẽ âm thầm trả về rỗng thay vì báo lỗi.

**Vì các lỗi trên, `analyze_debt.py` luôn tự cộng tay từ dữ liệu chi tiết (hàng 14 trở đi) thay vì tin vào dòng Tổng cộng (hàng 12) có sẵn.** Nếu về sau sheet gốc được sửa đúng (range nhất quán), số tự tính và số trên sheet sẽ khớp nhau và mục "2. Số liệu báo cáo đang hiển thị SAI" trong báo cáo sẽ tự động đổi thành "Kiểm tra chéo số liệu báo cáo" (xác nhận khớp) — không cần sửa script.

## Lưu ý bản chất kế toán — cột "Phải trả" (F, H)

Cột F/H lấy dữ liệu từ `DATA Pay`, và cấu trúc thật của `DATA Pay` (cột "Thanh toán", "Tài khoản nhận" trỏ về tài khoản ngân hàng của chính SGA) cho thấy đây là **tiền khách hàng đã thanh toán vào cho SGA**, không phải khoản SGA nợ ai. Gọi là "Phải trả" là sai bản chất — về logic tính toán (Đầu kỳ + Tăng − Giảm = Cuối kỳ) vẫn đúng, nhưng **tên cột gây hiểu nhầm nghiêm trọng**. Báo cáo đánh giá luôn nhắc lại điểm này ở mục khuyến nghị cuối cùng. Nếu người quản lý sheet đồng ý đổi tên cột trên sheet gốc, script không cần sửa gì thêm (vẫn đọc đúng vị trí cột).

## Layout báo cáo Word (đã xác nhận với người dùng — 2026-07-25)

1. **Letterhead**: bảng 2 cột không viền — cột trái là logo SGA (`assets/sga_logo.png`, 95×95), cột phải là tên công ty (đậm) + địa chỉ (nghiêng, màu xám) + hotline (nghiêng, màu xám).
2. **Tiêu đề**: "BÁO CÁO ĐÁNH GIÁ CÔNG NỢ", in đậm, cỡ 18 (size 36 half-point), màu tím đậm `#26215C`, **căn giữa**.
3. **Subheader**: chỉ 1 dòng "Kỳ báo cáo: <từ ngày> - <đến ngày>", nghiêng, màu xám, **căn giữa**. Không hiển thị dòng "Người thực hiện/Ngày lập" hay "Nguồn dữ liệu" (đã bỏ theo yêu cầu người dùng).
4. **Mục 1 — Tổng quan số liệu**: mở đầu bằng 4 metric card (bảng 4 cột, nền màu):
   - Card 1 (nền xám `#F1EFE8`): "Công nợ phải thu cuối kỳ" — giá trị + số công ty còn nợ.
   - Card 2 (nền đỏ nhạt `#FCEBEB`, chữ đỏ `#A32D2D`): "Top N chiếm tổng nợ" — %.
   - Card 3 (nền vàng nhạt `#FAEEDA`, chữ nâu `#854F0B`): "Số liệu báo cáo bị thiếu" — số tiền lệch (hoặc "Không lệch" nếu không có chênh lệch).
   - Card 4 (nền xám): "Nợ khó đòi còn hiệu lực" — số tiền + % + số khách hàng.
   - Ngay sau đó là callout đỏ nêu khách hàng/nhóm rủi ro tập trung chính, rồi bảng số liệu tổng hợp (Đầu kỳ/Trong kỳ/Cuối kỳ) và biểu đồ đối chiếu (`reconciliation.png`).
5. **Mục 2** — động theo `discrepancies`: nếu có chênh lệch → liệt kê từng callout đỏ; nếu không → 1 đoạn xác nhận khớp số liệu.
6. **Mục 3 — Rủi ro tập trung**: bảng Top N khách nợ + `top_debtors.png` + `concentration.png` + callout (nếu có khách vượt ngưỡng).
7. **Mục 4 — Nợ khó đòi**, **Mục 5 — Mức đủ dữ liệu tuổi nợ**: đoạn văn động theo số liệu.
8. **Mục 6 — Khoản dư có/trả trước**: bảng Top N khách trả trước + `top_credit.png` + giải thích bản chất kế toán (deferred revenue).
9. **Mục 7 (nếu có ghi chú đặc biệt)**: liệt kê từng dòng ghi chú.
10. **Mục Kết luận** (số thứ tự tự điều chỉnh theo có/không có mục 7): danh sách khuyến nghị hành động, chỉ hiện các mục thực sự áp dụng cho kỳ đó.

## Ngưỡng và tham số có thể chỉnh trong `analyze_debt.py`

- `TOP_N = 10` — số lượng khách hàng hiển thị trong bảng Top khách nợ / Top khách trả trước.
- `CONCENTRATION_THRESHOLD = 20.0` — % công nợ của 1 khách hàng đơn lẻ để tính là "vượt ngưỡng cảnh báo tập trung".

Đổi 2 tham số này trực tiếp trong file script nếu người dùng yêu cầu ngưỡng khác cho lần chạy sau.
