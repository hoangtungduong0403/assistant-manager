"""
Phân tích công nợ từ nguồn JSON - Mission: Đánh giá công nợ (Debt Evaluation)
==============================================================================
USAGE:
    python3 analyze_debt_json.py <debt_data.json> <ky_tu ddMMyyyy> <ky_den ddMMyyyy> <output_dir>

Thay thế analyze_debt.py (đọc trực tiếp Google Sheet qua Drive connector) kể
từ 2026-07-30: nguồn dữ liệu bây giờ là JSON do người dùng cung cấp trực tiếp,
tương đương các dòng từ hàng 14 của sheet DEBT. Xem mapping field JSON <-> cột
sheet gốc tại mapping.md.

Khác biệt so với analyze_debt.py:
- Không có dòng Tổng cộng gốc (hàng 12) để đối chiếu -> reconciliation_available
  = false, KHÔNG tự bịa số so sánh hay suy diễn "khớp".
- Nếu JSON không có field tương đương cột "Khó đòi" (L) -> kho_doi_data_available
  = false, KHÔNG mặc định bằng 0.

OUTPUT:
    <output_dir>/analysis.json           - toàn bộ số liệu đã tính cho build_report.js
    <output_dir>/charts/reconciliation.png
    <output_dir>/charts/top_debtors.png
    <output_dir>/charts/top_credit.png
    <output_dir>/charts/concentration.png
"""

import sys
import json
import os
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "DejaVu Sans"

TOP_N = 10
CONCENTRATION_THRESHOLD = 20.0  # % - ngưỡng cảnh báo tập trung vào 1 khách hàng

# Các field trong JSON được hiểu là field khó đòi nếu có mặt (không quan sát
# thấy trong dữ liệu mẫu 2026-07-30, giữ lại để tương thích về sau).
KHO_DOI_FIELD_CANDIDATES = ["Khó đòi", "KHÓ ĐÒI", "Kho doi", "kho_doi"]


def to_num(v):
    if v is None or v == "":
        return 0
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0


def clean_str(v):
    if v is None:
        return None
    return str(v).strip()


def is_valid_company_row(row):
    ma = row.get("Mã công ty")
    if ma is None or str(ma).strip() == "":
        return False
    # Lọc dòng rác (chữ ký, ngày lập...) lỡ lọt vào do "Mã công ty" rỗng nhưng
    # field khác chứa text dài bất thường - phòng hờ thêm.
    return True


def load_rows(data):
    kho_doi_field = next((f for f in KHO_DOI_FIELD_CANDIDATES if any(f in r for r in data)), None)
    rows = []
    for r in data:
        if not is_valid_company_row(r):
            continue
        rows.append({
            "stt": r.get("STT"),
            "ma": clean_str(r.get("Mã công ty")),
            "mst": clean_str(r.get("Mã số thuế")),
            "dau_ky_thu": to_num(r.get("Phải thu ĐẦU KỲ")),
            "dau_ky_tra": to_num(r.get("Phải trả ĐẦU KỲ")),
            "trong_ky_thu": to_num(r.get("Phải thu TRONG KỲ")),
            "trong_ky_tra": to_num(r.get("Phải trả TRONG KỲ")),
            "cuoi_ky_thu": to_num(r.get("Phải thu CUỐI kỳ")),
            "cuoi_ky_tra": to_num(r.get("Phải trả CUỐI kỳ")),
            "ghi_chu": clean_str(r.get("Ghi chú")),
            "kho_doi": clean_str(r.get(kho_doi_field)) if kho_doi_field else None,
            "han": clean_str(r.get("THỜI HẠN THANH TOÁN")),
        })
    return rows, (kho_doi_field is not None)


