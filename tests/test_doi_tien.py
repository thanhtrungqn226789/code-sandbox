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

    def test_doc_so_hop_le(self):
        for chuoi, mong_doi in [
            ("25450", "25450"),
            ("25,450", "25450"),
            ("1,000,000", "1000000"),
            ("25450.5", "25450.5"),
            ("25,450.5", "25450.5"),
            ("25.45", "25.45"),
            ("0.125", "0.125"),
            ("1234.567", "1234.567"),
            (" 2500000 ", "2500000"),
        ]:
            with self.subTest(chuoi=chuoi):
                self.assertEqual(doc_so(chuoi, "x"), Decimal(mong_doi))

    def test_doc_so_chu(self):
        for sai in ["abc", "", ".", ",", "12a", "nan", "inf", "-5", "-0", "1e6", "1e-30", "1_000", "1 000"]:
            with self.subTest(sai=sai), self.assertRaises(LoiNhapLieu):
                doc_so(sai, "x")

    def test_tu_choi_dau_cham_nhom_nghin(self):
        # "25.450" kiểu VN = 25450, nếu nhận sẽ thành 25.45 (lệch 1000 lần).
        for sai in ["25.450", "1.000", "999.999", "1.000.000", "25.450,5"]:
            with self.subTest(sai=sai), self.assertRaises(LoiNhapLieu):
                doc_so(sai, "x")

    def test_tu_choi_dau_phay_sai_vi_tri(self):
        # "25,5" kiểu VN = 25.5, nếu bỏ dấu phẩy sẽ thành 255; "1,0,0" thành 100.
        for sai in ["25,5", "1,0,0", "25,45", "2,5000", ",450", "450,", "0,450", "1,000,00", "1,,000"]:
            with self.subTest(sai=sai), self.assertRaises(LoiNhapLieu):
                doc_so(sai, "x")

    def test_thong_bao_mo_ho_goi_y_cach_viet(self):
        with self.assertRaises(LoiNhapLieu) as ctx:
            doc_so("25.450", "Tỷ giá")
        msg = str(ctx.exception)
        for goi_y in ["25450", "25,450", "25.45"]:
            self.assertIn(goi_y, msg)

    def test_qua_lon_khong_crash(self):
        with self.assertRaises(LoiNhapLieu):
            vnd_sang_usd(Decimal(10) ** 26, Decimal(1))
        with self.assertRaises(LoiNhapLieu):
            vnd_sang_usd(Decimal(100), Decimal("1e-30"))


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

    def test_tu_choi_cach_viet_mo_ho(self):
        for so_vnd, ty_gia in [
            ("2500000", "25.450"),
            ("2500000", "25,5"),
            ("2500000", "1,0,0"),
            ("25.450", "25000"),
            ("25,5", "25000"),
            ("1,0,0", "25000"),
            ("1.000.000", "25000"),
        ]:
            with self.subTest(so_vnd=so_vnd, ty_gia=ty_gia):
                code, out, err = chay(so_vnd, "--ty-gia", ty_gia)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertTrue(err.startswith("Lỗi: "), err)
                self.assertIn("25450", err)  # có gợi ý cách viết đúng
                self.assertNotIn("Traceback", err)

    def test_so_cuc_nho_cuc_lon(self):
        ty_gia_cuc_nho = "0." + "0" * 29 + "1"  # 1e-30 viết dạng thập phân
        for so_vnd, ty_gia in [
            ("100", "1e-30"),
            ("100", ty_gia_cuc_nho),
            ("1" + "0" * 26, "1"),
            ("1" + "0" * 40, "25000"),
        ]:
            with self.subTest(so_vnd=so_vnd, ty_gia=ty_gia):
                code, out, err = chay(so_vnd, "--ty-gia", ty_gia)
                self.assertEqual(code, 2)
                self.assertEqual(out, "")
                self.assertTrue(err.startswith("Lỗi: "), err)
                self.assertNotIn("Traceback", err)

    def test_so_lon_van_tinh_duoc(self):
        code, out, _ = chay("1" + "0" * 26, "--ty-gia", "25000")
        self.assertEqual(code, 0)
        self.assertIn("= 4,000,000,000,000,000,000,000.00 USD", out)

    def test_dau_phay_dung_cho_ca_hai_tham_so(self):
        code, out, _ = chay("2,500,000", "--ty-gia", "25,450.5")
        self.assertEqual(code, 0)
        self.assertIn("= 98.23 USD", out)

    def test_thieu_ty_gia(self):
        code, _, err = chay("1000")
        self.assertEqual(code, 2)
        self.assertIn("--ty-gia", err)


if __name__ == "__main__":
    unittest.main()
