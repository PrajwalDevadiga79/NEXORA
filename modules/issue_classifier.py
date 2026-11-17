"""
NyayaSathi - Legal Issue Classifier Module
Identifies the legal domain, urgency level (RED/YELLOW/GREEN), and jurisdiction
from natural language descriptions across English, Hindi, and Kannada.
"""

import re
from typing import Dict, Any

CATEGORY_KEYWORDS = {
    "criminal_offences": {
        "en": [
            "thieves", "thief", "robbery", "robbed", "theft", "stole gold", "stole my", "stolen gold",
            "knife", "weapon", "attacked", "stabbed", "assault", "assaulted", "physical assault",
            "injured", "injuries", "injury", "bleeding", "hospital", "break in", "broken into",
            "entered my house", "trespassed into house", "house breaking", "burglary", "dacoity",
            "fir", "police complaint", "threat to life", "threatened to kill", "extortion", "beaten up",
            "loot", "looted"
        ],
        "hi": [
            "चोर", "चोरी", "डकैती", "लूट", "लूटपाट", "चाकू", "हथियार", "हमला", "चाकू मारा",
            "चोट", "घायल", "अस्पताल", "घर में घुसे", "ताला तोड़ा", "मारपीट", "एफआईआर",
            "पुलिस शिकायत", "जान से मारने की धमकी"
        ],
        "kn": [
            "ಕಳ್ಳರು", "ಕಳ್ಳತನ", "ದರೋಡೆ", "ಚಿನ್ನ ಕಳ್ಳತನ", "ಚಾಕು", "ಆಯುಧ", "ದಾಳಿ", "ಹಲ್ಲೆ",
            "ಗಾಯ", "ರಕ್ತ", "ಆಸ್ಪತ್ರೆ", "ಮನೆಗೆ ನುಗ್ಗಿದ್ದಾರೆ", "ಬೀಗ ಒಡೆದು", "ಎಫ್‌ಐಆರ್", "ಪೊಲೀಸ್ ದೂರು"
        ]
    },
    "cyber_fraud": {
        "en": [
            "upi", "fraud", "scam", "lost money", "bank", "otp", "phishing", "cyber", "hacked",
            "google pay", "phonepe", "paytm", "unauthorized", "deducted", "stolen", "fake call",
            "lottery", "qr code", "apk", "cheated", "account debited", "transfer", "credited",
            "online fraud", "internet banking", "sms fraud", "social media hack", "whatsapp fraud",
            "loan app", "credit card fraud", "1930"
        ],
        "hi": [
            "यूपीआई", "धोखाधड़ी", "फ्रॉड", "पैसे कट", "बैंक", "ओटीपी", "साइबर", "हैक",
            "गूगल पे", "फोनपे", "पेटीएम", "अनधिकृत", "चोरी", "नकली कॉल", "लॉटरी", "क्यूआर कोड",
            "पैसे चले गए", "खाते से कट", "ऑनलाइन धोखा", "फर्जी लिंक"
        ],
        "kn": [
            "ಯುಪಿಐ", "ವಂಚನೆ", "ಫ್ರಾಡ್", "ಹಣ ಕಳೆದುಹೋಯಿತು", "ಬ್ಯಾಂಕ್", "ಒಟಿಪಿ", "ಸೈಬರ್",
            "ಗೂಗಲ್ ಪೇ", "ಫೋನ್‌ಪೇ", "ಪೇಟಿಎಂ", "ಹಣ ಕಡಿತ", "ನಕಲಿ ಕರೆ", "ಖಾತೆಯಿಂದ ಕಡಿತ", "ಮೋಸ"
        ]
    },
    "tenant_landlord": {
        "en": [
            "tenant", "landlord", "rent", "deposit", "eviction", "agreement", "lease",
            "owner", "vacate", "security deposit", "rental flat", "rented apartment",
            "electricity cut", "water cut", "notice to vacate", "broker", "lockout", "evict", "pg"
        ],
        "hi": [
            "किरायेदार", "मकान मालिक", "किराया", "डिपॉजिट", "अमानत राशि", "खाली करने का नोटिस",
            "किरायानामा", "एग्रीमेंट", "बिजली काट", "पानी बंद", "बेदखली"
        ],
        "kn": [
            "ಬಾಡಿಗೆದಾರ", "ಮನೆ ಮಾಲೀಕ", "ಬಾಡಿಗೆ", "ಮುಂಗಡ", "ಅಡ್ವಾನ್ಸ್", "ಖಾಲಿ ಮಾಡಲು",
            "ಕರಾರು", "ಅಗ್ರಿಮೆಂಟ್", "ವಿದ್ಯುತ್ ಕಡಿತ", "ನೀರು ನಿಲ್ಲಿಸಿದ್ದಾರೆ"
        ]
    },
    "consumer_complaint": {
        "en": [
            "defective", "warranty", "consumer", "refund", "replacement",
            "amazon", "flipkart", "repair", "service center", "seller",
            "guarantee", "not working", "online shopping", "cancelled flight",
            "damaged item", "insurance claim", "overcharged", "defective item"
        ],
        "hi": [
            "उपभोक्ता", "खराब सामान", "वारंटी", "रिफंड", "वापसी", "अमेज़न", "फ्लिपकार्ट",
            "दोषपूर्ण", "मरम्मत", "सर्विस सेंटर", "दुकानदार", "काम नहीं कर रहा"
        ],
        "kn": [
            "ಗ್ರಾಹಕ", "ದೋಷಯುಕ್ತ", "ವಾರಂಟಿ", "ರಿಫಂಡ್", "ಹಣ ವಾಪಸ್", "ಅಮೆಜಾನ್", "ಫ್ಲಿಪ್‌ಕಾರ್ಟ್",
            "ಕೆಲಸ ಮಾಡುತ್ತಿಲ್ಲ", "ಹಾಳಾದ ವಸ್ತು", "ಸರ್ವೀಸ್ ಸೆಂಟರ್", "ವ್ಯಾಪಾರಿ"
        ]
    },
    "employment_salary": {
        "en": [
            "salary", "employer", "unpaid salary", "fired", "terminated", "notice pay",
            "resignation", "full and final", "pf", "provident fund", "gratuity", "wage",
            "boss", "company not paying", "wrongful termination", "severance"
        ],
        "hi": [
            "वेतन", "सैलरी", "तनख्वाह", "नौकरी से निकाला", "बकाया वेतन", "मालिक पैसे नहीं दे रहा",
            "कंपनी", "इस्तीफा", "पीएफ", "पीएफ का पैसा", "ग्रेच्युटी"
        ],
        "kn": [
            "ಸಂಬಳ", "ವೇತನ", "ಕೆಲಸದಿಂದ ತೆಗೆದುಹಾಕಲಾಗಿದೆ", "ಮಾಲೀಕ ಸಂಬಳ ನೀಡುತ್ತಿಲ್ಲ",
            "ಕಂಪನಿ", "ರಾಜೀನಾಮೆ", "ಪಿಎಫ್", "ಉದ್ಯೋಗ"
        ]
    },
    "property_disputes": {
        "en": [
            "property", "land", "encroachment", "boundary", "trespass", "plot",
            "sale deed", "registry", "patta", "khata", "illegal possession", "stay order"
        ],
        "hi": [
            "संपत्ति", "जमीन", "कब्जा", "अवैध कब्जा", "प्लॉट", "रजिस्ट्री", "बिक्री पत्र",
            "पटवारी", "खाता", "स्टे ऑर्डर", "अतिक्रमण"
        ],
        "kn": [
            "ಆಸ್ತಿ", "ಭೂಮಿ", "ಅಕ್ರಮ ಒತ್ತುವರಿ", "ಖಾತಾ", "ಕ್ರಯಪತ್ರ", "ಪ್ಲಾಟ್",
            "ನೋಂದಣಿ", "ಜಮೀನು", "ಸ್ಟೇ ಆರ್ಡರ್"
        ]
    },
    "family_domestic": {
        "en": [
            "husband", "wife", "domestic violence", "dowry", "maintenance", "custody",
            "beating", "beats", "beat", "abuse", "abusive", "divorce", "harassment by in-laws", "alimony", "498a"
        ],
        "hi": [
            "घरेलू हिंसा", "पति", "पत्नी", "दहेज", "खर्चा", "गुजारा भत्ता", "तलाक",
            "मारपीट", "ससुराल वाले", "कस्टडी"
        ],
        "kn": [
            "ಕೌಟುಂಬಿಕ ದೌರ್ಜನ್ಯ", "ಗಂಡ", "ಹೆಂಡತಿ", "ವರದಕ್ಷಿಣೆ", "ಜೀವನಾಂಶ", "ವಿಚ್ಛೇದನ",
            "ಹಿಂಸೆ", "ಮಕ್ಕಳ ರಕ್ಷಣೆ"
        ]
    }
}

