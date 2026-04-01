<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1d14ef9b-4deb-4467-93d2-45b0dbb9cbc2" />

# Anime Recommendation System

Project web nhỏ sử dụng Flask để gợi ý anime tương tự dựa trên thể loại (genres) trong file dataset `anime-standalone.csv`.

## 1) Yêu cầu môi trường

- Python 3.9+ (khuyến nghị Python 3.10 hoặc 3.11)
- Pip

## 2) Cài đặt

Mở terminal tại thư mục project, sau đó chạy:

```powershell
python -m venv .venv
```

Kích hoạt virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cài dependencies:

```powershell
pip install flask pandas scikit-learn
```

Nếu PowerShell báo lỗi script execution bị chặn, chạy tạm thời:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

rồi kích hoạt lại `.venv`.

## 3) Chạy project

Chạy web app:

```powershell
python app.py
```

Sau khi chạy thành công, mở trình duyệt tại:

```text
http://127.0.0.1:5000
```

## 4) Cách sử dụng

1. Nhập tên anime vào ô tìm kiếm.
2. Chọn số lượng gợi ý (1 đến 50).
3. Bấm **Gợi ý Anime** để xem kết quả.

## 5) Cấu trúc chính

```text
anime recommendation system/
|- app.py                 # Flask app và API /recommend
|- anime.py               # Logic tính độ tương đồng và gợi ý
|- anime-standalone.csv   # Dữ liệu anime
|- templates/index.html   # Giao diện HTML
|- static/style.css       # CSS
|- static/script.js       # JS gọi API và render kết quả
```

## 6) Lỗi thường gặp

- **ModuleNotFoundError** (vd: không tìm thấy `flask`, `pandas`, `sklearn`):
  - Đảm bảo đã kích hoạt `.venv`
  - Cài lại bằng đúng interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install flask pandas scikit-learn
```

- **Không tìm thấy file CSV**:
  - Đảm bảo file `anime-standalone.csv` nằm cùng cấp với `app.py`.

- **Port 5000 đang bị chiếm**:
  - Tắt ứng dụng đang dùng port 5000 hoặc đổi port trong `app.py`.

## 7) Ghi chú

- `app.py` đang để `debug=True`, phù hợp cho local dev.
- Khi deploy production, nên dùng WSGI server (gunicorn/waitress) và tắt debug mode.
