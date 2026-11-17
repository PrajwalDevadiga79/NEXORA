"""
NyayaSathi - Action Plan Generator Module
Produces structured, chronologically sequenced, actionable steps tailored to Indian citizens
for cyber fraud, tenancy disputes, and consumer protection.
Supports English, Hindi, and Kannada localizations.
"""

from typing import Dict, List, Any


def get_action_plan(category_id: str, language: str = "en", details: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Returns step-by-step action plan cards with timeframes, legal basis, and official actions.
    """
    details = details or {}
    amount = details.get("amount", "")

    if category_id == "criminal_offences":
        return [
            {
                "step": 1,
                "title": "Seek Immediate Emergency Medical Attention & Get MLC Recorded",
                "timeframe": "Immediate (First 1-2 Hours)",
                "badge": "Critical Life Safety",
                "badge_color": "danger",
                "description": "Visit the nearest Government/District Hospital casualty. Request the medical officer to prepare a formal Medico-Legal Certificate (MLC) recording all knife wounds, bruises, and physical trauma. The MLC is conclusive forensic evidence under Bharatiya Sakshya Adhiniyam, 2023.",
                "action_link": "tel:108",
                "action_text": "Call Ambulance (108)",
                "legal_backing": "BNSS 2023 Section 53 & 184 / BSA 2023 (Medico-Legal Examination)"
            },
            {
                "step": 2,
                "title": "Report to Police Station & Lodge First Information Report (FIR)",
                "timeframe": "Within 24 Hours",
                "badge": "Mandatory Statutory FIR",
                "badge_color": "danger",
                "description": "Approach the jurisdictional police station or call 112. File a detailed written complaint specifying time, date, physical description of offenders, stolen gold jewellery details, weapons used, and injuries inflicted. If outside jurisdiction, demand registration of a 'Zero FIR'.",
                "action_link": "tel:112",
                "action_text": "Dial Police (112)",
                "legal_backing": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) Section 173"
            },
            {
                "step": 3,
                "title": "Demand Signed Copy of Registered FIR Free of Cost",
                "timeframe": "Immediately Upon Registration",
                "badge": "Statutory Right",
                "badge_color": "warning",
                "description": "Under Section 173(2) of BNSS, police officers are legally obligated to furnish an official signed copy of the FIR to the complainant immediately free of charge. Verify that appropriate sections for Robbery (BNS 309), Weapon Hurt (BNS 118), and House-breaking (BNS 331) are invoked.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "BNSS 2023 Section 173(2) (Complainant's Statutory Right to Free FIR Copy)"
            },
            {
                "step": 4,
                "title": "Preserve Crime Scene, Physical Evidence & Gold Invoices",
                "timeframe": "Before Police Inspection",
                "badge": "Evidence Integrity",
                "badge_color": "info",
                "description": "Do not clean or disturb the room where the break-in occurred until police forensics/fingerprint experts inspect. Collect photographs of injuries, CCTV camera footage from premises and neighbors, and original tax invoices/hallmark certificates for stolen gold.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "Bharatiya Sakshya Adhiniyam, 2023 (BSA) Section 61 & 63 (Electronic & Forensic Evidence)"
            },
            {
                "step": 5,
                "title": "Escalate to Superintendent of Police (SP) if FIR is Refused or Delayed",
                "timeframe": "Within 48 Hours if Inaction",
                "badge": "Remedy Against Non-Registration",
                "badge_color": "secondary",
                "description": "If the station house officer (SHO) refuses to register the FIR, send your signed complaint with MLC copy via Registered Post / Speed Post to the District Superintendent of Police (SP / DCP) under BNSS Section 173(3), or file an application before the Judicial Magistrate under BNSS Section 175(3).",
                "action_link": "",
                "action_text": "",
                "legal_backing": "BNSS 2023 Section 173(3) & Section 175(3) (Judicial Remedy)"
            },
            {
                "step": 6,
                "title": "Apply for Free Legal Aid & Victim Compensation through DLSA",
                "timeframe": "Post FIR Registration",
                "badge": "Victim Compensation",
                "badge_color": "primary",
                "description": "Approach the District Legal Services Authority (DLSA) at the district court complex or call 15100. As a victim of violent crime, you are entitled to free legal counsel and state compensation for medical expenses and loss of property under BNSS Section 396.",
                "action_link": "tel:15100",
                "action_text": "NALSA Helpline (15100)",
                "legal_backing": "BNSS 2023 Section 396 & Legal Services Authorities Act, 1987"
            }
        ]

    if category_id == "cyber_fraud":
        if language == "hi":
            return [
                {
                    "step": 1,
                    "title": "तुरंत 1930 साइबर हेल्पलाइन पर कॉल करें (गोल्डन ऑवर)",
                    "timeframe": "घटना के 2 से 24 घंटे के भीतर",
                    "badge": "अत्यंत महत्वपूर्ण",
                    "badge_color": "danger",
                    "description": "तुरंत 1930 डायल करें। अपने बैंक का नाम, खाता संख्या, लेन-देन (UTR/UPI) आईडी और धोखेबाज का मोबाइल नंबर बताएं। गृह मंत्रालय का CFCFRMS सिस्टम पैसे को आरोपी के बैंक खाते में तुरंत फ्रीज करने की प्रक्रिया शुरू करेगा।",
                    "action_link": "tel:1930",
                    "action_text": "1930 पर कॉल करें",
                    "legal_backing": "नागरिक वित्तीय साइबर धोखाधड़ी रिपोर्टिंग प्रणाली (गृह मंत्रालय, भारत सरकार)"
                },
                {
                    "step": 2,
                    "title": "अपने बैंक में लिखित विवाद/अनधिकृत लेन-देन दर्ज कराएं",
                    "timeframe": "3 कार्य दिवसों के भीतर",
                    "badge": "आरबीआई शून्य देयता",
                    "badge_color": "warning",
                    "description": "अपने बैंक शाखा में जाकर या मोबाइल बैंकिंग पर 'अनधिकृत इलेक्ट्रॉनिक लेनदेन' का औपचारिक विवाद दर्ज करें। आरबीआई परिपत्र के अनुसार, 3 दिनों के भीतर सूचित करने पर आपकी देयता शून्य हो सकती है।",
                    "action_link": "https://www.rbi.org.in",
                    "action_text": "आरबीआई दिशानिर्देश देखें",
                    "legal_backing": "RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18"
                },
                {
                    "step": 3,
                    "title": "cybercrime.gov.in पोर्टल पर औपचारिक शिकायत दर्ज करें",
                    "timeframe": "24 से 48 घंटे के भीतर",
                    "badge": "औपचारिक रिकॉर्ड",
                    "badge_color": "info",
                    "description": "राष्ट्रीय साइबर अपराध रिपोर्टिंग पोर्टल पर 'वित्तीय धोखाधड़ी' श्रेणी चुनें। बैंक स्टेटमेंट, लेन-देन का स्क्रीनशॉट और कॉल रिकॉर्ड अपलोड करें। एक्नॉलेजमेंट नंबर सुरक्षित रखें।",
                    "action_link": "https://cybercrime.gov.in",
                    "action_text": "पोर्टल खोलें",
                    "legal_backing": "सूचना प्रौद्योगिकी अधिनियम 2000 धारा 66D"
                },
                {
                    "step": 4,
                    "title": "यूपीआई पिन, कार्ड और बैंकिंग एक्सेस तुरंत ब्लॉक/बदलें",
                    "timeframe": "तुरंत",
                    "badge": "सुरक्षा कदम",
                    "badge_color": "secondary",
                    "description": "अपने संबंधित बैंक का यूपीआई पिन रीसेट करें, डेबिट/क्रेडिट कार्ड को अस्थायी रूप से हॉटलिस्ट (ब्लॉक) करें, और मोबाइल से किसी भी संदिग्ध रिमोट ऐप (जैसे AnyDesk, TeamViewer) को तुरंत अनइंस्टॉल करें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "सुरक्षा प्रोटोकॉल"
                },
                {
                    "step": 5,
                    "title": "आरबीआई ओम्बड्समैन या आईटी सचिव के समक्ष अपील",
                    "timeframe": "30 दिनों के बाद यदि बैंक समाधान न दे",
                    "badge": "अपील का अधिकार",
                    "badge_color": "primary",
                    "description": "यदि बैंक 30 दिनों में राशि वापस नहीं करता, तो आरबीआई बैंकिंग लोकपाल (cms.rbi.org.in) या आईटी अधिनियम की धारा 46 के तहत राज्य आईटी सचिव के समक्ष क्षतिपूर्ति हेतु आवेदन करें।",
                    "action_link": "https://cms.rbi.org.in",
                    "action_text": "आरबीआई लोकपाल पोर्टल",
                    "legal_backing": "आईटी अधिनियम धारा 46 एवं आरबीआई लोकपाल योजना"
                }
            ]

        elif language == "kn":
            return [
                {
                    "step": 1,
                    "title": "ತಕ್ಷಣ 1930 ಸೈಬರ್ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿ (ಗೋಲ್ಡನ್ ಅವರ್)",
                    "timeframe": "ವಂಚನೆ ನಡೆದ 2 ರಿಂದ 24 ಗಂಟೆಗಳ ಒಳಗೆ",
                    "badge": "ಅತ್ಯಂತ ತುರ್ತು",
                    "badge_color": "danger",
                    "description": "ತಕ್ಷಣವೇ 1930 ಗೆ ಕರೆ ಮಾಡಿ. ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಹೆಸರು, ಖಾತೆ ಸಂಖ್ಯೆ, ಯುಪಿಐ ರೆಫರೆನ್ಸ್ (UTR) ಸಂಖ್ಯೆ ಮತ್ತು ವಂಚಕನ ಸಂಖ್ಯೆಯನ್ನು ತಿಳಿಸಿ. ವಂಚಕರ ಬ್ಯಾಂಕ್ ಖಾತೆಯಲ್ಲಿ ಹಣವನ್ನು ಫ್ರೀಜ್ ಮಾಡಲು ಇದು ನೆರವಾಗುತ್ತದೆ.",
                    "action_link": "tel:1930",
                    "action_text": "1930 ಗೆ ಕರೆ ಮಾಡಿ",
                    "legal_backing": "ಗೃಹ ಸಚಿವಾಲಯದ ಸಿಎಫ್‌ಸಿಎಫ್‌ಆರ್‌ಎಂಎಸ್ ವ್ಯವಸ್ಥೆ"
                },
                {
                    "step": 2,
                    "title": "ನಿಮ್ಮ ಬ್ಯಾಂಕಿನಲ್ಲಿ ಅಧಿಕೃತ ದೂರು ದಾಖಲಿಸಿ",
                    "timeframe": "3 ಕೆಲಸದ ದಿನಗಳ ಒಳಗೆ",
                    "badge": "ಆರ್‌ಬಿಐ ಶೂನ್ಯ ಹೊಣೆಗಾರಿಕೆ",
                    "badge_color": "warning",
                    "description": "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ತೆರಳಿ ಅನಧಿಕೃತ ವಹಿವಾಟಿನ ಕುರಿತು ಲಿಖಿತ ದೂರು ನೀಡಿ. ಆರ್‌ಬಿಐ ನಿಯಮಾವಳಿಯಂತೆ 3 ದಿನಗಳಲ್ಲಿ ತಿಳಿಸಿದರೆ ಗ್ರಾಹಕರ ಹೊಣೆಗಾರಿಕೆ ಶೂನ್ಯವಾಗಿರುತ್ತದೆ.",
                    "action_link": "https://www.rbi.org.in",
                    "action_text": "ಆರ್‌ಬಿಐ ಸುತ್ತೋಲೆ",
                    "legal_backing": "RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18"
                },
                {
                    "step": 3,
                    "title": "cybercrime.gov.in ನಲ್ಲಿ ಅಧಿಕೃತ ದೂರು ಸಲ್ಲಿಸಿ",
                    "timeframe": "24 ರಿಂದ 48 ಗಂಟೆಗಳ ಒಳಗೆ",
                    "badge": "ಅಧಿಕೃತ ಸೈಬರ್ ಎಫ್‌ಐಆರ್ ದಾಖಲೆ",
                    "badge_color": "info",
                    "description": "ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಅಪರಾಧ ಪೋರ್ಟಲ್‌ನಲ್ಲಿ ಆನ್‌ಲೈನ್ ದೂರು ಸಲ್ಲಿಸಿ. ಬ್ಯಾಂಕ್ ಸ್ಟೇಟ್‌ಮೆಂಟ್ ಹಾಗೂ ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ಸ್ವೀಕೃತಿ ಸಂಖ್ಯೆಯನ್ನು ಉಳಿಸಿಕೊಳ್ಳಿ.",
                    "action_link": "https://cybercrime.gov.in",
                    "action_text": "ಪೋರ್ಟಲ್ ಭೇಟಿ ನೀಡಿ",
                    "legal_backing": "ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ ಕಾಯ್ದೆ 2000 ಕಲಂ 66D"
                },
                {
                    "step": 4,
                    "title": "ಯುಪಿಐ ಪಿನ್ ಮತ್ತು ಕಾರ್ಡ್‌ಗಳನ್ನು ತಕ್ಷಣ ನಿರ್ಬಂಧಿಸಿ",
                    "timeframe": "ತಕ್ಷಣ",
                    "badge": "ಖಾತೆ ರಕ್ಷಣೆ",
                    "badge_color": "secondary",
                    "description": "ನಿಮ್ಮ ಯುಪಿಐ ಪಿನ್ ಬದಲಾಯಿಸಿ, ಎಟಿಎಂ ಕಾರ್ಡ್ ಬ್ಲಾಕ್ ಮಾಡಿ ಮತ್ತು ಯಾವುದೇ ಅಪರಿಚಿತ ಮೊಬೈಲ್ ಅಪ್ಲಿಕೇಶನ್‌ಗಳನ್ನು ಡಿಲೀಟ್ ಮಾಡಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಬ್ಯಾಂಕಿಂಗ್ ಭದ್ರತಾ ಕ್ರಮಗಳು"
                },
                {
                    "step": 5,
                    "title": "ಆರ್‌ಬಿಐ ಒಂಬುಡ್ಸ್‌ಮನ್ ಅಥವಾ ಐಟಿ ಪ್ರಾಧಿಕಾರಕ್ಕೆ ಮೇಲ್ಮನವಿ",
                    "timeframe": "ಬ್ಯಾಂಕ್ 30 ದಿನಗಳಲ್ಲಿ ಪರಿಹರಿಸದಿದ್ದರೆ",
                    "badge": "ಪರಿಹಾರ ಕೋರಿಕೆ",
                    "badge_color": "primary",
                    "description": "ಬ್ಯಾಂಕ್ 30 ದಿನಗಳಲ್ಲಿ ಹಣ ಮರಳಿಸದಿದ್ದರೆ ಆರ್‌ಬಿಐ ಬ್ಯಾಂಕಿಂಗ್ ಒಂಬುಡ್ಸ್‌ಮನ್ ಅಥವಾ ಐಟಿ ಕಾಯ್ದೆ ಕಲಂ 46 ರ ಅಡಿಯಲ್ಲಿ ರಾಜ್ಯ ಐಟಿ ಕಾರ್ಯದರ್ಶಿಗೆ ಪರಿಹಾರ ಕೋರಿ ಅರ್ಜಿ ಸಲ್ಲಿಸಬಹುದು.",
                    "action_link": "https://cms.rbi.org.in",
                    "action_text": "ಆರ್‌ಬಿಐ ಒಂಬುಡ್ಸ್‌ಮನ್ ಪೋರ್ಟಲ್",
                    "legal_backing": "ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ ಕಾಯ್ದೆ ಕಲಂ 46"
                }
            ]

        else:  # Default English
            return [
                {
                    "step": 1,
                    "title": "Call National Cybercrime Helpline 1930 (Golden Hour Action)",
                    "timeframe": "Within first 2 to 24 hours of transaction",
                    "badge": "CRITICAL IMMEDIATE",
                    "badge_color": "danger",
                    "description": f"Dial 1930 immediately. Report the incident to the Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS). Provide your bank name, account number, UPI reference ID (UTR), debit amount {f'({amount})' if amount else ''}, and suspect's account/VPA to initiate immediate fund freezing in beneficiary accounts.",
                    "action_link": "tel:1930",
                    "action_text": "Dial 1930 Now",
                    "legal_backing": "Citizen Financial Cyber Fraud Reporting System (MHA, Govt of India)"
                },
                {
                    "step": 2,
                    "title": "Notify Your Bank & Claim Zero Liability Protection",
                    "timeframe": "Within 3 working days",
                    "badge": "RBI Statutory Protection",
                    "badge_color": "warning",
                    "description": "Submit a formal written dispute and unauthorized transaction form to your home branch and via NetBanking. Under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, reporting within 3 days legally entitles you to Zero Liability.",
                    "action_link": "https://www.rbi.org.in",
                    "action_text": "Read RBI Circular",
                    "legal_backing": "RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18"
                },
                {
                    "step": 3,
                    "title": "Register Formal Complaint on National Cyber Crime Portal",
                    "timeframe": "Within 24 to 48 hours",
                    "badge": "Formal Statutory Filing",
                    "badge_color": "info",
                    "description": "Visit cybercrime.gov.in and report under 'Financial Fraud'. Upload your bank statement, transaction SMS/screenshot, and scammer communication. Note and preserve the Acknowledgement / Docket Number for police FIR processing.",
                    "action_link": "https://cybercrime.gov.in",
                    "action_text": "Visit cybercrime.gov.in",
                    "legal_backing": "Information Technology Act 2000 Section 66D & BNS Section 318(4)"
                },
                {
                    "step": 4,
                    "title": "Block Compromised Channels & Reset Security Credentials",
                    "timeframe": "Immediate",
                    "badge": "Account Security",
                    "badge_color": "secondary",
                    "description": "Immediately change your UPI PIN, NetBanking passwords, and request your bank to temporarily hotlist/block linked ATM debit cards. Check your phone for unauthorized remote desktop applications (e.g., AnyDesk, QuickSupport) and uninstall them.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Digital Banking Security Guidelines"
                },
                {
                    "step": 5,
                    "title": "Escalate to Banking Ombudsman or State IT Adjudicating Officer",
                    "timeframe": "After 30 days if grievance is unresolved",
                    "badge": "Statutory Redressal",
                    "badge_color": "primary",
                    "description": "If your bank fails to credit back the defrauded amount or rejects your claim after 30 days, file an online appeal before the RBI Banking Ombudsman (cms.rbi.org.in). You may also petition the State IT Secretary (Adjudicating Officer) under Section 46 of the IT Act for compensation up to ₹5 Crore.",
                    "action_link": "https://cms.rbi.org.in",
                    "action_text": "File RBI Ombudsman Complaint",
                    "legal_backing": "IT Act 2000 Section 46 & RBI Integrated Ombudsman Scheme"
                }
            ]

    elif category_id == "tenant_landlord":
        if language == "hi":
            return [
                {
                    "step": 1,
                    "title": "किराया समझौता (रेंट एग्रीमेंट) एवं रसीदों की समीक्षा करें",
                    "timeframe": "कदम 1",
                    "badge": "दस्तावेज़ सत्यापन",
                    "badge_color": "info",
                    "description": "अपने रेंट एग्रीमेंट में सुरक्षा राशि वापसी (सिक्योरिटी डिपॉजिट), नोटिस अवधि और रख-रखाव की शर्तों की जांच करें। मासिक किराया भुगतान के बैंक रिकॉर्ड सुरक्षित करें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "भारतीय अनुबंध अधिनियम 1872 एवं मॉडल किरायेदारी अधिनियम"
                },
                {
                    "step": 2,
                    "title": "मकान मालिक को औपचारिक लिखित नोटिस या ईमेल भेजें",
                    "timeframe": "7 से 15 दिनों का समय दें",
                    "badge": "औपचारिक सूचना",
                    "badge_color": "warning",
                    "description": "व्हाट्सएप, ईमेल या पंजीकृत डाक द्वारा स्पष्ट विवरण सहित औपचारिक पत्र भेजें। अवैधानिक कटौती या अवैध बेदखली का विरोध करें और समाधान हेतु 15 दिनों का समय दें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "संपत्ति अंतरण अधिनियम 1882 धारा 106"
                },
                {
                    "step": 3,
                    "title": "अवैध बिजली/पानी कटौती या जबरन बेदखली के विरुद्ध पुलिस शिकायत",
                    "timeframe": "अवैध दबाव की स्थिति में तुरंत",
                    "badge": "सुरक्षा कदम",
                    "badge_color": "danger",
                    "description": "मकान मालिक आवश्यक सेवाएं (बिजली, पानी) नहीं काट सकता और न ही जबरन ताला लगा सकता है। ऐसा करने पर 112 डायल करें या स्थानीय थाने में आपराधिक धमकी (बीएनएस धारा 351) की शिकायत दें।",
                    "action_link": "tel:112",
                    "action_text": "112 पुलिस हेल्पलाइन",
                    "legal_backing": "मॉडल किरायेदारी अधिनियम धारा 20 एवं बीएनएस 2023 धारा 351"
                },
                {
                    "step": 4,
                    "title": "जिला विधिक सेवा प्राधिकरण (DLSA) में निःशुल्क मध्यस्थता",
                    "timeframe": "कोर्ट जाने से पूर्व",
                    "badge": "मुफ्त कानूनी सहायता",
                    "badge_color": "success",
                    "description": "जिला अदालत में डीएलएसए (DLSA) या नालसा (NALSA) के माध्यम से प्री-लिटिगेशन मध्यस्थता का आवेदन करें। यह बिना किसी कोर्ट फीस के दोनों पक्षों में समझौता कराता है।",
                    "action_link": "https://nalsa.gov.in",
                    "action_text": "नालसा पोर्टल देखें",
                    "legal_backing": "विधिक सेवा प्राधिकरण अधिनियम 1987"
                },
                {
                    "step": 5,
                    "title": "रेंट अथॉरिटी / सिविल कोर्ट में बेदखली निषेध या वसूली वाद",
                    "timeframe": "यदि मध्यस्थता विफल रहे",
                    "badge": "न्यायिक वाद",
                    "badge_color": "primary",
                    "description": "अवैध निष्कासन के विरुद्ध विनिर्दिष्ट अनुतोष अधिनियम धारा 6 के तहत सिविल कोर्ट में कब्जे की बहाली या रेंट कोर्ट में सुरक्षा राशि वसूली का वाद दायर करें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "विनिर्दिष्ट अनुतोष अधिनियम 1963 धारा 6"
                }
            ]
        elif language == "kn":
            return [
                {
                    "step": 1,
                    "title": "ಬಾಡಿಗೆ ಒಪ್ಪಂದ ಮತ್ತು ರಸೀದಿಗಳನ್ನು ಪರಿಶೀಲಿಸಿ",
                    "timeframe": "ಹಂತ 1",
                    "badge": "ದಾಖಲೆ ಪರಿಶೀಲನೆ",
                    "badge_color": "info",
                    "description": "ನಿಮ್ಮ ಬಾಡಿಗೆ ಕರಾರು ಪತ್ರದಲ್ಲಿನ ಠೇವಣಿ ಮರುಪಾವತಿ ನಿಯಮ ಹಾಗೂ ನೋಟಿಸ್ ಅವಧಿಯನ್ನು ಪರಿಶೀಲಿಸಿ. ಮಾಸಿಕ ಬಾಡಿಗೆ ಪಾವತಿಸಿದ ಬ್ಯಾಂಕ್ ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಆಸ್ತಿ ವರ್ಗಾವಣೆ ಕಾಯ್ದೆ 1882 ಕಲಂ 106"
                },
                {
                    "step": 2,
                    "title": "ಮನೆ ಮಾಲೀಕರಿಗೆ ಲಿಖಿತ ನೋಟಿಸ್ ನೀಡಿ",
                    "timeframe": "7 ರಿಂದ 15 ದಿನಗಳ ಕಾಲಾವಕಾಶ",
                    "badge": "ಅಧಿಕೃತ ನೋಟಿಸ್",
                    "badge_color": "warning",
                    "description": "ವಾಟ್ಸಾಪ್ ಅಥವಾ ಇಮೇಲ್ ಮೂಲಕ ವಿವರವಾದ ನೋಟಿಸ್ ಕಳುಹಿಸಿ, ಮುಂಗಡ ಠೇವಣಿಯನ್ನು ಪೂರ್ಣವಾಗಿ ಮರಳಿಸಲು 15 ದಿನಗಳ ಕಾಲಾವಕಾಶ ನೀಡಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಮಾದರಿ ಬಾಡಿಗೆ ಕಾಯ್ದೆ 2021 ಕಲಂ 11"
                },
                {
                    "step": 3,
                    "title": "ಅಕ್ರಮ ನೀರು/ವಿದ್ಯುತ್ ಕಡಿತದ ವಿರುದ್ಧ ಪೊಲೀಸ್ ರಕ್ಷಣೆ",
                    "timeframe": "ಬೆದರಿಕೆಯುಂಟಾದ ತಕ್ಷಣ",
                    "badge": "ಕ್ರಿಮಿನಲ್ ರಕ್ಷಣೆ",
                    "badge_color": "danger",
                    "description": "ಮಾಲೀಕರು ನೀರು ಅಥವಾ ವಿದ್ಯುತ್ ನಿಲ್ಲಿಸುವಂತಿಲ್ಲ. ಹಾಗೆ ಮಾಡಿದಲ್ಲಿ 112 ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ.",
                    "action_link": "tel:112",
                    "action_text": "112 ಪೊಲೀಸ್ ಸಹಾಯವಾಣಿ",
                    "legal_backing": "ಮಾದರಿ ಬಾಡಿಗೆ ಕಾಯ್ದೆ ಕಲಂ 20 ಮತ್ತು ಬಿಎನ್‌ಎಸ್ ಕಲಂ 351"
                },
                {
                    "step": 4,
                    "title": "ಡಿಎಲ್ಎಸ್ಎ (DLSA) ಮೂಲಕ ಉಚಿತ ಮಧ್ಯಸ್ಥಿಕೆ",
                    "timeframe": "ನ್ಯಾಯಾಲಯಕ್ಕೆ ಹೋಗುವ ಮುನ್ನ",
                    "badge": "ಉಚಿತ ಕಾನೂನು ನೆರವು",
                    "badge_color": "success",
                    "description": "ಜಿಲ್ಲಾ ಕಾನೂನು ಸೇವೆಗಳ ಪ್ರಾಧಿಕಾರಕ್ಕೆ (DLSA) ಅರ್ಜಿ ಸಲ್ಲಿಸಿ ಉಚಿತ ಮಧ್ಯಸ್ಥಿಕೆ ಮತ್ತು ಲೋಕ ಅದಾಲತ್ ಮೂಲಕ ಶಾಂತಿಯುತ ಪರಿಹಾರ ಕಂಡುಕೊಳ್ಳಿ.",
                    "action_link": "https://nalsa.gov.in",
                    "action_text": "ನಾಲ್ಸಾ ಪೋರ್ಟಲ್",
                    "legal_backing": "ಕಾನೂನು ಸೇವೆಗಳ ಪ್ರಾಧಿಕಾರ ಕಾಯ್ದೆ 1987"
                },
                {
                    "step": 5,
                    "title": "ರೆಂಟ್ ಕೋರ್ಟ್‌ನಲ್ಲಿ ಅರ್ಜಿ ಸಲ್ಲಿಕೆ",
                    "timeframe": "ಮಧ್ಯಸ್ಥಿಕೆ ವಿಫಲವಾದರೆ",
                    "badge": "ನ್ಯಾಯಾಲಯ ಪರಿಹಾರ",
                    "badge_color": "primary",
                    "description": "ಸ್ಥಳೀಯ ರೆಂಟ್ ಅಥಾರಿಟಿ ಅಥವಾ ಸಿವಿಲ್ ಕೋರ್ಟ್‌ನಲ್ಲಿ ಠೇವಣಿ ಮರುಪಾವತಿ ಕೋರಿ ಕಾನೂನು ಪ್ರಕಾರ ಅರ್ಜಿ ದಾಖಲಿಸಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ನಿರ್ದಿಷ್ಟ ಪರಿಹಾರ ಕಾಯ್ದೆ 1963 ಕಲಂ 6"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "title": "Audit Rental Agreement, Notice Terms & Payment Proofs",
                    "timeframe": "Day 1",
                    "badge": "Contract Verification",
                    "badge_color": "info",
                    "description": "Examine the signed Tenancy/Lease Agreement. Verify deposit return timelines, lock-in period clauses, and required eviction notice periods (typically 15 to 30 days). Compile bank statements proving timely rent transfers.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Transfer of Property Act 1882 Section 106 & Indian Contract Act"
                },
                {
                    "step": 2,
                    "title": "Issue a Formal Written Grievance Notice",
                    "timeframe": "Allow 7 to 15 days response window",
                    "badge": "Statutory Notice",
                    "badge_color": "warning",
                    "description": "Send a registered post or formal email detailing the deposit withholding or dispute. Demand an itemized statement of claimed deductions and cite the 30-day deposit return timeline under the Model Tenancy Act.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Model Tenancy Act 2021 Section 11"
                },
                {
                    "step": 3,
                    "title": "Police Protection Against Essential Supply Cuts or Forced Lockout",
                    "timeframe": "Immediate if landlord threatens force",
                    "badge": "Criminal Protection",
                    "badge_color": "danger",
                    "description": "Landlords are strictly prohibited by law from cutting off water, electricity, elevator access, or locking tenants out without a court eviction order. In case of coercive threats, dial 112 or file a police complaint under BNS Section 351 (Criminal Intimidation).",
                    "action_link": "tel:112",
                    "action_text": "Emergency Police 112",
                    "legal_backing": "Model Tenancy Act Section 20 & BNS 2023 Section 351"
                },
                {
                    "step": 4,
                    "title": "Pre-Litigation Mediation via DLSA / NALSA Legal Aid",
                    "timeframe": "Before approaching regular courts",
                    "badge": "Free Legal Aid",
                    "badge_color": "success",
                    "description": "Approach the District Legal Services Authority (DLSA) at the local court complex or dial 15100. DLSA provides free mediation and Lok Adalat dispute resolution without legal representation costs.",
                    "action_link": "https://nalsa.gov.in",
                    "action_text": "Visit NALSA Portal",
                    "legal_backing": "Legal Services Authorities Act 1987"
                },
                {
                    "step": 5,
                    "title": "Petition Rent Court or File Injunction Suit for Possession",
                    "timeframe": "If landlord refuses mediation",
                    "badge": "Civil Legal Remedy",
                    "badge_color": "primary",
                    "description": "File a petition before the local Rent Authority/Rent Tribunal under the State Tenancy Act. If dispossessed unlawfully, file a civil suit under Section 6 of the Specific Relief Act, 1963 for immediate possession recovery within 6 months.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Specific Relief Act 1963 Section 6 & State Rent Control Acts"
                }
            ]

    else:  # consumer_complaint
        if language == "hi":
            return [
                {
                    "step": 1,
                    "title": "टैक्स इनवॉइस, वारंटी कार्ड एवं खराबी के साक्ष्य सुरक्षित करें",
                    "timeframe": "पहला कदम",
                    "badge": "साक्ष्य संग्रह",
                    "badge_color": "info",
                    "description": "उत्पाद का टैक्स इनवॉइस, ऑर्डर आईडी, वारंटी कार्ड, सर्विस सेंटर की जॉब शीट और खराबी की तस्वीरें/वीडियो सुरक्षित रखें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "उपभोक्ता संरक्षण अधिनियम 2019 धारा 2(9)"
                },
                {
                    "step": 2,
                    "title": "कंपनी को औपचारिक शिकायत ईमेल भेजकर समाधान मांगें",
                    "timeframe": "7 कार्य दिवसों का समय दें",
                    "badge": "आंतरिक निवारण",
                    "badge_color": "secondary",
                    "description": "विक्रेता या निर्माता की आधिकारिक ग्राहक सेवा ईमेल और नोडल अधिकारी को स्पष्ट ईमेल भेजें। 7 दिनों में मुफ्त मरम्मत, प्रतिस्थापन (रिप्लेसमेंट) या पूर्ण रिफंड की मांग करें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "उपभोक्ता संरक्षण अधिनियम धारा 2(11)"
                },
                {
                    "step": 3,
                    "title": "राष्ट्रीय उपभोक्ता हेल्पलाइन (NCH 1915) पर शिकायत दर्ज करें",
                    "timeframe": "कंपनी के इनकार पर तुरंत",
                    "badge": "सरकारी मध्यस्थता",
                    "badge_color": "warning",
                    "description": "1915 पर कॉल करें या consumerhelpline.gov.in पर डॉकेट दर्ज करें। एनसीएच (NCH) सरकार की पहल है जो 1000 से अधिक कंपनियों के साथ सीधे बातचीत कर विवाद सुलझाती है।",
                    "action_link": "https://consumerhelpline.gov.in",
                    "action_text": "एनसीएच पोर्टल पर जाएं",
                    "legal_backing": "उपभोक्ता मामले विभाग, भारत सरकार"
                },
                {
                    "step": 4,
                    "title": "वकील के माध्यम से या स्वयं वैधानिक लीगल नोटिस भेजें",
                    "timeframe": "15 दिनों का नोटिस",
                    "badge": "विधिक नोटिस",
                    "badge_color": "primary",
                    "description": "यदि एनसीएच में भी समाधान न मिले, तो कंपनी को 15 दिनों का औपचारिक लीगल नोटिस भेजें जिसमें उपभोक्ता फोरम में वाद दायर करने की चेतावनी दें।",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "उपभोक्ता संरक्षण अधिनियम 2019 धारा 35"
                },
                {
                    "step": 5,
                    "title": "e-Daakhil पोर्टल पर जिला उपभोक्ता आयोग में केस दर्ज करें",
                    "timeframe": "कारण उत्पन्न होने के 2 वर्ष के भीतर",
                    "badge": "उपभोक्ता न्यायालय",
                    "badge_color": "danger",
                    "description": "edaakhil.nic.in पोर्टल के जरिए घर बैठे जिला उपभोक्ता विवाद प्रतितोष आयोग में ऑनलाइन केस दर्ज करें। इसके लिए वकील रखना अनिवार्य नहीं है। रिफंड के साथ मानसिक उत्पीड़न हेतु क्षतिपूर्ति मांगें।",
                    "action_link": "https://edaakhil.nic.in",
                    "action_text": "e-Daakhil पोर्टल खोलें",
                    "legal_backing": "उपभोक्ता संरक्षण अधिनियम 2019 धारा 35 एवं 69"
                }
            ]
        elif language == "kn":
            return [
                {
                    "step": 1,
                    "title": "ತೆರಿಗೆ ಬಿಲ್ (ಇನ್‌ವಾಯ್ಸ್), ವಾರಂಟಿ ಕಾರ್ಡ್ ಮತ್ತು ದೋಷದ ಸಾಕ್ಷ್ಯ ಸಂಗ್ರಹಿಸಿ",
                    "timeframe": "ಹಂತ 1",
                    "badge": "ಸಾಕ್ಷ್ಯಾಧಾರ ಸಂಗ್ರಹ",
                    "badge_color": "info",
                    "description": "ಉತ್ಪನ್ನದ ಅಧಿಕೃತ ಜಿಎಸ್‌ಟಿ ತೆರಿಗೆ ಇನ್‌ವಾಯ್ಸ್, ವಾರಂಟಿ ಕಾರ್ಡ್, ಸರ್ವಿಸ್ ಸೆಂಟರ್‌ನ ತಪಾಸಣಾ ರಸೀದಿ ಹಾಗೂ ದೋಷವನ್ನು ತೋರಿಸುವ ಫೋಟೋ/ವಿಡಿಯೋಗಳನ್ನು ಸುರಕ್ಷಿತವಾಗಿರಿಸಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2019 ಕಲಂ 2(9)"
                },
                {
                    "step": 2,
                    "title": "ಕಂಪನಿಗೆ ಇಮೇಲ್ ಮೂಲಕ ಅಧಿಕೃತ ದೂರು ಸಲ್ಲಿಸಿ",
                    "timeframe": "7 ಕೆಲಸದ ದಿನಗಳ ಕಾಲಾವಕಾಶ",
                    "badge": "ಆಂತರಿಕ ಪರಿಹಾರ",
                    "badge_color": "secondary",
                    "description": "ಮಾರಾಟಗಾರ ಅಥವಾ ಕಂಪನಿಯ ನೋಡಲ್ ಅಧಿಕಾರಿಗೆ ಇಮೇಲ್ ಕಳುಹಿಸಿ ಉಚಿತ ದುರಸ್ತಿ, ಬದಲಿ ವಸ್ತು ಅಥವಾ ಪೂರ್ಣ ಹಣ ಮರುಪಾವತಿಸಲು ಕೋರಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ ಕಲಂ 2(11)"
                },
                {
                    "step": 3,
                    "title": "ರಾಷ್ಟ್ರೀಯ ಗ್ರಾಹಕ ಸಹಾಯವಾಣಿ (NCH 1915) ಗೆ ದೂರು ನೀಡಿ",
                    "timeframe": "ಕಂಪನಿ ನಿರಾಕರಿಸಿದ ತಕ್ಷಣ",
                    "badge": "ಸರ್ಕಾರಿ ಸಹಾಯವಾಣಿ",
                    "badge_color": "warning",
                    "description": "1915 ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ consumerhelpline.gov.in ನಲ್ಲಿ ದೂರು ದಾಖಲಿಸಿ ಸರ್ಕಾರದ ಡಾಕೆಟ್ ಸಂಖ್ಯೆ ಪಡೆಯಿರಿ.",
                    "action_link": "https://consumerhelpline.gov.in",
                    "action_text": "ಎನ್‌ಸಿಹೆಚ್ ಪೋರ್ಟಲ್",
                    "legal_backing": "ಗ್ರಾಹಕ ವ್ಯವಹಾರಗಳ ಇಲಾಖೆ, ಭಾರತ ಸರ್ಕಾರ"
                },
                {
                    "step": 4,
                    "title": "ಕಾನೂನು ಪ್ರಕಾರ 15 ದಿನಗಳ ಲೀಗಲ್ ನೋಟಿಸ್ ಕಳುಹಿಸಿ",
                    "timeframe": "15 ದಿನಗಳ ನೋಟಿಸ್",
                    "badge": "ವಿಧಿಬದ್ಧ ನೋಟಿಸ್",
                    "badge_color": "primary",
                    "description": "ಕಂಪನಿಯು ಸ್ಪಂದಿಸದಿದ್ದರೆ ನೋಂದಾಯಿತ ಅಂಚೆ ಅಥವಾ ಇಮೇಲ್ ಮೂಲಕ ಗ್ರಾಹಕ ನ್ಯಾಯಾಲಯದಲ್ಲಿ ಮೊಕದ್ದಮೆ ಹೂಡುವ ಮುನ್ನಚ್ಚರಿಕೆಯ ಲೀಗಲ್ ನೋಟಿಸ್ ರವಾನಿಸಿ.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2019 ಕಲಂ 35"
                },
                {
                    "step": 5,
                    "title": "e-Daakhil ಮೂಲಕ ಜಿಲ್ಲಾ ಗ್ರಾಹಕ ಆಯೋಗಕ್ಕೆ ಆನ್‌ಲೈನ್ ದೂರು ಸಲ್ಲಿಸಿ",
                    "timeframe": "ದೋಷ ಸಂಭವಿಸಿದ 2 ವರ್ಷಗಳ ಒಳಗೆ",
                    "badge": "ಗ್ರಾಹಕ ನ್ಯಾಯಾಲಯ",
                    "badge_color": "danger",
                    "description": "edaakhil.nic.in ಪೋರ್ಟಲ್ ಮೂಲಕ ವಕೀಲರ ಅಗತ್ಯವಿಲ್ಲದೆ ಸ್ವತಃ ಜಿಲ್ಲಾ ಗ್ರಾಹಕ ಆಯೋಗಕ್ಕೆ ಆನ್‌ಲೈನ್ ದೂರು ಸಲ್ಲಿಸಿ ಪರಿಹಾರ ಮತ್ತು ಮಾನಸಿಕ ಕಿರುಕುಳಕ್ಕೆ ನಷ್ಟ ಪರಿಹಾರ ಕೋರಿ.",
                    "action_link": "https://edaakhil.nic.in",
                    "action_text": "e-Daakhil ಪೋರ್ಟಲ್",
                    "legal_backing": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2019 ಕಲಂ 35 & 69"
                }
            ]
        else:
            return [
                {
                    "step": 1,
                    "title": "Secure Tax Invoice, Warranty Card & Defect Evidence",
                    "timeframe": "Step 1",
                    "badge": "Document Preservation",
                    "badge_color": "info",
                    "description": "Preserve the original tax invoice, packaging box, order confirmation email, service center job sheets, and photo/video evidence documenting the defect or service deficiency.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Consumer Protection Act 2019 Section 2(9) & 2(11)"
                },
                {
                    "step": 2,
                    "title": "Lodge Formal Written Grievance with Seller & Manufacturer",
                    "timeframe": "Allow 7 working days for response",
                    "badge": "Internal Escalation",
                    "badge_color": "secondary",
                    "description": "Email the company's designated Grievance / Nodal Officer. Demand one of three statutory remedies: (1) Free comprehensive repair, (2) Defect-free replacement, or (3) 100% refund.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Consumer Protection Act 2019 Section 2(47)"
                },
                {
                    "step": 3,
                    "title": "Register Dispute on National Consumer Helpline (NCH - 1915)",
                    "timeframe": "Immediate upon seller refusal",
                    "badge": "Govt Pre-Litigation Docket",
                    "badge_color": "warning",
                    "description": "Call 1915 or file on consumerhelpline.gov.in. NCH assigns an official government docket number and brings the converged corporate partner into formal conciliation.",
                    "action_link": "https://consumerhelpline.gov.in",
                    "action_text": "NCH Grievance Portal",
                    "legal_backing": "Dept. of Consumer Affairs, Ministry of Consumer Affairs"
                },
                {
                    "step": 4,
                    "title": "Serve Formal Pre-Litigation Legal Notice",
                    "timeframe": "15 days notice window",
                    "badge": "Legal Notice",
                    "badge_color": "primary",
                    "description": "Draft and dispatch a formal Legal Notice to the company's registered headquarters via Registered Post A.D. or email, stating that failure to remediate will lead to a complaint before the Consumer Commission.",
                    "action_link": "",
                    "action_text": "",
                    "legal_backing": "Civil Procedure & CPA 2019 Section 35"
                },
                {
                    "step": 5,
                    "title": "File Consumer Case via e-Daakhil before District Commission",
                    "timeframe": "Within statutory 2-year limitation period",
                    "badge": "Consumer Court Action",
                    "badge_color": "danger",
                    "description": "File an e-complaint on edaakhil.nic.in before the District Consumer Disputes Redressal Commission (DCDRC) having local jurisdiction. You can represent yourself without hiring a lawyer. Claim product cost refund plus compensation for harassment.",
                    "action_link": "https://edaakhil.nic.in",
                    "action_text": "e-Daakhil Portal",
                    "legal_backing": "Consumer Protection Act 2019 Section 35 & 69"
                }
            ]

    # GENERAL CATEGORY FALLBACK (Covers any other legal situation)
    if language == "hi":
        return [
            {
                "step": 1,
                "title": "प्राथमिक तथ्य, साक्ष्य एवं समय-सीमा (Timeline) दर्ज करें",
                "timeframe": "तुरंत",
                "badge": "साक्ष्य सुरक्षा",
                "badge_color": "danger",
                "description": "घटना का पूरा विवरण, तारीख, समय, शामिल व्यक्तियों के नाम, गवाहों और सभी संबंधित दस्तावेजों को सुरक्षित रखें।",
                "action_link": "",
                "action_text": "",
                "legal_backing": "भारतीय साक्ष्य अधिनियम / भारतीय साक्ष्य अधिनियम 2023"
            },
            {
                "step": 2,
                "title": "मुफ्त कानूनी सलाह हेतु NALSA हेल्पलाइन 15100 पर संपर्क करें",
                "timeframe": "1 से 2 दिन के भीतर",
                "badge": "निःशुल्क कानूनी सहायता",
                "badge_color": "warning",
                "description": "राष्ट्रीय विधिक सेवा प्राधिकरण (NALSA) या जिला विधिक सेवा प्राधिकरण (DLSA) से संपर्क कर अपनी पात्रता के अनुसार मुफ्त वकील या सलाह प्राप्त करें।",
                "action_link": "tel:15100",
                "action_text": "NALSA हेल्पलाइन (15100)",
                "legal_backing": "विधिक सेवा प्राधिकरण अधिनियम, 1987"
            },
            {
                "step": 3,
                "title": "संबंधित प्राधिकरण या पुलिस स्टेशन में शिकायत दर्ज करें",
                "timeframe": "मामले की गंभीरता के आधार पर",
                "badge": "प्राधिकरण शिकायत",
                "badge_color": "info",
                "description": "यदि मामला आपराधिक प्रकृति का है, तो नजदीकी पुलिस स्टेशन या 112 पर सूचना दें। यदि दीवानी है, तो संबंधित विभाग या फोरम में लिखित शिकायत दें।",
                "action_link": "tel:112",
                "action_text": "आपातकालीन नंबर 112",
                "legal_backing": "भारतीय नागरिक सुरक्षा संहिता (BNSS) 2023"
            },
            {
                "step": 4,
                "title": "औपचारिक कानूनी नोटिस भेजें (यदि लागू हो)",
                "timeframe": "वकील के परामर्श अनुसार",
                "badge": "विधिक प्रक्रिया",
                "badge_color": "secondary",
                "description": "विरोधी पक्ष को अपनी शिकायत और उचित समाधान की मांग करते हुए एक पंजीकृत कानूनी नोटिस भेजें।",
                "action_link": "",
                "action_text": "",
                "legal_backing": "सिविल प्रक्रिया संहिता (CPC)"
            },
            {
                "step": 5,
                "title": "उपयुक्त न्यायालय, न्यायाधिकरण या लोक अदालत में वाद दायर करें",
                "timeframe": "निर्धारित समय-सीमा के भीतर",
                "badge": "न्यायिक राहत",
                "badge_color": "primary",
                "description": "यदि आपसी सहमति या नोटिस से समाधान नहीं होता, तो सक्षम न्यायालय, उपभोक्ता फोरम या लोक अदालत के समक्ष औपचारिक याचिका दायर करें।",
                "action_link": "https://nalsa.gov.in",
                "action_text": "NALSA आधिकारिक पोर्टल",
                "legal_backing": "संबंधित क्षेत्राधिकार कानून"
            }
        ]
    elif language == "kn":
        return [
            {
                "step": 1,
                "title": "ಘಟನೆಯ ವಿವರಗಳು ಮತ್ತು ದಾಖಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ",
                "timeframe": "ತಕ್ಷಣ",
                "badge": "ದಾಖಲೆ ರಕ್ಷಣೆ",
                "badge_color": "danger",
                "description": "ಘಟನೆ ನಡೆದ ದಿನಾಂಕ, ಸಮಯ, ಸ್ಥಳ, ಸಂಬಂಧಿತ ವ್ಯಕ್ತಿಗಳು ಮತ್ತು ಎಲ್ಲಾ ಪತ್ರವ್ಯವಹಾರಗಳ ಪುರಾವೆಗಳನ್ನು ಭದ್ರವಾಗಿ ಇರಿಸಿಕೊಳ್ಳಿ.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "ಭಾರತೀಯ ಸಾಕ್ಷ್ಯ ಕಾಯ್ದೆ / ಭಾರತೀಯ ಸಾಕ್ಷ್ಯ ಅಧಿನಿಯಮ 2023"
            },
            {
                "step": 2,
                "title": "NALSA ಉಚಿತ ಕಾನೂನು ನೆರವು ಸಹಾಯವಾಣಿ 15100 ಗೆ ಕರೆ ಮಾಡಿ",
                "timeframe": "1 ರಿಂದ 2 ದಿನಗಳ ಒಳಗೆ",
                "badge": "ಉಚಿತ ಕಾನೂನು ನೆರವು",
                "badge_color": "warning",
                "description": "ರಾಷ್ಟ್ರೀಯ ಕಾನೂನು ಸೇವೆಗಳ ಪ್ರಾಧಿಕಾರ (NALSA) ಅಥವಾ ಜಿಲ್ಲಾ ಕಾನೂನು ಸೇವೆಗಳ ಪ್ರಾಧಿಕಾರಕ್ಕೆ (DLSA) ಸಂಪರ್ಕಿಸಿ ಉಚಿತ ಕಾನೂನು ಸಲಹೆ ಪಡೆಯಿರಿ.",
                "action_link": "tel:15100",
                "action_text": "NALSA ಸಹಾಯವಾಣಿ 15100",
                "legal_backing": "ಕಾನೂನು ಸೇವೆಗಳ ಪ್ರಾಧಿಕಾರಗಳ ಕಾಯ್ದೆ, 1987"
            },
            {
                "step": 3,
                "title": "ಸೂಕ್ತ ಪ್ರಾಧಿಕಾರ ಅಥವಾ ಪೊಲೀಸ್ ಠಾಣೆಗೆ ದೂರು ನೀಡಿ",
                "timeframe": "ಪ್ರಕರಣದ ತುರ್ತುಸ್ಥಿತಿಗೆ ಅನುಗುಣವಾಗಿ",
                "badge": "ಅಧಿಕೃತ ದೂರು",
                "badge_color": "info",
                "description": "ಅಪರಾಧ ಅಥವಾ ಬೆದರಿಕೆ ಇದ್ದರೆ ತಕ್ಷಣ 112 ಗೆ ಕರೆ ಮಾಡಿ ಅಥವಾ ಪೊಲೀಸ್ ಠಾಣೆಗೆ ಲಿಖಿತ ದೂರು ನೀಡಿ. ಸಿವಿಲ್ ವಿಷಯವಾಗಿದ್ದರೆ ಸೂಕ್ತ ಇಲಾಖೆಗೆ ದೂರು ಸಲ್ಲಿಸಿ.",
                "action_link": "tel:112",
                "action_text": "ತುರ್ತು ಕರೆ 112",
                "legal_backing": "ಭಾರತೀಯ ನಾಗರಿಕ ಸುರಕ್ಷಾ ಸಂಹಿತೆ (BNSS) 2023"
            },
            {
                "step": 4,
                "title": "ವಿಧಿಬದ್ಧ ಕಾನೂನು ನೋಟಿಸ್ ಜಾರಿಗೊಳಿಸಿ",
                "timeframe": "ಕಾನೂನು ಸಲಹೆಯ ಮೇರೆಗೆ",
                "badge": "ಕಾನೂನು ನೋಟಿಸ್",
                "badge_color": "secondary",
                "description": "ಎದುರುದಾರರಿಗೆ ವಿವಾದ ಪರಿಹಾರಕ್ಕೆ ಸೂಕ್ತ ಸಮಯ ನೀಡಿ ನೋಂದಾಯಿತ ಅಂಚೆ ಮೂಲಕ ಕಾನೂನು ನೋಟಿಸ್ ಕಳುಹಿಸಿ.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "ಸಿವಿಲ್ ಪ್ರಕ್ರಿಯಾ ಸಂಹಿತೆ (CPC)"
            },
            {
                "step": 5,
                "title": "ನ್ಯಾಯಾಲಯ ಅಥವಾ ಲೋಕ ಅದಾಲತ್‌ನಲ್ಲಿ ವ್ಯಾಜ್ಯ ಹೂಡಿ",
                "timeframe": "ಕಾಲಮಿತಿಯೊಳಗೆ",
                "badge": "ನ್ಯಾಯಾಂಗ ಪರಿಹಾರ",
                "badge_color": "primary",
                "description": "ವಿವಾದ ಬಗೆಹರಿಯದಿದ್ದರೆ ಸೂಕ್ತ ನ್ಯಾಯಾಲಯ, ಜಿಲ್ಲಾ ಗ್ರಾಹಕ ಆಯೋಗ ಅಥವಾ ಲೋಕ ಅದಾಲತ್ ಮೂಲಕ ಕಾನೂನು ಕ್ರಮ ಮುಂದುವರಿಸಿ.",
                "action_link": "https://nalsa.gov.in",
                "action_text": "NALSA ಪೋರ್ಟಲ್",
                "legal_backing": "ಸಂಬಂಧಿತ ನ್ಯಾಯಾಂಗ ನಿಯಮಗಳು"
            }
        ]
    else:
        return [
            {
                "step": 1,
                "title": "Document Facts, Timeline & Preserve Evidence",
                "timeframe": "Immediate",
                "badge": "Preserve Evidence",
                "badge_color": "danger",
                "description": "Compile a detailed chronological timeline of events, dates, messages, emails, receipts, contracts, and witness information. Admissible evidence is crucial.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "Bharatiya Sakshya Adhiniyam 2023 / Indian Evidence Act"
            },
            {
                "step": 2,
                "title": "Seek Free Legal Aid via NALSA Helpline (15100)",
                "timeframe": "Within 24-48 hours",
                "badge": "Free Legal Aid",
                "badge_color": "warning",
                "description": "Contact the National Legal Services Authority (NALSA) or District Legal Services Authority (DLSA) for free consultation, legal aid eligibility check, or pre-litigation mediation.",
                "action_link": "tel:15100",
                "action_text": "Call NALSA (15100)",
                "legal_backing": "Legal Services Authorities Act, 1987 Section 12"
            },
            {
                "step": 3,
                "title": "Lodge Complaint with Appropriate Authority or Police",
                "timeframe": "As soon as possible",
                "badge": "Official Reporting",
                "badge_color": "info",
                "description": "If cognizable criminal offence or imminent harm is involved, call 112 or visit the local Police Station to register an FIR / NCR. For civil disputes, approach the competent sectoral regulator.",
                "action_link": "tel:112",
                "action_text": "Police Emergency (112)",
                "legal_backing": "Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023"
            },
            {
                "step": 4,
                "title": "Issue Formal Legal Notice to Opposite Party",
                "timeframe": "15 to 30 days notice window",
                "badge": "Pre-Litigation Notice",
                "badge_color": "secondary",
                "description": "Send a formal demand/legal notice via Registered Post A.D. or Speed Post detailing the grievance and giving reasonable opportunity to rectify the issue.",
                "action_link": "",
                "action_text": "",
                "legal_backing": "Civil Procedure Code / Specific Statutory Requirements"
            },
            {
                "step": 5,
                "title": "Institute Formal Legal Proceedings or Approach Lok Adalat",
                "timeframe": "Within statutory limitation period",
                "badge": "Judicial Remedy",
                "badge_color": "primary",
                "description": "File an application before the jurisdictional Civil/Criminal Court, Tribunal, or Lok Adalat for amicable settlement or judicial decree.",
                "action_link": "https://nalsa.gov.in",
                "action_text": "NALSA Official Portal",
                "legal_backing": "Limitation Act 1963 & Jurisdictional Act"
            }
        ]
