```markdown
# 🏢 Apartment Allocation System

This is a FastAPI-based service that manages apartment allocation from predefined Excel blocks. It reads customer records, randomly assigns apartments, tracks remaining records, and allows for data resets and exports.

---

## 📦 Features

- Randomly fetch and remove customer records from Excel files.
- Track allocations and remaining records.
- Export assigned records as a downloadable Excel file.
- Reset data to the original state.
- CORS enabled for cross-origin access.

---

## 🧾 Directory Overview

```

├── main.py                   # FastAPI application <br>
├── Resources/                # Active Excel files (Block\_A/B/C.xlsx) <br>
├── Original\_Folder/          # Backup of the original Excel files <br>
├── Final\_output.xlsx         # Collected assigned records (auto-created) <br>
├── Preprocessing.ipynb       # Jupyter notebook for manual data preparation <br>
└── README.md                 # This documentation

````

---

## 🚀 API Endpoints

### `GET /records`
- Fetches one random record from a non-empty block (A, B, or C).
- Removes the record from the source file and adds it to `Final_output.xlsx`.

### `GET /download`
- Download the `Final_output.xlsx` file.

### `GET /reset`
- Deletes `Final_output.xlsx`.
- Restores original block files from `Original_Folder` into `Resources`.

---

## 📊 Data Format Requirements

Each Excel file must include the following **required columns**:
- `Customer Name`
- `Number of Rooms`
- `Type of Apartment`

Optional column:
- `FlatID` — if present, used to generate the full `Flat_ID`.

---

## ⚙️ Setup Instructions

1. Install dependencies:
```bash
pip install fastapi uvicorn pandas openpyxl
````

2. Run the application:

```bash
uvicorn main:app --reload
```

3. Open your browser and visit:

```
http://127.0.0.1:8000/docs
```

---

## 🧹 Preprocessing

The `Preprocessing.ipynb` file contains logic for cleaning or preparing Excel data before use. This may involve:

* Formatting column names
* Generating missing IDs
* Removing invalid rows

> Run this notebook before placing files in `Resources/`.

---

## ☁️ Deployment on AWS EC2 Instance

Follow these steps to deploy this API on an AWS EC2 server:

### 1. Launch EC2 Instance

* Use Ubuntu (recommended).
* Open ports **22**, **80**, and **8000** in the **Security Group**.

### 2. Connect to EC2 via SSH

```bash
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

### 3. Install Python and Pip

```bash
sudo apt update
sudo apt install python3-pip python3-venv -y
```

### 4. Clone or Upload Your Project

```bash
git clone https://github.com/your-repo-url.git
cd your-project-folder
```

Or use `scp` to upload files:

```bash
scp -i your-key.pem -r ./local-folder ubuntu@your-ec2-public-ip:/home/ubuntu/
```

### 5. Install Dependencies in a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or manually:

```bash
pip install fastapi uvicorn pandas openpyxl
```

### 6. Run the App

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 7. Access API

Go to:

```
http://your-ec2-public-ip:8000/docs
```

> For production, consider using **Gunicorn + Nginx** or **PM2** for process management.

---
