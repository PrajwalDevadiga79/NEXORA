"""
NyayaSathi - AI Legal Assistant & Analysis Module
Combines Gemini API (via google-genai SDK) with a verified RAG knowledge base.
Provides robust fallback to deterministic rule-based RAG demonstration mode if API key is absent.

KEY UPGRADE: Now handles ANY legal problem, not just 3 categories.
When Gemini API is available, it analyzes any legal issue and identifies relevant
IPC/BNS sections, Acts, legal provisions, and steps to take.
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

from modules.legal_retrieval import legal_retriever
from modules.issue_classifier import classify_legal_issue, detect_language
from modules.action_plan import get_action_plan
from modules.evidence_checklist import get_default_checklist


def get_gemini_client(api_key: Optional[str] = None):
    """Initializes and returns google.genai Client if valid key exists."""
    key = api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key or key.strip() == "" or "your_gemini_api_key" in key:
        return None, None
    try:
        from google import genai
        client = genai.Client(api_key=key.strip())
        return client, key.strip()
    except Exception as e:
        print(f"Error initializing Gemini client: {e}")
        return None, None


class LegalAssistant:
    """Core reasoning engine orchestrating RAG knowledge retrieval and LLM synthesis."""

    def __init__(self):
        self.retriever = legal_retriever

    def analyze_legal_problem(
        self,
        problem_text: str,
        user_selected_category: str = "auto",
        language: str = "en",
        custom_api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for analyzing a legal problem.
        1. Classifies the issue (now supports 'general' category for ANY problem).
        2. Retrieves verified Indian statutes from RAG repository if category is known.
        3. Attempts Gemini LLM synthesis if API key is active — can handle ANY legal issue.
        4. If API key missing or call fails, falls back to deterministic verified RAG mode.
        """
        # Step 1: Issue Classification
        classification_result = classify_legal_issue(problem_text, user_selected_category)
        category_id = classification_result["category_id"]

        # Step 2: Retrieve verified statutory provisions (may be empty for 'general')
        verified_provisions = self.retriever.retrieve_provisions(category_id, problem_text)
        cat_data = self.retriever.get_category_data(category_id)

        # Step 3: Check for Gemini API key
        client, active_key = get_gemini_client(custom_api_key)

        analysis_output = None
        ai_provisions = []
        provider_used = "Offline Verified RAG Engine (Zero Hallucination)"

        if client:
            try:
                analysis_output, ai_provisions = self._call_gemini_universal(
                    client=client,
                    problem_text=problem_text,
                    category_id=category_id,
                    classification_result=classification_result,
                    verified_provisions=verified_provisions,
                    language=language
                )
                if analysis_output:
                    provider_used = "Gemini 2.5 Flash + Indian Legal AI"
            except Exception as e:
                print(f"Gemini API call failed: {e}. Falling back to Rule-based RAG.")
                analysis_output = None

        # Step 4: Fallback to deterministic RAG if LLM was unavailable or failed
        if not analysis_output:
            analysis_output = self._deterministic_rag_synthesis(
                problem_text=problem_text,
                category_id=category_id,
                classification_result=classification_result,
                verified_provisions=verified_provisions,
                language=language
            )

        # If Gemini returned provisions from its analysis, merge with verified ones
        if ai_provisions:
            # Mark AI-identified provisions clearly
            for prov in ai_provisions:
                prov["verified"] = False
                prov["official_source"] = prov.get("official_source", "AI-identified (verify independently)")
            # Verified provisions first, then AI-identified ones
            all_provisions = verified_provisions + ai_provisions
        else:
            all_provisions = verified_provisions

        # Extract amount or entities for dynamic action plan
        amount_match = re.search(r"(?:₹|rs\.?|inr)\s*([\d,]+)", problem_text, re.IGNORECASE)
        amount_str = f"₹{amount_match.group(1)}" if amount_match else ""

        # Step 5: Generate Tailored Action Plan & Evidence Checklist
        action_plan = get_action_plan(category_id, language=language, details={"amount": amount_str})
        evidence_checklist = get_default_checklist(category_id, language=language)

        # For general category with Gemini, use AI-generated action plan & checklist if available
        if category_id == "general" and analysis_output:
            ai_action_plan = analysis_output.get("action_plan", [])
            ai_checklist = analysis_output.get("evidence_checklist", [])
            if ai_action_plan:
                action_plan = ai_action_plan
            if ai_checklist:
                evidence_checklist = ai_checklist

        return {
            "category_id": category_id,
            "category_name": analysis_output.get("detected_category", classification_result["category_name"]),
            "kannada_name": classification_result["kannada_name"],
            "hindi_name": classification_result["hindi_name"],
            "classification": analysis_output.get("nature_of_offence", classification_result["classification"]),
            "urgency": classification_result["urgency"],
            "urgency_badge": classification_result["urgency_badge"],
            "primary_authority": classification_result["primary_authority"],
            "confidence": classification_result["confidence"],
            "summary": analysis_output.get("summary", ""),
            "nature_of_offence": analysis_output.get("nature_of_offence", ""),
            "verified_provisions": all_provisions,
            "plain_language_guidance": analysis_output.get("plain_language_guidance", ""),
            "clarification_questions": analysis_output.get("clarification_questions", []),
            "action_plan": action_plan,
            "evidence_checklist": evidence_checklist,
            "emergency_contacts": cat_data.get("emergency_contacts", []) if cat_data else [
                {"name": "NALSA Free Legal Aid", "number": "15100", "details": "Free legal aid for eligible citizens"},
                {"name": "Police Emergency", "number": "112", "details": "For immediate safety threats"}
            ],
            "ai_provider": provider_used,
            "language": language
        }

    def _call_gemini_universal(
        self,
        client,
        problem_text: str,
        category_id: str,
        classification_result: Dict[str, Any],
        verified_provisions: List[Dict[str, Any]],
        language: str
    ) -> tuple:
        """
        Calls Gemini API with a UNIVERSAL legal analysis prompt.
        Can handle ANY legal problem — not limited to 3 categories.
        Returns (analysis_dict, ai_provisions_list).
        """
        # If we have RAG context for known categories, include it
        rag_context = ""
        if category_id != "general":
            rag_context = self.retriever.format_rag_context(category_id, problem_text)
            rag_section = f"""
VERIFIED LEGAL KNOWLEDGE BASE (use these as primary references):
{rag_context}
"""
        else:
            rag_section = """
NOTE: This problem does not fall into a pre-verified category.
You must identify the relevant Indian laws, IPC/BNS sections, and Acts from your training knowledge.
Clearly mark each provision you cite and state whether it needs independent verification.
"""

        lang_instruction = {
            "en": "Respond in clear, empathetic, plain English suitable for an Indian citizen who may not understand legal jargon.",
            "hi": "कृपया सरल, स्पष्ट हिंदी भाषा में उत्तर दें। कानूनी शब्दावली को सरल भाषा में समझाएं।",
            "kn": "ದಯವಿಟ್ಟು ಸರಳ ಮತ್ತು ಸ್ಪಷ್ಟ ಕನ್ನಡ ಭಾಷೆಯಲ್ಲಿ ಉತ್ತರಿಸಿ. ಕಾನೂನು ಪದಗಳನ್ನು ಸರಳವಾಗಿ ವಿವರಿಸಿ."
        }.get(language, "Respond in plain English.")

        prompt = f"""You are 'NyayaSathi', an expert AI legal information assistant specializing in Indian law.
You help ordinary Indian citizens understand their legal rights and the steps they should take.

A citizen has described the following legal concern:
\"\"\"{problem_text}\"\"\"

{rag_section}

LANGUAGE DIRECTIVE: {lang_instruction}

YOUR TASK — Analyze this legal problem comprehensively:

1. **Identify the legal domain**: Is this Criminal, Civil, Family, Labour, Constitutional, Consumer, Cyber, Property, or another area of law?
2. **Identify ALL relevant Indian laws and sections** that may apply:
   - IPC (Indian Penal Code) sections or BNS (Bharatiya Nyaya Sanhita 2023) sections
   - Relevant Acts (e.g., IT Act 2000, Consumer Protection Act 2019, Motor Vehicles Act, Domestic Violence Act, etc.)
   - Constitutional Articles if applicable
   - Relevant regulatory rules or government schemes
3. **Explain each law in simple language** that a common person can understand.
4. **Provide actionable steps** the citizen should take immediately and in the near future.
5. **Identify what evidence** they should collect and preserve.
6. **List important questions** they should consider or clarify before taking action.

STRICT SAFETY AND FIDELITY RULES:
- Do NOT invent fake section numbers. If you cite a section, it must be a real one.
- If you are not 100% sure about a section number, say "Section [approximate number] (verify this independently)".
- Do NOT guarantee any legal outcome, court victory, or compensation amount.
- For urgent matters (physical danger, ongoing crime), always advise calling 112 (Police) immediately.
- Always recommend consulting a qualified advocate for complex matters.
- If the problem involves a minor or domestic violence, flag it as high-priority.

Respond ONLY with a valid JSON object matching this schema:
{{
  "detected_category": "The specific legal domain/category name (e.g., 'Domestic Violence', 'Motor Vehicle Accident', 'Property Dispute', 'Labour Law Violation', 'Criminal Assault', 'Cyber Fraud', etc.)",
  "summary": "Concise 2-3 sentence summary of the citizen's situation and what kind of legal matter this is",
  "nature_of_offence": "Whether this is Criminal / Civil / Consumer / Family / Labour / Constitutional / Mixed — with brief reason",
  "plain_language_guidance": "Clear 3-5 sentence explanation of what laws protect them, what their rights are, and what the law says about their situation. Use simple language.",
  "relevant_provisions": [
    {{
      "act": "Full name of the Act",
      "section": "Section number",
      "title": "Title or short description of the section",
      "description": "What the section actually says (brief)",
      "simple_explanation": "What this means for the citizen in plain words",
      "official_source": "Source reference"
    }}
  ],
  "action_plan": [
    {{
      "step": 1,
      "title": "Title of the action step",
      "timeframe": "When to do this (e.g., 'Immediately', 'Within 24 hours', 'Within 1 week')",
      "badge": "Priority label (e.g., 'URGENT', 'IMPORTANT', 'RECOMMENDED')",
      "badge_color": "danger for urgent, warning for important, info for recommended",
      "description": "Detailed description of what to do and how",
      "action_link": "Official website URL if applicable, or empty string",
      "action_text": "Button text for the link, or empty string",
      "legal_backing": "Which law or authority backs this step"
    }}
  ],
  "evidence_checklist": [
    {{
      "id": "unique_id_for_item",
      "item": "Name of evidence to collect",
      "importance": "Mandatory / Important / Recommended",
      "details": "Why this evidence matters and how to preserve it"
    }}
  ],
  "clarification_questions": [
    "Important question 1 the citizen should consider?",
    "Important question 2?",
    "Important question 3?"
  ]
}}
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        resp_text = response.text.strip()
        # Clean potential markdown fences ```json ... ```
        if "```" in resp_text:
            resp_text = re.sub(r"^```(?:json)?\s*", "", resp_text)
            resp_text = re.sub(r"\s*```$", "", resp_text)

        parsed = json.loads(resp_text)

        # Extract AI-identified provisions separately
        ai_provisions = parsed.pop("relevant_provisions", [])

        return parsed, ai_provisions

    def _deterministic_rag_synthesis(
        self,
        problem_text: str,
        category_id: str,
        classification_result: Dict[str, Any],
        verified_provisions: List[Dict[str, Any]],
        language: str
    ) -> Dict[str, Any]:
        """
        Deterministic, zero-hallucination RAG synthesis providing comprehensive,
        accurate legal guidance tailored to the user's category and language.

        For 'general' category, provides a helpful generic response directing to legal aid.
        """
        amount_match = re.search(r"(?:₹|rs\.?|inr)\s*([\d,]+)", problem_text, re.IGNORECASE)
        amount_str = f"₹{amount_match.group(1)}" if amount_match else "the disputed funds"

        if category_id == "cyber_fraud":
            return self._cyber_fraud_response(language, amount_str)
        elif category_id == "tenant_landlord":
            return self._tenant_landlord_response(language)
        elif category_id == "consumer_complaint":
            return self._consumer_complaint_response(language)
        else:
            # GENERAL CATEGORY — handles ANY legal problem gracefully
            return self._general_response(language, problem_text)

    def _general_response(self, language: str, problem_text: str) -> Dict[str, Any]:
        """
        Provides a helpful generic response for any legal problem outside
        the 3 verified categories. Directs user to appropriate authorities
        and recommends getting a free Gemini API key for full AI analysis.
        """
        if language == "hi":
            return {
                "detected_category": "सामान्य कानूनी प्रश्न",
                "summary": "आपकी कानूनी समस्या का विश्लेषण किया जा रहा है। यह समस्या हमारी पूर्व-सत्यापित श्रेणियों (साइबर धोखाधड़ी, किरायेदारी विवाद, उपभोक्ता शिकायत) से बाहर है। पूर्ण AI विश्लेषण के लिए कृपया एक निःशुल्क Gemini API कुंजी कॉन्फ़िगर करें।",
                "nature_of_offence": "AI विश्लेषण द्वारा निर्धारित किया जाएगा। निःशुल्क Gemini API कुंजी के साथ, NyayaSathi किसी भी कानूनी समस्या का विस्तृत विश्लेषण कर सकता है।",
                "plain_language_guidance": "भारत में हर नागरिक को कानूनी सहायता का अधिकार है। आप NALSA हेल्पलाइन 15100 पर कॉल करके मुफ्त कानूनी सलाह प्राप्त कर सकते हैं। तत्काल खतरे में होने पर 112 (पुलिस) पर कॉल करें। NyayaSathi का AI इंजन किसी भी कानूनी समस्या का पूर्ण विश्लेषण करने में सक्षम है — कृपया साइडबार में निःशुल्क Gemini API कुंजी दर्ज करें (aistudio.google.com से प्राप्त करें)।",
                "clarification_questions": [
                    "क्या यह मामला आपकी व्यक्तिगत सुरक्षा से संबंधित है? यदि हां, तो तुरंत 112 पर कॉल करें।",
                    "क्या आपके पास इस मामले से संबंधित कोई लिखित दस्तावेज़, अनुबंध, या रसीद है?",
                    "क्या यह मामला किसी पुलिस स्टेशन में पहले से दर्ज है?",
                    "पूर्ण AI विश्लेषण के लिए, क्या आपने aistudio.google.com से निःशुल्क Gemini API कुंजी प्राप्त की है?"
                ]
            }
        elif language == "kn":
            return {
                "detected_category": "ಸಾಮಾನ್ಯ ಕಾನೂನು ಪ್ರಶ್ನೆ",
                "summary": "ನಿಮ್ಮ ಕಾನೂನು ಸಮಸ್ಯೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ. ಈ ಸಮಸ್ಯೆಯು ಪೂರ್ವ-ಪರಿಶೀಲಿತ ವಿಭಾಗಗಳ (ಸೈಬರ್ ವಂಚನೆ, ಬಾಡಿಗೆ ವಿವಾದ, ಗ್ರಾಹಕ ದೂರು) ಹೊರಗಿದೆ. ಸಂಪೂರ್ಣ AI ವಿಶ್ಲೇಷಣೆಗಾಗಿ ದಯವಿಟ್ಟು ಉಚಿತ Gemini API ಕೀ ಅನ್ನು ಕಾನ್ಫಿಗರ್ ಮಾಡಿ.",
                "nature_of_offence": "AI ವಿಶ್ಲೇಷಣೆಯಿಂದ ನಿರ್ಧರಿಸಲಾಗುವುದು. ಉಚಿತ Gemini API ಕೀ ಜೊತೆಗೆ, NyayaSathi ಯಾವುದೇ ಕಾನೂನು ಸಮಸ್ಯೆಯನ್ನು ವಿಸ್ತೃತವಾಗಿ ವಿಶ್ಲೇಷಿಸಬಹುದು.",
                "plain_language_guidance": "ಭಾರತದಲ್ಲಿ ಪ್ರತಿಯೊಬ್ಬ ನಾಗರಿಕನಿಗೂ ಕಾನೂನು ನೆರವು ಪಡೆಯುವ ಹಕ್ಕಿದೆ. NALSA ಸಹಾಯವಾಣಿ 15100 ಗೆ ಕರೆ ಮಾಡಿ ಉಚಿತ ಕಾನೂನು ಸಲಹೆ ಪಡೆಯಬಹುದು. ತುರ್ತು ಅಪಾಯದಲ್ಲಿದ್ದರೆ 112 (ಪೊಲೀಸ್) ಗೆ ಕರೆ ಮಾಡಿ. NyayaSathi ಯ AI ಎಂಜಿನ್ ಯಾವುದೇ ಕಾನೂನು ಸಮಸ್ಯೆಯನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ವಿಶ್ಲೇಷಿಸಬಲ್ಲದು — ಸೈಡ್‌ಬಾರ್‌ನಲ್ಲಿ ಉಚಿತ Gemini API ಕೀ ನಮೂದಿಸಿ (aistudio.google.com ನಿಂದ ಪಡೆಯಿರಿ).",
                "clarification_questions": [
                    "ಈ ಪ್ರಕರಣವು ನಿಮ್ಮ ವೈಯಕ್ತಿಕ ಸುರಕ್ಷತೆಗೆ ಸಂಬಂಧಿಸಿದೆಯೇ? ಹಾಗಿದ್ದಲ್ಲಿ, ತಕ್ಷಣ 112 ಗೆ ಕರೆ ಮಾಡಿ.",
                    "ಈ ವಿಷಯಕ್ಕೆ ಸಂಬಂಧಿಸಿದ ಯಾವುದಾದರೂ ಲಿಖಿತ ದಾಖಲೆ, ಒಪ್ಪಂದ, ಅಥವಾ ರಸೀದಿ ನಿಮ್ಮ ಬಳಿ ಇದೆಯೇ?",
                    "ಈ ಪ್ರಕರಣವನ್ನು ಈಗಾಗಲೇ ಯಾವುದಾದರೂ ಪೊಲೀಸ್ ಠಾಣೆಯಲ್ಲಿ ದಾಖಲಿಸಲಾಗಿದೆಯೇ?",
                    "ಸಂಪೂರ್ಣ AI ವಿಶ್ಲೇಷಣೆಗಾಗಿ, aistudio.google.com ನಿಂದ ಉಚಿತ Gemini API ಕೀ ಪಡೆದಿದ್ದೀರಾ?"
                ]
            }
        else:
            return {
                "detected_category": "General Legal Query",
                "summary": "Your legal problem is being analyzed. This issue falls outside NyayaSathi's pre-verified categories (Cyber Fraud, Tenant Disputes, Consumer Complaints). For a full AI-powered analysis of ANY legal problem, please configure a free Gemini API key in the sidebar.",
                "nature_of_offence": "To be determined by AI analysis. With a free Gemini API key, NyayaSathi can analyze ANY legal problem — including criminal cases, family disputes, property matters, labour issues, motor vehicle accidents, and more.",
                "plain_language_guidance": "Every Indian citizen has the right to legal assistance. You can call the NALSA Helpline at 15100 for free legal consultation. If you are in immediate danger, call 112 (Police) right away. NyayaSathi's AI engine is capable of analyzing ANY legal problem comprehensively — please enter a free Gemini API key in the sidebar (get one from aistudio.google.com at no cost). The AI will then identify relevant IPC/BNS sections, applicable Acts, your rights, and step-by-step actions.",
                "clarification_questions": [
                    "Does this matter involve your personal safety or physical harm? If yes, call 112 (Police) immediately.",
                    "Do you have any written documents, contracts, receipts, or agreements related to this matter?",
                    "Has this matter already been reported to any police station or authority?",
                    "For full AI analysis of your specific legal problem, have you obtained a free Gemini API key from aistudio.google.com?"
                ]
            }

    def _cyber_fraud_response(self, language: str, amount_str: str) -> Dict[str, Any]:
        """Deterministic response for cyber fraud category."""
        if language == "hi":
            return {
                "summary": f"उपयोगकर्ता के साथ कॉल या डिजिटल माध्यम से बैंक अधिकारी/प्रतिनिधि बनकर धोखाधड़ी की गई है, जिसके परिणामस्वरूप {amount_str} का अनधिकृत वित्तीय नुकसान हुआ है।",
                "nature_of_offence": "आपराधिक एवं नियामकीय अपराध (सूचना प्रौद्योगिकी अधिनियम एवं भारतीय न्याय संहिता के तहत गैर-जमानती वित्तीय धोखाधड़ी)।",
                "plain_language_guidance": "यह मामला सूचना प्रौद्योगिकी अधिनियम की धारा 66D (कंप्यूटर साधन द्वारा प्रतिरूपण करके धोखाधड़ी) तथा भारतीय न्याय संहिता 2023 की धारा 318(4) (धोखाधड़ी) के तहत गंभीर संज्ञेय अपराध है। आरबीआई के सर्कुलर के अनुसार, यदि आप 3 दिनों के भीतर बैंक को अनधिकृत डेबिट की सूचना देते हैं, तो आपकी वित्तीय देयता शून्य हो सकती है। 1930 पर तुरंत कॉल करने से फ्रॉड करने वाले के बैंक खाते में राशि तुरंत फ्रीज की जा सकती है।",
                "clarification_questions": [
                    "क्या आपने लेन-देन के 24 घंटे के भीतर 1930 साइबर हेल्पलाइन पर कॉल किया?",
                    "क्या आपने धोखेबाज के साथ कोई ओटीपी (OTP), यूपीआई पिन या रिमोट स्क्रीन-शेयरिंग ऐप (जैसे AnyDesk) साझा किया था?",
                    "क्या आपने अपने संबंधित बैंक की शाखा में लिखित अनधिकृत लेन-देन का विवाद दर्ज करा दिया है?",
                    "क्या आपके पास 12 अंकों का यूपीआई रेफरेंस / UTR नंबर और बैंक का एसएमएस रिकॉर्ड सुरक्षित है?"
                ]
            }
        elif language == "kn":
            return {
                "summary": f"ಬ್ಯಾಂಕ್ ಅಧಿಕಾರಿಯ ಸೋಗಿನಲ್ಲಿ ಕರೆ ಮಾಡಿ ಅಥವಾ ಡಿಜಿಟಲ್ ರೂಪದಲ್ಲಿ ವಂಚಿಸಿ {amount_str} ಮೊತ್ತವನ್ನು ಅನಧಿಕೃತವಾಗಿ ಯುಪಿಐ ಮೂಲಕ ಕಡಿತಗೊಳಿಸಲಾಗಿದೆ.",
                "nature_of_offence": "ಕ್ರಿಮಿನಲ್ ಮತ್ತು ನಿಯಂತ್ರಕ ಅಪರಾಧ (ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ ಕಾಯ್ದೆ ಮತ್ತು ಭಾರತೀಯ ನ್ಯಾಯ ಸಂಹಿತೆಯಡಿ ಜಾಮೀನು ರಹಿತ ವಂಚನೆ).",
                "plain_language_guidance": "ಈ ಪ್ರಕರಣವು ಮಾಹಿತಿ ತಂತ್ರಜ್ಞಾನ ಕಾಯ್ದೆ 2000 ರ ಕಲಂ 66D (ಕಂಪ್ಯೂಟರ್ ಸಂಪನ್ಮೂಲ ಬಳಸಿ ವಂಚನೆ) ಹಾಗೂ ಭಾರತೀಯ ನ್ಯಾಯ ಸಂಹಿತೆ 2023 ರ ಕಲಂ 318(4) ಅಡಿಯಲ್ಲಿ ಬರುತ್ತದೆ. ಆರ್‌ಬಿಐ ನಿಯಮಾವಳಿಗಳ ಪ್ರಕಾರ, 3 ದಿನಗಳ ಒಳಗೆ ನಿಮ್ಮ ಬ್ಯಾಂಕಿಗೆ ದೂರು ನೀಡಿದರೆ ಗ್ರಾಹಕರ ಹೊಣೆಗಾರಿಕೆ ಶೂನ್ಯವಾಗಿರುತ್ತದೆ. ತಕ್ಷಣವೇ 1930 ಗೆ ಕರೆ ಮಾಡುವುದರಿಂದ ವಂಚಕರ ಖಾತೆಯನ್ನು ಫ್ರೀಜ್ ಮಾಡಲು ಸಾಧ್ಯವಾಗುತ್ತದೆ.",
                "clarification_questions": [
                    "ವಂಚನೆ ನಡೆದ ತಕ್ಷಣ ಅಥವಾ 24 ಗಂಟೆಗಳ ಒಳಗೆ 1930 ಸೈಬರ್ ಸಹಾಯವಾಣಿಗೆ ಕರೆ ಮಾಡಿದ್ದೀರಾ?",
                    "ವಂಚಕರೊಂದಿಗೆ ಒಟಿಪಿ (OTP) ಅಥವಾ ಯುಪಿಐ ಪಿನ್ ಹಂಚಿಕೊಂಡಿದ್ದೀರಾ?",
                    "ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಖಾತೆಗೆ ಸಂಬಂಧಿಸಿದ ಲಿಖಿತ ದೂರನ್ನು ಬ್ಯಾಂಕ್ ಶಾಖೆಗೆ ಸಲ್ಲಿಸಿದ್ದೀರಾ?",
                    "ನಿಮ್ಮ ಬಳಿ 12 ಅಂಕಿಯ ಯುಟಿಆರ್ (UTR) ಸಂಖ್ಯೆ ಮತ್ತು ವಹಿವಾಟಿನ ಸಂದೇಶ ಲಭ್ಯವಿದೆಯೇ?"
                ]
            }
        else:
            return {
                "summary": f"The citizen reports being targeted by an impersonator posing as an official or trusted entity, resulting in an unauthorized financial loss of {amount_str} via electronic UPI transfer.",
                "nature_of_offence": "Criminal Cognizable Offence & Banking Regulatory Matter (IT Act 2000 & Bharatiya Nyaya Sanhita 2023).",
                "plain_language_guidance": "Under Indian law, impersonating an official over phone/internet to divert funds constitutes a cognizable criminal offence under Section 66D of the Information Technology Act, 2000 and Section 318(4) of the Bharatiya Nyaya Sanhita, 2023 (punishable by up to 3 to 7 years imprisonment). Furthermore, under RBI Circular DBR.No.Leg.BC.78/09.07.005/2017-18, a customer has Zero Liability if the unauthorized transaction is reported to the bank within 3 working days. Calling the 1930 National Cybercrime Helpline immediately triggers a system-wide freeze on the suspect's beneficiary account across Indian banks.",
                "clarification_questions": [
                    "Did you call the National Cyber Crime Helpline 1930 within the 'Golden Hour' (2-24 hours)?",
                    "Did you share an OTP, enter your UPI PIN, or download any screen-sharing tool (e.g. AnyDesk, RustDesk)?",
                    "Have you submitted a formal written dispute and unauthorized transaction form to your home bank branch?",
                    "Do you have the 12-digit Unique Transaction Reference (UTR) number and the fraudulent beneficiary's UPI ID / phone number preserved?"
                ]
            }

    def _tenant_landlord_response(self, language: str) -> Dict[str, Any]:
        """Deterministic response for tenant-landlord category."""
        if language == "hi":
            return {
                "summary": "किरायेदार और मकान मालिक के बीच सुरक्षा राशि (सिक्योरिटी डिपॉजिट) की वापसी, अवैधानिक कटौती अथवा बिना उचित प्रक्रिया के बेदखली का विवाद है।",
                "nature_of_offence": "दीवानी एवं संविदात्मक मामला (मॉडल किरायेदारी अधिनियम, 2021 एवं संपत्ति अंतरण अधिनियम, 1882)। यदि आवश्यक सेवाएं काटी जाएं तो यह आपराधिक धमकी का रूप ले सकता है।",
                "plain_language_guidance": "मॉडल किरायेदारी अधिनियम 2021 की धारा 11 के अनुसार मकान मालिक को किरायेदार द्वारा परिसर खाली करने पर सुरक्षा राशि (डिपॉजिट) वापस करनी होगी। धारा 20 एवं 21 के तहत मकान मालिक आवश्यक सेवाएं (जैसे बिजली, पानी) नहीं काट सकता और न ही अदालत के आदेश के बिना जबरन बेदखल कर सकता है। जबरन ताला लगाना या धमकी देना बीएनएस धारा 351 के तहत आपराधिक कृत्य है।",
                "clarification_questions": [
                    "क्या आपके पास हस्ताक्षरित एवं पंजीकृत/नोटरीकृत रेंट एग्रीमेंट की प्रति मौजूद है?",
                    "क्या मकान खाली करते समय आपने मकान मालिक को लिखित नोटिस (15-30 दिन) दिया था?",
                    "क्या आपके पास फ्लैट की स्थिति दर्शाने वाली तस्वीरें और मासिक किराया भुगतान के बैंक रिकॉर्ड हैं?",
                    "क्या मकान मालिक ने आवश्यक सेवाएं (बिजली/पानी) काटने अथवा जबरन ताला लगाने की धमकी दी है?"
                ]
            }
        elif language == "kn":
            return {
                "summary": "ಬಾಡಿಗೆದಾರ ಮತ್ತು ಮನೆ ಮಾಲೀಕರ ನಡುವೆ ಮುಂಗಡ ಠೇವಣಿ (ಸೆಕ್ಯುರಿಟಿ ಡೆಪಾಸಿಟ್) ಮರುಪಾವತಿ ಅಥವಾ ಕಾನೂನುಬಾಹಿರವಾಗಿ ಮನೆ ಖಾಲಿ ಮಾಡಿಸುವ ಕುರಿತಾದ ವಿವಾದವಾಗಿದೆ.",
                "nature_of_offence": "ಸಿವಿಲ್ ಮತ್ತು ಒಪ್ಪಂದದ ವ್ಯಾಜ್ಯ (ಮಾದರಿ ಬಾಡಿಗೆ ಕಾಯ್ದೆ 2021 ಮತ್ತು ಆಸ್ತಿ ವರ್ಗಾವಣೆ ಕಾಯ್ದೆ 1882). ಬಲಪ್ರಯೋಗ ಅಥವಾ ನೀರು/ವಿದ್ಯುತ್ ಕಡಿತಗೊಳಿಸಿದರೆ ಕ್ರಿಮಿನಲ್ ದೂರು ದಾಖಲಿಸಬಹುದು.",
                "plain_language_guidance": "ಮಾದರಿ ಬಾಡಿಗೆ ಕಾಯ್ದೆ 2021 ರ ಕಲಂ 11 ರ ಪ್ರಕಾರ, ಮನೆ ಖಾಲಿ ಮಾಡಿದ ನಂತರ ಮಾಲೀಕರು ಸೆಕ್ಯುರಿಟಿ ಡೆಪಾಸಿಟ್ ಹಣವನ್ನು ಮರಳಿಸಬೇಕು. ಕಲಂ 20 ಮತ್ತು 21 ರ ಅಡಿಯಲ್ಲಿ ಯಾವುದೇ ಮಾಲೀಕರು ನೀರು ಅಥವಾ ವಿದ್ಯುತ್ ಸಂಪರ್ಕವನ್ನು ಕಡಿತಗೊಳಿಸುವಂತಿಲ್ಲ ಮತ್ತು ನ್ಯಾಯಾಲಯದ ಆದೇಶವಿಲ್ಲದೆ ಬಲವಂತವಾಗಿ ಹೊರಹಾಕುವಂತಿಲ್ಲ. ಹಾಗೆ ಮಾಡುವುದು ಬಿಎನ್‌ಎಸ್ ಕಲಂ 351 ರ ಅಡಿಯಲ್ಲಿ ಕ್ರಿಮಿನಲ್ ಅಪರಾಧವಾಗಿದೆ.",
                "clarification_questions": [
                    "ನಿಮ್ಮ ಬಳಿ ಸಹಿ ಮಾಡಿದ ಬಾಡಿಗೆ ಕರಾರು ಪತ್ರ (ಅಗ್ರಿಮೆಂಟ್) ಇದೆಯೇ?",
                    "ಮನೆ ಖಾಲಿ ಮಾಡುವ ಮುನ್ನ ನಿಗದಿತ ನೋಟಿಸ್ (15 ರಿಂದ 30 ದಿನ) ನೀಡಿದ್ದೀರಾ?",
                    "ಬಾಡಿಗೆ ಪಾವತಿಸಿದ ಬ್ಯಾಂಕ್ ದಾಖಲೆಗಳು ಹಾಗೂ ಮನೆಯ ಸ್ಥಿತಿಯ ಫೋಟೋಗಳು ಲಭ್ಯವಿದೆಯೇ?",
                    "ಮಾಲೀಕರು ವಿದ್ಯುತ್/ನೀರು ಕಡಿತಗೊಳಿಸುವ ಅಥವಾ ಬೆದರಿಕೆ ಹಾಕುವ ಪ್ರಯತ್ನ ಮಾಡಿದ್ದಾರೆಯೇ?"
                ]
            }
        else:
            return {
                "summary": "The citizen is experiencing a tenancy dispute involving security deposit withholding, unjustified maintenance deductions, or threats of unlawful eviction.",
                "nature_of_offence": "Civil & Contractual Property Matter governed by the Model Tenancy Act, 2021 and Transfer of Property Act, 1882 (with potential criminal liability under BNS Section 351 if force or service disconnection occurs).",
                "plain_language_guidance": "Under Section 11 of the Model Tenancy Act, 2021, landlords must refund the security deposit upon the tenant vacating the premises, after providing an itemized statement for any genuine agreed deductions. Crucially, Sections 20 and 21 strictly forbid landlords from withholding essential supplies (water, electricity) or forcibly locking tenants out without due process of law. Any physical coercion or lockout is actionable under Section 6 of the Specific Relief Act, 1963 and Section 351 of the Bharatiya Nyaya Sanhita, 2023.",
                "clarification_questions": [
                    "Do you possess an executed and registered/notarized Rental/Lease Agreement?",
                    "Did you serve a formal written notice of vacation adhering to the contractual notice period?",
                    "Do you have timestamped photographs and video records documenting the undamaged condition of the property at move-out?",
                    "Has the landlord issued any written itemized breakdown justifying the withheld deposit amount?"
                ]
            }

    def _consumer_complaint_response(self, language: str) -> Dict[str, Any]:
        """Deterministic response for consumer complaint category."""
        if language == "hi":
            return {
                "summary": "उपयोगकर्ता को खरीदे गए उत्पाद/सेवा में खराबी, वारंटी सेवा में कमी या विक्रेता द्वारा रिफंड/बदलने से अनुचित इनकार का सामना करना पड़ा है।",
                "nature_of_offence": "उपभोक्ता दीवानी विवाद (उपभोक्ता संरक्षण अधिनियम, 2019 के तहत सेवा में कमी एवं अनुचित व्यापार व्यवहार)।",
                "plain_language_guidance": "उपभोक्ता संरक्षण अधिनियम 2019 की धारा 2(7) के तहत आप एक विधिक उपभोक्ता हैं, चाहे खरीदारी ऑनलाइन की गई हो या दुकान से। धारा 2(9) एवं 2(11) के तहत खराब उत्पाद बेचना या वारंटी के तहत ठीक न करना 'सेवा में कमी' (Deficiency in Service) है। आप 1915 पर राष्ट्रीय उपभोक्ता हेल्पलाइन में शिकायत दर्ज करा सकते हैं अथवा e-Daakhil पोर्टल के माध्यम से जिला उपभोक्ता फोरम में बिना वकील के भी वाद दायर कर सकते हैं।",
                "clarification_questions": [
                    "क्या आपके पास विक्रेता का वैध जीएसटी टैक्स इनवॉइस (खरीद बिल) उपलब्ध है?",
                    "क्या खराबी अधिकृत वारंटी या गारंटी अवधि के भीतर सामने आई थी?",
                    "क्या आपके पास अधिकृत सर्विस सेंटर की जॉब शीट या निरीक्षण रिपोर्ट मौजूद है?",
                    "क्या आपने कंपनी के नोडल/शिकायत अधिकारी को औपचारिक ईमेल भेजा है?"
                ]
            }
        elif language == "kn":
            return {
                "summary": "ಖರೀದಿಸಿದ ಉತ್ಪನ್ನ ಅಥವಾ ಸೇವೆಯಲ್ಲಿ ದೋಷವಿದ್ದು, ವಾರಂಟಿ ದುರಸ್ತಿ ಅಥವಾ ಹಣ ಮರುಪಾವತಿಸಲು ವ್ಯಾಪಾರಿ/ಕಂಪನಿ ನಿರಾಕರಿಸಿರುವ ಪ್ರಕರಣವಾಗಿದೆ.",
                "nature_of_offence": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಸಿವಿಲ್ ವ್ಯಾಜ್ಯ (ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2019 ರ ಅಡಿಯಲ್ಲಿ ಸೇವೆಯಲ್ಲಿ ನ್ಯೂನತೆ ಮತ್ತು ಅನುಚಿತ ವ್ಯಾಪಾರ ಪದ್ಧತಿ).",
                "plain_language_guidance": "ಗ್ರಾಹಕ ಸಂರಕ್ಷಣಾ ಕಾಯ್ದೆ 2019 ರ ಪ್ರಕಾರ ನೀವು ಆನ್‌ಲೈನ್ ಅಥವಾ ಅಂಗಡಿಯಲ್ಲಿ ಖರೀದಿಸಿದ ಪ್ರತಿಯೊಬ್ಬ ಗ್ರಾಹಕನೂ ರಕ್ಷಣೆ ಪಡೆಯಲು ಅರ್ಹರು. ಕಳಪೆ ವಸ್ತು ನೀಡುವುದು ಅಥವಾ ವಾರಂಟಿ ಸೇವೆ ನೀಡದಿರುವುದು 'ಸೇವೆಯಲ್ಲಿ ನ್ಯೂನತೆ' (Deficiency in Service) ಆಗಿದೆ. ನೀವು 1915 ಗೆ ಕರೆ ಮಾಡಿ ರಾಷ್ಟ್ರೀಯ ಗ್ರಾಹಕ ಸಹಾಯವಾಣಿಗೆ ದೂರು ನೀಡಬಹುದು ಅಥವಾ e-Daakhil ಮೂಲಕ ಜಿಲ್ಲಾ ಗ್ರಾಹಕ ನ್ಯಾಯಾಲಯಕ್ಕೆ ಯಾವುದೇ ವಕೀಲರಿಲ್ಲದೆ ಸ್ವತಃ ದೂರು ದಾಖಲಿಸಬಹುದು.",
                "clarification_questions": [
                    "ನಿಮ್ಮ ಬಳಿ ಖರೀದಿಸಿದ ಅಧಿಕೃತ ಜಿಎಸ್‌ಟಿ ತೆರಿಗೆ ಬಿಲ್ (ಇನ್‌ವಾಯ್ಸ್) ಲಭ್ಯವಿದೆಯೇ?",
                    "ಉತ್ಪನ್ನದ ದೋಷವು ವಾರಂಟಿ ಅವಧಿಯ ಒಳಗಾಗಿಯೇ ಸಂಭವಿಸಿದೆಯೇ?",
                    "ಅಧಿಕೃತ ಸರ್ವಿಸ್ ಸೆಂಟರ್‌ನಿಂದ ನೀಡಲಾದ ತಪಾಸಣಾ ರಸೀದಿ (ಜಾಬ್ ಶೀಟ್) ಇದೆಯೇ?",
                    "ಕಂಪನಿಯ ಗ್ರಾಹಕ ಸೇವಾ ಅಧಿಕಾರಿಗೆ ಲಿಖಿತವಾಗಿ ಇಮೇಲ್ ಮೂಲಕ ದೂರು ನೀಡಿದ್ದೀರಾ?"
                ]
            }
        else:
            return {
                "summary": "The citizen has purchased goods or contracted a service that is defective, sub-standard, or where the merchant/manufacturer has wrongfully refused repair, replacement, or refund.",
                "nature_of_offence": "Civil Consumer Protection Matter governed by the Consumer Protection Act, 2019 (Deficiency in Service & Unfair Trade Practice).",
                "plain_language_guidance": "Under Section 2(7) of the Consumer Protection Act, 2019, any individual who purchases goods or avails services for consideration (online via platforms like Amazon/Flipkart or offline) is protected as a Consumer. Delivering a defective product or failing to honor warranty repairs constitutes 'Defect in Goods' (Section 2(9)) and 'Deficiency in Service' (Section 2(11)). Consumers have the legal right to approach the National Consumer Helpline (1915) or file an electronic case via the e-Daakhil portal (edaakhil.nic.in) before the District Consumer Disputes Redressal Commission (DCDRC) within a 2-year limitation period.",
                "clarification_questions": [
                    "Do you possess the original retail tax invoice showing GSTIN, date, and serial number?",
                    "Did the defect manifest within the manufacturer's active warranty period?",
                    "Do you have inspection receipts or job sheets issued by an authorized service center?",
                    "Have you documented the defect with clear photographs or unboxing video recordings?"
                ]
            }


# Singleton instance
legal_assistant = LegalAssistant()
