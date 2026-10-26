import contextlib
import io
import unittest
from decimal import Decimal

from doi_tien import LoiNhapLieu, doc_so, main, vnd_sang_usd


def chay(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = main(list(argv))
        except SystemExit as e:
            code = e.code
    return code, out.getvalue(), err.getvalue()


class TestQuyDoi(unittest.TestCase):
    def test_chia_tron(self):
        self.assertEqual(vnd_sang_usd(Decimal(2500000), Decimal(25000)), Decimal("100.00"))

    def test_lam_tron_2_chu_so(self):
        # 100000 / 24500 = 4.0816... -> 4.08
        self.assertEqual(vnd_sang_usd(Decimal(100000), Decimal(24500)), Decimal("4.08"))

    def test_ty_gia_bang_0(self):
        with self.assertRaises(LoiNhapLieu):
            vnd_sang_usd(Decimal(1000), Decimal(0))

    def test_doc_so_co_dau_phay(self):
        self.assertEqual(doc_so("2,500,000", "x"), Decimal(2500000))

    def test_doc_so_chu(self):
        for sai in ["abc", "", "12a", "nan", "inf", "-5"]:
            with self.subTest(sai=sai), self.assertRaises(LoiNhapLieu):
                doc_so(sai, "x")


class TestCLI(unittest.TestCase):
    def test_lenh_mau(self):
        code, out, _ = chay("2500000", "--ty-gia", "25000")
        self.assertEqual(code, 0)
        self.assertIn("= 100.00 USD", out)

    def test_nhap_chu_khong_crash(self):
        code, out, err = chay("hai-trieu", "--ty-gia", "25000")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("Lỗi: Số tiền VND phải là một số", err)

    def test_ty_gia_chu(self):
        code, _, err = chay("1000", "--ty-gia", "abc")
        self.assertEqual(code, 2)
        self.assertIn("Lỗi: Tỷ giá phải là một số", err)

    def test_ty_gia_0(self):
        code, _, err = chay("1000", "--ty-gia", "0")
        self.assertEqual(code, 2)
        self.assertIn("Tỷ giá phải lớn hơn 0", err)

    def test_thieu_ty_gia(self):
        code, _, err = chay("1000")
        self.assertEqual(code, 2)
        self.assertIn("--ty-gia", err)


if __name__ == "__main__":
    unittest.main()
