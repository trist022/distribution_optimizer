# Chương Trình Tối Ưu Phân Phối Hàng Hóa (Greedy Algorithm)

## Mô Tả

Chương trình đơn giản giúp phân phối hàng hóa từ các trạm phát đến các trạm thu với chi phí thấp.

### Bài toán:
- Có nhiều kho hàng (trạm phát) với số lượng hàng khác nhau
- Có nhiều cửa hàng (trạm thu) cần hàng với nhu cầu khác nhau  
- Mỗi tuyến vận chuyển có chi phí riêng
- **Mục tiêu**: Phân phối hàng với chi phí thấp

### Thuật toán:
Chương trình dùng **thuật toán Greedy** (tham lam):
1. Tìm tuyến đường rẻ nhất còn khả dụng
2. Chuyển hàng tối đa có thể trên tuyến đó
3. Lặp lại cho đến khi đáp ứng hết nhu cầu

**Ưu điểm**: Đơn giản, dễ hiểu, chạy nhanh  
**Nhược điểm**: Không đảm bảo tối ưu tuyệt đối trong mọi trường hợp

## Yêu Cầu

- Python 3.7+
- Thư viện: `pandas`, `openpyxl`

```bash
pip install pandas openpyxl
```

## Cấu Trúc File Excel Đầu Vào

File Excel cần có **3 sheet**:

### 1. Sheet "TramPhat" (Trạm Phát)
| TenTram | Cung |
|---------|------|
| Kho A   | 100  |
| Kho B   | 150  |
| Kho C   | 200  |

- **TenTram**: Tên trạm phát (kho hàng)
- **Cung**: Số lượng hàng có sẵn

### 2. Sheet "TramThu" (Trạm Thu)
| TenTram    | NhuCau |
|------------|--------|
| Cửa hàng 1 | 80     |
| Cửa hàng 2 | 120    |
| Cửa hàng 3 | 150    |

- **TenTram**: Tên trạm thu (cửa hàng)
- **NhuCau**: Số lượng hàng cần thiết

### 3. Sheet "ChiPhi" (Chi Phí Vận Chuyển)
| TramPhat | Cửa hàng 1 | Cửa hàng 2 | Cửa hàng 3 |
|----------|------------|------------|------------|
| Kho A    | 5          | 8          | 12         |
| Kho B    | 7          | 6          | 9          |
| Kho C    | 10         | 11         | 4          |

- **TramPhat**: Tên trạm phát
- **Các cột khác**: Chi phí vận chuyển 1 đơn vị hàng từ trạm phát đến từng trạm thu

## Cách Sử Dụng

### Bước 1: Chuẩn bị file dữ liệu
Tạo file Excel (ví dụ: `du_lieu_phan_phoi.xlsx`) theo cấu trúc trên

### Bước 2: Chạy chương trình
```bash
python main.py du_lieu_phan_phoi.xlsx
```

### Bước 3: Xem kết quả
- Kết quả hiển thị trên màn hình
- File `result.xlsx` được tạo tự động

## Ví Dụ Kết Quả

### Trên màn hình:
```
=== KẾ HOẠCH TỐI ƯU ===
    From          To  Quantity  UnitCost    Cost
  Kho A  Cửa hàng 1        80         5     400
  Kho B  Cửa hàng 2       120         6     720
  Kho C  Cửa hàng 3       150         4     600

Tổng chi phí: 1,720 VND

Đã lưu kết quả vào: result.xlsx
```

### File result.xlsx có 2 sheet:
1. **Plan**: Bảng chi tiết từng tuyến vận chuyển
2. **Summary**: Tổng chi phí

## Giải Thích Code

Code có 4 hàm chính, rất đơn giản:

### 1. `read_excel(file_path)` - Đọc dữ liệu
```python
# Đọc 3 sheet từ file Excel
# Chuyển đổi thành dictionary để xử lý dễ dàng
# Trả về: supply, demand, costs
```

### 2. `find_optimal_plan(supply, demand, costs)` - Tìm phương án
```python
# Vòng lặp chính:
while còn nhu cầu chưa đáp ứng:
    # Tìm tuyến đường rẻ nhất
    for mỗi trạm phát:
        for mỗi trạm thu:
            if chi_phí < chi_phí_tốt_nhất:
                lưu_lại_tuyến_này
    
    # Chuyển hàng trên tuyến rẻ nhất
    số_lượng = min(hàng_còn_lại, nhu_cầu_còn_lại)
    ghi_nhận_kết_quả
    cập_nhật_số_lượng_còn_lại
```

### 3. `save_excel(df, total_cost)` - Lưu kết quả
```python
# Ghi kết quả vào file Excel với 2 sheet:
# - Plan: Chi tiết phân phối
# - Summary: Tổng chi phí
```

### 4. `main()` - Hàm chính
```python
# Điều phối toàn bộ chương trình:
# Đọc → Tính toán → Hiển thị → Lưu
```