"""
Update Summary Quotation from Client Information
===================================================
Mission: Bao gia (Quotation) - SGA

USAGE
-----
    python3 update_summary_quotation.py <client_information.xlsx> <summary_quotation_template.xlsx>

Reads every customer row from the Client Information file, skips any customer
whose MA CONG TY already exists in the Summary Quotation template, and adds
one new row per new customer into the correct sheet (DATA LONG - TERM or
DATA SHORT - TERM, based on LOAI). Saves the result as a NEW file named
SummaryQuotation_<yyyyMMdd_HHmm>.xlsx in /mnt/user-data/outputs -- the
template itself is never modified.

ASSUMPTIONS / DEFAULTS (documented so they can be reviewed each run)
----------------------------------------------------------------------
- MA SO THUE (tax code) is written as a static value (from Client Info),
  not the original IMPORTRANGE formula, since IMPORTRANGE does not work in
  a local .xlsx file.
- "So hop dong" (DATA LONG - TERM, col E) defaults to "CHUA CO" when no
  contract exists yet, per mapping.md.
- Sequential numbers (col G in LONG-TERM, col D in SHORT-TERM) auto-continue
  from the highest existing number in that sheet.
- VAT (SHORT-TERM col I) defaults to 0.08 (8%), the standing default noted
  in mapping.md.
- Fields with NO source in Client Information are left BLANK, never guessed:
    LONG-TERM:  F (Tinh trang hop dong), I (DVT phu phi), J (Hoa don),
                L (Ngay thuc hien), N (Tinh trang bao gia)
    SHORT-TERM: F (Ngay thuc hien), H (Don gia), M (Tinh trang)
  Because "Ngay hieu luc" is an existing formula that adds 15 days to a
  blank "Ngay thuc hien", it will show a meaningless placeholder date
  (15/01/1900) until that field is filled in manually -- this is a known
  side effect of the ORIGINAL formula, left untouched per convention.
- Style (font/fill/border/number format) is copied from the last existing
  data row in each sheet, so new rows visually match the template.
- Customers with LOAI blank/unrecognized are skipped and listed separately
  for manual review -- never guessed.

Run `python3 /mnt/skills/public/xlsx/scripts/recalc.py <output.xlsx>` after
this script to compute formula values before delivering the file.
"""

import os
import sys
import re
from copy import copy
from datetime import datetime

import openpyxl

CLIENT_INFO_HEADER_ROW = 3
CLIENT_INFO_DATA_START_ROW = 4
COL_MA_CONG_TY = 2       # B
COL_MA_SO_THUE = 5       # E
COL_TEN_CONG_TY = 6      # F... actually F is "TÊN CÔNG TY" -> see note below
COL_LOAI = 14             # N
COL_SERVICE_1 = 15        # O - Dich vu phan tich - thong ke
COL_SERVICE_2 = 16        # P - Dich vu nhan su
COL_SERVICE_3 = 17        # Q - Dich vu phap che doanh nghiep
SERVICE_NAMES = {
    COL_SERVICE_1: "Dịch vụ phân tích - thống kê",
    COL_SERVICE_2: "Dịch vụ nhân sự",
    COL_SERVICE_3: "Dịch vụ pháp chế doanh nghiệp",
}

LT_SHEET = "DATA LONG - TERM"
ST_SHEET = "DATA SHORT - TERM"


def copy_row_style(ws, src_row, dst_row, ncols):
    ws.row_dimensions[dst_row].height = ws.row_dimensions[src_row].height
    for c in range(1, ncols + 1):
        s = ws.cell(row=src_row, column=c)
        d = ws.cell(row=dst_row, column=c)
        d.font = copy(s.font)
        d.fill = copy(s.fill)
        d.border = copy(s.border)
        d.number_format = s.number_format
        d.alignment = copy(s.alignment)
        d.protection = copy(s.protection)


def read_client_information(path):
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb["Information"]
    customers = []
    r = CLIENT_INFO_DATA_START_ROW
    while True:
        code = ws.cell(row=r, column=COL_MA_CONG_TY).value
        if code in (None, ""):
            break
        mst = ws.cell(row=r, column=COL_MA_SO_THUE).value
        loai = ws.cell(row=r, column=COL_LOAI).value
        levels = []
        for col in (COL_SERVICE_1, COL_SERVICE_2, COL_SERVICE_3):
            lvl = ws.cell(row=r, column=col).value
            if lvl not in (None, ""):
                levels.append((SERVICE_NAMES[col], str(lvl).strip()))
        customers.append({
            "code": str(code).strip(),
            "mst": str(mst).strip() if mst not in (None, "") else "",
            "loai": str(loai).strip() if loai not in (None, "") else "",
            "levels": levels,
        })
        r += 1
    return customers


def existing_codes(ws, code_col, start_row=4):
    codes = set()
    last_row = start_row - 1
    r = start_row
    while r <= ws.max_row:
        v = ws.cell(row=r, column=code_col).value
        if v not in (None, ""):
            codes.add(str(v).strip().upper())
            last_row = r
        r += 1
    return codes, last_row


