# code-sandbox

## doi_tien.py — đổi VND sang USD

Tool CLI Python, chỉ dùng thư viện chuẩn. Bạn nhập tỷ giá qua tham số, tool không gọi API nào. Mới chạy thử trên Python 3.13.

```
python doi_tien.py 2500000 --ty-gia 25000
# 2,500,000 VND = 100.00 USD (tỷ giá 25,000 VND/USD)
```

### Cách viết số (áp dụng cho cả số tiền và tỷ giá)

Dấu chấm `.` luôn là phần thập phân. Dấu phẩy `,` chỉ dùng để nhóm 3 chữ số.

| Được nhận | Bị từ chối (exit 2) | Lý do từ chối |
|---|---|---|
| `25450`, `25,450`, `1,000,000` | `25.450`, `1.000` | Dễ hiểu nhầm, có thể lệch 1000 lần. Hãy viết `25450`, `25,450` hoặc `25.45` |
| `25450.5`, `25,450.5`, `25.45` | `25,5`, `1,0,0`, `1,000,00` | Dấu phẩy đặt sai vị trí nhóm 3 chữ số |
| | `1.000.000`, `25.450,5` | Dùng kiểu viết số Việt Nam |
| | `1e6`, `1_000`, `-5`, `-0`, `abc` | Không phải số thập phân dương viết thường |

- Kết quả làm tròn tới 2 chữ số thập phân (half-up).
- Nếu tỷ giá bằng 0 hoặc kết quả vượt 28 chữ số (ví dụ tỷ giá `0.000…01` quá nhỏ), tool cũng báo lỗi.
- Mọi lỗi nhập liệu đều in `Lỗi: ...` ra stderr và trả exit 2, không in traceback.
- Nên đặt số có dấu phẩy trong nháy (`--ty-gia "25,450"`) cho chắc. Windows PowerShell 5.1 không có nháy vẫn chạy đúng; PowerShell 7 và các shell khác chưa kiểm.

## Test

```
python -m unittest -v
```
