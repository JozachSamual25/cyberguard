# 🛡️ CyberGuard – SOC-Style Cybersecurity Dashboard

CyberGuard is a cybersecurity monitoring system that simulates real-world attacks and detects them in real time using a SOC-style dashboard.

---

## 🚀 Features

- 🔐 Secure Login System
- 🚨 SQL Injection Detection
- ⚡ Brute Force Attack Detection
- 📊 Real-Time Dashboard Monitoring
- 📁 Log Export (CSV)
- 🔥 Severity-Based Alerts (INFO, WARNING, CRITICAL)

---

## 🧠 Tech Stack

- Python (Flask)
- SQLite
- JavaScript (Chart.js)
- HTML + Bootstrap

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/JozachSamual25/cyberguard.git
cd cyberguard

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python db_setup.py
python app.py
