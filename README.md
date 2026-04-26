# 📊 BizHealth — Professional Business Intelligence Dashboard

🌐 **Live Website:** https://bizhealth.onrender.com

BizHealth is a modern, high-performance SaaS-grade business intelligence dashboard designed to monitor key performance indicators (KPIs), visualize financial metrics, and provide actionable insights for smarter decision-making.

It transforms raw business data into **clear, interactive visual insights** to help track growth, performance, and financial health in real time.

---

![License](https://img.shields.io/github/license/Dewri-Dev/buisness-dashboard)
![Stars](https://img.shields.io/github/stars/Dewri-Dev/buisness-dashboard)
![Issues](https://img.shields.io/github/issues/Dewri-Dev/buisness-dashboard)

[**🌐 Live Demo**](https://bizhealth.onrender.com)
[**🐞 Report Bug**](https://github.com/Dewri-Dev/buisness-dashboard/issues)

---

## 🚀 Overview

BizHealth provides business owners and teams with a centralized, professional dashboard to:

✔ Monitor revenue and expense performance in real-time
✔ Track business growth trends with Month-over-Month (MoM) signals
✔ Visualize revenue distribution by category (Sales, Marketing, Operations, etc.)
✔ Analyze business "Vitality Index" (Health Score)
✔ Run risk simulations to detect potential financial bottlenecks

---

## ✨ Key Features

### 📈 Professional Analytics & Forecasting
* **Real-Time KPI Cards:** Track Total Revenue, Expenses, Net Profit, and Health Score.
* **Interactive Trends:** Dynamic line charts powered by Chart.js with smooth gradients and custom tooltips.
* **Revenue Forecasting:** Automated 3-month moving average engine to predict next month's performance.
* **Category Breakdown:** Interactive donut charts showing where your money is coming from.

### 🔔 Smart Risk Alerts
* **Notification System:** A functional bell icon with a dropdown listing real-time risk alerts (e.g., high cash burn, declining margins).
* **Advanced Simulations:** A dedicated tool to simulate financial scenarios and get AI-driven risk assessments.

### 🌏 Multi-Language Support
* **Global Localization:** Toggle seamlessly between **English** and **অসমীয়া (Assamese)** via a global language switcher.
* **Localized UI:** Every chart label, sidebar link, and insight is translated for a native experience.

### 👥 User Authentication & Data Privacy
* **Secure Database Auth:** Robust SQLite-backed user registration and login system.
* **User Data Isolation:** Every user manages their own private financial data; no data is shared between accounts.

### 📱 Premium Responsive Design
* **Professional White Theme:** A clean, "Enterprise-Light" aesthetic using Tailwind CSS and Inter typography.
* **Glassmorphism:** Modern UI components with subtle blurs and shadows.
* **Lucide Icons:** High-quality vector iconography throughout the platform.

---

## 🛠️ Tech Stack

### 🎨 Frontend
* HTML5 / CSS3 (Vanilla + Tailwind CSS)
* **Chart.js:** For high-performance data visualizations.
* **Lucide-Icons:** For modern UI iconography.
* **Inter:** Premium typography from Google Fonts.

### ⚙️ Backend
* **Python / Flask:** Core application framework.
* **Flask-Login:** For secure session management.
* **ReportLab:** For generating PDF business reports.

### 🗄️ Database
* **SQLite3:** Relational database for users and business records.

### ☁️ Deployment
* **Render:** Cloud hosting for web services.
* **Gunicorn:** Production-grade WSGI server.

---

## 📦 Installation & Local Setup

Follow these steps to run BizHealth locally:

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Dewri-Dev/buisness-dashboard.git
cd buisness-dashboard
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the application
```bash
python app.py
```

Open your browser and visit: `http://127.0.0.1:5000`

---

## 📊 Dashboard Metrics

BizHealth visualizes important business indicators such as:
* 💰 **Revenue Trends:** Smooth line charts for cash flow analysis.
* 🍩 **Category Distribution:** Revenue share by unit (Sales, Salary, Marketing, etc.).
* 📉 **Expense Tracking:** Monitoring spikes in operational costs.
* 📈 **Growth signals:** Automated MoM percentage calculations.
* 🛡️ **Vitality Index:** A circular score (0-100) based on overall business stability.

---

## 👨‍💻 Authors

**Nayan Dewri**, **Dwibon Bhargab Deka**, **Barnil Mahanta**, **Tanisha Deka**

Developer & Computer Science Student
Assam, India

---

## ⭐ Support

If you like this project:
⭐ Star the repository
🍴 Fork it
📢 Share it with others
