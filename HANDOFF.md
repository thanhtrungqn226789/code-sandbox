# HANDOFF — Tool CLI đổi VND sang USD (issue #1)

**Đã làm:** `doi_tien.py` (CLI, thư viện chuẩn, Decimal, làm tròn 2 số) + `tests/test_doi_tien.py` (10 test) + README. Nhánh `task/doi-tien`, không đụng `main`.

**Smoke:**
- `python doi_tien.py 2500000 --ty-gia 25000` → `2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)`
- `python doi_tien.py abc --ty-gia 25000` → `Lỗi: Số tiền VND phải là một số, nhận được: 'abc'` (exit 2, không crash)

**Test:** `python -m unittest -v` → 10/10 OK (Python 3.13, Windows 10).

**Rủi ro còn lại:**
- Dấu `,` = phân cách nghìn, `.` = thập phân. Viết kiểu VN `25.450` sẽ bị hiểu thành 25,45 (sai im lặng, không báo lỗi).
- Chưa test trên Linux/macOS; output ép UTF-8, terminal cũ có thể hiển thị lỗi font tiếng Việt.
- Không có key/token/dữ liệu thật.
