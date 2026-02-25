from flask import Flask, render_template, request, jsonify, session
import json
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'healthai_secret_2025'

# Mock symptom database with conditions, severity, and recommendations
SYMPTOM_DATABASE = {
    "fever": {
        "conditions": ["Common Cold", "Flu", "Malaria", "Dengue", "Typhoid"],
        "severity_weight": 2
    },
    "cough": {
        "conditions": ["Common Cold", "Flu", "Bronchitis", "Tuberculosis", "COVID-19"],
        "severity_weight": 2
    },
    "headache": {
        "conditions": ["Migraine", "Tension Headache", "Dengue", "Hypertension", "Sinusitis"],
        "severity_weight": 1
    },
    "chest pain": {
        "conditions": ["Angina", "Heart Attack", "Pneumonia", "Anxiety", "GERD"],
        "severity_weight": 5
    },
    "shortness of breath": {
        "conditions": ["Asthma", "Pneumonia", "Heart Failure", "COVID-19", "Anemia"],
        "severity_weight": 5
    },
    "fatigue": {
        "conditions": ["Anemia", "Diabetes", "Thyroid Disorder", "Depression", "Malaria"],
        "severity_weight": 1
    },
    "nausea": {
        "conditions": ["Gastroenteritis", "Food Poisoning", "Migraine", "Pregnancy", "Appendicitis"],
        "severity_weight": 2
    },
    "vomiting": {
        "conditions": ["Gastroenteritis", "Food Poisoning", "Appendicitis", "Migraine"],
        "severity_weight": 3
    },
    "diarrhea": {
        "conditions": ["Gastroenteritis", "Food Poisoning", "Cholera", "IBS", "Typhoid"],
        "severity_weight": 3
    },
    "abdominal pain": {
        "conditions": ["Appendicitis", "Gastritis", "IBS", "Kidney Stones", "Peptic Ulcer"],
        "severity_weight": 3
    },
    "rash": {
        "conditions": ["Dengue", "Chickenpox", "Allergy", "Measles", "Typhoid"],
        "severity_weight": 2
    },
    "joint pain": {
        "conditions": ["Arthritis", "Dengue", "Chikungunya", "Gout", "Lupus"],
        "severity_weight": 2
    },
    "back pain": {
        "conditions": ["Muscle Strain", "Kidney Infection", "Herniated Disc", "Osteoporosis"],
        "severity_weight": 2
    },
    "dizziness": {
        "conditions": ["Vertigo", "Low Blood Pressure", "Anemia", "Dehydration", "Inner Ear Infection"],
        "severity_weight": 2
    },
    "sore throat": {
        "conditions": ["Strep Throat", "Tonsillitis", "Common Cold", "Flu"],
        "severity_weight": 1
    },
    "runny nose": {
        "conditions": ["Common Cold", "Flu", "Allergic Rhinitis", "Sinusitis"],
        "severity_weight": 1
    },
    "high fever": {
        "conditions": ["Malaria", "Dengue", "Typhoid", "Sepsis", "Severe Flu"],
        "severity_weight": 4
    },
    "unconscious": {
        "conditions": ["Stroke", "Heart Attack", "Severe Hypoglycemia", "Seizure", "Severe Dehydration"],
        "severity_weight": 10
    },
    "blurred vision": {
        "conditions": ["Diabetes", "Hypertension", "Migraine", "Glaucoma", "Stroke"],
        "severity_weight": 4
    },
    "swelling": {
        "conditions": ["Heart Failure", "Kidney Disease", "Liver Disease", "DVT", "Allergy"],
        "severity_weight": 3
    }
}