def hbar_chart(path, labels, values, color):
    labels = labels[::-1]
    values = values[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 3.6), dpi=200)
    bars = ax.barh(labels, [v / 1e6 for v in values], color=color, height=0.6)
    ax.set_xlabel("Triệu đồng", fontsize=10, color="#5F5E5A")
    ax.tick_params(axis="y", labelsize=10)
    ax.tick_params(axis="x", labelsize=9, colors="#5F5E5A")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7")
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.grid(axis="x", color="#e1e0d9", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f"{v/1e6:.1f}tr", va="center", fontsize=9, color="#2C2C2A")
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def concentration_chart(path, top_pct, rest_pct, n_top, n_rest):
    fig, ax = plt.subplots(figsize=(4.2, 4.2), dpi=200)
    colors = ["#d03b3b", "#e1e0d9"]
    wedges, texts, autotexts = ax.pie(
        [top_pct, rest_pct], colors=colors, startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
        autopct=lambda p: f"{p:.1f}%", pctdistance=0.79,
    )
    for t in autotexts:
        t.set_fontsize(11)
        t.set_color("#2C2C2A")
    ax.legend(wedges, [f"Top {n_top} khách hàng", f"{n_rest} khách hàng còn lại"],
              loc="lower center", bbox_to_anchor=(0.5, -0.18), fontsize=9, frameon=False, ncol=1)
    ax.set_title("Mức tập trung công nợ phải thu", fontsize=12, color="#2C2C2A", pad=10)
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def reconciliation_chart(path, dau_ky, tang, thu, cuoi_ky):
    fig, ax = plt.subplots(figsize=(7.2, 3.2), dpi=200)
    cats = ["Đầu kỳ", "+ Phát sinh tăng", "- Đã thu", "Cuối kỳ"]
    vals = [dau_ky / 1e6, tang / 1e6, -thu / 1e6, cuoi_ky / 1e6]
    bar_colors = ["#888780", "#639922", "#d03b3b", "#888780"]
    bars = ax.bar(cats, vals, color=bar_colors, width=0.55, zorder=3)
    ax.axhline(0, color="#c3c2b7", linewidth=0.8)
    ax.set_ylabel("Triệu đồng", fontsize=10, color="#5F5E5A")
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=9, colors="#5F5E5A")
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    ax.grid(axis="y", color="#e1e0d9", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for bar, v in zip(bars, vals):
        va = "bottom" if v >= 0 else "top"
        off = 8 if v >= 0 else -8
        ax.annotate(f"{v:.1f}tr", (bar.get_x() + bar.get_width() / 2, v), textcoords="offset points", xytext=(0, off), ha="center", fontsize=9, color="#2C2C2A")
    fig.tight_layout()
    fig.savefig(path, transparent=True)
    plt.close(fig)


def main(json_path, ky_tu, ky_den, out_dir):
    charts_dir = os.path.join(out_dir, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rows, kho_doi_data_available = load_rows(raw)
    n_total = len(rows)

    true_dau_ky_thu = sum(r["dau_ky_thu"] for r in rows)
    true_dau_ky_tra = sum(r["dau_ky_tra"] for r in rows)
    true_trong_ky_thu = sum(r["trong_ky_thu"] for r in rows)
    true_trong_ky_tra = sum(r["trong_ky_tra"] for r in rows)
    true_cuoi_ky_thu = sum(r["cuoi_ky_thu"] for r in rows)
    true_cuoi_ky_tra = sum(r["cuoi_ky_tra"] for r in rows)

    true_totals = {
        "dau_ky_thu": true_dau_ky_thu, "dau_ky_tra": true_dau_ky_tra,
        "trong_ky_thu": true_trong_ky_thu, "trong_ky_tra": true_trong_ky_tra,
        "cuoi_ky_thu": true_cuoi_ky_thu, "cuoi_ky_tra": true_cuoi_ky_tra,
    }

    # Nguồn JSON không có dòng Tổng cộng gốc để đối chiếu -> không thể phát
    # hiện chênh lệch như quy trình đọc trực tiếp Google Sheet.
    reconciliation_available = False
    discrepancies = []

    # Top N khách nợ nhiều nhất (cuối kỳ - phải thu)
    debtors = sorted([r for r in rows if r["cuoi_ky_thu"] > 0], key=lambda r: -r["cuoi_ky_thu"])
    top_debtors = debtors[:TOP_N]
    top_debtors_sum = sum(r["cuoi_ky_thu"] for r in top_debtors)
    top_debtors_pct = round(top_debtors_sum / true_cuoi_ky_thu * 100, 1) if true_cuoi_ky_thu else 0

    # Top N khách trả trước / dư có nhiều nhất
    creditors = sorted([r for r in rows if r["cuoi_ky_tra"] > 0], key=lambda r: -r["cuoi_ky_tra"])
    top_creditors = creditors[:TOP_N]
    top_creditors_sum = sum(r["cuoi_ky_tra"] for r in top_creditors)
    top_creditors_pct = round(top_creditors_sum / true_cuoi_ky_tra * 100, 1) if true_cuoi_ky_tra else 0

    # Khách hàng vượt ngưỡng tập trung cá nhân (>20% tổng công nợ)
    concentrated = [r for r in debtors if true_cuoi_ky_thu and (r["cuoi_ky_thu"] / true_cuoi_ky_thu * 100) >= CONCENTRATION_THRESHOLD]

    # Nợ khó đòi - chỉ tính nếu JSON có field tương ứng
    if kho_doi_data_available:
        kho_doi_flagged = [r for r in rows if (r["kho_doi"] or "").strip() in ("Nợ khó đòi", "Khó đòi")]
        kho_doi_active = [r for r in kho_doi_flagged if r["cuoi_ky_thu"] > 0]
        kho_doi_stale = [r for r in kho_doi_flagged if r["cuoi_ky_thu"] == 0]
        kho_doi_active_sum = sum(r["cuoi_ky_thu"] for r in kho_doi_active)
    else:
        kho_doi_flagged, kho_doi_active, kho_doi_stale, kho_doi_active_sum = [], [], [], 0

    # Ghi chú "Sai số" hoặc các ghi chú cần rà soát thủ công
    flagged_notes = [r for r in rows if (r["ghi_chu"] or "").strip() not in ("", None)]

    # Dữ liệu "Thời hạn thanh toán" có đủ để làm aging không
    han_filled = sum(1 for r in rows if r["han"] not in (None, ""))
    han_coverage_pct = round(han_filled / n_total * 100, 1) if n_total else 0

    result = {
        "ky_tu": ky_tu,
        "ky_den": ky_den,
        "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_source": "json",
        "n_companies_total": n_total,
        "n_debtors": len(debtors),
        "n_creditors": len(creditors),
        "totals": true_totals,
        "reconciliation_available": reconciliation_available,
        "report_totals": None,
        "discrepancies": discrepancies,
        "top_debtors": [{"ma": r["ma"], "so_tien": r["cuoi_ky_thu"]} for r in top_debtors],
        "top_debtors_sum": top_debtors_sum,
        "top_debtors_pct": top_debtors_pct,
        "top_creditors": [{"ma": r["ma"], "so_tien": r["cuoi_ky_tra"]} for r in top_creditors],
        "top_creditors_sum": top_creditors_sum,
        "top_creditors_pct": top_creditors_pct,
        "concentration_threshold_pct": CONCENTRATION_THRESHOLD,
        "concentrated_customers": [{"ma": r["ma"], "pct": round(r["cuoi_ky_thu"] / true_cuoi_ky_thu * 100, 1)} for r in concentrated],
        "kho_doi_data_available": kho_doi_data_available,
        "kho_doi_flagged_count": len(kho_doi_flagged),
        "kho_doi_active": [{"ma": r["ma"], "so_tien": r["cuoi_ky_thu"]} for r in kho_doi_active],
        "kho_doi_active_sum": kho_doi_active_sum,
        "kho_doi_stale_count": len(kho_doi_stale),
        "flagged_notes": [{"ma": r["ma"], "ghi_chu": r["ghi_chu"]} for r in flagged_notes],
        "han_coverage_pct": han_coverage_pct,
    }

    with open(os.path.join(out_dir, "analysis.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    # Charts
    reconciliation_chart(
        os.path.join(charts_dir, "reconciliation.png"),
        true_dau_ky_thu, true_trong_ky_thu, true_trong_ky_tra, true_cuoi_ky_thu,
    )
    hbar_chart(os.path.join(charts_dir, "top_debtors.png"),
               [r["ma"] for r in top_debtors], [r["cuoi_ky_thu"] for r in top_debtors], "#d03b3b")
    hbar_chart(os.path.join(charts_dir, "top_credit.png"),
               [r["ma"] for r in top_creditors], [r["cuoi_ky_tra"] for r in top_creditors], "#1baf7a")
    concentration_chart(os.path.join(charts_dir, "concentration.png"),
                         top_debtors_pct, round(100 - top_debtors_pct, 1), TOP_N, max(len(debtors) - TOP_N, 0))

    print(f"Kỳ báo cáo: {result['ky_tu']} - {result['ky_den']}")
    print(f"Số công ty có phát sinh: {n_total}")
    print("Nguồn JSON không có số liệu Tổng cộng gốc -> không đối chiếu chênh lệch (reconciliation_available=False).")
    if not kho_doi_data_available:
        print("Nguồn JSON không có field 'Khó đòi' -> kho_doi_data_available=False.")
    print(f"Đã ghi analysis.json và 4 biểu đồ vào {out_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 analyze_debt_json.py <debt_data.json> <ky_tu ddMMyyyy> <ky_den ddMMyyyy> <output_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