def next_seq(ws, col, start_row, last_row, width=3):
    max_n = 0
    for r in range(start_row, last_row + 1):
        v = ws.cell(row=r, column=col).value
        if v not in (None, ""):
            m = re.match(r"^\d+", str(v))
            if m:
                max_n = max(max_n, int(m.group()))
    return str(max_n + 1).zfill(width)


def add_long_term_row(ws, r, cust):
    level = cust["levels"][0][1] if cust["levels"] else ""
    seq = next_seq(ws, 7, 4, r - 1)
    ws.cell(row=r, column=1, value=f'=IF(B{r}="","",SUBTOTAL(3,$B$4:B{r}))')
    ws.cell(row=r, column=2, value=cust["code"])
    ws.cell(row=r, column=3, value=cust["mst"])
    ws.cell(row=r, column=4, value=level)
    ws.cell(row=r, column=5, value="CHUA CO")
    ws.cell(row=r, column=6, value=None)
    ws.cell(row=r, column=7, value=seq)
    ws.cell(row=r, column=8, value=f'=IF(B{r}="","",(G{r} &"/LT/2025"))')
    ws.cell(row=r, column=9, value=None)
    ws.cell(row=r, column=10, value=None)
    ws.cell(row=r, column=11, value=f'=IF(J{r},"Quý","")')
    ws.cell(row=r, column=12, value=None)
    ws.cell(row=r, column=13, value=f'=IF(B{r}="","",(L{r}+15))')
    ws.cell(row=r, column=14, value=None)


def add_short_term_row(ws, r, cust):
    dien_giai = "\n".join(f"{name} - {lvl}" for name, lvl in cust["levels"]) or "Chưa được cung cấp"
    no = next_seq(ws, 4, 4, r - 1)
    ws.cell(row=r, column=1, value=f'=IF(D{r}="","",SUBTOTAL(3,$D$4:D{r}))')
    ws.cell(row=r, column=2, value=cust["code"])
    ws.cell(row=r, column=3, value=cust["mst"])
    ws.cell(row=r, column=4, value=no)
    ws.cell(row=r, column=5, value=f'=IF(B{r}="","",(D{r} &"/ST/2025"))')
    ws.cell(row=r, column=6, value=None)
    ws.cell(row=r, column=7, value=dien_giai)
    ws.cell(row=r, column=8, value=None)
    ws.cell(row=r, column=9, value=0.08)
    ws.cell(row=r, column=10, value=f'=H{r}*I{r}')
    ws.cell(row=r, column=11, value=f'=IF(E{r}="","",(E{r}+15))')
    ws.cell(row=r, column=12, value=f'=IF(F{r}="","",(F{r}+15))')
    ws.cell(row=r, column=13, value=None)
    ws.cell(row=r, column=14, value=f'=IF(M{r}="Done",F{r},"")')


def main(client_info_path, template_path):
    customers = read_client_information(client_info_path)

    wb = openpyxl.load_workbook(template_path, data_only=False)
    ws_lt = wb[LT_SHEET]
    ws_st = wb[ST_SHEET]

    lt_codes, lt_last = existing_codes(ws_lt, 2)
    st_codes, st_last = existing_codes(ws_st, 2)

    added_lt, added_st, skipped_dup, skipped_unclassified = [], [], [], []

    for cust in customers:
        code_upper = cust["code"].upper()
        loai = cust["loai"]
        if "long-term" in loai.lower():
            if code_upper in lt_codes:
                skipped_dup.append(cust["code"])
                continue
            lt_last += 1
            copy_row_style(ws_lt, lt_last - 1, lt_last, 14)
            add_long_term_row(ws_lt, lt_last, cust)
            lt_codes.add(code_upper)
            added_lt.append(cust["code"])
        elif "short-term" in loai.lower():
            if code_upper in st_codes:
                skipped_dup.append(cust["code"])
                continue
            st_last += 1
            copy_row_style(ws_st, st_last - 1, st_last, 14)
            add_short_term_row(ws_st, st_last, cust)
            st_codes.add(code_upper)
            added_st.append(cust["code"])
        else:
            skipped_unclassified.append(cust["code"])

    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"SummaryQuotation_{ts}.xlsx"

    mission_output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "output"
    )
    os.makedirs(mission_output_dir, exist_ok=True)
    mission_out_path = os.path.join(mission_output_dir, filename)
    wb.save(mission_out_path)

    # Also drop a copy where the chat UI can present it for download.
    delivery_dir = "/mnt/user-data/outputs"
    delivery_path = None
    if os.path.isdir(delivery_dir) or delivery_dir == "/mnt/user-data/outputs":
        try:
            os.makedirs(delivery_dir, exist_ok=True)
            delivery_path = os.path.join(delivery_dir, filename)
            wb.save(delivery_path)
        except Exception:
            delivery_path = None

    print(f"Saved to mission output folder: {mission_out_path}")
    if delivery_path:
        print(f"Copy for download: {delivery_path}")
    print(f"Added to {LT_SHEET}: {added_lt}")
    print(f"Added to {ST_SHEET}: {added_st}")
    print(f"Skipped (already existed): {skipped_dup}")
    print(f"Skipped (LOAI blank/unrecognized - needs manual review): {skipped_unclassified}")
    return mission_out_path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 update_summary_quotation.py <client_information.xlsx> <template.xlsx>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