CONDITION_INFO = {
    "Common Cold": {"type": "mild", "description": "Viral infection of upper respiratory tract"},
    "Flu": {"type": "moderate", "description": "Influenza - contagious respiratory illness"},
    "Malaria": {"type": "severe", "description": "Mosquito-borne parasitic infection - needs immediate attention"},
    "Dengue": {"type": "severe", "description": "Mosquito-borne viral infection - monitor platelet count"},
    "Typhoid": {"type": "severe", "description": "Bacterial infection spread through contaminated food/water"},
    "Tuberculosis": {"type": "severe", "description": "Bacterial lung infection - requires long-term treatment"},
    "Bronchitis": {"type": "moderate", "description": "Inflammation of bronchial tubes"},
    "COVID-19": {"type": "severe", "description": "Coronavirus infection - isolate and consult doctor"},
    "Migraine": {"type": "moderate", "description": "Severe recurring headaches often with nausea"},
    "Heart Attack": {"type": "emergency", "description": "EMERGENCY - Call ambulance immediately"},
    "Stroke": {"type": "emergency", "description": "EMERGENCY - Call ambulance immediately"},
    "Pneumonia": {"type": "severe", "description": "Lung infection - needs immediate medical attention"},
    "Appendicitis": {"type": "emergency", "description": "EMERGENCY - Requires immediate surgery"},
    "Asthma": {"type": "moderate", "description": "Chronic airway inflammation - use inhaler if prescribed"},
    "Anemia": {"type": "moderate", "description": "Low blood iron/hemoglobin - diet and supplements needed"},
    "Diabetes": {"type": "moderate", "description": "Blood sugar regulation disorder - needs monitoring"},
    "Gastroenteritis": {"type": "mild", "description": "Stomach bug - rest and hydration recommended"},
    "Food Poisoning": {"type": "moderate", "description": "Foodborne illness - hydration is key"},
    "Cholera": {"type": "severe", "description": "Severe bacterial diarrhea - needs immediate rehydration"},
    "Chickenpox": {"type": "moderate", "description": "Viral infection with itchy rash - isolate from others"},
    "Arthritis": {"type": "moderate", "description": "Joint inflammation - physiotherapy and medication needed"},
    "Dengue": {"type": "severe", "description": "Mosquito-borne fever - monitor for warning signs"},
    "Vertigo": {"type": "moderate", "description": "Balance disorder - avoid sudden movements"},
    "Hypertension": {"type": "moderate", "description": "High blood pressure - lifestyle changes and medication"},
    "Allergy": {"type": "mild", "description": "Immune response to allergens - antihistamines may help"},
}

