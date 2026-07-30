/*
 * Build báo cáo đánh giá công nợ (Word) từ analysis.json
 * ========================================================
 * USAGE:
 *   node build_report.js <analysis.json> <charts_dir> <logo_path> <output.docx>
 *
 * Đọc toàn bộ số liệu đã tính sẵn bởi analyze_debt.py và dựng file .docx
 * đúng theo layout đã chốt: letterhead (logo + tên công ty) -> tiêu đề +
 * kỳ báo cáo (căn giữa) -> 4 metric card -> callout rủi ro tập trung ->
 * 8 mục nội dung kèm bảng/biểu đồ.
 */
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell,
  WidthType, ShadingType, BorderStyle, AlignmentType, VerticalAlign, ImageRun,
} = require("docx");

const [, , analysisPath, chartsDir, logoPath, outputPath] = process.argv;
if (!analysisPath || !chartsDir || !logoPath || !outputPath) {
  console.error("Usage: node build_report.js <analysis.json> <charts_dir> <logo_path> <output.docx>");
  process.exit(1);
}
const A = JSON.parse(fs.readFileSync(analysisPath, "utf-8"));

const DXA_PAGE_WIDTH = 11906;
const PAGE_MARGIN = 1000;
const USABLE_WIDTH = DXA_PAGE_WIDTH - PAGE_MARGIN * 2;

const COLOR_HEADER = "26215C";
const COLOR_RED = "A32D2D", COLOR_RED_BG = "FCEBEB";
const COLOR_AMBER = "854F0B", COLOR_AMBER_BG = "FAEEDA";
const COLOR_MUTED = "5F5E5A";
const COLOR_TABLE_HEADER_BG = "EEEDFE";
const COLOR_GRAY_BG = "F1EFE8", COLOR_GRAY_VALUE = "2C2C2A", COLOR_GRAY_SUB = "888780";

const fmt = (n) => Math.round(n).toLocaleString("vi-VN") + " đ";
const fmtTr = (n) => (n / 1e6).toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + " tr đ";
const fmtPct = (n) => n.toLocaleString("vi-VN", { maximumFractionDigits: 1 }) + "%";

function h1(text) { return new Paragraph({ text, heading: HeadingLevel.HEADING_1, spacing: { before: 300, after: 150 } }); }
function p(text, opts = {}) {
  return new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text, bold: !!opts.bold, italics: !!opts.italics, color: opts.color, size: opts.size })] });
}
function bullet(text) { return new Paragraph({ text, bullet: { level: 0 }, spacing: { after: 60 } }); }

function calloutBox(text, { bg, borderColor, textColor }) {
  return new Table({
    width: { size: USABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [USABLE_WIDTH],
    rows: [new TableRow({ children: [new TableCell({
      width: { size: USABLE_WIDTH, type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: bg },
      borders: {
        top: { style: BorderStyle.SINGLE, size: 4, color: borderColor },
        bottom: { style: BorderStyle.SINGLE, size: 4, color: borderColor },
        left: { style: BorderStyle.SINGLE, size: 24, color: borderColor },
        right: { style: BorderStyle.SINGLE, size: 4, color: borderColor },
      },
      margins: { top: 120, bottom: 120, left: 160, right: 160 },
      children: [new Paragraph({ children: [new TextRun({ text, color: textColor, bold: true })] })],
    })] })],
  });
}

function dataTable(headers, rows, colWidths) {
  const total = colWidths.reduce((a, b) => a + b, 0);
  const scaled = colWidths.map((w) => Math.round((w / total) * USABLE_WIDTH));
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map((htext, i) => new TableCell({
      width: { size: scaled[i], type: WidthType.DXA },
      shading: { type: ShadingType.CLEAR, fill: COLOR_TABLE_HEADER_BG },
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 80, bottom: 80, left: 100, right: 100 },
      children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT, children: [new TextRun({ text: htext, bold: true, size: 20 })] })],
    })),
  });
  const bodyRows = rows.map((r) => new TableRow({
    children: r.map((cell, i) => new TableCell({
      width: { size: scaled[i], type: WidthType.DXA },
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({ alignment: i === 0 ? AlignmentType.LEFT : AlignmentType.RIGHT, children: [new TextRun({ text: String(cell), size: 20 })] })],
    })),
  }));
  return new Table({ width: { size: USABLE_WIDTH, type: WidthType.DXA }, columnWidths: scaled, rows: [headerRow, ...bodyRows] });
}

