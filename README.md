# 💰 Financial Analytics Dashboard

Ứng dụng phân tích danh mục cho vay và dự đoán lãi suất thông minh dựa trên dữ liệu lịch sử và Machine Learning.

🔗 **Link Demo:** [https://mdt3001-financial-analytics-dashboard-app-73qpsy.streamlit.app/](https://mdt3001-financial-analytics-dashboard-app-73qpsy.streamlit.app/)

---

## 🌟 Giới thiệu

**Financial Analytics Dashboard** là một nền tảng phân tích dữ liệu tự phục vụ (Self-Service Analytics) giúp các tổ chức tài chính quản lý danh mục cho vay hiệu quả hơn. Ứng dụng không chỉ cung cấp cái nhìn tổng quan về hiệu suất các khoản vay hiện tại mà còn tích hợp mô hình AI mạnh mẽ để dự báo lãi suất dựa trên hồ sơ rủi ro của khách hàng.

---

## 🚀 Tính năng nổi bật

### 1. 📊 Dashboard Phân tích Toàn diện (Interactive Dashboard)

- **KPI Metrics:** Theo dõi các chỉ số quan trọng:
  - Tổng khối lượng khoản vay (Total Loan Volume)
  - Lãi suất trung bình (Avg Interest Rate)
  - Tỷ lệ rủi ro (Risk Rate)
  - Số tiền vay trung bình

- **Hệ thống biểu đồ đa dạng:**
  - Phân phối khoản vay theo hạng tín dụng (Grade) và lãi suất đi kèm
  - Tỷ lệ trạng thái khoản vay (Fully Paid, Current, Charged Off)
  - Bản đồ nhiệt (Treemap) phân bố khoản vay theo khu vực (Region) và lãi suất
  - Phân tích mục đích vay vốn và tương quan giữa thu nhập với số tiền vay

### 2. 🤖 Dự đoán Lãi suất bằng AI (AI Prediction)

- **Mô hình XGBoost:** Sử dụng thuật toán XGBoost tiên tiến để dự đoán lãi suất dựa trên 7 đặc trưng chính:
  - DTI (Debt-to-Income Ratio)
  - Số tiền vay
  - Kỳ hạn
  - Hạng tín dụng (đã mã hóa)
  - Trạng thái xác minh thu nhập
  - Mục đích vay

- **Kết quả trực quan:**
  - Hiển thị lãi suất dự đoán qua biểu đồ Gauge
  - So sánh với lãi suất trung bình thị trường
  - Tính toán chi tiết số tiền phải trả hàng tháng (Installment)

- **Lời khuyên tài chính:** Đưa ra các gợi ý cụ thể để khách hàng có thể cải thiện hồ sơ tín dụng và nhận được mức lãi suất tốt hơn.

### 3. 📁 Khám phá và Xuất dữ liệu (Data Explorer)

- **Bộ lọc linh hoạt:** Lọc dữ liệu theo hạng tín dụng, bang, vùng miền, số tiền vay và biên độ lãi suất
- **Quản lý dữ liệu:** Cho phép người dùng tải lên file CSV tùy chỉnh để phân tích trên giao diện Dashboard có sẵn
- **Xuất báo cáo:** Hỗ trợ tải xuống dữ liệu đã lọc dưới dạng CSV để phục vụ các báo cáo bên ngoài

---

## 🛠 Công nghệ sử dụng

| Công nghệ | Mô tả |
|-----------|-------|
| **Python** | Ngôn ngữ chính |
| **Streamlit** | Giao diện web với Custom CSS cho UI/UX hiện đại |
| **Pandas, Numpy** | Xử lý và phân tích dữ liệu |
| **Plotly** | Trực quan hóa dữ liệu tương tác |
| **XGBoost** | Mô hình Machine Learning dự đoán lãi suất |
| **Scikit-learn** | Tiền xử lý và chuẩn hóa dữ liệu |
| **Joblib** | Lưu trữ model và scaler |

---

## 📁 Cấu trúc thư mục dự án

```
├── app.py                      # Điểm khởi đầu của ứng dụng
├── requirements.txt            # Danh sách thư viện cần cài đặt
├── financial_loan_clean.csv    # Dữ liệu mẫu (đã làm sạch)
├── xgb.joblib                  # Mô hình XGBoost đã huấn luyện
├── scaler.pkl                  # Bộ chuẩn hóa dữ liệu đầu vào
│
├── config/
│   └── settings.py             # Cấu hình giao diện, CSS và các mapping
│
├── components/                 # Các thành phần giao diện
│   ├── header.py               # Header & Footer
│   ├── sidebar.py              # Bộ lọc và upload dữ liệu
│   ├── kpi_metrics.py          # Các thẻ chỉ số KPI
│   └── tabs/                   # Nội dung các Tab chính
│
├── charts/
│   └── visualizations.py       # Logic tạo biểu đồ Plotly
│
└── utils/                      # Các hàm tiện ích
    ├── data_loader.py          # Tải và cache dữ liệu
    ├── helpers.py              # Tính toán tài chính và xử lý feature
    └── model_loader.py         # Tải và cache Model/Scaler
```

---

## 💻 Hướng dẫn chạy dự án cục bộ

### Yêu cầu hệ thống
- Python >= 3.8
- pip (Python package manager)

### Các bước cài đặt

1. **Clone repository:**
```bash
git clone <URL_REPOSITORY>
cd financial-analytics-dashboard
```

2. **Tạo môi trường ảo (khuyến nghị):**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Cài đặt thư viện:**
```bash
pip install -r requirements.txt
```

4. **Khởi chạy ứng dụng:**
```bash
streamlit run app.py
```

5. **Truy cập ứng dụng:** Mở trình duyệt tại `http://localhost:8501`

---

## 📄 License

This project is licensed under the MIT License.

---