def analyze_symptoms(symptoms_list, age, duration, additional_info=""):
    matched = {}
    total_severity = 0
    
    symptoms_lower = [s.lower().strip() for s in symptoms_list]
    
    for symptom in symptoms_lower:
        for key, data in SYMPTOM_DATABASE.items():
            if key in symptom or symptom in key:
                for condition in data["conditions"]:
                    matched[condition] = matched.get(condition, 0) + data["severity_weight"]
                total_severity += data["severity_weight"]
    
    # Sort by score
    sorted_conditions = sorted(matched.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Determine urgency
    if total_severity >= 10:
        urgency = "EMERGENCY"
        urgency_color = "#dc2626"
        action = "🚨 Go to Emergency Room IMMEDIATELY or call 108"
    elif total_severity >= 6:
        urgency = "HIGH"
        urgency_color = "#ea580c"
        action = "⚠️ Visit a hospital/doctor TODAY - Do not delay"
    elif total_severity >= 3:
        urgency = "MODERATE"
        urgency_color = "#d97706"
        action = "📋 Visit a clinic within 24-48 hours"
    else:
        urgency = "LOW"
        urgency_color = "#16a34a"
        action = "💊 Rest at home, monitor symptoms. Visit clinic if worsening"

    # Age adjustments
    if age < 5 or age > 65:
        if urgency in ["LOW", "MODERATE"]:
            urgency = "MODERATE" if urgency == "LOW" else "HIGH"
            action = f"⚠️ Given patient age ({age}), extra caution recommended. " + action

    conditions_detail = []
    for cond, score in sorted_conditions:
        info = CONDITION_INFO.get(cond, {"type": "unknown", "description": "Consult a doctor for accurate diagnosis"})
        conditions_detail.append({
            "name": cond,
            "likelihood": min(round((score / max(total_severity, 1)) * 100), 95),
            "type": info["type"],
            "description": info["description"]
        })

    # First aid tips
    first_aid = get_first_aid(symptoms_lower, urgency)
    
    return {
        "urgency": urgency,
        "urgency_color": urgency_color,
        "action": action,
        "conditions": conditions_detail,
        "first_aid": first_aid,
        "disclaimer": "⚠️ This is an AI-assisted preliminary assessment ONLY. Always consult a qualified healthcare professional for proper diagnosis and treatment."
    }

def get_first_aid(symptoms, urgency):
    tips = []
    if urgency == "EMERGENCY":
        tips.append("Call 108 (India Emergency) immediately")
        tips.append("Do NOT leave the patient alone")
        tips.append("Keep patient calm and still")
    if any(s in symptoms for s in ["fever", "high fever"]):
        tips.append("Apply cool wet cloth on forehead")
        tips.append("Give paracetamol if available (follow dosage)")
        tips.append("Ensure adequate fluid intake")
    if any(s in symptoms for s in ["vomiting", "diarrhea", "nausea"]):
        tips.append("ORS (Oral Rehydration Solution) every 15-20 mins")
        tips.append("Avoid solid food until vomiting stops")
        tips.append("Watch for signs of dehydration")
    if any(s in symptoms for s in ["cough", "shortness of breath"]):
        tips.append("Keep the patient in upright/sitting position")
        tips.append("Ensure good ventilation in the room")
    if any(s in symptoms for s in ["chest pain"]):
        tips.append("🚨 Make patient sit/lie comfortably")
        tips.append("Loosen tight clothing")
        tips.append("Rush to emergency - could be cardiac")
    if not tips:
        tips.append("Rest and stay hydrated")
        tips.append("Monitor for worsening symptoms")
        tips.append("Avoid self-medication without doctor advice")
    return tips


# Mock health data for dashboard
HEALTH_DATA = {
    "regions": [
        {"name": "Anantapur", "risk": "High", "cases": 142, "disease": "Malaria"},
        {"name": "Kurnool", "risk": "Medium", "cases": 87, "disease": "Dengue"},
        {"name": "Guntur", "risk": "Low", "cases": 34, "disease": "Typhoid"},
        {"name": "Vizag", "risk": "Medium", "cases": 95, "disease": "COVID-19"},
        {"name": "Nellore", "risk": "High", "cases": 118, "disease": "Dengue"},
        {"name": "Chittoor", "risk": "Low", "cases": 28, "disease": "Common Cold"},
        {"name": "Kadapa", "risk": "High", "cases": 156, "disease": "Malaria"},
        {"name": "Prakasam", "risk": "Medium", "cases": 73, "disease": "Typhoid"},
    ],
    "monthly_cases": [120, 145, 98, 167, 203, 189, 234, 178, 145, 167, 189, 210],
    "disease_distribution": {
        "Malaria": 28,
        "Dengue": 24,
        "Typhoid": 18,
        "COVID-19": 15,
        "Others": 15
    }
}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/triage')
def triage():
    return render_template('triage.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=HEALTH_DATA)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json
    symptoms = data.get('symptoms', [])
    age = int(data.get('age', 30))
    duration = data.get('duration', '1-2 days')
    additional = data.get('additional', '')
    
    if not symptoms:
        return jsonify({"error": "Please provide at least one symptom"}), 400
    
    result = analyze_symptoms(symptoms, age, duration, additional)
    return jsonify(result)

@app.route('/api/health-data')
def health_data():
    return jsonify(HEALTH_DATA)


# ─── Medicine Suggestions ──────────────────────────────────────────────────────
MEDICINE_SUGGESTIONS = {
    "Common Cold": ["Paracetamol (500mg)", "Vitamin C supplements", "Steam inhalation", "Antihistamine (if runny nose)"],
    "Flu": ["Paracetamol (500mg) every 6 hrs", "Rest and fluids", "ORS if sweating heavily", "Consult doctor for antivirals"],
    "Malaria": ["⚠️ Prescription needed - visit doctor immediately", "Do NOT self-medicate with chloroquine without test"],
    "Dengue": ["Paracetamol ONLY (avoid ibuprofen/aspirin)", "ORS every hour", "Platelet monitoring required"],
    "Migraine": ["Ibuprofen 400mg or Paracetamol", "Rest in dark quiet room", "Cold compress on head"],
    "Gastroenteritis": ["ORS after every loose motion", "Zinc tablets (10 days for children)", "Avoid dairy temporarily"],
    "Food Poisoning": ["ORS every 15-20 mins", "Activated charcoal (if available)", "Avoid solid food for 6 hours"],
    "Asthma": ["Use prescribed inhaler immediately", "Sit upright, breathe slowly", "Avoid triggers"],
    "Allergy": ["Cetirizine 10mg (antihistamine)", "Avoid allergen", "Calamine lotion for skin rash"],
    "Vertigo": ["Betahistine (consult pharmacist)", "Rest, avoid sudden movements", "Ginger tea may help"],
    "Anemia": ["Iron + Folic acid supplements", "Eat iron-rich foods (spinach, lentils)", "Vitamin C with iron for absorption"],
}

# ─── Nearby Hospitals (Mock data for AP regions) ────────────────────────────────
HOSPITALS = {
    "anantapur": [
        {"name": "Government General Hospital Anantapur", "type": "Government", "distance": "2.1 km", "phone": "08554-272233", "emergency": True},
        {"name": "Srinivasa Nursing Home", "type": "Private", "distance": "3.4 km", "phone": "08554-275566", "emergency": True},
        {"name": "PHC Anantapur North", "type": "PHC", "distance": "1.2 km", "phone": "08554-277788", "emergency": False},
    ],
    "kurnool": [
        {"name": "Government General Hospital Kurnool", "type": "Government", "distance": "1.8 km", "phone": "08518-222444", "emergency": True},
        {"name": "Raghavendra Hospital", "type": "Private", "distance": "4.2 km", "phone": "08518-226688", "emergency": True},
    ],
    "default": [
        {"name": "Nearest Government Hospital", "type": "Government", "distance": "Varies", "phone": "104 (Health Helpline)", "emergency": True},
        {"name": "Call Health Helpline", "type": "Helpline", "distance": "—", "phone": "104", "emergency": True},
        {"name": "Emergency Services", "type": "Emergency", "distance": "—", "phone": "108", "emergency": True},
    ]
}

# ─── Patient History (in-memory store) ─────────────────────────────────────────
patient_history = []

# ─── Outbreak Alerts ───────────────────────────────────────────────────────────
OUTBREAK_ALERTS = [
    {"region": "Kadapa", "disease": "Malaria", "level": "RED", "cases_7days": 47, "message": "Active outbreak - avoid stagnant water areas"},
    {"region": "Anantapur", "disease": "Dengue", "level": "ORANGE", "cases_7days": 28, "message": "Rising cases - use mosquito repellent"},
    {"region": "Nellore", "disease": "Cholera", "level": "ORANGE", "cases_7days": 19, "message": "Water contamination suspected - boil water before drinking"},
    {"region": "Vizag", "disease": "COVID-19", "level": "YELLOW", "cases_7days": 12, "message": "Mild uptick - masks recommended in crowded spaces"},
]

# ─── Hindi/Telugu Translations ─────────────────────────────────────────────────
TRANSLATIONS = {
    "te": {
        "emergency": "అత్యవసర పరిస్థితి",
        "high": "అధిక ప్రమాదం",
        "moderate": "మోస్తరు ప్రమాదం",
        "low": "తక్కువ ప్రమాదం",
        "call_108": "108కి వెంటనే కాల్ చేయండి",
        "visit_today": "ఈరోజే ఆసుపత్రికి వెళ్ళండి",
        "visit_soon": "24-48 గంటల్లో క్లినిక్‌కు వెళ్ళండి",
        "rest": "విశ్రాంతి తీసుకోండి, నీళ్ళు ఎక్కువగా తాగండి",
    },
    "hi": {
        "emergency": "आपातकालीन स्थिति",
        "high": "उच्च जोखिम",
        "moderate": "मध्यम जोखिम",
        "low": "कम जोखिम",
        "call_108": "तुरंत 108 पर कॉल करें",
        "visit_today": "आज ही अस्पताल जाएं",
        "visit_soon": "24-48 घंटे में क्लिनिक जाएं",
        "rest": "आराम करें और खूब पानी पिएं",
    }
}

@app.route('/hospitals')
def hospitals():
    return render_template('hospitals.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/bmi')
def bmi():
    return render_template('bmi.html')

@app.route('/api/hospitals')
def get_hospitals():
    region = request.args.get('region', 'default').lower()
    data = HOSPITALS.get(region, HOSPITALS['default'])
    return jsonify(data)

@app.route('/api/medicines')
def get_medicines():
    condition = request.args.get('condition', '')
    suggestions = MEDICINE_SUGGESTIONS.get(condition, ["Consult a doctor for appropriate medication"])
    return jsonify({"condition": condition, "medicines": suggestions})

@app.route('/api/outbreak-alerts')
def outbreak_alerts():
    return jsonify(OUTBREAK_ALERTS)

@app.route('/api/save-history', methods=['POST'])
def save_history():
    data = request.json
    data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    data['id'] = len(patient_history) + 1
    patient_history.append(data)
    return jsonify({"success": True, "id": data['id']})

@app.route('/api/get-history')
def get_history():
    return jsonify(patient_history[-10:])  # last 10 records

@app.route('/api/translate')
def translate():
    lang = request.args.get('lang', 'te')
    return jsonify(TRANSLATIONS.get(lang, TRANSLATIONS['te']))

@app.route('/api/bmi', methods=['POST'])
def calculate_bmi():
    data = request.json
    weight = float(data.get('weight', 0))
    height_cm = float(data.get('height', 0))
    age = int(data.get('age', 25))
    
    if weight <= 0 or height_cm <= 0:
        return jsonify({"error": "Invalid values"}), 400
    
    height_m = height_cm / 100
    bmi = round(weight / (height_m ** 2), 1)
    
    if bmi < 18.5:
        category = "Underweight"
        color = "#f59e0b"
        advice = ["Increase calorie intake with nutritious food", "Eat iron-rich foods (lentils, spinach)", "Consult doctor to rule out malnutrition or anemia", "Add protein: eggs, milk, pulses"]
        risk = "Risk: Anemia, Malnutrition, Weak immunity"
    elif bmi < 25:
        category = "Normal Weight"
        color = "#16a34a"
        advice = ["Maintain current healthy lifestyle", "Exercise 30 mins daily", "Balanced diet with fruits and vegetables", "Annual health checkup recommended"]
        risk = "Low health risk - Keep it up!"
    elif bmi < 30:
        category = "Overweight"
        color = "#ea580c"
        advice = ["Reduce oil and sugar intake", "Walk 45 mins daily", "Avoid processed/junk food", "Monitor blood pressure and sugar levels"]
        risk = "Risk: Diabetes, Hypertension, Heart Disease"
    else:
        category = "Obese"
        color = "#dc2626"
        advice = ["Consult doctor for weight management plan", "Strict diet control needed", "Regular exercise under guidance", "Check for diabetes and BP regularly"]
        risk = "High Risk: Diabetes, Heart Attack, Joint Problems"
    
    ideal_min = round(18.5 * (height_m ** 2), 1)
    ideal_max = round(24.9 * (height_m ** 2), 1)
    
    return jsonify({
        "bmi": bmi,
        "category": category,
        "color": color,
        "advice": advice,
        "risk": risk,
        "ideal_weight_range": f"{ideal_min} - {ideal_max} kg"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# ─────────────────────────────────────────────────────────────────────────────
# NEW FEATURES
# ─────────────────────────────────────────────────────────────────────────────

# AI Health Chatbot KB
CHATBOT_KB = {
    "malaria": {"answer": "Malaria is caused by Plasmodium parasites via mosquito bites. Symptoms: high fever, chills, sweating, headache. Prevention: mosquito nets, repellent, eliminate stagnant water. Treatment requires prescription — visit doctor immediately.", "hindi": "मलेरिया मच्छर के काटने से होता है। लक्षण: तेज बुखार, ठंड। तुरंत डॉक्टर से मिलें।", "telugu": "మలేరియా దోమ కాటు వల్ల వస్తుంది. వెంటనే డాక్టర్‌ని సంప్రదించండి."},
    "dengue": {"answer": "Dengue is spread by Aedes mosquitoes. Symptoms: sudden high fever, rash, severe joint pain. Warning: bleeding or vomiting blood = go to ER. Monitor platelet count.", "hindi": "डेंगू में तेज बुखार, दाने होते हैं। प्लेटलेट काउंट जांचें।", "telugu": "డెంగ్యూ: అకస్మాత్ జ్వరం, దద్దురు. ప్లేట్లెట్ కౌంట్ తనిఖీ చేయండి."},
    "diabetes": {"answer": "Diabetes = high blood sugar. Symptoms: frequent urination, thirst, blurred vision. Management: diet, exercise, medication, regular sugar monitoring.", "hindi": "मधुमेह में रक्त शर्करा अधिक होती है। व्यायाम और सही खान-पान जरूरी।", "telugu": "మధుమేహం: రక్తంలో చక్కెర అధికం. ఆహార నియంత్రణ, వ్యాయామం అవసరం."},
    "hypertension": {"answer": "High BP (above 140/90) is a silent killer. Reduce salt, exercise daily, take medications. Check BP regularly.", "hindi": "140/90 से अधिक BP खतरनाक है। नमक कम करें, व्यायाम करें।", "telugu": "140/90 కంటే ఎక్కువ BP ప్రమాదకరం. ఉప్పు తగ్గించండి."},
    "tuberculosis": {"answer": "TB = bacterial lung infection. Symptoms: cough 2+ weeks, blood in sputum, night sweats. Free DOTS treatment at government hospitals.", "hindi": "टीबी: 2+ सप्ताह खांसी, रात को पसीना। सरकारी अस्पताल में मुफ्त इलाज।", "telugu": "క్షయ: 2+ వారాలు దగ్గు. ప్రభుత్వ ఆసుపత్రిలో ఉచిత DOTS చికిత్స."},
    "anemia": {"answer": "Anemia = low iron/hemoglobin. Symptoms: fatigue, pale skin, dizziness. Eat iron-rich foods: spinach, lentils, jaggery. Take iron+folic acid tablets.", "hindi": "एनीमिया में आयरन कम होता है। पालक, दाल खाएं, आयरन की गोलियां लें।", "telugu": "రక్తహీనత: పాలకూర, పప్పులు తినండి. ఇనుము మాత్రలు వాడండి."},
    "covid": {"answer": "COVID-19: fever, cough, loss of smell/taste, breathlessness. Isolate if infected. Vaccinate. Emergency if oxygen below 94%.", "hindi": "COVID-19: बुखार, खांसी, स्वाद/गंध खोना। टीका लगवाएं।", "telugu": "COVID-19: జ్వరం, దగ్గు, వాసన కోల్పోవడం. టీకా వేయించుకోండి."},
    "cholera": {"answer": "Cholera = waterborne disease. Symptoms: sudden watery diarrhea, vomiting, dehydration. Give ORS immediately. Boil drinking water.", "hindi": "हैजा जल जनित रोग है। ORS पिएं, पानी उबालें।", "telugu": "కలరా: నీళ్ళ విరేచనాలు. ORS తీసుకోండి, నీళ్ళు మరిగించండి."},
    "fever": {"answer": "Fever above 38C: take paracetamol, cool compress, drink fluids. See doctor if fever persists 3+ days or exceeds 103F.", "hindi": "38C से अधिक बुखार: पैरासिटामोल लें, ठंडी पट्टी लगाएं।", "telugu": "38C కంటే జ్వరం: పారాసిటమాల్ తీసుకోండి."},
    "default": {"answer": "I can help with malaria, dengue, diabetes, TB, fever, anemia, COVID, cholera, hypertension. Please type your symptom or disease name.", "hindi": "मैं आपका AI स्वास्थ्य सहायक हूं। बीमारी का नाम या लक्षण टाइप करें।", "telugu": "నేను మీ AI ఆరోగ్య సహాయకుడిని. వ్యాధి పేరు లేదా లక్షణం టైప్ చేయండి."},
}

def chatbot_response(message, lang='en'):
    msg = message.lower()
    matched = None
    for key in CHATBOT_KB:
        if key in msg:
            matched = CHATBOT_KB[key]
            break
    if not matched:
        matched = CHATBOT_KB['default']
    if lang == 'hi':
        return matched.get('hindi', matched['answer'])
    elif lang == 'te':
        return matched.get('telugu', matched['answer'])
    return matched['answer']

# Doctors for Telemedicine
appointments = []
DOCTORS = [
    {"id": 1, "name": "Dr. Ramesh Kumar", "specialty": "General Physician", "available": ["9:00 AM", "10:00 AM", "11:00 AM", "2:00 PM", "3:00 PM"], "location": "Anantapur PHC"},
    {"id": 2, "name": "Dr. Priya Sharma", "specialty": "Pediatrician", "available": ["9:30 AM", "10:30 AM", "2:30 PM", "4:00 PM"], "location": "Kurnool District Hospital"},
    {"id": 3, "name": "Dr. Suresh Reddy", "specialty": "Internal Medicine", "available": ["10:00 AM", "11:30 AM", "3:00 PM", "4:30 PM"], "location": "Nellore General Hospital"},
    {"id": 4, "name": "Dr. Lakshmi Devi", "specialty": "Gynecologist", "available": ["9:00 AM", "11:00 AM", "2:00 PM"], "location": "Kadapa Womens Hospital"},
    {"id": 5, "name": "Dr. Venkat Rao", "specialty": "Cardiologist", "available": ["10:00 AM", "3:00 PM"], "location": "Vizag Telemedicine Center"},
]

def predict_outbreak_risk(region, season, sanitation, water_source, vaccination_rate):
    season_monsoon = season in ['monsoon', 'post-monsoon']
    poor_san = sanitation == 'poor'
    bad_water = water_source in ['river', 'pond', 'unfiltered']
    low_vax = int(vaccination_rate) < 60
    risks = {}
    base = {"Malaria": 10, "Dengue": 10, "Cholera": 20, "Typhoid": 10, "COVID": 20}
    for d, b in base.items():
        s = b
        if season_monsoon: s += 25 if d in ['Malaria','Dengue'] else 15
        if poor_san: s += 20 if d in ['Cholera','Typhoid'] else 5
        if bad_water: s += 30 if d in ['Cholera','Typhoid'] else 5
        if low_vax and d == 'COVID': s += 25
        s = min(s, 95)
        risks[d] = {'score': s, 'level': 'HIGH' if s >= 60 else 'MEDIUM' if s >= 35 else 'LOW'}
    return sorted(risks.items(), key=lambda x: x[1]['score'], reverse=True)

def personal_risk_score(age, gender, smoking, alcohol, exercise, diet, bp_history, diabetes_history, family_history):
    r = {"Heart Disease": 10, "Diabetes Type 2": 10, "Hypertension": 10, "Anemia": 5, "Lung Disease": 5, "Liver Disease": 5}
    if age > 45: r["Heart Disease"] += 20; r["Hypertension"] += 15
    if age > 60: r["Diabetes Type 2"] += 10; r["Heart Disease"] += 10
    if smoking: r["Lung Disease"] += 35; r["Heart Disease"] += 25; r["Hypertension"] += 15
    if alcohol: r["Liver Disease"] += 30; r["Heart Disease"] += 10
    if exercise == 'none': r["Heart Disease"] += 15; r["Diabetes Type 2"] += 20; r["Hypertension"] += 10
    if diet == 'poor': r["Diabetes Type 2"] += 15; r["Anemia"] += 10; r["Hypertension"] += 10
    if bp_history: r["Heart Disease"] += 20; r["Hypertension"] += 25
    if diabetes_history: r["Diabetes Type 2"] += 30; r["Heart Disease"] += 15
    if family_history: r["Heart Disease"] += 15; r["Diabetes Type 2"] += 15
    if gender == 'female' and age < 50: r["Anemia"] += 20
    return {k: min(v, 95) for k, v in sorted(r.items(), key=lambda x: x[1], reverse=True)}

HEALTH_EDUCATION = [
    {"id": 1, "title": "Preventing Malaria", "category": "Prevention", "icon": "🦟", "color": "#dc2626", "summary": "Simple steps to prevent mosquito-borne malaria.", "content": "Use mosquito nets while sleeping. Eliminate stagnant water near your home. Apply repellent. Wear full-sleeve clothes at dusk. Early symptoms: fever with chills — see doctor immediately.", "hindi": "मलेरिया से बचाव: मच्छरदानी उपयोग करें, रुके पानी को हटाएं।", "telugu": "మలేరియా నివారణ: దోమతెర ఉపయోగించండి, నిల్వ నీటిని తొలగించండి."},
    {"id": 2, "title": "Clean Water & Sanitation", "category": "Prevention", "icon": "💧", "color": "#0ea5e9", "summary": "Safe water practices to prevent waterborne diseases.", "content": "Always boil drinking water. Use ORS for diarrhea. Wash hands before eating. Store water in covered containers. Use toilets — open defecation spreads disease.", "hindi": "पीने का पानी उबालें, हाथ धोएं, शौचालय का उपयोग करें।", "telugu": "తాగునీటిని మరిగించండి, చేతులు కడుక్కోండి."},
    {"id": 3, "title": "Child Nutrition & Vaccination", "category": "Children", "icon": "👶", "color": "#16a34a", "summary": "Keep children healthy with nutrition and vaccines.", "content": "Breastfeed exclusively 6 months. Ensure all vaccines on time (BCG, Polio, DPT, Measles). Give iron supplements. Visit ASHA worker monthly.", "hindi": "6 माह स्तनपान कराएं, समय पर टीके लगवाएं।", "telugu": "6 నెలలు తల్లి పాలు పట్టించండి, టీకాలు వేయించండి."},
    {"id": 4, "title": "Maternal Health", "category": "Women", "icon": "🤱", "color": "#7c3aed", "summary": "Essential care during pregnancy and after delivery.", "content": "Register pregnancy at PHC. Take 4 antenatal checkups. Take iron+folic acid daily. Deliver at hospital. Watch for: bleeding, severe headache, reduced fetal movement.", "hindi": "गर्भावस्था में 4 जांच जरूरी, आयरन की गोलियां लें, अस्पताल में प्रसव।", "telugu": "గర్భం నమోదు చేయించుకోండి, 4 తనిఖీలు తప్పనిసరి."},
    {"id": 5, "title": "Managing Diabetes", "category": "Chronic Disease", "icon": "🩸", "color": "#ea580c", "summary": "Control blood sugar naturally and with medication.", "content": "Test blood sugar regularly. Avoid white rice, sugar, maida. Walk 30 mins daily. Never skip medicines. Low sugar warning: sweating, trembling — eat sugar immediately.", "hindi": "नियमित रक्त शर्करा जांच, सही खान-पान, दवाइयां नियमित लें।", "telugu": "క్రమంగా రక్తంలో చక్కెర పరీక్షించండి, మందులు వదలకండి."},
    {"id": 6, "title": "Mental Health Awareness", "category": "Mental Health", "icon": "🧠", "color": "#0f766e", "summary": "Recognize depression and anxiety in rural communities.", "content": "Signs of depression: sadness, loss of interest, sleep problems. Talk to trusted person. Call iCall: 9152987821. Avoid alcohol for stress — it worsens mental health.", "hindi": "अवसाद: उदासी, रुचि कम होना। iCall: 9152987821", "telugu": "నిరాశ లక్షణాలు: దుఃఖం, ఆసక్తి తగ్గడం. iCall: 9152987821"},
]

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/telemedicine')
def telemedicine():
    return render_template('telemedicine.html')

@app.route('/outbreak-predictor')
def outbreak_predictor():
    return render_template('outbreak_predictor.html')

@app.route('/health-risk')
def health_risk():
    return render_template('health_risk.html')

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/frontline')
def frontline():
    return render_template('frontline.html')

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.json
    response = chatbot_response(data.get('message', ''), data.get('lang', 'en'))
    return jsonify({"response": response})

@app.route('/api/doctors')
def get_doctors():
    return jsonify(DOCTORS)

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    data['id'] = len(appointments) + 1
    data['status'] = 'Confirmed'
    data['booking_time'] = datetime.now().strftime("%Y-%m-%d %H:%M")
    appointments.append(data)
    return jsonify({"success": True, "appointment": data})

@app.route('/api/appointments')
def get_appointments():
    return jsonify(appointments)

@app.route('/api/predict-outbreak', methods=['POST'])
def predict_outbreak():
    d = request.json
    risks = predict_outbreak_risk(d.get('region',''), d.get('season','summer'), d.get('sanitation','moderate'), d.get('water_source','tap'), d.get('vaccination_rate', 70))
    return jsonify([{"disease": dis, "score": r["score"], "level": r["level"]} for dis, r in risks])

@app.route('/api/personal-risk', methods=['POST'])
def personal_risk():
    d = request.json
    risks = personal_risk_score(int(d.get('age',30)), d.get('gender','male'), d.get('smoking',False), d.get('alcohol',False), d.get('exercise','moderate'), d.get('diet','moderate'), d.get('bp_history',False), d.get('diabetes_history',False), d.get('family_history',False))
    overall = round(sum(risks.values()) / len(risks))
    level = 'HIGH' if overall >= 50 else 'MEDIUM' if overall >= 30 else 'LOW'
    return jsonify({"risks": [{"disease": k, "score": v} for k, v in risks.items()], "overall": overall, "level": level})

@app.route('/api/education')
def get_education():
    category = request.args.get('category', '')
    lang = request.args.get('lang', 'en')
    data = [e.copy() for e in HEALTH_EDUCATION]
    if category:
        data = [e for e in data if e['category'] == category]
    for item in data:
        if lang == 'hi': item['display_content'] = item.get('hindi', item['content'])
        elif lang == 'te': item['display_content'] = item.get('telugu', item['content'])
        else: item['display_content'] = item['content']
    return jsonify(data)

@app.route('/api/frontline-summary')
def frontline_summary():
    region = request.args.get('region', 'Anantapur')
    region_data = next((r for r in HEALTH_DATA['regions'] if r['name'] == region), HEALTH_DATA['regions'][0])
    alert = next((a for a in OUTBREAK_ALERTS if a['region'] == region), None)
    return jsonify({"region": region, "active_cases": region_data['cases'], "dominant_disease": region_data['disease'], "risk_level": region_data['risk'], "alert": alert, "today_visits": random.randint(8,24), "pending_reports": random.randint(2,8), "referrals_today": random.randint(1,5), "patients_due_followup": random.randint(3,12)})

@app.route('/voice')
def voice():
    return render_template('voice.html')