function chartImage(file, width, height) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 200 },
    children: [new ImageRun({ type: "png", data: fs.readFileSync(path.join(chartsDir, file)), transformation: { width, height } })],
  });
}

function metricCard(label, value, sub, { bg, valueColor, labelColor, subColor }) {
  return new TableCell({
    width: { size: Math.round(USABLE_WIDTH / 4), type: WidthType.DXA },
    shading: { type: ShadingType.CLEAR, fill: bg },
    margins: { top: 160, bottom: 160, left: 160, right: 160 },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: "FFFFFF" }, bottom: { style: BorderStyle.SINGLE, size: 2, color: "FFFFFF" },
      left: { style: BorderStyle.SINGLE, size: 2, color: "FFFFFF" }, right: { style: BorderStyle.SINGLE, size: 2, color: "FFFFFF" },
    },
    children: [
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: label, size: 17, color: labelColor })] }),
      new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: value, size: 32, bold: true, color: valueColor })] }),
      new Paragraph({ children: [new TextRun({ text: sub, size: 16, color: subColor })] }),
    ],
  });
}

// ---- Số liệu động lấy từ analysis.json ----
const reconciliationAvailable = A.reconciliation_available !== false; // mặc định true cho analysis.json cũ (nguồn Google Sheet)
const khoDoiDataAvailable = A.kho_doi_data_available !== false; // mặc định true cho analysis.json cũ
const majorDiscrepancy = reconciliationAvailable ? A.discrepancies.find((d) => d.field === "trong_ky_thu") : null;
const kpiMissingText = !reconciliationAvailable ? "Chưa được cung cấp" : (majorDiscrepancy ? `${majorDiscrepancy.diff < 0 ? "" : "-"}${fmtTr(Math.abs(majorDiscrepancy.diff))}` : "Không lệch");
const kpiMissingSub = !reconciliationAvailable ? "không có số Tổng cộng gốc để đối chiếu" : (majorDiscrepancy ? `${majorDiscrepancy.diff_pct}% do lỗi công thức trên sheet` : "số liệu khớp với sheet");

const metricCardRow = new Table({
  width: { size: USABLE_WIDTH, type: WidthType.DXA },
  columnWidths: [1, 1, 1, 1].map(() => Math.round(USABLE_WIDTH / 4)),
  rows: [new TableRow({ children: [
    metricCard("Công nợ phải thu cuối kỳ", fmtTr(A.totals.cuoi_ky_thu), `${A.n_debtors}/${A.n_companies_total} công ty còn nợ`, { bg: COLOR_GRAY_BG, valueColor: COLOR_GRAY_VALUE, labelColor: COLOR_MUTED, subColor: COLOR_GRAY_SUB }),
    metricCard(`Top ${A.top_debtors.length} chiếm tổng nợ`, fmtPct(A.top_debtors_pct), "rủi ro tập trung cao", { bg: COLOR_RED_BG, valueColor: COLOR_RED, labelColor: COLOR_RED, subColor: COLOR_RED }),
    metricCard("Số liệu báo cáo bị thiếu", kpiMissingText, kpiMissingSub, { bg: COLOR_AMBER_BG, valueColor: COLOR_AMBER, labelColor: COLOR_AMBER, subColor: COLOR_AMBER }),
    metricCard("Nợ khó đòi còn hiệu lực", fmtTr(A.kho_doi_active_sum), `${fmtPct(round1(A.kho_doi_active_sum / A.totals.cuoi_ky_thu * 100))} tổng công nợ (${A.kho_doi_active.length} khách)`, { bg: COLOR_GRAY_BG, valueColor: COLOR_GRAY_VALUE, labelColor: COLOR_MUTED, subColor: COLOR_GRAY_SUB }),
  ] })],
});

function round1(n) { return Math.round(n * 10) / 10; }

