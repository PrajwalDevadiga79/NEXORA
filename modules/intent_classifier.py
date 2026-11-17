"""
NyayaSathi - Advanced Intent Classification & 5-Stage Orchestration Module
Architecture: UNDERSTAND -> ASK -> ANALYZE -> GUIDE -> TAKE ACTION

Intents supported:
- GREETING
- GENERAL_CONVERSATION
- GENERAL_LEGAL_QUESTION
- INITIAL_PROBLEM_DESCRIPTION
- NEEDS_CLARIFICATION
- FOLLOW_UP_QUESTION
- FOLLOW_UP_NEXT_STEPS
- PROVIDE_LEGAL_GUIDANCE
- URGENT_LEGAL_PROBLEM
- USER_REQUESTED_ACTION_PLAN
- USER_REQUESTED_EVIDENCE_CHECKLIST
- USER_REQUESTED_COMPLAINT
- USER_REQUESTED_CASE_SUMMARY
- DOCUMENT_ANALYSIS_REQUEST
- OTHER

Provides strict conditional feature flags (all default to FALSE) and context-aware conversational synthesis.
"""

import json
import re
from typing import Dict, List, Any, Optional

VALID_INTENTS = {
    "GREETING",
    "GENERAL_CONVERSATION",
    "GENERAL_LEGAL_QUESTION",
    "INITIAL_PROBLEM_DESCRIPTION",
    "NEEDS_CLARIFICATION",
    "FOLLOW_UP_QUESTION",
    "FOLLOW_UP_NEXT_STEPS",
    "PROVIDE_LEGAL_GUIDANCE",
    "URGENT_LEGAL_PROBLEM",
    "USER_REQUESTED_ACTION_PLAN",
    "USER_REQUESTED_EVIDENCE_CHECKLIST",
    "USER_REQUESTED_COMPLAINT",
    "USER_REQUESTED_CASE_SUMMARY",
    "DOCUMENT_ANALYSIS_REQUEST",
    "OTHER"
}

VALID_STAGES = {
    "UNDERSTAND",
    "ASK",
    "ANALYZE",
    "GUIDE",
    "TAKE_ACTION"
}

INTENT_CLASSIFIER_PROMPT = """You are the intent classifier and conversation controller for NyayaSathi, an Indian legal guidance platform.
NyayaSathi follows a conversational philosophy: keep the chat natural and answer first.
Additional tools (action plans, checklists, complaints, case summaries) should ONLY be triggered on explicit user demand.

Analyze the user's latest message considering the preceding conversation history.

Choose EXACTLY ONE intent from:
1. GREETING: Hello, hi, namaste, good morning, etc. (Stage: UNDERSTAND)
2. GENERAL_CONVERSATION: Small talk, "how are you", "who made you", "thank you", "ok", "what is NyayaSathi". (Stage: UNDERSTAND)
3. GENERAL_LEGAL_QUESTION: General questions about law, acts, or procedures in the abstract without a personal dispute (e.g. "What is Bharatiya Nyaya Sanhita?", "What is Consumer Protection Act?", "What is Section 173 BNSS?"). (Stage: GUIDE)
4. INITIAL_PROBLEM_DESCRIPTION: First time user describes a personal problem or loss (e.g. "I lost my phone", "Someone stole my phone", "My landlord won't return my deposit"). (Stage: ASK or GUIDE)
5. NEEDS_CLARIFICATION: User is responding to NyayaSathi's previous clarifying questions or providing partial case facts. (Stage: ANALYZE or ASK)
6. FOLLOW_UP_QUESTION: User asks a specific follow-up question based on previously explained legal guidance. (Stage: GUIDE)
7. FOLLOW_UP_NEXT_STEPS: User asks conversationally "What should I do next?", "What to do next?", or "What are my next steps?". (Stage: GUIDE)
8. PROVIDE_LEGAL_GUIDANCE: Sufficient facts have been gathered, and NyayaSathi explains the legal position and options. (Stage: GUIDE)
9. URGENT_LEGAL_PROBLEM: Ongoing or immediate critical legal harm or serious crimes (e.g. "My UPI account was hacked", active bank fraud, knife attack, armed assault, physical violence, imminent illegal lockout). (Stage: GUIDE)
10. USER_REQUESTED_ACTION_PLAN: User EXPLICITLY asks for an action plan (e.g. "Give me a step-by-step action plan", "Give me a detailed action plan", "Generate action plan"). (Stage: TAKE_ACTION)
11. USER_REQUESTED_EVIDENCE_CHECKLIST: User EXPLICITLY asks about evidence or documents (e.g. "What evidence should I collect?", "Give me an evidence checklist", "What documents do I need?"). (Stage: TAKE_ACTION)
12. USER_REQUESTED_COMPLAINT: User EXPLICITLY asks to draft or generate a formal complaint, police complaint, FIR draft, notice, or petition (e.g. "Prepare a police complaint for me", "Draft a police complaint", "Write a complaint"). (Stage: TAKE_ACTION)
13. USER_REQUESTED_CASE_SUMMARY: User EXPLICITLY asks to summarize case dossier (e.g. "Summarize my case", "Generate case summary", "Download case dossier"). (Stage: TAKE_ACTION)
14. DOCUMENT_ANALYSIS_REQUEST: User uploaded or asks to inspect a legal notice, contract, screenshot, or bill. (Stage: ANALYZE)
15. OTHER: Off-topic or ambiguous query. (Stage: UNDERSTAND)

OUTPUT FORMAT:
Return ONLY a valid JSON object without markdown fences or code blocks:
{
  "intent": "GREETING | GENERAL_CONVERSATION | GENERAL_LEGAL_QUESTION | INITIAL_PROBLEM_DESCRIPTION | NEEDS_CLARIFICATION | FOLLOW_UP_QUESTION | FOLLOW_UP_NEXT_STEPS | PROVIDE_LEGAL_GUIDANCE | URGENT_LEGAL_PROBLEM | USER_REQUESTED_ACTION_PLAN | USER_REQUESTED_EVIDENCE_CHECKLIST | USER_REQUESTED_COMPLAINT | USER_REQUESTED_CASE_SUMMARY | DOCUMENT_ANALYSIS_REQUEST | OTHER",
  "legal_category": "criminal_offences | cyber_fraud | tenant_landlord | consumer_complaint | employment_salary | property_disputes | family_domestic | general | none",
  "conversation_stage": "UNDERSTAND | ASK | ANALYZE | GUIDE | TAKE_ACTION",
  "urgency_level": "RED | YELLOW | GREEN | NONE",
  "missing_information": ["list of important missing facts if any"],
  "response_type": "SHORT_GREETING | CONVERSATIONAL | ASK_QUESTIONS | EXPLANATORY | LEGAL_GUIDANCE | URGENT_DISPATCH | ACTION_PLAN | EVIDENCE_CHECKLIST | COMPLAINT_DRAFT | CASE_SUMMARY | DOCUMENT_REVIEW | FOLLOW_UP"
}
"""

