"""Đổi VND sang USD với tỷ giá nhập tay.

Ví dụ:
    python doi_tien.py 2500000 --ty-gia 25000
    -> 2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)
"""

import argparse
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP


class LoiNhapLieu(ValueError):
    """Lỗi do người dùng nhập sai."""


def doc_so(chuoi, ten):
    """Chuyển chuỗi thành Decimal dương; cho phép dấu phẩy/gạch dưới phân cách hàng nghìn."""
    sach = chuoi.strip().replace(",", "").replace("_", "")
    try:
        so = Decimal(sach)
    except InvalidOperation:
        raise LoiNhapLieu(f"{ten} phải là một số, nhận được: '{chuoi}'") from None
    if not so.is_finite():
        raise LoiNhapLieu(f"{ten} phải là một số hữu hạn, nhận được: '{chuoi}'")
    if so < 0:
        raise LoiNhapLieu(f"{ten} không được âm, nhận được: '{chuoi}'")
    return so


def vnd_sang_usd(so_vnd, ty_gia):
    """Đổi số VND sang USD, làm tròn 2 chữ số thập phân."""
    if ty_gia <= 0:
        raise LoiNhapLieu("Tỷ giá phải lớn hơn 0")
    return (so_vnd / ty_gia).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


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