MIN_CONFIDENCE_THRESHOLD = 2.0


def detect_language(text: str) -> str:
    kannada_chars = len(re.findall(r"[\u0C80-\u0CFF]", text))
    hindi_chars = len(re.findall(r"[\u0900-\u097F]", text))

    if kannada_chars > 3:
        return "kn"
    elif hindi_chars > 3:
        return "hi"
    return "en"


def classify_legal_issue(text: str, user_selected_category: str = "auto") -> Dict[str, Any]:
    text_lower = text.lower()
    scores = {cat: 0 for cat in CATEGORY_KEYWORDS}

    for cat, lang_dict in CATEGORY_KEYWORDS.items():
        for lang, words in lang_dict.items():
            for w in words:
                if w in text_lower:
                    weight = 2.0 if " " in w or w in ["1930", "upi", "deposit", "evict", "warranty", "refund", "salary", "dowry", "knife", "robbery", "attacked", "injured", "thieves", "weapon"] else 1.0
                    scores[cat] += weight

    detected_lang = detect_language(text)

    if user_selected_category in scores or user_selected_category == "general":
        best_cat = user_selected_category
        confidence = 0.95
    else:
        best_cat = max(scores, key=scores.get)
        highest_score = scores[best_cat]
        confidence = min(0.95, 0.45 + (highest_score * 0.15)) if highest_score > 0 else 0.30

        if highest_score < MIN_CONFIDENCE_THRESHOLD:
            best_cat = "general"
            confidence = 0.40

    category_metadata = {
        "criminal_offences": {
            "name": "Criminal Offences, Robbery & Physical Assault",
            "kannada_name": "ಅಪರಾಧ ಕೃತ್ಯಗಳು, ದರೋಡೆ ಮತ್ತು ದೈಹಿಕ ಹಲ್ಲೆ",
            "hindi_name": "आपराधिक अपराध, डकैती एवं शारीरिक हमला",
            "classification": "Cognizable Criminal Offences (BNS & BNSS, 2023)",
            "urgency": "RED",
            "urgency_badge": "🚨 RED ALERT: Immediate Safety, Emergency Medical Care (MLC) & FIR Required",
            "urgency_reason": "Cognizable violent crime with physical injury and theft. Immediate medical examination (MLC) and FIR registration under BNSS are vital.",
            "primary_authority": "Local Police Station (112) / Govt Hospital (MLC) / Judicial Magistrate"
        },
        "cyber_fraud": {
            "name": "UPI & Cyber Financial Fraud",
            "kannada_name": "ಯುಪಿಐ ಮತ್ತು ಸೈಬರ್ ವಂಚನೆ",
            "hindi_name": "यूपीआई और साइबर वित्तीय धोखाधड़ी",
            "classification": "Criminal & Regulatory (IT Act & Banking Law)",
            "urgency": "RED",
            "urgency_badge": "🚨 RED ALERT: Immediate Action Required (< 24 Hours Golden Hour)",
            "urgency_reason": "Immediate reporting to 1930 is vital to freeze the beneficiary account before funds are siphoned.",
            "primary_authority": "National Cyber Crime Portal (1930 / cybercrime.gov.in)"
        },
        "family_domestic": {
            "name": "Family & Domestic Disputes",
            "kannada_name": "ಕುಟುಂಬ ಮತ್ತು ಕೌಟುಂಬಿಕ ವಿವಾದಗಳು",
            "hindi_name": "पारिवारिक एवं घरेलू विवाद",
            "classification": "Civil, Family & Criminal Law",
            "urgency": "RED",
            "urgency_badge": "🚨 RED ALERT: Safety & Immediate Protection Orders",
            "urgency_reason": "Physical harm, domestic cruelty, or urgent maintenance orders require immediate intervention.",
            "primary_authority": "National Women Helpline (181) / Police (112) / Magistrate Court"
        },
        "tenant_landlord": {
            "name": "Tenant & Landlord Disputes",
            "kannada_name": "ಬಾಡಿಗೆದಾರ ಮತ್ತು ಮನೆ ಮಾಲೀಕರ ವಿವಾದಗಳು",
            "hindi_name": "किरायेदार और मकान मालिक विवाद",
            "classification": "Civil & Contractual (Tenancy & Property Law)",
            "urgency": "YELLOW",
            "urgency_badge": "⚠️ YELLOW: Important Action Recommended (Notice & Mediation)",
            "urgency_reason": "Statutory notice periods apply. Prevent utility disconnections or unlawful eviction via Rent Authority.",
            "primary_authority": "Rent Authority / Rent Court / Lok Adalat Mediation"
        },
        "consumer_complaint": {
            "name": "Consumer Complaints & Defective Goods/Services",
            "kannada_name": "ಗ್ರಾಹಕರ ದೂರುಗಳು ಮತ್ತು ದೋಷಯುಕ್ತ ಸೇವೆಗಳು",
            "hindi_name": "उपभोक्ता शिकायतें एवं दोषपूर्ण सामान/सेवाएं",
            "classification": "Civil & Consumer Protection Law",
            "urgency": "YELLOW",
            "urgency_badge": "⚠️ YELLOW: Action Recommended (2-Year Limitation Period)",
            "urgency_reason": "Lodge grievance on NCH 1915 or e-Daakhil with purchase invoice and warranty documentation.",
            "primary_authority": "National Consumer Helpline (1915 / e-Daakhil Portal)"
        },
        "employment_salary": {
            "name": "Employment & Unpaid Salary Disputes",
            "kannada_name": "ಉದ್ಯೋಗ ಮತ್ತು ಬಾಕಿ ಸಂಬಳ ವಿವಾದಗಳು",
            "hindi_name": "रोजगार एवं बकाया वेतन विवाद",
            "classification": "Labor & Employment Law",
            "urgency": "YELLOW",
            "urgency_badge": "⚠️ YELLOW: Statutory Recovery of Wages",
            "urgency_reason": "Recovery petition before Labour Commissioner under Payment of Wages Act.",
            "primary_authority": "Labour Commissioner / Shram Suvidha Portal"
        },
        "property_disputes": {
            "name": "Property & Land Disputes",
            "kannada_name": "ಆಸ್ತಿ ಮತ್ತು ಭೂಮಿ ವಿವಾದಗಳು",
            "hindi_name": "संपत्ति एवं भूमि विवाद",
            "classification": "Civil & Criminal Property Law",
            "urgency": "YELLOW",
            "urgency_badge": "⚠️ YELLOW: Title Verification & Injunction Relief",
            "urgency_reason": "Risk of illegal possession or fraudulent sale requires immediate civil injunction (stay order).",
            "primary_authority": "Civil Court / Executive Magistrate (BNSS 164) / DLSA"
        },
        "general": {
            "name": "General Legal Query",
            "kannada_name": "ಸಾಮಾನ್ಯ ಕಾನೂನು ಪ್ರಶ್ನೆ",
            "hindi_name": "सामान्य कानूनी प्रश्न",
            "classification": "Indian Civil / Criminal Law",
            "urgency": "GREEN",
            "urgency_badge": "ℹ️ GREEN: Informational & Educational Guidance",
            "urgency_reason": "Explore legal provisions and options. For court proceedings, consult a qualified advocate.",
            "primary_authority": "NALSA Free Legal Aid Helpline (15100) / Local Police (112)"
        }
    }

    meta = category_metadata.get(best_cat, category_metadata["general"])

    return {
        "category_id": best_cat,
        "category_name": meta["name"],
        "kannada_name": meta["kannada_name"],
        "hindi_name": meta["hindi_name"],
        "classification": meta["classification"],
        "urgency": meta["urgency"],
        "urgency_badge": meta["urgency_badge"],
        "urgency_reason": meta["urgency_reason"],
        "primary_authority": meta["primary_authority"],
        "confidence": confidence,
        "detected_language": detected_lang,
        "scores": scores
    }