const concentratedNames = A.concentrated_customers.map((c) => `${c.ma} (${fmtPct(c.pct)})`).join(", ");
const riskCalloutText = A.concentrated_customers.length
  ? `${concentratedNames} - các khách hàng vượt ngưỡng cảnh báo tập trung ${A.concentration_threshold_pct}%/khách hàng`
  : `Top ${A.top_debtors.length} khách hàng chiếm ${fmtPct(A.top_debtors_pct)} tổng công nợ phải thu`;

const children = [
  new Table({
    width: { size: USABLE_WIDTH, type: WidthType.DXA },
    columnWidths: [1400, USABLE_WIDTH - 1400],
    rows: [new TableRow({ children: [
      new TableCell({
        width: { size: 1400, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
        margins: { top: 0, bottom: 0, left: 0, right: 120 },
        children: [new Paragraph({ children: [new ImageRun({ type: "png", data: fs.readFileSync(logoPath), transformation: { width: 95, height: 95 } })] })],
      }),
      new TableCell({
        width: { size: USABLE_WIDTH - 1400, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
        children: [
          new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: "CÔNG TY TNHH SAIGON ALH", bold: true, size: 22 })] }),
          new Paragraph({ spacing: { after: 20 }, children: [new TextRun({ text: "Địa chỉ: Số 14/12 Đường 22, Khu phố 4, Phường Linh Đông, Thành phố Thủ Đức, TPHCM", italics: true, size: 18, color: COLOR_MUTED })] }),
          new Paragraph({ children: [new TextRun({ text: "Hotline: 028 2200 6069", italics: true, size: 18, color: COLOR_MUTED })] }),
        ],
      }),
    ] })],
  }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 200, after: 40 }, children: [new TextRun({ text: "BÁO CÁO ĐÁNH GIÁ CÔNG NỢ", bold: true, size: 36, color: COLOR_HEADER })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: `Kỳ báo cáo: ${A.ky_tu} - ${A.ky_den}`, italics: true, color: COLOR_MUTED, size: 22 })] }),

  h1("1. Tổng quan số liệu"),
  p(`Kỳ báo cáo ghi nhận ${A.n_companies_total} công ty có phát sinh công nợ. Các chỉ số chính:`),
  metricCardRow,
  p(""),
  calloutBox(riskCalloutText, { bg: COLOR_RED_BG, borderColor: COLOR_RED, textColor: COLOR_RED }),
  p(""),
  p("Chi tiết số liệu tổng hợp:"),
  dataTable(["Chỉ tiêu", "Số tiền"], [
    ["Đầu kỳ - còn phải thu", fmt(A.totals.dau_ky_thu)],
    ["Phát sinh tăng trong kỳ (đã tính đúng lại)", fmt(A.totals.trong_ky_thu)],
    ["Đã thu trong kỳ", fmt(A.totals.trong_ky_tra)],
    ["Cuối kỳ - còn phải thu", fmt(A.totals.cuoi_ky_thu)],
    ["Cuối kỳ - dư có / trả trước", fmt(A.totals.cuoi_ky_tra)],
  ], [3, 2]),
  p(""),
  p(`Số đã thu trong kỳ (${fmtTr(A.totals.trong_ky_tra)}) ${A.totals.trong_ky_tra >= A.totals.trong_ky_thu ? "lớn hơn" : "nhỏ hơn"} số phát sinh mới (${fmtTr(A.totals.trong_ky_thu)}). Số liệu gộp có thể che khuất rủi ro cục bộ, xem các mục dưới đây.`),
  chartImage("reconciliation.png", 600, 267),
];

