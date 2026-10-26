# HANDOFF — Tool CLI đổi VND sang USD (issue #1, PR #2)

**Đã làm:** `doi_tien.py` (CLI, thư viện chuẩn, Decimal) + 19 test + README. Đã sửa theo review: số tiền và tỷ giá viết dễ hiểu nhầm (`25.450`, `25,5`, `1,0,0`, `1.000.000`) bị từ chối, exit 2, có gợi ý cách viết đúng. Số quá lớn hoặc quá nhỏ (`--ty-gia 1e-30`, số tiền 10^26) giờ báo `Lỗi:` (exit 2) thay vì crash.

**Smoke:**
- `python doi_tien.py 2500000 --ty-gia 25000` → `2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)`
- `python doi_tien.py abc --ty-gia 25000` → `Lỗi: Số tiền VND phải là một số, nhận được: 'abc'. ...` (exit 2)
- `python doi_tien.py 2500000 --ty-gia 25.450` → `Lỗi: Tỷ giá '25.450' dễ hiểu nhầm: ... viết 25450 hoặc 25,450; ... 25.45.` (exit 2)

**Test:** `python -m unittest -v` → 19/19 OK (Python 3.13, Windows 10, Git Bash).

**Chưa kiểm:** Linux/macOS; Python dưới 3.13; cmd.exe, PowerShell 7 (PowerShell 5.1 gốc mới smoke tay 3 lệnh, chưa chạy bộ test); CI (repo chưa có CI).

**Rủi ro còn lại:** chưa giới hạn khoảng tỷ giá hợp lý. Gõ thẳng `25.45` hoặc `25.4500` vẫn được nhận như tỷ giá 25.45 VND/USD. Không dùng key, token hay dữ liệu thật.
