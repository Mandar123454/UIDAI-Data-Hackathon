<p align="center">
  <img src="https://img.shields.io/badge/UIDAI-Data%20Hackathon%202026-00aa44?style=for-the-badge" alt="UIDAI Hackathon"/>
</p>

<h1 align="center">🏛️ UIDAI Aadhaar Enrolment Analytics Dashboard</h1>
<h3 align="center">Maharashtra State Analysis — Government-Grade Insights</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-3.1-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Pandas-2.3-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Plotly-6.5-3F4F75?style=flat-square&logo=plotly&logoColor=white" alt="Plotly"/>
  <img src="https://img.shields.io/badge/Azure-App%20Service-0078D4?style=flat-square&logo=microsoftazure&logoColor=white" alt="Azure"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License"/>
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square" alt="Status"/>
  <img src="https://img.shields.io/badge/Theme-Dark%20Mode-1a1a2e?style=flat-square" alt="Dark Mode"/>
</p>

<p align="center">
  <a href="https://uidai-maharashtra-dashboard-cwcccngcfzbwcca2.centralindia-01.azurewebsites.net/">🔗 Live Dashboard</a>
  <!-- If you prefer a badge-style button instead, uncomment the next line -->
  <!-- <a href="https://uidai-maharashtra-dashboard-cwcccngcfzbwcca2.centralindia-01.azurewebsites.net/"><img src="https://img.shields.io/badge/Live%20Dashboard-Open-00aa44?style=for-the-badge" alt="Live Dashboard"/></a> -->
</p>

---

## 📋 Overview

A comprehensive, **judge-ready analytics solution** for the UIDAI Data Hackathon 2026. This project transforms raw Aadhaar enrolment data into actionable policy insights through interactive visualizations and a professional PDF report.

| Metric | Value |
|--------|-------|
| 📊 Records Analyzed | **93,184** |
| 📅 Monthly Data Points | **101** |
| 🏘️ Districts Covered | **53** |
| 📍 Pincodes Mapped | **1,585** |

---

## ✨ Features

### 🎯 Analytics Dashboard
- **Dark mode UI** — Professional, easy on the eyes
- **7 interactive Plotly charts** — Zoom, pan, export to PNG
- **Real-time insights** — Auto-generated from live data
- **Policy recommendations** — Data-driven, actionable

### 📈 Visualizations
| Chart | Purpose |
|-------|---------|
| State Monthly Trend | Track enrolment momentum over time |
| Age Group Dynamics | Understand demographic composition |
| District Disparities | Identify top/bottom performers |
| Pincode Distribution | Assess local-level variability |
| Seasonality Index | Plan campaigns by peak months |
| Risk Flag Summary | Flag saturation, volatility, momentum |
| Child Momentum | Monitor child enrolment share |

### 📑 PDF Report Generator
- **8-section professional document**
- Government-grade formatting
- Executive summary + findings + recommendations
- Auto-generated from analysis pipeline

### 📥 Downloads
- Dataset (CSV) and Report (PDF) available directly from dashboard

---

## 🔍 Key Findings

```
┌─────────────────────────────────────────────────────────────┐
│  📈 Overall Growth:        +635.0%                          │
│  📉 Recent MoM Trend:      −11.1%                           │
│  👶 Child Share (0-17):    97.8%                            │
│  ⚠️  Saturation Risk:       49 districts                    │
│  📊 Volatile Districts:    22                               │
│  📅 Peak Months:           July & April                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Project Structure

```
UIDAI Data Hackathon/
├── 📄 app.py                    # Flask application entry
├── 📄 data_pipeline.py          # Data processing & visualizations
├── 📄 generate_report.py        # Technical PDF report generator
├── 📄 generate_student_report.py # Student project report generator
├── 📄 run_data_check.py         # Quick validation script
├── 📄 wsgi.py                   # Azure App Service entrypoint
├── 📄 requirements.txt          # Python dependencies
├── 📄 LICENSE                   # MIT License
├── 📂 Dataset/
│   └── Aadhar Enrolment Dataset.csv
├── 📂 templates/
│   └── index.html               # Dashboard UI
├── 📂 static/
│   └── styles.css               # Dark theme styles
├── 📄 UIDAI_Aadhaar_Analytics_Report.pdf
└── 📄 UIDAI_Report.pdf           # Student project report
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone or navigate to project
cd "UIDAI Data Hackathon"

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run Dashboard

```bash
python app.py
```
🌐 Open **http://localhost:5000**

### Generate PDF Report

```bash
python generate_report.py
```
📄 Output: `UIDAI_Aadhaar_Analytics_Report.pdf`

### Generate Student Report

```bash
python generate_student_report.py
```
📄 Output: `UIDAI_Report.pdf` — Simple student project report in plain academic English

### Validate Data Pipeline

```bash
python run_data_check.py
```

---

## ☁️ Azure Deployment

### App Service Configuration

| Setting | Value |
|---------|-------|
| Runtime | Python 3.10+ |
| Startup Command | `gunicorn --bind=0.0.0.0:$PORT wsgi:app` |
| SKU | B1 or higher recommended |

### Deploy

1. Create Azure App Service (Linux, Python)
2. Configure startup command
3. Deploy via Git, ZIP, or Azure CLI
4. Ensure `Dataset/` folder is included

---

## 📊 Advanced Metrics

| Metric | Definition |
|--------|------------|
| **Saturation Index** | Last 3-month avg ÷ Rolling 12-month max |
| **Volatility Flag** | 12-month std dev > 1.5× state median |
| **Low Momentum** | Last 3-month avg < 50% of 12-month avg |
| **Child Momentum** | Share of 0–17 age enrolments over time |

---

## 🎯 Policy Recommendations

Based on data-driven analysis:

1. **👶 Child Infrastructure** — Prioritize biometric updates for children (93.9% share)
2. **🚐 Mobile Units** — Deploy to Gondia, Ahilyanagar, Hingoli
3. **📅 Campaign Timing** — Align with July & April peaks
4. **⚠️ Monitor Volatility** — Focus on Jalgaon, Jalna, Ahmadnagar
5. **🎯 Service Quality** — Shift focus in 49 saturated districts

---

## 🛠️ Tech Stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,flask,azure,html,css" alt="Tech Stack"/>
</p>

| Layer | Technology |
|-------|------------|
| Backend | Flask 3.1, Gunicorn |
| Data | Pandas 2.3, NumPy |
| Visualization | Plotly 6.5 |
| PDF Generation | ReportLab 4.4 |
| Hosting | Azure App Service |
| Theme | Custom Dark Mode |

---

## 📜 License

This project is licensed under the **MIT License**.

```
MIT License © 2026 Mandar Kajbaje
```

See [LICENSE](LICENSE) for full details.

---

## 👤 Author

<p align="center">
  <strong>Mandar Kajbaje</strong><br/>
  UIDAI Data Hackathon 2026
</p>

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-%F0%9F%92%96-red?style=for-the-badge" alt="Made with love"/>
  <img src="https://img.shields.io/badge/For-UIDAI%20Hackathon-00aa44?style=for-the-badge" alt="For UIDAI"/>
</p>
