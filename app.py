"""
NyayaSathi – AI-Powered Multilingual Legal Guidance Assistant for India
Tagline: Know Your Rights. Take Your Next Step.
FirstCommit '26 Hackathon Edition
"""

import os
import io
import json
from datetime import datetime
from PIL import Image
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load local environment
load_dotenv()

# Import specialized modules
from modules.auth import authenticate_user, create_user
from modules.intent_classifier import (
    classify_user_intent, determine_required_features, construct_contextual_prompt,
    generate_deterministic_legal_response
)
from modules.issue_classifier import classify_legal_issue, detect_language
from modules.legal_retrieval import legal_retriever
from modules.action_plan import get_action_plan
from modules.evidence_checklist import get_default_checklist
from modules.complaint_generator import generate_complaint_text, generate_complaint_pdf
from modules.case_summary import generate_case_summary_pdf
from modules.database import (
    init_db, save_case, get_saved_cases, get_case_by_id, delete_case,
    save_complaint, get_recent_complaints
)
from modules.voice_input import inject_chat_voice_input

# Page configuration
st.set_page_config(
    page_title="NyayaSathi | AI Legal Guidance Platform",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Load custom dark CSS
css_path = os.path.join(os.path.dirname(__file__), "styles", "dark_theme.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# AI Client
@st.cache_resource
def get_ai_client():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

client = get_ai_client()

def generate_ai_response(prompt_text: str, image_obj: Image.Image = None) -> str:
    if not client:
        return "⚠️ Gemini API key is not configured in `.env`. Please add your GEMINI_API_KEY to enable AI intelligence."

    candidate_models = [
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
    ]
    last_err = None
    contents = [image_obj, prompt_text] if image_obj else prompt_text

    for model_name in candidate_models:
        try:
            res = client.models.generate_content(
                model=model_name,
                contents=contents,
            )
            if res and res.text:
                return res.text.strip()
        except Exception as e:
            last_err = e
            continue
    return f"⚠️ Unable to obtain AI response due to temporary service load. Error: `{last_err}`"


# Session State Initialization
if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False
if "user_info" not in st.session_state:
    st.session_state.user_info = None

if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_case_title" not in st.session_state:
    st.session_state.current_case_title = "Untitled Legal Inquiry"
if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None
if "current_features" not in st.session_state:
    st.session_state.current_features = {}
if "custom_evidence_items" not in st.session_state:
    st.session_state.custom_evidence_items = []
if "checklist_checked" not in st.session_state:
    st.session_state.checklist_checked = {}
if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "💬 AI Legal Chatbot"

# ==============================================================================
# AUTHENTICATION GATEWAY
# ==============================================================================
if not st.session_state.user_authenticated:
    # Render Login Page
    st.markdown("""
    <div style="max-width: 900px; margin: 4rem auto 1.5rem auto; text-align: center;">
        <span style="font-size: 2.8rem;">⚖️</span>
        <h1 style="color: #FFFFFF; font-size: 2.2rem; font-weight: 700; margin: 0.2rem 0;">NyayaSathi</h1>
        <p style="color: #38BDF8; font-size: 1rem; font-weight: 600; margin: 0;">Know Your Rights. Take Your Next Step.</p>
        <p style="color: #94A3B8; font-size: 0.9rem; margin-top: 0.4rem;">Your trusted AI-powered multilingual legal guidance assistant for India.</p>
    </div>
    """, unsafe_allow_html=True)

    login_col1, login_col2, login_col3 = st.columns([1, 1.8, 1])
    with login_col2:
        with st.container():
            st.markdown("""
            <div style="background: #141C2E; border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; padding: 2rem 2.2rem; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
                <h3 style="color:#FFFFFF; margin-top:0; margin-bottom: 0.2rem;">Welcome Back</h3>
                <p style="color:#94A3B8; font-size: 0.88rem; margin-bottom: 1.5rem;">Sign in to continue to NyayaSathi.</p>
            </div>
            """, unsafe_allow_html=True)

            username_input = st.text_input("Username:", placeholder="Enter your username", key="auth_user")
            password_input = st.text_input("Password:", type="password", placeholder="Enter your password", key="auth_pass")

            auth_action_col1, auth_action_col2 = st.columns([1, 1])
            with auth_action_col1:
                remember_me = st.checkbox("Remember me", value=True)
            with auth_action_col2:
                auth_mode = st.radio("Mode", ["Sign In", "Create Account"], horizontal=True, label_visibility="collapsed")

            if auth_mode == "Sign In":
                if st.button("🔐 Sign In", use_container_width=True, type="primary"):
                    if not username_input or not password_input:
                        st.error("Please enter both username and password.")
                    else:
                        with st.spinner("Authenticating credentials..."):
                            success, user_obj, msg = authenticate_user(username_input, password_input)
                            if success:
                                st.session_state.user_authenticated = True
                                st.session_state.user_info = user_obj
                                st.success("Authentication successful! Loading dashboard...")
                                st.rerun()
                            else:
                                st.error(msg)
            else:
                full_name_input = st.text_input("Full Name:", placeholder="Your Name (Optional)", key="auth_fname")
                if st.button("✨ Create Account", use_container_width=True, type="primary"):
                    if not username_input or not password_input:
                        st.error("Please enter both username and password.")
                    else:
                        with st.spinner("Registering user..."):
                            created, msg = create_user(username_input, password_input, full_name_input)
                            if created:
                                st.success("Account created successfully! Please sign in with your credentials.")
                            else:
                                st.error(msg)

            st.markdown("""
            <div style="text-align: center; margin-top: 1.5rem;">
                <span style="color: #64748B; font-size: 0.78rem;">🔒 Your privacy and security matter to us. Passwords are cryptographically hashed using PBKDF2-SHA256.</span>
            </div>
            """, unsafe_allow_html=True)
    st.stop()


# ==============================================================================
# MAIN APPLICATION INTERFACE (POST-AUTHENTICATION)
# ==============================================================================
user = st.session_state.user_info or {"id": 1, "username": "Citizen", "full_name": "Citizen"}

# SIDEBAR — ChatGPT-inspired pure black minimal design (Strict Left-Aligned)
# Navigation items and their mapping to session state nav values
_NAV_ITEMS = [
    {"label": "AI Legal Chatbot",         "icon": "💬", "nav": "💬 AI Legal Chatbot"},
    {"label": "My Saved Cases",           "icon": "📁", "nav": "📁 My Saved Cases"},
    {"label": "Complaint Generator",      "icon": "📝", "nav": "📝 Complaint Generator"},
    {"label": "Verified Legal Resources", "icon": "📚", "nav": "📚 Verified Legal Resources"},
    {"label": "Explore Helplines",        "icon": "☎️", "nav": "☎️ Explore Helplines"},
]

with st.sidebar:
    # ── Brand header ──
    st.markdown("""
    <div class="ns-sidebar-brand">
        <div class="ns-sidebar-brand-icon">⚖️</div>
        <div class="ns-sidebar-brand-text-wrap">
            <div class="ns-sidebar-brand-text">NyayaSathi</div>
            <div class="ns-sidebar-brand-sub">AI Legal Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── New Conversation (Strictly left-aligned) ──
    st.markdown('<div class="ns-new-conv-wrap">', unsafe_allow_html=True)
    if st.button("＋  New Conversation", key="ns_new_conv", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_case_title = "Untitled Legal Inquiry"
        st.session_state.current_analysis = None
        st.session_state.current_features = {}
        st.session_state.custom_evidence_items = []
        st.session_state.checklist_checked = {}
        st.session_state.selected_nav = "💬 AI Legal Chatbot"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ns-divider"></div>', unsafe_allow_html=True)

    # ── Top Navigation (All 5 items identically styled & left-aligned) ──
    for nav in _NAV_ITEMS:
        is_active = st.session_state.selected_nav == nav["nav"]
        if is_active:
            st.markdown('<div class="ns-nav-active-wrap">', unsafe_allow_html=True)
        if st.button(
            f"{nav['icon']}  {nav['label']}",
            key=f"ns_nav_{nav['nav']}",
            use_container_width=True,
        ):
            st.session_state.selected_nav = nav["nav"]
            st.rerun()
        if is_active:
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ns-divider"></div>', unsafe_allow_html=True)

    # ── Pinned section (cases with urgency RED) ──
    user_cases_all = get_saved_cases(user_id=user["id"], limit=20)
    pinned_cases = [c for c in user_cases_all if c.get("urgency") == "RED"]

    if pinned_cases:
        st.markdown('<div class="ns-section-header">Pinned</div>', unsafe_allow_html=True)
        for pc in pinned_cases[:5]:
            pc_title = pc.get("title", f"Case #{pc['id']}")
            pc_label = pc_title[:28] + ("…" if len(pc_title) > 28 else "")
            if st.button(
                f"📌  {pc_label}",
                key=f"ns_pin_{pc['id']}",
                use_container_width=True,
            ):
                st.session_state.messages = pc.get("messages", [])
                st.session_state.current_case_title = pc_title
                st.session_state.selected_nav = "💬 AI Legal Chatbot"
                last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), "")
                if last_user_msg:
                    cls_res = classify_legal_issue(last_user_msg)
                    st.session_state.current_analysis = {
                        "category_id": cls_res["category_id"],
                        "category_name": cls_res["category_name"],
                        "classification": cls_res["classification"],
                        "urgency": cls_res["urgency"],
                        "urgency_badge": cls_res["urgency_badge"],
                        "urgency_reason": cls_res["urgency_reason"],
                        "primary_authority": cls_res["primary_authority"],
                        "detected_language": cls_res["detected_language"],
                        "provisions": legal_retriever.retrieve_provisions(cls_res["category_id"], last_user_msg),
                        "action_plan": get_action_plan(cls_res["category_id"], cls_res["detected_language"]),
                        "evidence": get_default_checklist(cls_res["category_id"], cls_res["detected_language"])
                    }
                    st.session_state.current_features = determine_required_features("LEGAL_PROBLEM", cls_res["urgency"])
                st.rerun()
        st.markdown('<div class="ns-divider"></div>', unsafe_allow_html=True)

    # ── My Cases section ──
    st.markdown('<div class="ns-section-header">My Cases</div>', unsafe_allow_html=True)
    non_pinned_cases = [c for c in user_cases_all if c.get("urgency") != "RED"]

    if not non_pinned_cases:
        st.markdown('<div class="ns-conv-empty">No saved cases</div>', unsafe_allow_html=True)
    else:
        for mc in non_pinned_cases[:5]:
            mc_title = mc.get("title", f"Case #{mc['id']}")
            mc_label = mc_title[:28] + ("…" if len(mc_title) > 28 else "")
            if st.button(
                f"⚖️  {mc_label}",
                key=f"ns_case_{mc['id']}",
                use_container_width=True,
            ):
                st.session_state.messages = mc.get("messages", [])
                st.session_state.current_case_title = mc_title
                st.session_state.selected_nav = "💬 AI Legal Chatbot"
                last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), "")
                if last_user_msg:
                    cls_res = classify_legal_issue(last_user_msg)
                    st.session_state.current_analysis = {
                        "category_id": cls_res["category_id"],
                        "category_name": cls_res["category_name"],
                        "classification": cls_res["classification"],
                        "urgency": cls_res["urgency"],
                        "urgency_badge": cls_res["urgency_badge"],
                        "urgency_reason": cls_res["urgency_reason"],
                        "primary_authority": cls_res["primary_authority"],
                        "detected_language": cls_res["detected_language"],
                        "provisions": legal_retriever.retrieve_provisions(cls_res["category_id"], last_user_msg),
                        "action_plan": get_action_plan(cls_res["category_id"], cls_res["detected_language"]),
                        "evidence": get_default_checklist(cls_res["category_id"], cls_res["detected_language"])
                    }
                    st.session_state.current_features = determine_required_features("LEGAL_PROBLEM", cls_res["urgency"])
                st.rerun()

    st.markdown('<div class="ns-divider"></div>', unsafe_allow_html=True)

    # ── Recents section ──
    # Exclude cases already shown in Pinned or My Cases to avoid duplicate widget keys
    _shown_ids = {c["id"] for c in pinned_cases[:5]} | {c["id"] for c in non_pinned_cases[:5]}
    st.markdown('<div class="ns-section-header">Recents</div>', unsafe_allow_html=True)
    recent_cases = [c for c in user_cases_all if c["id"] not in _shown_ids][:8]

    if not recent_cases:
        st.markdown('<div class="ns-conv-empty">No recent conversations</div>', unsafe_allow_html=True)
    else:
        for rc in recent_cases:
            rc_title = rc.get("title", f"Case #{rc['id']}")
            rc_label = rc_title[:30] + ("…" if len(rc_title) > 30 else "")
            if st.button(
                f"💬  {rc_label}",
                key=f"ns_recent_{rc['id']}",
                use_container_width=True,
            ):
                st.session_state.messages = rc.get("messages", [])
                st.session_state.current_case_title = rc_title
                st.session_state.selected_nav = "💬 AI Legal Chatbot"
                last_user_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"), "")
                if last_user_msg:
                    cls_res = classify_legal_issue(last_user_msg)
                    st.session_state.current_analysis = {
                        "category_id": cls_res["category_id"],
                        "category_name": cls_res["category_name"],
                        "classification": cls_res["classification"],
                        "urgency": cls_res["urgency"],
                        "urgency_badge": cls_res["urgency_badge"],
                        "urgency_reason": cls_res["urgency_reason"],
                        "primary_authority": cls_res["primary_authority"],
                        "detected_language": cls_res["detected_language"],
                        "provisions": legal_retriever.retrieve_provisions(cls_res["category_id"], last_user_msg),
                        "action_plan": get_action_plan(cls_res["category_id"], cls_res["detected_language"]),
                        "evidence": get_default_checklist(cls_res["category_id"], cls_res["detected_language"])
                    }
                    st.session_state.current_features = determine_required_features("LEGAL_PROBLEM", cls_res["urgency"])
                st.rerun()

    # ── Bottom profile section ──
    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    _initials = "".join([w[0].upper() for w in user.get("full_name", user["username"]).split()[:2]]) or "U"
    st.markdown(f"""
    <div class="ns-profile-section">
        <div class="ns-profile-row">
            <div class="ns-avatar">{_initials}</div>
            <div class="ns-profile-name">{user.get('full_name', user['username'])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="ns-logout-wrap">', unsafe_allow_html=True)
    if st.button("↪  Log out", key="ns_logout", use_container_width=True):
        st.session_state.user_authenticated = False
        st.session_state.user_info = None
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# TOP NAVIGATION BAR (Clean, modern aesthetic)
st.markdown(f"""
<div style="display: flex; align-items: center; gap: 12px; padding: 0.5rem 0;">
    <span style="font-size: 0.95rem; font-weight: 600; color: #E2E8F0;">NyayaSathi Workspace</span>
    <span style="color: #64748B;">/</span>
    <span style="font-size: 0.88rem; color: #38BDF8;">{st.session_state.selected_nav}</span>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# SECTION 1: CHATBOT INTERFACE (MAIN EXPERIENCE)
# ==============================================================================
if st.session_state.selected_nav == "💬 AI Legal Chatbot":
    # If no messages, render Modern Central Welcome Hero
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="chat-hero">
            <div class="chat-hero-icon">⚖️</div>
            <h1>Have a legal concern? Let's solve it together.</h1>
            <p>Ask anything about your legal rights, procedures, or dispute resolution. NyayaSathi is here to guide you.</p>
        </div>
        """, unsafe_allow_html=True)

    # Active Conversation View
    else:
        req_features = st.session_state.current_features or {}

        # Contextual Urgency Banner (Only rendered when show_urgency_alert is True)
        if req_features.get("show_urgency_alert") and st.session_state.current_analysis:
            ana = st.session_state.current_analysis
            urgency_code = ana.get("urgency", "GREEN")
            u_cls = "urgency-red" if urgency_code == "RED" else ("urgency-yellow" if urgency_code == "YELLOW" else "urgency-green")
            st.markdown(f"""
            <div class="urgency-banner {u_cls}">
                <div>
                    <b>{ana.get('urgency_badge')}</b><br>
                    <span style="font-size: 0.8rem; opacity: 0.9;">{ana.get('urgency_reason')}</span>
                </div>
                <div style="text-align: right; font-size: 0.78rem;">
                    <b>Authority:</b> {ana.get('primary_authority')}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Render Messages
        for msg in st.session_state.messages:
            avatar = "⚖️" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["content"])

        # CONDITIONAL RENDERING: Render legal tools ONLY when explicitly requested
        has_tools_to_show = any([
            req_features.get("show_action_plan"),
            req_features.get("show_evidence_checklist"),
            req_features.get("show_complaint_generator"),
            req_features.get("show_case_summary_export"),
            req_features.get("show_case_summary")
        ])

        if has_tools_to_show and st.session_state.current_analysis:
            curr_ana = st.session_state.current_analysis
            cat_id = curr_ana.get("category_id", "general")
            lang = curr_ana.get("detected_language", "en")

            # Dynamically determine tabs to construct
            tab_titles = []
            if req_features.get("show_action_plan"):
                tab_titles.append("📋 Step-by-Step Action Plan")
            if req_features.get("show_evidence_checklist"):
                tab_titles.append("📁 Evidence Checklist")
            if req_features.get("show_complaint_generator"):
                tab_titles.append("📝 Draft Legal Complaint")
            if req_features.get("show_case_summary_export") or req_features.get("show_case_summary"):
                tab_titles.append("📥 Case Summary Dossier")

            if tab_titles:
                st.markdown("---")
                st.markdown("<span style='font-size:0.9rem; font-weight:600; color:#38BDF8;'>🛠️ Requested Legal Tool</span>", unsafe_allow_html=True)

                rendered_tabs = st.tabs(tab_titles)
                tab_idx = 0

                # Tab 1: Action Plan
                if req_features.get("show_action_plan"):
                    with rendered_tabs[tab_idx]:
                        st.markdown("#### Step-by-Step Action Plan")
                    plan_steps = curr_ana.get("action_plan", []) or get_action_plan(cat_id, lang)
                    tot_steps = len(plan_steps)
                    done_steps = 0
                    for s in plan_steps:
                        sk = f"step_chk_{s.get('step')}"
                        chk = st.checkbox(
                            f"**Step {s.get('step')}: {s.get('title')}** ({s.get('timeframe')})",
                            key=sk,
                            value=st.session_state.checklist_checked.get(sk, False)
                        )
                        st.session_state.checklist_checked[sk] = chk
                        if chk:
                            done_steps += 1
                        st.caption(f"{s.get('description')} *[Statutory backing: {s.get('legal_backing', 'Indian Law')}]*")
                        if s.get("action_link"):
                            st.markdown(f"👉 [{s.get('action_text', 'Official Link')}]({s.get('action_link')})")
                    prg = (done_steps / tot_steps) if tot_steps > 0 else 0.0
                    st.progress(prg, text=f"Progress: {done_steps}/{tot_steps} Actions Completed ({int(prg*100)}%)")
                tab_idx += 1

            # Tab 2: Evidence Checklist
            if req_features.get("show_evidence_checklist"):
                with rendered_tabs[tab_idx]:
                    st.markdown("#### Evidence Checklist")
                    ev_list = curr_ana.get("evidence", []) or get_default_checklist(cat_id, lang)
                    tot_ev = len(ev_list) + len(st.session_state.custom_evidence_items)
                    done_ev = 0
                    for ev in ev_list:
                        iname = ev.get("item", str(ev))
                        ek = f"ev_chk_{ev.get('id', iname)}"
                        echk = st.checkbox(
                            f"**{iname}** — *[{ev.get('importance', 'Required')}]*",
                            key=ek,
                            value=st.session_state.checklist_checked.get(ek, False)
                        )
                        st.session_state.checklist_checked[ek] = echk
                        if echk:
                            done_ev += 1
                        if ev.get("details"):
                            st.caption(ev.get("details"))

                    # Custom evidence items
                    if st.session_state.custom_evidence_items:
                        st.markdown("**Custom Evidence:**")
                        for ci, citem in enumerate(st.session_state.custom_evidence_items):
                            ck = f"cust_ev_{ci}"
                            cval = st.checkbox(f"**{citem}** *(User Item)*", key=ck, value=st.session_state.checklist_checked.get(ck, False))
                            st.session_state.checklist_checked[ck] = cval
                            if cval:
                                done_ev += 1

                    ev_prg = (done_ev / tot_ev) if tot_ev > 0 else 0.0
                    st.progress(ev_prg, text=f"Evidence Collection: {done_ev}/{tot_ev} Preserved ({int(ev_prg*100)}%)")

                    add_c_in = st.text_input("Add Custom Evidence:", placeholder="e.g. Call audio recording, Bank dispute acknowledgement", key="in_add_ev")
                    if st.button("➕ Add to Checklist", key="btn_add_ev_chat"):
                        if add_c_in.strip() and add_c_in.strip() not in st.session_state.custom_evidence_items:
                            st.session_state.custom_evidence_items.append(add_c_in.strip())
                            st.rerun()
                tab_idx += 1

            # Tab 3: Complaint Generator
            if req_features.get("show_complaint_generator"):
                with rendered_tabs[tab_idx]:
                    st.markdown("#### Formal Complaint Draft")
                    def_comp = generate_complaint_text(
                        category_id=cat_id,
                        complainant_name=user.get("full_name", "Citizen"),
                        incident_details=st.session_state.messages[0]["content"] if st.session_state.messages else ""
                    )
                    comp_edit = st.text_area("Complaint Draft:", value=def_comp, height=260, key="quick_comp_text")
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button("📄 Download TXT", data=comp_edit, file_name=f"Complaint_{cat_id}.txt", mime="text/plain", use_container_width=True)
                    with col_d2:
                        pdf_b = generate_complaint_pdf(comp_edit, title="Formal Complaint Draft")
                        st.download_button("📑 Download PDF", data=pdf_b, file_name=f"Complaint_{cat_id}.pdf", mime="application/pdf", use_container_width=True)
                tab_idx += 1

            # Tab 4: Case Summary Dossier
            if req_features.get("show_case_summary_export"):
                with rendered_tabs[tab_idx]:
                    st.markdown("#### Export Case Dossier")
                    summary_b = generate_case_summary_pdf(
                        title=st.session_state.current_case_title,
                        problem_text=st.session_state.messages[0]["content"] if st.session_state.messages else "Legal Query",
                        category_name=curr_ana.get("category_name", "General"),
                        urgency_badge=curr_ana.get("urgency_badge", "General Guidance"),
                        ai_analysis_text=st.session_state.messages[-1]["content"] if st.session_state.messages else "",
                        action_plan=curr_ana.get("action_plan", []),
                        checklist=curr_ana.get("evidence", []) + [{"item": it, "importance": "Custom"} for it in st.session_state.custom_evidence_items]
                    )
                    st.download_button("📥 Download Case Summary (PDF)", data=summary_b, file_name=f"NyayaSathi_Summary_{datetime.now().strftime('%Y%m%d')}.pdf", mime="application/pdf", use_container_width=True)

    # Integrated Attachment / Multimodal Drawer
    with st.expander("📎 Attach Legal Document / Screenshot (Optional)", expanded=False):
        up_img = st.file_uploader("Upload Notice, Bill, or Transaction Screenshot:", type=["png", "jpg", "jpeg"], key="chat_img_uploader")
        doc_q = st.text_input("Question regarding this attachment:", placeholder="e.g. Is this eviction notice valid? Explain this bank debit message.")
        if up_img and st.button("🔍 Send Document for Legal Analysis", key="btn_send_img"):
            try:
                pil_im = Image.open(up_img)
                st.image(pil_im, width=280)
                with st.spinner("Analyzing document clauses, dates, and legal validity..."):
                    d_prompt = (
                        f"SYSTEM:\n"
                        f"You are NyayaSathi. The citizen uploaded a document/screenshot. "
                        f"Question: {doc_q or 'Analyze this document, extract key facts, and explain legal rights in simple terms.'}\n"
                        f"Explain clearly. Never guarantee legal validity without the stamped original."
                    )
                    d_resp = generate_ai_response(d_prompt, image_obj=pil_im)
                    st.session_state.messages.append({"role": "user", "content": f"[Attached Document]: {up_img.name}. {doc_q}"})
                    st.session_state.messages.append({"role": "assistant", "content": d_resp})
                    st.session_state.current_features = determine_required_features("DOCUMENT_ANALYSIS_REQUEST", "NONE")
                    st.rerun()
            except Exception as e:
                st.error(f"Image analysis error: {e}")

    # Inject ChatGPT-styled microphone & multilingual voice recognition into chat input
    inject_chat_voice_input()

    # Modern Bottom Chat Input Bar
    chat_prompt = st.chat_input("Ask NyayaSathi anything about your legal concern (English / हिन्दी / ಕನ್ನಡ)...", key="nyayasathi_chat_input")
    if chat_prompt:
        st.session_state.messages.append({"role": "user", "content": chat_prompt})

        # STEP 1 & 2: Classify Intent using conversation context & Gemini / semantic classifier
        intent_result = classify_user_intent(chat_prompt, st.session_state.messages[:-1], client=client)
        user_intent = intent_result["intent"]
        urgency_lvl = intent_result["urgency_level"]
        stage = intent_result.get("conversation_stage", "UNDERSTAND")

        # STEP 3: Determine Required Features Conditionally based on 5-stage flow
        active_features = determine_required_features(user_intent, urgency_lvl, stage)
        st.session_state.current_features = active_features

        # STEP 4: Legal Category Classification & RAG (only if legal context is needed)
        cid = intent_result.get("legal_category", "general")
        if cid in ["none", None]:
            cid = "general"

        # Preserve existing category in ongoing conversation for tool requests
        if cid == "general" and st.session_state.current_analysis:
            prev_cid = st.session_state.current_analysis.get("category_id", "general")
            if prev_cid != "general":
                cid = prev_cid

        clang = detect_language(chat_prompt)
        ret_provs = []

        # Maintain or construct analysis only when legal analysis is relevant
        has_active_tool = any([
            active_features.get("show_action_plan"),
            active_features.get("show_evidence_checklist"),
            active_features.get("show_complaint_generator"),
            active_features.get("show_case_summary_export"),
            active_features.get("show_case_summary")
        ])
        if has_active_tool or user_intent in ["INITIAL_PROBLEM_DESCRIPTION", "PROVIDE_LEGAL_GUIDANCE", "URGENT_LEGAL_PROBLEM", "FOLLOW_UP_NEXT_STEPS"]:
            cls_info = classify_legal_issue(chat_prompt)
            if (cls_info.get("category_id") != "general" and cls_info.get("confidence", 0) >= 0.5):
                cid = cls_info["category_id"]
            clang = cls_info["detected_language"]
            ret_provs = legal_retriever.retrieve_provisions(cid, chat_prompt)
            a_plan = get_action_plan(cid, clang)
            c_list = get_default_checklist(cid, clang)

            st.session_state.current_analysis = {
                "category_id": cid,
                "category_name": cls_info["category_name"],
                "classification": cls_info["classification"],
                "urgency": cls_info["urgency"],
                "urgency_badge": cls_info["urgency_badge"],
                "urgency_reason": cls_info["urgency_reason"],
                "primary_authority": cls_info["primary_authority"],
                "detected_language": clang,
                "provisions": ret_provs,
                "action_plan": a_plan,
                "evidence": c_list
            }

        # Update title if initial inquiry was a legal problem
        if st.session_state.current_case_title == "Untitled Legal Inquiry" and user_intent in ["INITIAL_PROBLEM_DESCRIPTION", "LEGAL_PROBLEM", "URGENT_LEGAL_PROBLEM"]:
            st.session_state.current_case_title = chat_prompt[:36] + ("..." if len(chat_prompt) > 36 else "")

        with st.chat_message("user", avatar="👤"):
            st.markdown(chat_prompt)

        with st.chat_message("assistant", avatar="⚖️"):
            with st.spinner("NyayaSathi is thinking..."):
                final_prompt = construct_contextual_prompt(
                    user_message=chat_prompt,
                    history=st.session_state.messages[:-1],
                    intent_data=intent_result,
                    rag_provisions=ret_provs
                )
                ans_text = generate_ai_response(final_prompt)
                if not ans_text or ans_text.startswith("⚠️"):
                    ans_text = generate_deterministic_legal_response(
                        user_message=chat_prompt,
                        intent_data=intent_result,
                        rag_provisions=ret_provs,
                        category_id=cid,
                        language=clang,
                        history=st.session_state.messages[:-1]
                    )
                st.markdown(ans_text)

        st.session_state.messages.append({"role": "assistant", "content": ans_text})

        # Persist session if part of an ongoing case
        if user_intent not in ["GREETING", "GENERAL_CONVERSATION"]:
            save_case(
                title=st.session_state.current_case_title,
                messages=st.session_state.messages,
                category_id=cid,
                urgency=urgency_lvl if urgency_lvl != "NONE" else "GREEN",
                user_id=user["id"]
            )
        st.rerun()


# ==============================================================================
# SECTION 2: MY SAVED CASES (ISOLATED TO AUTHENTICATED USER)
# ==============================================================================
elif st.session_state.selected_nav == "📁 My Saved Cases":
    st.markdown("## 📁 My Saved Cases & Inquiries")
    st.caption(f"Authenticated workspace for @{user['username']} — Only you have access to these legal records.")

    cases = get_saved_cases(user_id=user["id"], limit=30)
    if not cases:
        st.info("No saved cases found for your account. Start an inquiry in the AI Legal Chatbot to save cases automatically.")
    else:
        for c in cases:
            c_id = c["id"]
            title = c.get("title", f"Case #{c_id}")
            created = c.get("created_at", "")
            cat = c.get("category_id", "General")
            urgency = c.get("urgency", "GREEN")
            msgs = c.get("messages", [])

            with st.container():
                col_i, col_b1, col_b2 = st.columns([4, 1.2, 1])
                with col_i:
                    ub = "🔴 URGENT" if urgency == "RED" else ("🟡 RECOMMENDED" if urgency == "YELLOW" else "🟢 GENERAL")
                    st.markdown(f"**{title}** `{ub}`")
                    st.caption(f"Created: {created} | Category: {cat} | Messages: {len(msgs)}")
                with col_b1:
                    if st.button("🔄 Resume Case", key=f"btn_res_{c_id}", use_container_width=True):
                        st.session_state.messages = msgs
                        st.session_state.current_case_title = title
                        st.session_state.selected_nav = "💬 AI Legal Chatbot"
                        st.rerun()
                with col_b2:
                    if st.button("🗑️ Delete", key=f"btn_del_{c_id}", use_container_width=True):
                        delete_case(c_id, user_id=user["id"])
                        st.warning(f"Deleted case #{c_id}")
                        st.rerun()
                st.markdown("---")


# ==============================================================================
# SECTION 3: COMPLAINT GENERATOR (STANDALONE WORKSPACE)
# ==============================================================================
elif st.session_state.selected_nav == "📝 Complaint Generator":
    st.markdown("## 📝 Legal Complaint & Demand Notice Generator")
    st.caption("Generate structured pre-litigation notices and formal police/cyber/consumer complaints.")

    cg_col1, cg_col2 = st.columns(2)
    with cg_col1:
        comp_cat = st.selectbox("Select Complaint Type:", [
            ("cyber_fraud", "Cybercrime / UPI Fraud Police Complaint"),
            ("tenant_landlord", "Tenant Security Deposit Demand Notice"),
            ("consumer_complaint", "Consumer Court / e-Daakhil Complaint"),
            ("general", "General Legal Grievance & Pre-Litigation Notice")
        ], format_func=lambda x: x[1])
        c_name = st.text_input("Your Full Name:", value=user.get("full_name", "Shri/Smt. Citizen"), key="cg_name")
        c_contact = st.text_input("Your Contact Number & Email:", value="9876543210 | citizen@email.com", key="cg_contact")
        c_addr = st.text_input("Your Residential Address:", value="House No. 12, Main Road, Bengaluru, Karnataka", key="cg_addr")

    with cg_col2:
        o_name = st.text_input("Opposite Party / Entity Name:", value="Opposite Party / Fraudster / Company", key="cg_oname")
        o_addr = st.text_input("Opposite Party Address / Portal:", value="Branch Address / Official Email", key="cg_oaddr")
        d_amount = st.text_input("Dispute / Claim Amount (₹):", value="₹15,000", key="cg_amount")
        d_date = st.text_input("Date of Incident / Occurrence:", value=datetime.now().strftime("%d-%m-%Y"), key="cg_date")

    details_in = st.text_area("Detailed Statement of Occurrence / Facts:", placeholder="Explain chronologically what transpired...", height=120)

    generated_draft = generate_complaint_text(
        category_id=comp_cat[0],
        complainant_name=c_name,
        complainant_address=c_addr,
        complainant_contact=c_contact,
        opposite_party_name=o_name,
        opposite_party_address=o_addr,
        incident_date=d_date,
        incident_location="Bengaluru / Online",
        dispute_amount=d_amount,
        incident_details=details_in,
        transaction_ref="[UPI UTR / Order No / Agreement ID]"
    )

    st.markdown("### Formal Draft Preview & Editor")
    final_complaint = st.text_area("Review & Edit Draft:", value=generated_draft, height=320, key="cg_final_editor")

    exp_c1, exp_c2, exp_c3 = st.columns(3)
    with exp_c1:
        st.download_button("📄 Download as TXT", data=final_complaint, file_name=f"Complaint_{comp_cat[0]}.txt", mime="text/plain", use_container_width=True)
    with exp_c2:
        pdf_data = generate_complaint_pdf(final_complaint, title="Formal Complaint Draft")
        st.download_button("📑 Download as PDF", data=pdf_data, file_name=f"Complaint_{comp_cat[0]}.pdf", mime="application/pdf", use_container_width=True)
    with exp_c3:
        if st.button("💾 Save Complaint to My Records", use_container_width=True, key="btn_save_complaint"):
            save_complaint(
                analysis_id=None,
                title=f"Draft: {c_name} vs {o_name}",
                category_id=comp_cat[0],
                complainant_name=c_name,
                opposite_party=o_name,
                incident_date=d_date,
                incident_location="Online/Local",
                dispute_amount=d_amount,
                complaint_text=final_complaint,
                user_id=user["id"]
            )
            st.success("Complaint draft saved to your database!")


# ==============================================================================
# SECTION 4: VERIFIED LEGAL RESOURCES & STATUTES (RAG BROWSER)
# ==============================================================================
elif st.session_state.selected_nav == "📚 Verified Legal Resources":
    st.markdown("## 📚 Verified Indian Legal Knowledge Base (RAG)")
    st.caption("Statutory provisions sourced from official Gazette publications and government repositories.")

    all_cats = legal_retriever.get_all_categories()
    sel_cat = st.selectbox(
        "Select Legal Category:",
        options=list(all_cats.keys()),
        format_func=lambda x: all_cats[x].get("name", x)
    )

    if sel_cat in all_cats:
        cdata = all_cats[sel_cat]
        st.markdown(f"### {cdata.get('name')}")
        st.markdown(f"**Hindi:** {cdata.get('hindi_name')} | **Kannada:** {cdata.get('kannada_name')}")
        st.markdown(f"**Classification:** {cdata.get('classification')}")
        st.markdown(f"**Default Urgency Level:** `{cdata.get('urgency_level')}`")
        if cdata.get("urgency_reason"):
            st.info(f"**Urgency Basis:** {cdata.get('urgency_reason')}")

        st.markdown("#### 🚨 Official Designated Contacts & Helplines")
        for con in cdata.get("emergency_contacts", []):
            st.markdown(f"- **{con.get('name')}**: `{con.get('number', con.get('url', ''))}` ({con.get('details', '')})")

        st.markdown("#### 📜 Statutory Provisions & Simplified Explanations")
        for p in cdata.get("provisions", []):
            with st.expander(f"**{p.get('act')} — {p.get('section')}: {p.get('title')}**", expanded=True):
                st.markdown(f"**Official Description:** {p.get('description')}")
                st.markdown(f"**Plain Language Meaning:** {p.get('simple_explanation')}")
                st.caption(f"Source: {p.get('official_source')} | Verified: {'✅ Yes' if p.get('verified') else '⚠️ Pending'}")


# ==============================================================================
# SECTION 5: NATIONAL EMERGENCY & LEGAL HELPLINES DIRECTORY
# ==============================================================================
elif st.session_state.selected_nav == "☎️ Explore Helplines":
    st.markdown("## ☎️ Verified National Emergency & Legal Helplines")
    st.caption("Official 24x7 toll-free emergency numbers, government authorities, and legal aid institutions across India.")

    h_col1, h_col2 = st.columns(2)
    with h_col1:
        st.markdown("""
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">🚨 National Cyber Financial Fraud</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">1930</div>
            <div class="prompt-card-desc">Citizen Financial Cyber Fraud Reporting System (MHA / I4C). Report within the golden hour to freeze unauthorized banking transactions.</div>
            <div style="margin-top: 0.6rem;"><a href="https://cybercrime.gov.in" target="_blank" style="color: #38BDF8; font-size: 0.82rem;">Official Portal: cybercrime.gov.in ↗</a></div>
        </div>
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">⚖️ NALSA Free Legal Aid Helpline</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">15100</div>
            <div class="prompt-card-desc">National Legal Services Authority. Free legal advice, lawyer assignment, and representation for eligible citizens under Legal Services Authorities Act, 1987.</div>
            <div style="margin-top: 0.6rem;"><a href="https://nalsa.gov.in" target="_blank" style="color: #38BDF8; font-size: 0.82rem;">Official Portal: nalsa.gov.in ↗</a></div>
        </div>
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">👩 Women in Distress Helpline</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">181</div>
            <div class="prompt-card-desc">Ministry of Women and Child Development. 24-hour emergency response for women affected by violence, domestic abuse, harassment, and dowry threats.</div>
        </div>
        <div class="prompt-card">
            <div class="prompt-card-title">👶 Childline Emergency</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">1098</div>
            <div class="prompt-card-desc">Emergency outreach service for children in need of care and protection, abandonment, child labor, and abuse reporting.</div>
        </div>
        """, unsafe_allow_html=True)

    with h_col2:
        st.markdown("""
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">🚓 All-India Police & Emergency Services</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">112</div>
            <div class="prompt-card-desc">Emergency Response Support System (ERSS). Integrated pan-India emergency number for Police, Fire, and Ambulance services.</div>
        </div>
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">🛍️ National Consumer Helpline (NCH)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">1915</div>
            <div class="prompt-card-desc">Department of Consumer Affairs. Register grievances regarding defective products, refund denials, misleading ads, and unfair trade practices.</div>
            <div style="margin-top: 0.6rem;"><a href="https://consumerhelpline.gov.in" target="_blank" style="color: #38BDF8; font-size: 0.82rem;">Official Portal: consumerhelpline.gov.in ↗</a></div>
        </div>
        <div class="prompt-card" style="margin-bottom: 1rem;">
            <div class="prompt-card-title">👴 Elderline (Senior Citizens Helpline)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">14567</div>
            <div class="prompt-card-desc">Ministry of Social Justice and Empowerment. Guidance on elderly rights, abandonment, maintenance under MWPSC Act, and legal aid.</div>
        </div>
        <div class="prompt-card">
            <div class="prompt-card-title">🩺 Tele-MANAS (Mental Health Support)</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #38BDF8; margin: 0.3rem 0;">14416</div>
            <div class="prompt-card-desc">National Tele Mental Health Programme of India. Comprehensive, 24x7 mental health counseling and crisis support in multiple Indian languages.</div>
        </div>
        """, unsafe_allow_html=True)
