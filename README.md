<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1d14ef9b-4deb-4467-93d2-45b0dbb9cbc2" />

# Anime Recommendation System

Project web nho su dung Flask de goi y anime tuong tu dua tren the loai (genres) trong file dataset `anime-standalone.csv`.

## 1) Yeu cau moi truong

- Python 3.9+ (khuyen nghi Python 3.10 hoac 3.11)
- Pip

## 2) Cai dat

Mo terminal tai thu muc project, sau do chay:

```powershell
python -m venv .venv
```

Kich hoat virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Cai dependencies:

```powershell
pip install flask pandas scikit-learn
```

Neu PowerShell bao loi script execution bi chan, chay tam thoi:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

roi kich hoat lai `.venv`.

## 3) Chay project

Chay web app:

```powershell
python app.py
```

Sau khi chay thanh cong, mo trinh duyet tai:

```text
http://127.0.0.1:5000
```

## 4) Cach su dung

1. Nhap ten anime vao o tim kiem.
2. Chon so luong goi y (1 den 50).
3. Bam **Goi y Anime** de xem ket qua.

## 5) Cau truc chinh

```text
anime recommendation system/
|- app.py                 # Flask app va API /recommend
|- anime.py               # Logic tinh do tuong dong va goi y
|- anime-standalone.csv   # Du lieu anime
|- templates/index.html   # Giao dien HTML
|- static/style.css       # CSS
|- static/script.js       # JS goi API va render ket qua
```

## 6) Loi thuong gap

- **ModuleNotFoundError** (vd: khong tim thay `flask`, `pandas`, `sklearn`):
  - Dam bao da kich hoat `.venv`
  - Cai lai bang dung interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install flask pandas scikit-learn
```

- **Khong tim thay file CSV**:
  - Dam bao file `anime-standalone.csv` nam cung cap voi `app.py`.

- **Port 5000 dang bi chiem**:
  - Tat ung dung dang dung port 5000 hoac doi port trong `app.py`.

## 7) Ghi chu

- `app.py` dang de `debug=True`, phu hop cho local dev.
- Khi deploy production, nen dung WSGI server (gunicorn/waitress) va tat debug mode.
