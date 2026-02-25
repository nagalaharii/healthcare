# 🏥 HealthAI - AI for Equitable Healthcare

A complete hackathon project for the **Healthcare & MedTech AI** domain.

## 🚀 Quick Start (2 minutes)

### Step 1: Install Flask
```bash
pip install flask
```

### Step 2: Run the app
```bash
cd healthcare_app
python app.py
```

### Step 3: Open browser
Go to: **http://localhost:5000**

---

## 📋 Features

### 1. 🩺 AI Symptom Triage (`/triage`)
- Enter symptoms via text or quick-add buttons
- AI analyzes and returns:
  - Urgency level (Emergency / High / Moderate / Low)
  - Top 5 possible conditions with likelihood %
  - Immediate first-aid instructions
  - Referral recommendation

### 2. 📊 Health Dashboard (`/dashboard`)
- Real-time KPIs (Active Cases, Risk Districts, Telemedicine stats)
- Active outbreak alerts
- Monthly case trend (Line chart)
- Disease distribution (Donut chart)
- Regional risk table by district
- Cases by district bar chart

### 3. 🏠 Home Page (`/`)
- Problem overview
- Feature showcase
- Impact statistics

---

## 🗂️ Project Structure
```
healthcare_app/
├── app.py              # Flask backend + symptom analysis engine
├── requirements.txt    # Dependencies
└── templates/
    ├── base.html       # Navigation + layout
    ├── index.html      # Home page
    ├── triage.html     # Symptom checker
    └── dashboard.html  # Health dashboard
```

---

## 🧠 How the AI Works (No API needed!)
- Rule-based symptom matching with severity weights
- 20+ symptoms mapped to 30+ conditions
- Severity scoring determines urgency level
- Age-adjusted recommendations
- First-aid tips based on symptom profile

---

## 🎯 Hackathon Alignment
- ✅ Addresses Urban-Rural healthcare gap
- ✅ Frontline worker support (ASHA/ANM)
- ✅ Data-driven public health decisions
- ✅ Ethical AI (privacy-first, no data stored)
- ✅ Scalable web-based solution
- ✅ Real-world applicable

---

## 🚨 Emergency
**India Emergency: 108**
This tool is for preliminary guidance only. Always consult a qualified doctor.