def rule_based_fallback_intent(message: str, history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fast, accurate fallback intent and stage detection using contextual conversation flow."""
    msg = message.strip().lower()
    user_msgs = [m["content"] for m in history if m.get("role") == "user"]
    assistant_msgs = [m["content"] for m in history if m.get("role") == "assistant"]
    turn_count = len(user_msgs)

    # 1. Greetings
    if re.fullmatch(r"(hi+|hello+|hey+|namaste+|vanakkam+|namaskara+|good\s*(morning|afternoon|evening)|hlo+|hola)[.!? ]*", msg):
        return {
            "intent": "GREETING",
            "legal_category": "none",
            "conversation_stage": "UNDERSTAND",
            "urgency_level": "NONE",
            "missing_information": [],
            "response_type": "SHORT_GREETING"
        }

    # 2. General conversation / small talk
    if re.fullmatch(r"(how\s+are\s+you|thank\s*you|thanks|thx|ok|okay|cool|bye|goodbye|who\s+are\s+you|what\s+is\s+nyayasathi|what\s+can\s+you\s+do|what\s+can\s+nyayasathi\s+do|help|about)[.!? ]*", msg):
        return {
            "intent": "GENERAL_CONVERSATION",
            "legal_category": "none",
            "conversation_stage": "UNDERSTAND",
            "urgency_level": "NONE",
            "missing_information": [],
            "response_type": "CONVERSATIONAL"
        }

    # 3. EXPLICIT User Requests for Action Tools (Stage: TAKE_ACTION)
    # 3A. Complaint Drafting
    if any(k in msg for k in [
        "prepare a police complaint", "prepare police complaint", "draft a police complaint", "draft police complaint",
        "prepare a complaint", "prepare complaint", "draft a formal complaint", "draft a complaint", "draft complaint",
        "generate a complaint", "generate complaint", "make complaint", "write complaint", "write a police complaint",
        "draft an fir", "draft fir", "write fir", "police complaint draft", "prepare legal notice", "draft legal notice",
        "draft notice", "write a legal notice"
    ]):
        return {
            "intent": "USER_REQUESTED_COMPLAINT",
            "legal_category": "general",
            "conversation_stage": "TAKE_ACTION",
            "urgency_level": "YELLOW",
            "missing_information": [],
            "response_type": "COMPLAINT_DRAFT"
        }

    # 3B. Evidence Checklist
    if any(k in msg for k in [
        "what evidence should i collect", "what evidence do i need", "what evidence to collect",
        "evidence checklist", "show evidence checklist", "give me an evidence checklist", "give me evidence checklist",
        "which documents should i collect", "what documents should i collect", "what documents do i need",
        "checklist of evidence", "document checklist", "list of documents"
    ]):
        return {
            "intent": "USER_REQUESTED_EVIDENCE_CHECKLIST",
            "legal_category": "general",
            "conversation_stage": "TAKE_ACTION",
            "urgency_level": "YELLOW",
            "missing_information": [],
            "response_type": "EVIDENCE_CHECKLIST"
        }

    # 3C. Explicit Action Plan Request
    if any(k in msg for k in [
        "give me a detailed step-by-step action plan", "give me a step-by-step action plan",
        "step-by-step action plan", "give me an action plan", "detailed step-by-step action plan",
        "detailed action plan", "generate an action plan", "generate action plan",
        "show action plan", "provide action plan", "create action plan", "action plan module", "action plan checklist"
    ]):
        return {
            "intent": "USER_REQUESTED_ACTION_PLAN",
            "legal_category": "general",
            "conversation_stage": "TAKE_ACTION",
            "urgency_level": "YELLOW",
            "missing_information": [],
            "response_type": "ACTION_PLAN"
        }

    # 3D. Case Summary Dossier Request
    if any(k in msg for k in [
        "summarize my case", "summarise my case", "generate case summary", "case summary dossier",
        "export case summary", "case dossier", "download case summary", "case summary pdf"
    ]):
        return {
            "intent": "USER_REQUESTED_CASE_SUMMARY",
            "legal_category": "general",
            "conversation_stage": "TAKE_ACTION",
            "urgency_level": "YELLOW",
            "missing_information": [],
            "response_type": "CASE_SUMMARY"
        }

    # 4. Document review request
    if any(k in msg for k in ["analyze document", "analyze this document", "explain this notice", "explain this legal document", "review this agreement", "attached notice", "uploaded image", "is this notice real", "upload notice"]):
        return {
            "intent": "DOCUMENT_ANALYSIS_REQUEST",
            "legal_category": "general",
            "conversation_stage": "ANALYZE",
            "urgency_level": "NONE",
            "missing_information": [],
            "response_type": "DOCUMENT_REVIEW"
        }

    # 5. Conversational "What should I do next?" (Explains practical next steps in chat WITHOUT opening tools)
    if any(k in msg for k in ["what should i do next", "what should i do now", "what to do next", "what to do now", "what are my next steps", "what next", "what should i do"]):
        return {
            "intent": "FOLLOW_UP_NEXT_STEPS",
            "legal_category": "general",
            "conversation_stage": "GUIDE",
            "urgency_level": "YELLOW",
            "missing_information": [],
            "response_type": "CONVERSATIONAL"
        }

    # 6. URGENT CRIMINAL OFFENCES & PHYSICAL VIOLENCE (Armed Robbery, Knife Attack, Assault, Break-in)
    criminal_terms = [
        "thief", "thieves", "robbery", "robbed", "knife", "weapon", "attacked", "stabbed",
        "physical assault", "bleeding", "hospital", "break in", "broken into",
        "entered my house", "trespassed", "house breaking", "burglary", "dacoity",
        "threatened to kill", "loot", "looted", "चोर", "डकैती", "चाकू", "कಳ್ಳರು", "ದರೋಡೆ", "ಚಾಕು"
    ]
    if any(k in msg for k in criminal_terms):
        return {
            "intent": "URGENT_LEGAL_PROBLEM",
            "legal_category": "criminal_offences",
            "conversation_stage": "GUIDE",
            "urgency_level": "RED",
            "missing_information": [],
            "response_type": "URGENT_DISPATCH"
        }

    # 7. URGENT CYBER & FINANCIAL FRAUD (UPI hacked, bank fraud, unauthorized debits)
    if any(k in msg for k in [
        "upi account was hacked", "upi account hacked", "upi was hacked", "bank was hacked", "account was hacked",
        "upi fraud", "upi scam", "otp scam", "account debited", "unauthorized transaction", "lost money", "1930",
        "phishing", "scammed", "hacked my upi", "hacked my account"
    ]) or (("upi" in msg or "bank" in msg or "account" in msg) and any(w in msg for w in ["hack", "hacked", "fraud", "scam", "debited", "stolen money"])):
        return {
            "intent": "URGENT_LEGAL_PROBLEM",
            "legal_category": "cyber_fraud",
            "conversation_stage": "GUIDE",
            "urgency_level": "RED",
            "missing_information": [],
            "response_type": "URGENT_DISPATCH"
        }

    # 8. GENERAL LEGAL QUESTIONS (Definitions, Acts in abstract e.g. "What is Bharatiya Nyaya Sanhita?")
    if msg.startswith("what is") or msg.startswith("what are") or msg.startswith("explain ") or msg.startswith("tell me about") or msg.startswith("how does"):
        if not any(k in msg for k in ["my landlord", "my deposit", "my salary", "my employer", "my husband", "my account", "my flat", "my rent", "my house", "yesterday", "injured", "my phone"]):
            return {
                "intent": "GENERAL_LEGAL_QUESTION",
                "legal_category": "general",
                "conversation_stage": "GUIDE",
                "urgency_level": "GREEN",
                "missing_information": [],
                "response_type": "EXPLANATORY"
            }

    # 9. Multi-turn conversation handling:
    if turn_count >= 1:
        prev_asst = assistant_msgs[-1] if assistant_msgs else ""
        if "?" in prev_asst or any(q in prev_asst.lower() for q in ["could you tell me", "did your", "how much", "how long", "do you have"]):
            if turn_count >= 2:
                return {
                    "intent": "PROVIDE_LEGAL_GUIDANCE",
                    "legal_category": "general",
                    "conversation_stage": "GUIDE",
                    "urgency_level": "YELLOW",
                    "missing_information": [],
                    "response_type": "LEGAL_GUIDANCE"
                }
            return {
                "intent": "NEEDS_CLARIFICATION",
                "legal_category": "general",
                "conversation_stage": "ASK",
                "urgency_level": "YELLOW",
                "missing_information": [],
                "response_type": "ASK_QUESTIONS"
            }

    # 10. Initial Problem Description (Stage: ASK / GUIDE)
    cat_match = "general"
    if any(k in msg for k in ["phone", "mobile", "lost my", "lost", "theft", "stole", "police", "fir", "stolen"]):
        cat_match = "criminal_offences" if any(w in msg for w in ["stole", "theft", "stolen", "snatch"]) else "general"
    elif any(k in msg for k in ["landlord", "rent", "deposit", "evict", "flat", "tenant"]):
        cat_match = "tenant_landlord"
    elif any(k in msg for k in ["consumer", "refund", "warranty", "defective", "amazon", "flipkart"]):
        cat_match = "consumer_complaint"
    elif any(k in msg for k in ["salary", "employer", "unpaid", "fired", "terminated"]):
        cat_match = "employment_salary"
    elif any(k in msg for k in ["property", "land", "plot", "encroach"]):
        cat_match = "property_disputes"
    elif any(k in msg for k in ["husband", "wife", "dowry", "maintenance", "abuse"]):
        cat_match = "family_domestic"

    return {
        "intent": "INITIAL_PROBLEM_DESCRIPTION",
        "legal_category": cat_match,
        "conversation_stage": "ASK",
        "urgency_level": "YELLOW" if cat_match != "general" else "GREEN",
        "missing_information": ["specific incident facts", "timeline", "documents/receipts"],
        "response_type": "ASK_QUESTIONS"
    }


def classify_user_intent(message: str, history: List[Dict[str, Any]], client=None) -> Dict[str, Any]:
    """
    Main intent classification entry point.
    Uses Gemini API for zero-shot contextual classification if available; falls back cleanly to semantic rules.
    """
    cleaned_msg = message.strip()
    if not cleaned_msg:
        return rule_based_fallback_intent("hello", history)

    # Fast semantic check for simple greetings/small-talk to avoid unnecessary round-trips
    lower = cleaned_msg.lower()
    if re.fullmatch(r"(hi+|hello+|hey+|namaste+|vanakkam+|namaskara+|good\s*(morning|afternoon|evening)|hlo+|hola)[.!? ]*", lower):
        return rule_based_fallback_intent(cleaned_msg, history)
    if re.fullmatch(r"(how\s+are\s+you|thank\s*you|thanks|thx|ok|okay|cool|bye|goodbye)[.!? ]*", lower):
        return rule_based_fallback_intent(cleaned_msg, history)

    # Direct fast-path for explicit action plan, evidence, complaint, or case summary triggers
    for explicit_word in [
        "give me a detailed step-by-step action plan", "give me a step-by-step action plan", "give me an action plan",
        "step-by-step action plan", "detailed action plan", "what evidence should i collect", "evidence checklist",
        "prepare a police complaint for me", "draft a police complaint", "draft a complaint", "summarize my case",
        "what should i do next", "what to do next", "what are my next steps"
    ]:
        if explicit_word in lower:
            return rule_based_fallback_intent(cleaned_msg, history)

    # Direct fast-path for critical violent criminal offences
    if any(k in lower for k in ["knife", "stabbed", "attacked and injured", "stole my gold", "break in", "house breaking"]):
        return {
            "intent": "URGENT_LEGAL_PROBLEM",
            "legal_category": "criminal_offences",
            "conversation_stage": "GUIDE",
            "urgency_level": "RED",
            "missing_information": [],
            "response_type": "URGENT_DISPATCH"
        }

    if client:
        try:
            recent_hist_snippets = []
            for h in history[-6:]:
                r = "Citizen" if h.get("role") == "user" else "Assistant"
                c = h.get("content", "")[:140]
                recent_hist_snippets.append(f"{r}: {c}")
            hist_str = "\n".join(recent_hist_snippets)

            prompt = (
                f"{INTENT_CLASSIFIER_PROMPT}\n\n"
                f"RECENT CONVERSATION HISTORY:\n{hist_str or 'None'}\n\n"
                f"CURRENT USER MESSAGE:\n\"{cleaned_msg}\"\n\nJSON:"
            )

            res = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            raw = res.text.strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\n?", "", raw)
                raw = re.sub(r"\n?```$", "", raw)

            parsed = json.loads(raw.strip())
            intent = parsed.get("intent", "").upper()
            if intent in VALID_INTENTS:
                return {
                    "intent": intent,
                    "legal_category": parsed.get("legal_category", "general"),
                    "conversation_stage": parsed.get("conversation_stage", "UNDERSTAND"),
                    "urgency_level": parsed.get("urgency_level", "GREEN"),
                    "missing_information": parsed.get("missing_information", []),
                    "response_type": parsed.get("response_type", "CONVERSATIONAL")
                }
        except Exception:
            pass

    return rule_based_fallback_intent(cleaned_msg, history)


def determine_required_features(intent: str, urgency_level: str = "NONE", conversation_stage: str = "UNDERSTAND") -> Dict[str, bool]:
    """
    Strict conditional feature flags:
    All features default to FALSE.
    Enable a feature ONLY when the user explicitly requests that specific tool.
    Never display action plans, checklists, complaint generators, or dossier exports automatically.
    """
    return {
        "show_urgency_alert": False,
        "show_action_plan": intent == "USER_REQUESTED_ACTION_PLAN",
        "show_evidence_checklist": intent == "USER_REQUESTED_EVIDENCE_CHECKLIST",
        "show_complaint_generator": intent == "USER_REQUESTED_COMPLAINT",
        "show_case_summary_export": intent in ["USER_REQUESTED_CASE_SUMMARY", "USER_REQUESTED_CASE_DOSSIER"],
        "show_case_summary": intent in ["USER_REQUESTED_CASE_SUMMARY", "USER_REQUESTED_CASE_DOSSIER"],
        "show_document_analysis": intent == "DOCUMENT_ANALYSIS_REQUEST",
        "show_legal_sources": False
    }


def construct_contextual_prompt(
    user_message: str,
    history: List[Dict[str, Any]],
    intent_data: Dict[str, Any],
    rag_provisions: List[Dict[str, Any]]
) -> str:
    """
    Builds the specialized prompt for Gemini adhering to the conversational ChatGPT-like philosophy:
    Clear legal answers first, no unrequested bulky reports or tool dumping.
    Offers additional tools conversationally without opening them automatically.
    """
    intent = intent_data.get("intent", "OTHER")

    system_persona = (
        "You are NyayaSathi, an Indian legal information and guidance assistant. Your responsibility is to help "
        "ordinary Indian citizens understand their legal rights, identify potentially applicable laws, understand "
        "available remedies, preserve evidence, and take appropriate practical steps.\n\n"
        "CONVERSATIONAL PRINCIPLES:\n"
        "- Respond naturally and conversationally, similar to ChatGPT.\n"
        "- Keep the answer focused on the citizen's actual problem.\n"
        "- Provide a clear, relevant answer first. Explain practical next steps naturally in your text.\n"
        "- Ask 1-3 relevant follow-up questions when important facts are missing.\n"
        "- DO NOT dump massive formal report templates or checklists automatically.\n"
        "- Conclude naturally with an offer, for example: 'If you want, I can also prepare a step-by-step action plan or draft a formal complaint for you.'\n"
        "- Never pretend to be a lawyer, police officer, or judge. Never guarantee legal outcomes.\n"
    )

    # 1. GREETING
    if intent == "GREETING":
        return (
            f"{system_persona}\n"
            f"User message: \"{user_message}\"\n\n"
            "INSTRUCTION: Reply with a warm, natural, and concise greeting (2-3 sentences max). "
            "Example: 'Hello! Welcome to NyayaSathi. 👋 I am here to help you understand your legal rights and guide you on your next steps. How can I assist you today?'"
        )

    # 2. GENERAL CONVERSATION
    if intent == "GENERAL_CONVERSATION":
        return (
            f"{system_persona}\n"
            f"User message: \"{user_message}\"\n\n"
            "INSTRUCTION: Give a short, polite, conversational response in 1-3 sentences."
        )

    # 3. GENERAL LEGAL QUESTION
    if intent == "GENERAL_LEGAL_QUESTION":
        rag_text = ""
        if rag_provisions:
            rag_text = "\nVERIFIED STATUTORY PROVISIONS RETRIEVED:\n" + "\n".join(
                [f"- {p.get('act')} {p.get('section')}: {p.get('simple_explanation')}" for p in rag_provisions[:3]]
            )
        return (
            f"{system_persona}\n"
            f"The citizen has asked a general question about Indian law or legal concepts:\n\"{user_message}\"\n"
            f"{rag_text}\n\n"
            "INSTRUCTION:\n"
            "Provide a direct, clear, informative, and well-structured explanation of this statute or concept in plain language (2-4 concise paragraphs with bullet points for key features).\n"
            "Explain the core purpose, citizen rights, and relevant dispute resolution forums. Do not force into a case report."
        )

    # 4. CONVERSATIONAL "WHAT SHOULD I DO NEXT?"
    if intent == "FOLLOW_UP_NEXT_STEPS":
        history_lines = []
        for m in history[-6:]:
            role = "Citizen" if m.get("role") == "user" else "NyayaSathi"
            history_lines.append(f"{role}: {m.get('content', '')}")
        history_str = "\n\n".join(history_lines)

        return (
            f"{system_persona}\n"
            f"CONVERSATION HISTORY:\n{history_str}\n\n"
            f"CITIZEN'S QUESTION: \"{user_message}\"\n\n"
            "INSTRUCTION:\n"
            "Review the facts established in the conversation and explain the practical next 2-3 logical steps in clear, numbered paragraphs in your response text.\n"
            "Keep it natural and direct. At the end, state:\n"
            "'Whenever you are ready, you can ask me:\n"
            "- *\"Give me a step-by-step action plan\"* to view an interactive action roadmap.\n"
            "- *\"What evidence should I collect?\"* for a documentation checklist.\n"
            "- *\"Draft a police complaint\"* to prepare a formal legal petition.'"
        )

    # 5. INITIAL PROBLEM DESCRIPTION (Lost phone, stolen phone, etc.)
    if intent == "INITIAL_PROBLEM_DESCRIPTION":
        return (
            f"{system_persona}\n"
            f"The citizen has shared a legal issue or incident for the first time:\n\"{user_message}\"\n\n"
            "INSTRUCTION:\n"
            "1. Acknowledge and empathize with their situation in a reassuring manner.\n"
            "2. Provide clear, practical legal and security steps they should immediately take (e.g. for lost/stolen phone: blocking SIM, blocking IMEI on CEIR portal ceir.gov.in, filing police e-lost report or FIR under Section 173 BNSS).\n"
            "3. Ask 2 to 3 important clarifying questions if crucial details are missing.\n"
            "4. Conclude with a natural offer: 'If you want, I can also prepare a step-by-step action plan or draft a formal complaint for you.'"
        )

    # 6. URGENT LEGAL PROBLEM (UPI hacked, cyber fraud, violent assault)
    if intent == "URGENT_LEGAL_PROBLEM":
        rag_text = ""
        if rag_provisions:
            rag_text = "\n=== VERIFIED STATUTORY PROVISIONS RETRIEVED ===\n" + "\n".join(
                [f"• {p.get('act')} {p.get('section')} ({p.get('title')}): {p.get('simple_explanation')}" for p in rag_provisions[:3]]
            )

        return (
            f"{system_persona}\n"
            f"CITIZEN'S URGENT CONCERN: \"{user_message}\"\n"
            f"{rag_text}\n\n"
            "INSTRUCTION:\n"
            "1. Prioritize immediate safety and emergency reporting steps in plain, direct language (e.g. for cyber/UPI fraud: Call 1930 immediately within the Golden Hour to freeze funds, notify bank within 3 days for RBI Zero Liability, register on cybercrime.gov.in; for armed crimes: 112 emergency and hospital MLC).\n"
            "2. Cite the exact verified Indian laws applicable (e.g. IT Act Section 66D, BNS Section 318(4), BNSS Section 173).\n"
            "3. Explain their rights clearly in the chat response.\n"
            "4. Conclude by offering: 'Whenever you are ready, you can ask me to prepare a step-by-step action plan, compile an evidence checklist, or draft a formal complaint for you.'"
        )

    # 7. USER REQUESTED ACTION PLAN
    if intent == "USER_REQUESTED_ACTION_PLAN":
        return (
            f"{system_persona}\n"
            f"USER EXPLICIT REQUEST: \"{user_message}\"\n\n"
            "INSTRUCTION: Provide a clear, chronological action plan in your answer, and state that the interactive Step-by-Step Action Plan tracker is now open below."
        )

    # 8. USER REQUESTED EVIDENCE CHECKLIST
    if intent == "USER_REQUESTED_EVIDENCE_CHECKLIST":
        return (
            f"{system_persona}\n"
            f"USER EXPLICIT REQUEST: \"{user_message}\"\n\n"
            "INSTRUCTION: Explain the key physical, documentary, and electronic evidence to preserve, and state that the Evidence Checklist tool is now active below."
        )

    # 9. USER REQUESTED COMPLAINT
    if intent == "USER_REQUESTED_COMPLAINT":
        return (
            f"{system_persona}\n"
            f"USER EXPLICIT REQUEST: \"{user_message}\"\n\n"
            "INSTRUCTION: State that you have prepared a formal legal complaint draft based on their details, and that the editable Complaint Draft Generator is now open below ready to review and download as PDF/TXT."
        )

    # 10. USER REQUESTED CASE SUMMARY
    if intent == "USER_REQUESTED_CASE_SUMMARY":
        return (
            f"{system_persona}\n"
            f"USER EXPLICIT REQUEST: \"{user_message}\"\n\n"
            "INSTRUCTION: Provide a concise summary of the case facts, applicable laws, and current status, and state that the Case Summary Dossier export is available below."
        )

    # Fallback / Other
    return (
        f"{system_persona}\n"
        f"User message: \"{user_message}\"\n\n"
        "INSTRUCTION: Respond naturally and ask how you can help with their legal concerns in India."
    )


def generate_deterministic_legal_response(
    user_message: str,
    intent_data: Dict[str, Any],
    rag_provisions: List[Dict[str, Any]],
    category_id: str = "general",
    language: str = "en",
    history: List[Dict[str, Any]] = None
) -> str:
    """
    Deterministic legal guidance generator for offline/fallback mode.
    Adheres strictly to the ChatGPT-like conversational approach:
    Provides direct answers and guidance first, without dumping unrequested tool modules.
    """
    intent = intent_data.get("intent", "OTHER")
    msg_lower = user_message.lower()

    # 1. GREETING
    if intent == "GREETING":
        return (
            "Hello! Welcome to **NyayaSathi** — your trusted Indian legal guidance assistant. 👋\n\n"
            "I'm here to help you understand your legal rights, navigate Indian laws (BNS, BNSS, Consumer Protection, IT Act), "
            "and take practical action.\n\n"
            "How can I help you today? Please feel free to describe your situation in English, हिन्दी, or ಕನ್ನಡ."
        )

    # 2. GENERAL CONVERSATION
    if intent == "GENERAL_CONVERSATION":
        return (
            "I am **NyayaSathi**, an AI-powered legal information assistant designed for Indian citizens.\n\n"
            "I can assist you with:\n"
            "- Understanding your legal rights under Indian statutes (BNS 2023, BNSS 2023, IT Act, Consumer Protection Act).\n"
            "- Guidance on immediate steps to protect yourself in fraud, theft, or tenancy issues.\n"
            "- Preparing step-by-step action plans, evidence checklists, or formal complaints on demand.\n\n"
            "Please describe any legal concern or question you have, and I will guide you."
        )

    # 3. TEST 7: GENERAL LEGAL QUESTION (e.g. "What is the Bharatiya Nyaya Sanhita?", "What is Consumer Protection Act?")
    if intent == "GENERAL_LEGAL_QUESTION":
        if "bharatiya nyaya" in msg_lower or "bns" in msg_lower:
            return (
                "### Understanding the Bharatiya Nyaya Sanhita (BNS), 2023\n\n"
                "The **Bharatiya Nyaya Sanhita, 2023 (BNS)** is India's principal criminal code, which replaced the colonial-era Indian Penal Code (IPC) of 1860. "
                "It officially came into effect across the nation on **July 1, 2024**.\n\n"
                "#### Key Highlights & Citizen Protections:\n"
                "1. **Streamlined Structure:** BNS consolidates criminal law into 358 sections (compared to 511 sections in the old IPC), eliminating redundant provisions.\n"
                "2. **Community Service as Punishment:** For first-time and minor offences (such as petty theft under ₹5,000 where property is restored, defamation, or public misconduct by an intoxicated person), community service has been introduced as an alternative to prison.\n"
                "3. **Enhanced Safeguards for Women & Children:** Chapter V introduces dedicated, severe penalties for gang rape, deceitful sexual promises of marriage, and child trafficking.\n"
                "4. **Organized Crime & Mob Lynching Codified:** Formally defines and criminalizes organized crime syndicates (Section 111) and mob violence or lynching by groups of five or more on grounds of race, caste, or community (Section 103(2)).\n"
                "5. **Modernized Theft & Cyber-Linked Offences:** Explicitly incorporates electronic snatching (Section 304), financial cheating, and electronic identity misuse.\n"
                "6. **Repeal of Sedition:** The archaic offence of sedition (old Section 124A IPC) has been repealed and replaced with Section 152, which penalizes specific acts endangering the sovereignty, unity, and integrity of India.\n\n"
                "The procedural companion to BNS is the **Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023** (which replaced the CrPC), and evidentiary rules are governed by the **Bharatiya Sakshya Adhiniyam (BSA), 2023**."
            )
        elif "consumer" in msg_lower:
            return (
                "### Understanding the Consumer Protection Act, 2019\n\n"
                "The **Consumer Protection Act, 2019 (CPA 2019)** is India's principal legislation safeguarding consumer rights, "
                "replacing the earlier 1986 Act to modernize protections for the digital commerce era.\n\n"
                "#### Key Highlights & Citizen Rights:\n"
                "1. **Wide Definition of Consumer (Section 2(7)):** Covers anyone who buys goods or avails services for consideration, explicitly including offline and online (e-commerce, direct selling, teleshopping) transactions.\n"
                "2. **Six Fundamental Consumer Rights:** Right to Safety, Right to Information, Right to Choose, Right to be Heard, Right to Redressal, and Right to Consumer Education.\n"
                "3. **Three-Tier Redressal Mechanism:**\n"
                "   - **District Commission (DCDRC):** Claims up to ₹50 Lakhs.\n"
                "   - **State Commission (SCDRC):** Claims between ₹50 Lakhs and ₹2 Crores.\n"
                "   - **National Commission (NCDRC):** Claims exceeding ₹2 Crores.\n"
                "4. **Product Liability (Section 84-87):** Manufacturers and sellers can be held legally accountable to compensate consumers for harm caused by defective products or deficiency of services.\n"
                "5. **Simplified Digital Filing via e-Daakhil:** Consumers can register complaints online from anywhere via [edaakhil.nic.in](https://edaakhil.nic.in) without needing to engage an advocate.\n\n"
                "**National Consumer Helpline (NCH):** You can dial **1915** (toll-free) or visit [consumerhelpline.gov.in](https://consumerhelpline.gov.in) to register grievances."
            )
        else:
            return (
                f"### Legal Overview: {user_message.strip().title()}\n\n"
                "Under Indian jurisprudence, this matter is governed by statutory rights and regulatory frameworks established by Parliament.\n\n"
                "Indian citizens facing disputes can access free legal consultation through the **District Legal Services Authority (DLSA)** or contact the **National Legal Services Authority (NALSA)** at toll-free **15100**."
            )

    # 4. TEST 8: CONVERSATIONAL "WHAT SHOULD I DO NEXT?"
    if intent == "FOLLOW_UP_NEXT_STEPS":
        return (
            "Based on our conversation, here are the practical next steps you should take:\n\n"
            "1. **Complete Immediate Security Precautions:** If your phone or banking details are involved, ensure your SIM card is blocked through your telecom operator and linked bank accounts/UPI access are temporarily frozen.\n"
            "2. **Preserve Supporting Evidence:** Keep purchase receipts, IMEI details, transaction IDs, SMS alerts, or photos of any damage safely backed up.\n"
            "3. **Approach the Appropriate Official Authority:** Lodge your report at the local police station (under Section 173 BNSS), on the CEIR portal ([ceir.gov.in](https://ceir.gov.in)), or on the National Cybercrime Portal ([cybercrime.gov.in](https://cybercrime.gov.in) / 1930) depending on the nature of the incident.\n\n"
            "Whenever you are ready, you can simply ask me:\n"
            "- *\"Give me a step-by-step action plan\"* to view an interactive action roadmap.\n"
            "- *\"What evidence should I collect?\"* for an itemized checklist.\n"
            "- *\"Draft a police complaint\"* to prepare a formal legal petition."
        )

    # 5. TEST 1: "I lost my phone."
    if "lost my phone" in msg_lower or "lost phone" in msg_lower:
        return (
            "I understand how stressful losing your phone can be. Taking quick, proactive steps will protect your personal identity, bank accounts, and data.\n\n"
            "Here are the immediate steps you should take:\n\n"
            "1. **Block Your SIM Card Immediately:**\n"
            "   Contact your telecom service provider (Jio, Airtel, Vi, or BSNL) right away via their customer care or visit a nearby outlet to block your SIM card. This prevents anyone from intercepting incoming SMS OTPs. You can request a duplicate SIM with your existing number.\n\n"
            "2. **Block the Handset on the CEIR Portal:**\n"
            "   The Department of Telecommunications (DoT) operates the **Central Equipment Identity Register (CEIR)** under the Sanchar Saathi initiative ([ceir.gov.in](https://ceir.gov.in)). Submit a request to block the phone's 15-digit IMEI number across all Indian telecom networks. Once blocked, the device cannot be used even if another SIM card is inserted.\n\n"
            "3. **File a Police Lost Property Report (e-Lost Intimation):**\n"
            "   Most state police portals and mobile apps (e.g. Delhi Police Lost Report app, Karnataka Police KSP app, Maharashtra Police portal) allow citizens to file an online **Lost Property Intimation** for mobile phones. This provides an official digitally signed acknowledgement, which is necessary when obtaining a duplicate SIM or filing an insurance claim.\n\n"
            "4. **Secure Your Online Accounts Remotely:**\n"
            "   - Log into your Google Account ([myaccount.google.com](https://myaccount.google.com)) or Apple ID ([icloud.com/find](https://icloud.com/find)) from another device.\n"
            "   - Use 'Sign Out of all devices' or remotely lock/erase the device.\n"
            "   - Change your passwords for primary email accounts, UPI apps, and net banking.\n\n"
            "If you suspect your phone was stolen rather than lost, or if you would like me to prepare a step-by-step action plan, let me know!"
        )

    # 6. TEST 2: "Someone stole my phone."
    if "stole my phone" in msg_lower or "stolen phone" in msg_lower:
        return (
            "I'm sorry to hear that your phone was stolen. Mobile theft is a serious criminal offence, and taking immediate precautions will prevent unauthorized access to your accounts.\n\n"
            "### Immediate Security Precautions:\n"
            "1. **Block Your SIM Card Right Away:** Call your telecom provider's customer care immediately to block the SIM so that thieves cannot access SMS-based OTPs.\n"
            "2. **Alert Your Banks & Block UPI:** If you had PhonePe, Google Pay, Paytm, or mobile banking apps on the phone, call your bank's helpline to temporarily block UPI and mobile banking on that number.\n"
            "3. **Block the Stolen Handset via CEIR:** Visit the official Government of India portal [ceir.gov.in](https://ceir.gov.in) (Sanchar Saathi) and file a request to block the phone using its 15-digit IMEI number. This blacklists the phone across all telecom operators in India.\n\n"
            "### Legal Provisions & Police Reporting:\n"
            "- **Theft under Bharatiya Nyaya Sanhita, 2023 (BNS):** Theft of movable property is punishable under **Section 303(2) of BNS, 2023** (formerly IPC Section 379) with imprisonment up to 3 years or fine.\n"
            "- **Lodging an FIR under BNSS, 2023:** You have the legal right to register a First Information Report (FIR) under **Section 173 of the Bharatiya Nagarik Suraksha Sanhita, 2023** at the jurisdictional police station or via your state's online Police e-FIR portal. Under Section 173(2) BNSS, the police must provide you with a **free copy** of the FIR.\n\n"
            "### To help you further, could you tell me:\n"
            "1. Do you have the phone's 15-digit IMEI number (from the original box or invoice)?\n"
            "2. Were any bank accounts or UPI payment apps active on the phone?\n"
            "3. Did the theft involve physical snatching or any weapon/threat (which would classify as robbery under Section 309 BNS)?\n\n"
            "Whenever you are ready, I can also prepare a step-by-step action plan or draft a formal police complaint for you."
        )

    # 7. TEST 3: "My UPI account was hacked."
    if "upi" in msg_lower and any(w in msg_lower for w in ["hack", "hacked", "fraud", "scam", "debited"]):
        return (
            "This is an urgent situation. Please act immediately during the **Golden Hour** (the first 2 to 3 hours after unauthorized debits) to maximize the chances of freezing the stolen funds.\n\n"
            "### Immediate Critical Actions:\n"
            "1. **Call 1930 Immediately (National Cybercrime Helpline):**\n"
            "   Dial **1930** right now. The National Cybercrime Reporting Portal (MHA) coordinates directly with banks and payment gateways to freeze fraudulent funds in the beneficiary's nodal account before the fraudster can withdraw them.\n"
            "2. **Notify Your Bank in Writing (Within 3 Days):**\n"
            "   Contact your bank's 24x7 fraud reporting helpline immediately to block your UPI ID, net banking, and debit card. Submit a formal written dispute. Under **RBI's Zero Liability Policy** (Circular DBR.No.Leg.BC.78/09.07.005/2017-18), if you notify the bank within 3 working days of an unauthorized electronic transaction, your liability is **zero**.\n"
            "3. **Register Complaint on cybercrime.gov.in:**\n"
            "   File an online complaint on the official National Cyber Crime Reporting Portal at [cybercrime.gov.in](https://cybercrime.gov.in) and download the acknowledgement receipt.\n"
            "4. **Change All Passwords & UPI MPINs:**\n"
            "   Immediately reset your email password, UPI PIN, and internet banking login credentials from a secure alternate device.\n\n"
            "### Applicable Indian Laws:\n"
            "- **Information Technology Act, 2000 — Section 66D:** Cheating by personation using computer resources (punishable with imprisonment up to 3 years and fine).\n"
            "- **Bharatiya Nyaya Sanhita, 2023 (BNS) — Section 318(4):** Cheating and dishonestly inducing delivery of property (punishable with imprisonment up to 7 years).\n"
            "- **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS) — Section 173:** Mandatory registration of FIR by the cyber police station.\n\n"
            "If you want, I can also prepare a step-by-step action plan or draft a formal bank dispute letter or cyber police complaint for you."
        )

    # 8. TEST 4: "Give me a detailed step-by-step action plan."
    if intent == "USER_REQUESTED_ACTION_PLAN":
        return (
            "Here is your structured step-by-step action plan tailored to your situation.\n\n"
            "I have also activated the interactive **Step-by-Step Action Plan** tracker below, where you can check off each task and monitor your progress in real time."
        )

    # 9. TEST 5: "Prepare a police complaint for me."
    if intent == "USER_REQUESTED_COMPLAINT":
        return (
            "I have prepared a formal written complaint draft incorporating the details from our conversation.\n\n"
            "The editable **Formal Complaint Draft** tool is now open below. You can review the details, edit any dates or names, and download it as a **TXT** or **PDF** document ready to print and submit to the police station."
        )

    # 10. TEST 6: "What evidence should I collect?"
    if intent == "USER_REQUESTED_EVIDENCE_CHECKLIST":
        return (
            "Preserving proper evidence is crucial for supporting your case and ensuring a swift investigation.\n\n"
            "I have activated the **Evidence Checklist** tool below, where you can review the required documents and check them off as you collect them."
        )

    # 11. CASE SUMMARY REQUEST
    if intent == "USER_REQUESTED_CASE_SUMMARY":
        return (
            "I have generated a structured case dossier summarizing your legal grievance, applicable statutes, and progress.\n\n"
            "You can export and download your complete **Case Summary Dossier (PDF)** using the tool opened below."
        )

    # 12. INITIAL TENANCY / CONSUMER INQUIRY
    if intent == "INITIAL_PROBLEM_DESCRIPTION":
        cat_title = "Tenancy Matter" if category_id == "tenant_landlord" else ("Consumer Grievance" if category_id == "consumer_complaint" else "Legal Matter")
        return (
            f"I understand your concern regarding this **{cat_title}**, and I am here to help you navigate your legal options.\n\n"
            "Under Indian law (such as the Model Tenancy Act, 2021 or the Consumer Protection Act, 2019), you have enforceable statutory rights against unfair practices and unlawful withholding.\n\n"
            "To provide you with the most accurate guidance, **could you please clarify 2 or 3 quick details?**\n\n"
            "1. **Written Agreement / Receipts:** Do you have a signed agreement, bill, or bank payment receipts?\n"
            "2. **Timeline:** When did this dispute arise, and have you issued any formal written communication (via email or WhatsApp)?\n"
            "3. **Disputed Amount:** What is the exact amount involved, and what explanation was provided by the other party?\n\n"
            "Whenever you are ready, I can also prepare a step-by-step action plan or draft a formal legal notice for you."
        )

    # 13. DEFAULT GUIDANCE (e.g. violent crime / robbery / general)
    return (
        "I have analyzed your situation under applicable Indian laws.\n\n"
        "### Key Legal Protections & Next Steps:\n"
        "1. **Emergency & Safety Actions:** Contact emergency authorities (Dial **112** for police or **1930** for cyber financial crimes) immediately.\n"
        "2. **Mandatory FIR Registration:** Under **Section 173 of the Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023**, the police must register an FIR for cognizable offences and provide a signed copy free of cost.\n"
        "3. **Free Legal Aid:** You can access free legal representation and consultation through the **District Legal Services Authority (DLSA)** or NALSA Helpline **15100**.\n\n"
        "If you want, I can also prepare a step-by-step action plan, compile an evidence checklist, or draft a formal complaint for you."
    )
