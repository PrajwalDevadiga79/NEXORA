"""
NyayaSathi - Evidence Checklist Generator Module
Creates comprehensive, categorized evidence collection checklists tailored to Indian legal disputes.
Enables citizens to preserve admissible electronic and documentary evidence.
"""

from typing import Dict, List, Any


def get_default_checklist(category_id: str, language: str = "en") -> List[Dict[str, Any]]:
    """
    Returns structured checklist items with importance levels, guidance tips, and evidence types.
    """
    if category_id == "criminal_offences":
        return [
            {
                "id": "mlc_report",
                "item": "Medico-Legal Certificate (MLC) & Hospital Discharge Summary",
                "importance": "Mandatory Forensic Proof",
                "details": "Original MLC issued by the government hospital casualty doctor detailing the nature, depth, and weapon type of knife wounds."
            },
            {
                "id": "injury_photos",
                "item": "Clear Photographic & Video Evidence of Physical Injuries",
                "importance": "Crucial Admissible Evidence",
                "details": "High-resolution photos taken from multiple angles showing knife cuts, stab wounds, bandages, and bodily trauma before healing."
            },
            {
                "id": "gold_invoices",
                "item": "Original Invoices, Hallmark Certificates & Photos of Stolen Gold",
                "importance": "Mandatory for Recovery & Valuation",
                "details": "Jeweller purchase bills, BIS hallmark receipts, photographs of family members wearing the stolen jewellery, and itemized weight list."
            },
            {
                "id": "crime_scene_photos",
                "item": "Photographs of Broken Locks, Forcible Entry & Ransacked Property",
                "importance": "High Importance (House-Breaking Proof)",
                "details": "Photos of forced door latches, broken window grills, damaged cupboards, and footprint/fingerprint areas before disturbance."
            },
            {
                "id": "cctv_footage",
                "item": "CCTV Footage & Digital Video Recordings (Pen Drive / Cloud)",
                "importance": "Crucial for Offender Identification",
                "details": "Unedited video backup from your home security cameras, building entryway, elevator, or neighboring commercial shops along escape route."
            },
            {
                "id": "fir_copy",
                "item": "Official Signed & Stamped Copy of Registered FIR",
                "importance": "Mandatory Statutory Record",
                "details": "Ensure police provide a stamped, signed copy of the FIR under BNSS Section 173 with proper sections (BNS 309, 118, 331)."
            },
            {
                "id": "witness_details",
                "item": "Names, Phone Numbers & Statements of Eyewitnesses / Neighbors",
                "importance": "Corroborative Evidence",
                "details": "Contact details of family members present, security guards, neighbors who heard commotion or saw fleeing offenders."
            }
        ]

    if category_id == "cyber_fraud":
        if language == "hi":
            return [
                {
                    "id": "bank_statement",
                    "item": "बैंक खाता विवरण (बैंक स्टेटमेंट)",
                    "importance": "अनिवार्य",
                    "details": "धोखाधड़ी वाले लेन-देन को हाइलाइट करता हुआ आधिकारिक बैंक स्टेटमेंट (पीडीएफ या मुद्रित)।"
                },
                {
                    "id": "utr_number",
                    "item": "यूपीआई संदर्भ / UTR नंबर और लेन-देन आईडी",
                    "importance": "अनिवार्य",
                    "details": "12 अंकों का यूपीआई संदर्भ नंबर (UTR) जो पैसे ट्रांसफर होने पर एसएमएस या ऐप पर मिलता है।"
                },
                {
                    "id": "fraudster_details",
                    "item": "धोखेबाज का मोबाइल नंबर / यूपीआई आईडी / बैंक विवरण",
                    "importance": "अत्यंत महत्वपूर्ण",
                    "details": "धोखेबाज का फोन नंबर, वीपीए (VPA) जैसे xyz@okaxis, अथवा प्राप्तकर्ता खाता संख्या।"
                },
                {
                    "id": "chat_screenshots",
                    "item": "व्हाट्सएप, एसएमएस और कॉल हिस्ट्री के स्क्रीनशॉट",
                    "importance": "महत्वपूर्ण",
                    "details": "धोखेबाज के साथ बातचीत, फर्जी लिंक (URL), या फर्जी ऐप का स्क्रीनशॉट।"
                },
                {
                    "id": "bank_complaint_copy",
                    "item": "बैंक में दी गई शिकायत की पावती / ईमेल प्रति",
                    "importance": "अनिवार्य",
                    "details": "आरबीआई शून्य देयता का दावा करने हेतु बैंक को 3 दिनों में भेजी गई लिखित शिकायत का प्रमाण।"
                },
                {
                    "id": "cybercrime_acknowledgment",
                    "item": "1930 / cybercrime.gov.in शिकायत संख्या (एक्नॉलेजमेंट)",
                    "importance": "अनिवार्य",
                    "details": "राष्ट्रीय साइबर अपराध पोर्टल द्वारा जारी पावती रसीद व टोकन नंबर।"
                }
            ]
        elif language == "kn":
            return [
                {
                    "id": "bank_statement",
                    "item": "ಬ್ಯಾಂಕ್ ಖಾತೆಯ ವಿವರ (ಸ್ಟೇಟ್‌ಮೆಂಟ್)",
                    "importance": "ಕಡ್ಡಾಯ",
                    "details": "ವಂಚನೆ ನಡೆದ ವಹಿವಾಟನ್ನು ಗುರುತಿಸಿದ ಬ್ಯಾಂಕ್ ಸ್ಟೇಟ್‌ಮೆಂಟ್ ಪ್ರತಿ."
                },
                {
                    "id": "utr_number",
                    "item": "ಯುಪಿಐ ರೆಫರೆನ್ಸ್ / ಯುಟಿಆರ್ (UTR) ಸಂಖ್ಯೆ",
                    "importance": "ಕಡ್ಡಾಯ",
                    "details": "ಹಣ ವರ್ಗಾವಣೆಯಾದ 12 ಅಂಕಿಯ ಯುಟಿಆರ್ ಸಂಖ್ಯೆ ಮತ್ತು ವಹಿವಾಟು ಐಡಿ."
                },
                {
                    "id": "fraudster_details",
                    "item": "ವಂಚಕನ ಮೊಬೈಲ್ ಸಂಖ್ಯೆ ಮತ್ತು ಯುಪಿಐ ವಿಳಾಸ",
                    "importance": "ಅತ್ಯಂತ ಮುಖ್ಯ",
                    "details": "ಕರೆ ಮಾಡಿದವರ ದೂರವಾಣಿ ಸಂಖ್ಯೆ, ಯುಪಿಐ ಐಡಿ ಅಥವಾ ಖಾತೆಯ ವಿವರಗಳು."
                },
                {
                    "id": "chat_screenshots",
                    "item": "ವಾಟ್ಸಾಪ್, ಮೆಸೇಜ್ ಮತ್ತು ಕರೆ ಇತಿಹಾಸದ ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ಗಳು",
                    "importance": "ಮುಖ್ಯ",
                    "details": "ವಂಚಕರ ಸಂದೇಶಗಳು, ನಕಲಿ ಲಿಂಕ್‌ಗಳು ಅಥವಾ ಅಪ್ಲಿಕೇಶನ್‌ಗಳ ಸಾಕ್ಷ್ಯಗಳು."
                },
                {
                    "id": "bank_complaint_copy",
                    "item": "ಬ್ಯಾಂಕಿಗೆ ನೀಡಿದ ದೂರಿನ ಸ್ವೀಕೃತಿ ಪತ್ರ",
                    "importance": "ಕಡ್ಡಾಯ",
                    "details": "ಆರ್‌ಬಿಐ ನಿಯಮದಂತೆ 3 ದಿನಗಳ ಒಳಗೆ ಬ್ಯಾಂಕಿಗೆ ಸಲ್ಲಿಸಿದ ಲಿಖಿತ ದೂರಿನ ಪ್ರತಿ."
                },
                {
                    "id": "cybercrime_acknowledgment",
                    "item": "1930 / cybercrime.gov.in ದೂರಿನ ಸಂಖ್ಯೆ (ಸ್ವೀಕೃತಿ)",
                    "importance": "ಕಡ್ಡಾಯ",
                    "details": "ರಾಷ್ಟ್ರೀಯ ಸೈಬರ್ ಪೋರ್ಟಲ್ ನೀಡಿದ ದೂರು ಸಂಖ್ಯೆ ಮತ್ತು ಎಫ್‌ಐಆರ್ ದಾಖಲೆ."
                }
            ]
        else:
            return [
                {
                    "id": "bank_statement",
                    "item": "Bank Account Statement highlighting Debit Transaction",
                    "importance": "Mandatory",
                    "details": "Official stamped bank statement or e-statement clearly showing the unauthorized debit, date, time, and debit amount."
                },
                {
                    "id": "utr_number",
                    "item": "UPI Reference ID (UTR) & Bank Transaction Reference",
                    "importance": "Mandatory",
                    "details": "The 12-digit Unique Transaction Reference (UTR) number generated for UPI/IMPS transfers, needed by 1930 operators to freeze accounts."
                },
                {
                    "id": "fraudster_details",
                    "item": "Beneficiary / Impersonator Details (VPA, Account, Phone)",
                    "importance": "Crucial",
                    "details": "Beneficiary UPI VPA (e.g. merchant@ybl), recipient account number, IFSC, and suspect caller's mobile numbers."
                },
                {
                    "id": "chat_screenshots",
                    "item": "Screenshots of SMS, WhatsApp, Fake Links, or Remote Apps",
                    "importance": "High",
                    "details": "Clear screenshots showing fraudulent URLs, fake payment QR codes, APK file names, and conversation timestamps."
                },
                {
                    "id": "bank_complaint_copy",
                    "item": "Copy of Written Dispute Form / Email to Bank",
                    "importance": "Mandatory",
                    "details": "Dated proof that you notified your bank within 3 days to invoke RBI Zero Liability protection."
                },
                {
                    "id": "cybercrime_acknowledgment",
                    "item": "Cybercrime Portal (1930) Acknowledgement Receipt",
                    "importance": "Mandatory",
                    "details": "Official Acknowledgement Slip / Complaint Number generated from cybercrime.gov.in."
                }
            ]

    elif category_id == "tenant_landlord":
        if language == "hi":
            return [
                {
                    "id": "rent_agreement",
                    "item": "मूल रेंट एग्रीमेंट (किराया अनुबंध पत्र)",
                    "importance": "अनिवार्य",
                    "details": "दोनों पक्षों द्वारा हस्ताक्षरित एवं पंजीकृत अथवा नोटरीकृत रेंट एग्रीमेंट।"
                },
                {
                    "id": "deposit_receipt",
                    "item": "सुरक्षा राशि (डिपॉजिट) भुगतान का बैंक प्रमाण",
                    "importance": "अनिवार्य",
                    "details": "मकान मालिक को दिए गए सिक्योरिटी डिपॉजिट का बैंक ट्रांसफर, चेक या रसीद।"
                },
                {
                    "id": "rent_records",
                    "item": "मासिक किराया भुगतान के निरंतर बैंक रिकॉर्ड",
                    "importance": "उच्च",
                    "details": "यह सिद्ध करने हेतु कि आप समय पर किराया चुकाने वाले नियमित किरायेदार हैं।"
                },
                {
                    "id": "property_condition",
                    "item": "मकान खाली करते समय की तस्वीरें एवं वीडियो",
                    "importance": "उच्च",
                    "details": "यह साबित करने हेतु कि संपत्ति को कोई नुकसान नहीं हुआ है और अवैध कटौती गलत है।"
                },
                {
                    "id": "written_notices",
                    "item": "नोटिस, व्हाट्सएप संदेश एवं ईमेल पत्राचार",
                    "importance": "महत्वपूर्ण",
                    "details": "मकान खाली करने की पूर्व सूचना या मकान मालिक के अनुचित संदेशों का स्क्रीनशॉट।"
                }
            ]
        else:
            return [
                {
                    "id": "rent_agreement",
                    "item": "Original Signed Tenancy / Rental Agreement",
                    "importance": "Mandatory",
                    "details": "Registered or notarized lease deed showing security deposit clause, notice period, and maintenance provisions."
                },
                {
                    "id": "deposit_receipt",
                    "item": "Bank Proof / Receipt of Security Deposit Paid",
                    "importance": "Mandatory",
                    "details": "NetBanking transfer receipt, cheque record, or signed acknowledgment showing initial deposit amount paid."
                },
                {
                    "id": "rent_records",
                    "item": "Bank Statements Showing Timely Monthly Rent Transfers",
                    "importance": "High",
                    "details": "Clear bank records proving no rent defaults or arrears exist on the tenant's side."
                },
                {
                    "id": "property_condition",
                    "item": "Photographs & Video Inspection of Vacated Premises",
                    "importance": "High",
                    "details": "Dated high-resolution photos and video walkthrough proving the flat was left in clean, undamaged condition."
                },
                {
                    "id": "written_notices",
                    "item": "Copies of Eviction Notice, Vacation Notice, and Chat Logs",
                    "importance": "Crucial",
                    "details": "WhatsApp chats, email exchanges, and postal receipts regarding move-out notice, key handover, and deposit discussions."
                }
            ]

    else:  # consumer_complaint
        if language == "hi":
            return [
                {
                    "id": "tax_invoice",
                    "item": "मूल टैक्स इनवॉइस / खरीद बिल",
                    "importance": "अनिवार्य",
                    "details": "विक्रेता का नाम, जीएसटी नंबर, उत्पाद विवरण और खरीद तिथि दर्शाने वाला पक्का बिल।"
                },
                {
                    "id": "warranty_card",
                    "item": "वारंटी कार्ड एवं नियम पुस्तिका",
                    "importance": "उच्च",
                    "details": "निर्माता द्वारा दी गई वारंटी अवधि व शर्तों का आधिकारिक कार्ड।"
                },
                {
                    "id": "defect_evidence",
                    "item": "खराबी की तस्वीरें और कार्य न करने का वीडियो",
                    "importance": "उच्च",
                    "details": "उत्पाद में खराबी या पैकेजिंग क्षति को स्पष्ट रूप से दर्शाने वाले वीडियो या फोटो।"
                },
                {
                    "id": "service_sheets",
                    "item": "सर्विस सेंटर जॉब शीट / निरीक्षण रिपोर्ट",
                    "importance": "अत्यंत महत्वपूर्ण",
                    "details": "अधिकृत सर्विस सेंटर द्वारा दी गई जॉब शीट जिसमें बार-बार खराबी दर्ज हो।"
                },
                {
                    "id": "support_communications",
                    "item": "ग्राहक सेवा ईमेल, शिकायत टिकट एवं चैट रिकॉर्ड",
                    "importance": "अनिवार्य",
                    "details": "कंपनी के साथ समाधान हेतु किए गए पत्राचार और उनके द्वारा रिफंड/बदलने से इनकार का प्रमाण।"
                }
            ]
        else:
            return [
                {
                    "id": "tax_invoice",
                    "item": "Original Retail Tax Invoice / Purchase Bill",
                    "importance": "Mandatory",
                    "details": "Valid tax invoice containing GSTIN, seller address, product serial number, price paid, and transaction date."
                },
                {
                    "id": "warranty_card",
                    "item": "Official Warranty Card / Certificate",
                    "importance": "High",
                    "details": "Manufacturer warranty booklet specifying warranty period, terms, and coverage exclusions."
                },
                {
                    "id": "defect_evidence",
                    "item": "Photographs & Video Recording of Defect / Malfunction",
                    "importance": "High",
                    "details": "Unboxing video (for online orders) or video clearly capturing the hardware/software malfunction or non-performance."
                },
                {
                    "id": "service_sheets",
                    "item": "Authorized Service Center Job Sheets & Inspection Slips",
                    "importance": "Crucial",
                    "details": "Job sheets proving repeat service visits, unresolved defects, or technician inspection reports."
                },
                {
                    "id": "support_communications",
                    "item": "Email Correspondence, Ticket Numbers & Refusal Letters",
                    "importance": "Mandatory",
                    "details": "Written proof of grievance submission, customer support ticket numbers, and company's refusal to refund or replace."
                }
            ]

    # GENERAL CATEGORY FALLBACK (Covers any other legal situation)
    if language == "hi":
        return [
            {
                "id": "gen_chronology",
                "item": "घटना का तिथिवार विवरण (Timeline/Chronology of Events)",
                "importance": "अनिवार्य",
                "details": "घटना कब, कहां और कैसे घटी, उसका सिलसिलेवार लिखित विवरण।"
            },
            {
                "id": "gen_contracts_receipts",
                "item": "समझौते, अनुबंध, चालान या लेन-देन की रसीदें",
                "importance": "अनिवार्य",
                "details": "विवाद से जुड़े सभी हस्ताक्षरित दस्तावेज, बैंक रसीद या भुगतान के प्रमाण।"
            },
            {
                "id": "gen_communications",
                "item": "संदेश, ईमेल, कॉल रिकॉर्ड एवं चैट स्क्रीनशॉट",
                "importance": "अत्यंत महत्वपूर्ण",
                "details": "दोनों पक्षों के बीच हुए सभी लिखित या डिजिटल संवाद का सुरक्षित रिकॉर्ड।"
            },
            {
                "id": "gen_identity_proof",
                "item": "पहचान पत्र एवं पते का प्रमाण (आधार/पैन/वोटर आईडी)",
                "importance": "अनिवार्य",
                "details": "शिकायतकर्ता और यथासंभव विपक्षी पक्ष की पहचान के प्रमाण।"
            },
            {
                "id": "gen_witnesses",
                "item": "गवाहों के नाम, संपर्क व लिखित बयान (यदि उपलब्ध हो)",
                "importance": "महत्वपूर्ण",
                "details": "घटना के समय मौजूद स्वतंत्र व्यक्तियों या संबंधित पक्षों की जानकारी।"
            }
        ]
    elif language == "kn":
        return [
            {
                "id": "gen_chronology",
                "item": "ಘಟನೆಗಳ ದಿನಾಂಕವಾರು ವಿವರ (ಕಾಲಾನುಕ್ರಮ ಪಟ್ಟಿ)",
                "importance": "ಕಡ್ಡಾಯ",
                "details": "ಘಟನೆ ನಡೆದ ವಿವರ, ದಿನಾಂಕ, ಸಮಯ ಮತ್ತು ಸ್ಥಳದ ನಿಖರ ಲಿಖಿತ ದಾಖಲೆ."
            },
            {
                "id": "gen_contracts_receipts",
                "item": "ಕರಾರು ಪತ್ರ, ಬಿಲ್, ರಸೀದಿಗಳು ಮತ್ತು ಪಾವತಿ ದಾಖಲೆಗಳು",
                "importance": "ಕಡ್ಡಾಯ",
                "details": "ವಿವಾದಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಎಲ್ಲಾ ಒಪ್ಪಂದಗಳು ಮತ್ತು ಹಣಕಾಸಿನ ವಹಿವಾಟು ದಾಖಲೆಗಳು."
            },
            {
                "id": "gen_communications",
                "item": "ಇಮೇಲ್, ವಾಟ್ಸಾಪ್ ಸಂದೇಶಗಳು ಹಾಗೂ ಕರೆ ವಿವರಗಳು",
                "importance": "ಅತ್ಯಂತ ಮುಖ್ಯ",
                "details": "ಪರಸ್ಪರ ನಡೆಸಲಾದ ಎಲ್ಲಾ ಸಂವಹನಗಳ ಸ್ಕ್ರೀನ್‌ಶಾಟ್‌ಗಳು ಮತ್ತು ದಾಖಲೆಗಳು."
            },
            {
                "id": "gen_identity_proof",
                "item": "ಗುರುತಿನ ಚೀಟಿ ಮತ್ತು ವಿಳಾಸದ ಪುರಾವೆ",
                "importance": "ಕಡ್ಡಾಯ",
                "details": "ದೂರುದಾರರ ಮತ್ತು ಸಾಧ್ಯವಾದರೆ ಎದುರುದಾರರ ಅಧಿಕೃತ ಗುರುತಿನ ಚೀಟಿ."
            },
            {
                "id": "gen_witnesses",
                "item": "ಸಾಕ್ಷಿದಾರರ ಹೆಸರು, ಸಂಪರ್ಕ ಮತ್ತು ವಿವರಣೆ",
                "importance": "ಮುಖ್ಯ",
                "details": "ಘಟನೆಗೆ ಸಾಕ್ಷಿಯಾದ ವ್ಯಕ್ತಿಗಳ ವಿವರ ಮತ್ತು ಸಂಪರ್ಕ ಸಂಖ್ಯೆ."
            }
        ]
    else:
        return [
            {
                "id": "gen_chronology",
                "item": "Chronological Summary of Events & Incident Log",
                "importance": "Mandatory",
                "details": "Clear, dated sequence of all events, interactions, verbal agreements, or occurrences leading to the dispute."
            },
            {
                "id": "gen_contracts_receipts",
                "item": "Agreements, Contracts, Invoices, or Payment Proofs",
                "importance": "Mandatory",
                "details": "Any formal agreement, MOU, bill, bank transaction statement, or receipt directly establishing the legal relationship."
            },
            {
                "id": "gen_communications",
                "item": "Electronic Communications (Emails, SMS, WhatsApp Chats)",
                "importance": "Crucial",
                "details": "Exported chat histories, email threads, voice notes, or SMS with timestamps intact (admissible under BSA 2023)."
            },
            {
                "id": "gen_identity_proof",
                "item": "Identity and Address Verification of Parties",
                "importance": "Mandatory",
                "details": "Official government ID (Aadhaar, Passport, Voter ID) and identifiable details of the opposite party."
            },
            {
                "id": "gen_witnesses",
                "item": "Witness Information & Supporting Photographic/Audio Proof",
                "importance": "Important",
                "details": "Contact details of independent witnesses, photos, CCTV footage, or audio recordings relevant to the incident."
            }
        ]
