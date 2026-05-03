# ☀️ Pakistan Solar & Energy Efficiency Assessment Tool

A professional dashboard-style Streamlit web app that helps Pakistani households
understand their electricity usage, estimate solar system requirements, and
calculate financial savings.

---

## 🚀 How to Run Locally

### 1. Prerequisites

- Python 3.8 or higher installed
- pip package manager

### 2. Setup

```bash
# Clone or download the project files into a folder, then:

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## 📁 File Structure

```
project/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ⚙️ Core Formulas Used

| Calculation       | Formula                             |
| ----------------- | ----------------------------------- |
| Monthly Units     | Bill (PKR) ÷ 50                     |
| Solar System Size | Units ÷ 120 kW                      |
| Installation Cost | System Size × PKR 150,000           |
| Monthly Savings   | Units × PKR 50                      |
| Payback Period    | Total Cost ÷ (Monthly Savings × 12) |

---

## 🌍 Supported Cities

Karachi, Lahore, Islamabad, Peshawar, Quetta, Multan,
Faisalabad, Hyderabad, Sialkot, Rawalpindi

---

## 🔌 Features

- ✅ Energy Profile with bill-to-units conversion
- ✅ Solar system size recommendation
- ✅ Financial summary (cost, savings, payback)
- ✅ Net metering eligibility check
- ✅ City-specific peak sun hours
- ✅ Energy efficiency tips (bilingual EN/Urdu)
- ✅ Detailed analysis panel
- ✅ Downloadable report (.pdf)
- ✅ Professional SaaS-style dashboard UI

---

## 📋 Assumptions & Disclaimers

- Average electricity tariff: PKR 50/unit (NEPRA residential)
- Solar installation cost: PKR 150,000/kW (market average 2024-25)
- Net metering: NEPRA requires minimum 1 kW system
- Roof space: ~100 sq. ft. required per kW
- CO₂ factor: 0.46 kg/kWh (Pakistan national grid average)

_Consult a certified solar installer for exact system sizing and costs._
