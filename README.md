# code-sandbox

## doi_tien.py — đổi VND sang USD

Tool CLI Python (chỉ dùng thư viện chuẩn, Python 3.8+). Tỷ giá nhập tay qua tham số, không gọi API nào.

```
python doi_tien.py 2500000 --ty-gia 25000
# 2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)
```

- Chấp nhận dấu phẩy phân cách hàng nghìn: `python doi_tien.py 1,000,000 --ty-gia 25,450.5`
- Kết quả làm tròn 2 chữ số thập phân (half-up).
- Nhập sai (chữ, số âm, tỷ giá 0) → in `Lỗi: ...` ra stderr, exit code 2, không traceback.

## Test

```
python -m unittest -v
```