if (!reconciliationAvailable) {
  children.push(h1("2. Kiểm tra chéo số liệu báo cáo"));
  children.push(p("Chưa được cung cấp — nguồn dữ liệu kỳ này không có số liệu Tổng cộng gốc để đối chiếu với số tự tính lại từ dữ liệu chi tiết. Số liệu tổng hợp dưới đây là số tự cộng tay từ toàn bộ dòng công ty, chưa được đối chiếu chéo với nguồn khác."));
} else if (A.discrepancies.length) {
  children.push(h1("2. Số liệu báo cáo đang hiển thị SAI - cần sửa trước khi dùng"));
  A.discrepancies.forEach((d) => {
    children.push(calloutBox(
      `Cột "${d.field}": bảng đang hiển thị ${fmt(d.report_value)}, số đúng theo dữ liệu thật là ${fmt(d.true_value)} - lệch ${fmt(Math.abs(d.diff))}${d.diff_pct ? ` (${Math.abs(d.diff_pct)}%)` : ""}.`,
      { bg: COLOR_RED_BG, borderColor: COLOR_RED, textColor: COLOR_RED }
    ));
    children.push(p(""));
  });
  children.push(p("Mọi kết luận dựa vào số bảng đang hiển thị sẽ bị sai lệch. Khuyến nghị sửa công thức trước khi dùng số này báo cáo lên Ban Giám đốc."));
} else {
  children.push(h1("2. Kiểm tra chéo số liệu báo cáo"));
  children.push(p("Số liệu tự tính lại từ dữ liệu chi tiết khớp hoàn toàn với các ô Tổng cộng trên sheet - không phát hiện chênh lệch trong kỳ này."));
}

children.push(
  h1("3. Rủi ro tập trung công nợ (concentration risk)"),
  p(`Top ${A.top_debtors.length} khách hàng nợ nhiều nhất chiếm ${fmt(A.top_debtors_sum)} / ${fmt(A.totals.cuoi_ky_thu)} tổng công nợ, tương đương ${fmtPct(A.top_debtors_pct)}.`),
  dataTable(["Khách hàng", "Còn phải thu (cuối kỳ)"], A.top_debtors.map((r) => [r.ma, fmt(r.so_tien)]), [3, 2]),
  chartImage("top_debtors.png", 600, 300),
  chartImage("concentration.png", 320, 320),
  p(""),
);
if (A.concentrated_customers.length) {
  children.push(calloutBox(
    `${concentratedNames} - vượt ngưỡng cảnh báo tập trung ${A.concentration_threshold_pct}% vào 1 khách hàng đơn lẻ.`,
    { bg: COLOR_RED_BG, borderColor: COLOR_RED, textColor: COLOR_RED }
  ));
  children.push(p(""));
  children.push(p(`Theo chuẩn quản trị rủi ro tín dụng khách hàng, mức tập trung > ${A.concentration_threshold_pct}% vào 1 khách hàng đơn lẻ là mức cảnh báo cao. Khuyến nghị rà soát riêng lịch sử thanh toán và hạn mức tín dụng áp dụng cho các khách hàng này.`));
} else {
  children.push(p(`Không có khách hàng đơn lẻ nào vượt ngưỡng cảnh báo tập trung ${A.concentration_threshold_pct}% trong kỳ này.`));
}

