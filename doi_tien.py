"""Đổi VND sang USD với tỷ giá nhập tay.

Ví dụ:
    python doi_tien.py 2500000 --ty-gia 25000
    -> 2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)
"""

import argparse
import re
import sys
from decimal import Decimal, DecimalException, ROUND_HALF_UP

# Số không phân cách (25450, 25450.5) hoặc nhóm 3 chữ số bằng dấu phẩy (25,450, 1,000,000.5).
# Dấu chấm luôn là phần thập phân.
SO_HOP_LE = re.compile(r"[0-9]+(\.[0-9]+)?|[1-9][0-9]{0,2}(,[0-9]{3})+(\.[0-9]+)?")
# "25.450" hay "1.000": người Việt hay dùng dấu chấm để nhóm nghìn, đọc theo kiểu nào cũng lệch 1000 lần.
SO_MO_HO = re.compile(r"[1-9][0-9]{0,2}\.[0-9]{3}")
GOI_Y = "Viết 25450, 25,450 hoặc 25450.5 (dấu phẩy chỉ để nhóm 3 chữ số, dấu chấm là phần thập phân)."


class LoiNhapLieu(ValueError):
    """Lỗi do người dùng nhập sai."""


def doc_so(chuoi, ten):
    """Chuyển chuỗi thành Decimal không âm; từ chối mọi cách viết có thể bị hiểu nhầm."""
    sach = chuoi.strip()
    if sach.startswith("-"):
        raise LoiNhapLieu(f"{ten} không được âm, nhận được: '{chuoi}'")
    if not re.fullmatch(r"[0-9.,]+", sach) or not re.search(r"[0-9]", sach):
        raise LoiNhapLieu(f"{ten} phải là một số, nhận được: '{chuoi}'. {GOI_Y}")
    if SO_MO_HO.fullmatch(sach):
        nguyen = sach.replace(".", "")
        # Cách viết thập phân không trùng mẫu mơ hồ: bỏ số 0 cuối (25.45), hoặc thêm một số 0 (1.0050).
        thap_phan = sach.rstrip("0").rstrip(".")
        if thap_phan == sach:
            thap_phan = sach + "0"
        raise LoiNhapLieu(
            f"{ten} '{chuoi}' dễ hiểu nhầm: nếu ý là {nguyen} hãy viết {nguyen} "
            f"hoặc {int(nguyen):,}; nếu là số thập phân hãy viết {thap_phan}."
        )
    if not SO_HOP_LE.fullmatch(sach):
        raise LoiNhapLieu(f"{ten} viết sai định dạng: '{chuoi}'. {GOI_Y}")
    return Decimal(sach.replace(",", ""))


def vnd_sang_usd(so_vnd, ty_gia):
    """Đổi số VND sang USD, làm tròn 2 chữ số thập phân."""
    if ty_gia <= 0:
        raise LoiNhapLieu("Tỷ giá phải lớn hơn 0")
    try:
        return (so_vnd / ty_gia).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except DecimalException:
        raise LoiNhapLieu(
            "Kết quả quá lớn để tính chính xác (vượt 28 chữ số). "
            "Kiểm tra lại số tiền và tỷ giá."
        ) from None


def main(argv=None):
    # Windows có thể dùng cp1252 khi pipe output, không in được tiếng Việt.
    for luong in (sys.stdout, sys.stderr):
        if hasattr(luong, "reconfigure"):
            luong.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Đổi VND sang USD với tỷ giá nhập tay.")
    parser.add_argument("so_vnd", help="Số tiền VND, ví dụ 2500000 hoặc 2,500,000")
    parser.add_argument("--ty-gia", required=True, help="Tỷ giá VND cho 1 USD, ví dụ 25000")
    args = parser.parse_args(argv)

    try:
        so_vnd = doc_so(args.so_vnd, "Số tiền VND")
        ty_gia = doc_so(args.ty_gia, "Tỷ giá")
        usd = vnd_sang_usd(so_vnd, ty_gia)
    except LoiNhapLieu as loi:
        print(f"Lỗi: {loi}", file=sys.stderr)
        return 2

    print(f"{so_vnd:,f} VND = {usd:,.2f} USD (tỷ giá {ty_gia:,f} VND/USD)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
