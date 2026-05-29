# 📖 Học Khải Huyền – Kinh Thánh Tiếng Việt 1925

Ứng dụng web học thuộc lòng 22 đoạn sách Khải Huyền qua bài tập **điền vào chỗ trống**.

---

## 🚀 Cách chạy

### 1. Cài Python (nếu chưa có)
Tải tại https://python.org – chọn Python 3.9 trở lên.

### 2. Mở Terminal / Command Prompt, vào thư mục này
```
cd khai_huyen
```

### 3. Cài thư viện cần thiết
```
pip install flask
```

### 4. Chạy ứng dụng
```
python app.py
```

### 5. Mở trình duyệt
Truy cập: **http://localhost:5000**

---

## 🎮 Cách dùng

- **Chọn đoạn**: Dùng menu thả xuống để chọn đoạn 1-22, hoặc để **Ngẫu nhiên**.
- **Đọc câu hỏi**: Một câu Kinh Thánh được hiển thị với một chỗ trống (`___________`).
- **Điền đáp án**: Gõ vào ô trả lời rồi nhấn **Kiểm tra** hoặc **Enter**.
- **Xem kết quả**: App sẽ hiện đúng/sai và đáp án đúng.
- **Câu tiếp**: Nhấn **Câu tiếp →** hoặc **Enter** sau khi trả lời.

---

## 📊 Tính năng

- ✅ Toàn bộ 22 đoạn Khải Huyền bản 1925
- 🎲 Câu hỏi ngẫu nhiên từ bất kỳ câu nào
- 📈 Theo dõi điểm số, độ chính xác, chuỗi đúng liên tiếp
- 📜 Lịch sử 20 câu gần nhất
- ⌨️ Hỗ trợ phím Enter để trả lời nhanh

---

## 📁 Cấu trúc thư mục

```
khai_huyen/
├── app.py                  ← Ứng dụng Flask chính
├── khai_huyen_data.json    ← Dữ liệu 22 đoạn Khải Huyền
├── requirements.txt        ← Thư viện cần cài
├── templates/
│   └── index.html          ← Giao diện web
└── README.md               ← File này
```