children.push(
  h1("4. Nợ khó đòi"),
  ...(khoDoiDataAvailable ? [
    p(`${A.kho_doi_flagged_count} khách hàng được gắn cờ "Khó đòi" / "Nợ khó đòi" trong kỳ.${A.kho_doi_stale_count ? ` ${A.kho_doi_stale_count} trong số đó đã có số dư = 0 (đã tất toán) - cờ chưa được gỡ, là lỗi vệ sinh dữ liệu.` : ""}`),
    p(A.kho_doi_active.length
      ? `${A.kho_doi_active.length} khách hàng thực sự còn nợ và bị đánh dấu khó đòi: ${A.kho_doi_active.map((r) => r.ma).join(", ")}, tổng ${fmt(A.kho_doi_active_sum)} (${fmtPct(round1(A.kho_doi_active_sum / A.totals.cuoi_ky_thu * 100))} tổng công nợ).`
      : "Không có khách hàng nào vừa còn nợ vừa bị đánh dấu khó đòi trong kỳ này."),
  ] : [
    p("Chưa được cung cấp — nguồn dữ liệu kỳ này không có cột/field đánh dấu \"Khó đòi\", nên không thể xác định danh sách nợ khó đòi. Khuyến nghị bổ sung field này ở lần cung cấp dữ liệu tiếp theo nếu cần theo dõi."),
  ]),

  h1("5. Mức độ đầy đủ dữ liệu để đánh giá tuổi nợ (aging)"),
  p(`Cột "Thời hạn thanh toán" hiện có dữ liệu ở ${fmtPct(A.han_coverage_pct)} số dòng.${A.han_coverage_pct < 80 ? " Mức độ này chưa đủ để phân loại nợ theo nhóm tuổi (0-30 / 31-60 / 61-90+ ngày) một cách đáng tin cậy - công cụ chuẩn để đánh giá chất lượng công nợ và ước tính dự phòng." : " Mức độ này đủ tốt để cân nhắc lập báo cáo tuổi nợ chi tiết."}`),

  h1("6. Khoản dư có / trả trước - cần nhìn đúng bản chất kế toán"),
  p(`${A.n_creditors} khách hàng có số dư "Cuối kỳ - dư có" dương, tổng ${fmt(A.totals.cuoi_ky_tra)}, top ${A.top_creditors.length} chiếm ${fmtPct(A.top_creditors_pct)} (${fmt(A.top_creditors_sum)}):`),
  dataTable(["Khách hàng", "Dư có (cuối kỳ)"], A.top_creditors.map((r) => [r.ma, fmt(r.so_tien)]), [3, 2]),
  chartImage("top_credit.png", 600, 300),
  p(""),
  p("Về bản chất, đây không phải khoản công ty nợ khách theo nghĩa công nợ phải trả nhà cung cấp, mà là doanh thu nhận trước / tiền khách đặt cọc cho dịch vụ chưa thực hiện (deferred revenue). Khuyến nghị theo dõi và ghi nhận đúng khoản mục \"Người mua trả tiền trước\", tách biệt khỏi công nợ phải thu để không làm sai lệch bức tranh dòng tiền khi lập báo cáo tài chính."),
);

if (A.flagged_notes.length) {
  children.push(
    h1("7. Ghi chú cần đối chiếu tay"),
    p(`${A.flagged_notes.length} dòng có ghi chú đặc biệt cần lưu ý:`),
  );
  A.flagged_notes.forEach((n) => children.push(bullet(`${n.ma}: "${n.ghi_chu}"`)));
}

children.push(
  h1(`${A.flagged_notes.length ? "8" : "7"}. Kết luận và khuyến nghị hành động`),
  p("Thứ tự ưu tiên xử lý:"),
);
if (reconciliationAvailable && A.discrepancies.length) children.push(bullet("Sửa lỗi công thức trên sheet DEBT để có số liệu đúng ở dòng Tổng cộng."));
if (!reconciliationAvailable) children.push(bullet("Bổ sung số liệu Tổng cộng gốc ở lần cung cấp dữ liệu tiếp theo để có thể đối chiếu chéo, phát hiện sai lệch (nếu có)."));
if (A.concentrated_customers.length) children.push(bullet(`Rà soát riêng ${concentratedNames} do mức tập trung rủi ro vượt ngưỡng an toàn.`));
if (A.han_coverage_pct < 80) children.push(bullet("Bổ sung dữ liệu \"Thời hạn thanh toán\" đầy đủ để có thể lập báo cáo tuổi nợ chuẩn."));
if (!khoDoiDataAvailable) children.push(bullet("Bổ sung field \"Khó đòi\" trong dữ liệu cung cấp để có thể theo dõi nợ khó đòi."));
if (khoDoiDataAvailable && A.kho_doi_stale_count) children.push(bullet(`Dọn dẹp cờ "Khó đòi" đã hết hiệu lực (${A.kho_doi_stale_count} trường hợp).`));
if (A.flagged_notes.length) children.push(bullet("Đối chiếu chứng từ gốc cho các dòng có ghi chú đặc biệt ở mục 7."));
children.push(bullet("Đổi nhãn cột \"Phải trả\" thành \"Đã thu trong kỳ\" và ghi nhận đúng khoản mục kế toán cho số dư trả trước (deferred revenue)."));

const doc = new Document({
  sections: [{ properties: { page: { margin: { top: PAGE_MARGIN, bottom: PAGE_MARGIN, left: PAGE_MARGIN, right: PAGE_MARGIN } } }, children }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(outputPath, buf);
  console.log("Đã tạo báo cáo:", outputPath);
});
