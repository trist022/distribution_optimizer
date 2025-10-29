#  Phần mềm Tối ưu hoá Phân phối (Minimum Cost Flow)

##  Giới thiệu

Đây là chương trình **hoạch định kế hoạch phân phối tối ưu**, giúp tìm cách vận chuyển hàng hoá từ các **trạm phát (nơi có hàng)** tới các **trạm thu (nơi cần hàng)** sao cho **tổng chi phí vận chuyển là thấp nhất**.

Chương trình áp dụng **thuật toán dòng chi phí cực tiểu (Min-Cost Flow)** – một bài toán kinh điển trong lĩnh vực tối ưu hóa mạng (network optimization).

---

## ⚙️ Mục tiêu bài toán

Cho trước:
- Một tập **trạm phát (supply nodes)**, mỗi trạm có lượng hàng **Cung (Supply)**.
- Một tập **trạm thu (demand nodes)**, mỗi trạm có nhu cầu **Nhu cầu (Demand)**.
- Một bảng **chi phí vận chuyển (Cost Matrix)**, biểu diễn chi phí từ mỗi trạm phát → mỗi trạm thu.

👉 Nhiệm vụ: tìm kế hoạch phân phối hàng sao cho:
- Tất cả nhu cầu được đáp ứng (hoặc tối đa có thể).
- **Tổng chi phí vận chuyển nhỏ nhất.**

---

## Dữ liệu đầu vào

Chương trình đọc dữ liệu từ một file Excel có 3 sheet:

### 1. `TramPhat` – Thông tin các trạm phát
| TenTram | Cung |
|----------|------|
| A1 | 500 |
| A2 | 850 |
| A3 | 450 |

### 2. `TramThu` – Thông tin các trạm thu
| TenTram | NhuCau |
|----------|--------|
| B1 | 900 |
| B2 | 300 |
| B3 | 150 |
| B4 | 450 |

### 3. `ChiPhi` – Ma trận chi phí
| TramPhat | B1 | B2 | B3 | B4 |
|-----------|----|----|----|----|
| A1 | 31100 | 18000 | 45000 | 8500 |
| A2 | 26000 | 25000 | 42300 | 22000 |
| A3 | 29500 | 14000 | 45800 | 19000 |

---

##  Thuật toán giải (Min-Cost Flow)

Dưới đây là mô tả chi tiết **từng bước của thuật toán** được sử dụng trong chương trình:

### **Bước 1: Xây dựng đồ thị luồng (Flow Network)**

- Mỗi **trạm phát** và **trạm thu** được xem là một **nút (node)** trong đồ thị.  
- Thêm hai nút đặc biệt:
  - `SOURCE` (nguồn tổng)
  - `SINK` (đích tổng)

Các loại cạnh (edges):
1. `SOURCE → Trạm phát`: dung lượng = cung của trạm, chi phí = 0  
2. `Trạm phát → Trạm thu`: dung lượng rất lớn, chi phí = giá vận chuyển  
3. `Trạm thu → SINK`: dung lượng = nhu cầu, chi phí = 0

---

### **Bước 2: Thuật toán tìm dòng chi phí cực tiểu**

Chương trình sử dụng **Successive Shortest Path Algorithm (Luồng ngắn nhất lặp lại)**:

1. Khởi tạo tổng luồng = 0, tổng chi phí = 0.  
2. Trong khi vẫn còn nhu cầu chưa được đáp ứng:
   - Tìm **đường đi chi phí thấp nhất** từ `SOURCE` → `SINK` trong đồ thị dư (residual graph) bằng **Dijkstra**.  
   - Xác định **lượng hàng có thể gửi thêm** (bottleneck).  
   - Cập nhật:
     - Luồng mới trên từng cạnh.
     - Tổng chi phí += (lượng hàng) × (chi phí trên đường đó).
3. Lặp lại cho đến khi tất cả nhu cầu được thỏa mãn.

---

### **Bước 3: Kết quả tối ưu**

Sau khi hoàn tất:
- Chương trình sẽ trích xuất bảng phân phối cuối cùng:
  - Cột `From` – trạm phát.
  - Cột `To` – trạm thu.
  - Cột `Quantity` – số lượng gửi.
  - `UnitCost` – chi phí đơn vị.
  - `Cost` – tổng chi phí cho tuyến đó.

---

##  Kết quả đầu ra

File kết quả: **`allocation_optimal.xlsx`**

Bao gồm 4 sheet:
1. `OptimalPlan` – chi tiết kế hoạch phân phối tối ưu  
2. `SupplySummary` – tổng hàng đã gửi của từng trạm phát  
3. `DemandSummary` – tổng hàng đã nhận của từng trạm thu  
4. `Summary` – tổng chi phí tối thiểu

---

## 💻 Cách chạy chương trình

### 1️⃣ Cài đặt môi trường
```bash
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 2️⃣ Chạy chương trình
```bash
python3 distribution_optimizer_from_file.py du_lieu_phan_phoi.xlsx
```

### 3️⃣ Xem kết quả
- Màn hình sẽ hiển thị kết quả tóm tắt.
- File Excel `allocation_optimal.xlsx` sẽ được tạo trong cùng thư mục.

---

##  Cấu trúc thư mục
```
project/
├── distribution_optimizer_from_file.py   # Mã nguồn chính
├── requirements.txt                      # Các thư viện cần cài
├── du_lieu_phan_phoi.xlsx                # File đầu vào mẫu
└── allocation_optimal.xlsx               # File kết quả (tự động tạo)
```

---
