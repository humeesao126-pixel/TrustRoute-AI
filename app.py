import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from src.schemas import RiskLevel, DueDiligenceReport, ExtractedOffer
from src.agents import extract_text_from_pdf
from src.graph import pipeline

load_dotenv()

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="TrustRoute AI | Germany Job Offer Verification",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Senior UI/UX Theme Engine: Pure Champagne (#F8E7C9) + Clean White Cards
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

      /* Hide empty containers */
      .tr-card:empty,
      div:empty {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
      }

      /* Header & Toolbar */
      header[data-testid="stHeader"],
      .stAppHeader,
      div[data-testid="stToolbar"],
      div[data-testid="stDecoration"] {
        background-color: #f8e7c9 !important;
        background: #f8e7c9 !important;
        color: #0b3b2a !important;
      }
      header[data-testid="stHeader"] button,
      header[data-testid="stHeader"] svg,
      div[data-testid="stToolbar"] button,
      div[data-testid="stToolbar"] svg,
      div[data-testid="stToolbar"] span,
      .stAppDeployButton,
      .stAppDeployButton * {
        color: #0b3b2a !important;
        fill: #0b3b2a !important;
        stroke: #0b3b2a !important;
      }
      .stAppDeployButton > button {
        background-color: #ffffff !important;
        border: 1.5px solid #0b3b2a !important;
        border-radius: 8px !important;
      }

      /* Global Canvas */
      html, body, [class*="css"], .stApp, section[data-testid="stSidebar"], .main {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #f8e7c9 !important;
        color: #0a261b !important;
      }

      .main .block-container {
        max-width: 1180px;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        overflow-y: visible !important;
      }

      /* Hero Banner */
      .tr-hero {
        background: linear-gradient(135deg, #0b3b2a 0%, #14573f 60%, #072a1e 100%);
        color: #ffffff !important;
        padding: 2.2rem 2.5rem;
        border-radius: 14px;
        margin-bottom: 1.3rem;
        box-shadow: 0 10px 24px rgba(11, 59, 42, 0.16);
      }
      .tr-hero h1, .tr-hero p {
        color: #ffffff !important;
      }
      
      /* Pure Black Badge Text on Champagne Chip */
      .tr-hero .tr-tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.76rem;
        font-weight: 800 !important;
        text-transform: uppercase;
        color: #000000 !important;
        background-color: #f8e7c9 !important;
        border: 1.5px solid #d4c19f !important;
        padding: 5px 14px;
        border-radius: 6px;
        margin-bottom: 0.65rem;
        letter-spacing: 0.06em;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
      }

      .tr-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
        color: #ffffff !important;
      }
      .tr-subtitle {
        font-size: 0.98rem;
        margin-top: 0.45rem;
        color: #e2f4eb !important;
        max-width: 78ch;
        line-height: 1.55;
      }

      /* White Card Surfaces */
      .tr-card {
        background: #ffffff !important;
        border: 1px solid #e5d4b4 !important;
        border-radius: 12px;
        padding: 1.4rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 4px 12px rgba(11, 59, 42, 0.04);
      }
      .tr-card-header {
        font-size: 1.08rem;
        font-weight: 800;
        color: #0b3b2a !important;
        margin-bottom: 0.85rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
      }
      .tr-card-caption {
        font-size: 0.84rem;
        color: #4f6357 !important;
        margin-top: -0.4rem;
        margin-bottom: 1rem;
        line-height: 1.45;
      }

      /* Rule Box */
      .tr-rules-card {
        background: #ffffff !important;
        border: 1px solid #e5d4b4 !important;
        border-left: 6px solid #0b3b2a !important;
        border-radius: 12px;
        padding: 1.2rem 1.6rem;
        margin-bottom: 1.3rem;
        font-size: 0.88rem;
        line-height: 1.6;
        color: #0a261b !important;
        box-shadow: 0 4px 12px rgba(11, 59, 42, 0.04);
      }
      .tr-rules-card-title {
        font-weight: 800;
        font-size: 0.96rem;
        margin-bottom: 0.35rem;
        color: #0b3b2a;
      }
      .tr-rules-card ol {
        margin: 0.35rem 0 0 1.2rem;
        padding: 0;
      }
      .tr-rules-card li {
        margin-bottom: 0.25rem;
      }

      /* File Uploader Container */
      div[data-testid="stFileUploader"],
      div[data-testid="stFileUploader"] > section,
      div[data-testid="stFileUploaderDropzone"] {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1.5px solid #d4c19f !important;
        border-radius: 10px !important;
        color: #0a261b !important;
      }
      div[data-testid="stFileUploaderDropzone"] * {
        color: #0a261b !important;
      }
      div[data-testid="stFileUploaderDropzone"] button,
      div[data-testid="stFileUploader"] button {
        background-color: #f8e7c9 !important;
        color: #0b3b2a !important;
        border: 1.5px solid #d4c19f !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
      }

      /* Uploaded File Chip */
      div[data-testid="stFileUploaderFile"],
      div[data-testid="stFileUploaderFileData"],
      div[data-testid="stFileUploader"] ul li,
      div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
        background-color: #11281f !important;
        background: #11281f !important;
        border: 1.5px solid #0b3b2a !important;
        border-radius: 8px !important;
        color: #ffffff !important;
      }
      div[data-testid="stFileUploaderFile"] *,
      div[data-testid="stFileUploaderFileData"] *,
      div[data-testid="stFileUploaderFile"] span,
      div[data-testid="stFileUploaderFile"] small {
        color: #ffffff !important;
        fill: #ffffff !important;
        font-weight: 600 !important;
      }
      div[data-testid="stFileUploaderFile"] button {
        background-color: #0b3b2a !important;
        color: #ffffff !important;
        border: 1px solid #14573f !important;
      }

      /* Textarea & Inputs - Force Light Mode On Surface */
      .stTextArea,
      .stTextInput {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
      }

      div[data-baseweb="textarea"],
      div[data-baseweb="textarea"] > div,
      div[data-baseweb="input"],
      div[data-baseweb="input"] > div {
        background-color: #ffffff !important;
        background: #ffffff !important;
        border: 1.5px solid #d4c19f !important;
        border-radius: 10px !important;
        box-shadow: none !important;
      }

      div[data-baseweb="textarea"] textarea,
      div[data-baseweb="input"] input,
      .stTextArea textarea,
      .stTextInput input {
        background-color: #ffffff !important;
        background: #ffffff !important;
        color: #0a261b !important;
        -webkit-text-fill-color: #0a261b !important;
        font-size: 0.94rem !important;
        font-weight: 500 !important;
        line-height: 1.5 !important;
        padding: 0.85rem !important;
      }

      ::placeholder,
      textarea::placeholder,
      input::placeholder,
      div[data-baseweb="textarea"] textarea::placeholder,
      div[data-baseweb="input"] input::placeholder {
        color: #5d7065 !important;
        opacity: 0.9 !important;
        -webkit-text-fill-color: #5d7065 !important;
        font-weight: 500 !important;
      }

      div[data-baseweb="textarea"]:focus-within,
      div[data-baseweb="input"]:focus-within {
        border-color: #0b3b2a !important;
        box-shadow: 0 0 0 2px rgba(11, 59, 42, 0.15) !important;
      }

      /* Buttons */
      div.stButton > button[kind="primary"] {
        background-color: #0b3b2a !important;
        color: #ffffff !important;
        border: 1px solid #0b3b2a !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1.4rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
      }
      div.stButton > button[kind="primary"]:hover {
        background-color: #14573f !important;
        border-color: #14573f !important;
        box-shadow: 0 4px 12px rgba(11, 59, 42, 0.2) !important;
      }
      div.stButton > button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #0b3b2a !important;
        border: 1.5px solid #d4c19f !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1.4rem !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
      }
      div.stButton > button[kind="secondary"]:hover {
        background-color: #fcf4e6 !important;
        border-color: #0b3b2a !important;
      }

      /* Download Button */
      div[data-testid="stDownloadButton"] > button {
        background-color: #0b3b2a !important;
        background: #0b3b2a !important;
        color: #ffffff !important;
        border: 1.5px solid #0b3b2a !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 14px rgba(11, 59, 42, 0.15) !important;
        transition: all 0.2s ease-in-out !important;
      }
      div[data-testid="stDownloadButton"] > button:hover {
        background-color: #14573f !important;
        background: #14573f !important;
        border-color: #14573f !important;
        box-shadow: 0 6px 18px rgba(11, 59, 42, 0.25) !important;
      }
      div[data-testid="stDownloadButton"] > button * {
        color: #ffffff !important;
      }

      /* Structured Tiles */
      .tr-info-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 0.9rem;
        margin-top: 0.5rem;
      }
      .tr-info-tile {
        background: #fdfaf4;
        border: 1px solid #ebdcc5;
        border-radius: 10px;
        padding: 0.95rem 1.15rem;
      }
      .tr-info-label {
        font-size: 0.72rem;
        color: #5d7065;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 700;
      }
      .tr-info-value {
        font-size: 0.95rem;
        font-weight: 800;
        margin-top: 0.3rem;
        color: #0a261b;
      }

      /* Score Box */
      .tr-score-box {
        background: #ffffff;
        border: 1px solid #e5d4b4;
        border-left: 6px solid #0b3b2a;
        border-radius: 12px;
        padding: 1.6rem;
        margin-bottom: 1.3rem;
        box-shadow: 0 4px 14px rgba(11, 59, 42, 0.04);
      }
      .tr-score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
      }
      .tr-score-number {
        font-size: 3.2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
        line-height: 1;
      }
      .tr-pillar-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.85rem;
        margin-top: 1.3rem;
      }
      .tr-pillar-card {
        background: #fdfaf4;
        border: 1px solid #ebdcc5;
        border-radius: 10px;
        padding: 0.95rem 0.85rem;
        text-align: center;
      }
      .tr-pillar-title {
        font-size: 0.76rem;
        font-weight: 700;
        color: #5d7065;
      }
      .tr-pillar-status {
        font-size: 0.9rem;
        font-weight: 800;
        margin-top: 0.35rem;
      }

      /* Findings Cards */
      .tr-finding-card {
        background: #fdfaf4;
        border: 1px solid #ebdcc5;
        border-radius: 10px;
        padding: 1.25rem;
        margin-bottom: 0.9rem;
      }
      .tr-evidence-snippet {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        background: #ffffff;
        border: 1px solid #e5d4b4;
        border-left: 3.5px solid #0b3b2a;
        padding: 0.7rem 0.9rem;
        border-radius: 0 8px 8px 0;
        margin: 0.55rem 0;
        line-height: 1.45;
        color: #0a261b;
      }

      /* Badges */
      .badge-pass {
        background: #e2f7e7;
        color: #065f46;
        border: 1px solid #82d896;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.72rem;
      }
      .badge-warn {
        background: #fef4db;
        color: #854d0e;
        border: 1px solid #f2ce76;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.72rem;
      }
      .badge-fail {
        background: #fde5e5;
        color: #991b1b;
        border: 1px solid #f89d9d;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 800;
        font-size: 0.72rem;
      }

      /* Sidebar Component */
      .tr-author-box {
        background: #ffffff;
        border: 1px solid #e5d4b4;
        border-radius: 12px;
        padding: 1.25rem;
        margin-top: 1.2rem;
        box-shadow: 0 4px 12px rgba(11, 59, 42, 0.03);
      }
      .tr-author-name {
        font-size: 1.1rem;
        font-weight: 800;
        color: #0b3b2a;
        margin: 0;
      }
      .tr-author-sub {
        font-size: 0.82rem;
        color: #5d7065;
        margin-top: 0.2rem;
        margin-bottom: 0.85rem;
        font-weight: 600;
      }
      .tr-author-link {
        display: block;
        font-size: 0.84rem;
        font-weight: 700;
        color: #0b3b2a !important;
        text-decoration: none;
        margin-bottom: 0.35rem;
      }
      .tr-author-link:hover {
        text-decoration: underline;
      }

      .tr-footer {
        border-top: 1px solid #e5d4b4;
        padding: 2.2rem 0;
        margin-top: 4rem;
        text-align: center;
        color: #5d7065;
        font-size: 0.86rem;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# State Management
# -----------------------------------------------------------------------------
if "document_text" not in st.session_state:
    st.session_state.document_text = ""
if "extracted_offer" not in st.session_state:
    st.session_state.extracted_offer = None
if "audit_findings" not in st.session_state:
    st.session_state.audit_findings = []
if "final_report" not in st.session_state:
    st.session_state.final_report = None
if "human_reviewed" not in st.session_state:
    st.session_state.human_reviewed = False
if "reviewer_notes" not in st.session_state:
    st.session_state.reviewer_notes = "Official verification completed against government records."
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

def calculate_score(findings: list) -> tuple[int, str, str]:
    """Calculates a clean 0-100 authenticity score without artificial slashes."""
    if not findings:
        return 0, "#5d7065", "Not evaluated yet."

    score = 100
    for f in findings:
        if f.status == RiskLevel.WARNING:
            score -= 35
        elif f.status == RiskLevel.INCONSISTENCY:
            score -= 20
        elif f.status == RiskLevel.UNVERIFIED:
            score -= 10

    score = max(5, min(100, score))

    if score >= 80:
        return score, "#0b3b2a", "Safe offer. All government databases and statutory checks passed."
    elif score >= 50:
        return score, "#854d0e", "Moderate risk. Contract contains ambiguous terms requiring clarification."
    else:
        return score, "#991b1b", "High risk. Direct violations and suspicious financial terms detected."

def run_investigation():
    """Runs the LangGraph pipeline with explicit error reporting and safe execution."""
    if not st.session_state.document_text.strip():
        st.warning("⚠️ Please provide an employment contract text or PDF first.")
        return

    with st.spinner("⏳ Analyzing contract and verifying official registries..."):
        try:
            initial_state = {
                "document_text": st.session_state.document_text,
                "extracted_offer": None,
                "audit_findings": [],
                "final_report": None,
                "human_approved": False,
            }
            res = pipeline.invoke(initial_state)

            st.session_state.extracted_offer = res.get("extracted_offer")
            st.session_state.audit_findings = res.get("audit_findings", [])
            st.session_state.final_report = res.get("final_report")
            st.session_state.human_reviewed = False

            if not st.session_state.extracted_offer:
                st.error("⚠️ Extraction finished, but returned no entities. Check that the document contains text.")
                return

            score, _, _ = calculate_score(st.session_state.audit_findings)
            if score < 50:
                st.session_state.reviewer_notes = "Advisory: Serious discrepancies identified. Candidate should not pay fees or sign."
            elif score < 80:
                st.session_state.reviewer_notes = "Advisory: Employer or terms require direct follow-up before formal visa filing."
            else:
                st.session_state.reviewer_notes = "Cleared: Terms comply with German minimum wage, Blue Card statutes, and registered employers."

        except Exception as e:
            err_msg = str(e)
            if "RESOURCE_EXHAUSTED" in err_msg or "429" in err_msg:
                st.error("⚠️ Gemini API Rate Limit Reached (429 Quota Exceeded). Please verify your Google AI Studio quota or use an alternative key.")
            else:
                st.error(f"❌ Backend Execution Failed: {err_msg}")

# -----------------------------------------------------------------------------
# Sidebar: System Controls & Profile
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### System Health")
    has_api_key = bool(os.getenv("GEMINI_API_KEY"))
    if has_api_key:
        st.success("Verification Engine: Online")
    else:
        st.error("API Key Missing")

    db_path = os.path.join("data", "registries.db")
    if os.path.exists(db_path):
        st.success("Official Databases: Ready")
    else:
        st.error("Registries DB Missing")

    st.markdown("---")
    st.caption("Active Government Databases:")
    st.caption("• German Handelsregister (Company Registry)")
    st.caption("• Pakistan Bureau of Emigration (BEOE)")
    st.caption("• Mindestlohn & BAMF Salary Rules")

    st.markdown("---")
    if st.button("Start New Case", use_container_width=True):
        st.session_state.document_text = ""
        st.session_state.extracted_offer = None
        st.session_state.audit_findings = []
        st.session_state.final_report = None
        st.session_state.human_reviewed = False
        st.session_state.reviewer_notes = "Official verification completed against government records."
        st.session_state.uploader_key += 1
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div class="tr-author-box">
          <div class="tr-author-name">Hamza Shoaib</div>
          <div class="tr-author-sub">AI & ML Engineer</div>
          <a class="tr-author-link" href="https://linkedin.com/in/ch-hamza-shoaib" target="_blank">LinkedIn</a>
          <a class="tr-author-link" href="https://github.com/hamxashoaib" target="_blank">GitHub</a>
          <a class="tr-author-link" href="https://hamzashoaib.dev" target="_blank">Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# Main Hero Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="tr-hero">
      <span class="tr-tag" style="color: #000000 !important; font-weight: 800 !important;">
        Autonomous Employment Due Diligence
      </span>
      <h1 class="tr-title">TrustRoute AI</h1>
      <div class="tr-subtitle">
        Independent evidence-based verification for job offers bound for Germany. 
        Protects candidates by cross-examining company registrations, recruitment licenses, and wage laws.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Verification Rules Card
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="tr-rules-card">
      <div class="tr-rules-card-title">3 Key Verification Rules:</div>
      <ol>
        <li>Legitimate German employers never demand placement fees through JazzCash, EasyPaisa, or personal bank accounts.</li>
        <li>Official German visa processing fees are paid exclusively at official embassy centers (Gerry's or VFS Global).</li>
        <li>Pakistani overseas recruiting agencies must maintain an active license with the Bureau of Emigration (BEOE).</li>
      </ol>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# STEP 1: Document Intake
# -----------------------------------------------------------------------------
st.markdown('<div class="tr-card">', unsafe_allow_html=True)
st.markdown('<div class="tr-card-header">📄 Step 1: Upload or Paste Offer Letter</div>', unsafe_allow_html=True)
st.markdown('<div class="tr-card-caption">Upload an official candidate employment contract (PDF) or paste the clauses directly below for inspection.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Candidate Offer Letter (PDF)",
    type=["pdf"],
    key=f"uploader_{st.session_state.uploader_key}",
    label_visibility="collapsed",
)

if uploaded_file is not None:
    uploaded_file.seek(0)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name
    try:
        parsed_text = extract_text_from_pdf(tmp_path)
        if parsed_text and parsed_text != st.session_state.document_text:
            st.session_state.document_text = parsed_text
            st.session_state.extracted_offer = None
            st.session_state.audit_findings = []
            st.session_state.final_report = None
            st.session_state.human_reviewed = False
            st.rerun()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

st.write("")

# Single Clean & Bold Section Label
st.markdown('<div style="font-size: 0.96rem; font-weight: 800; color: #0b3b2a; margin-bottom: 0.45rem;">Offer Text Content:</div>', unsafe_allow_html=True)

doc_text_input = st.text_area(
    "",
    value=st.session_state.document_text,
    height=240,
    placeholder="Type or paste the job offer / contract text here, or upload a PDF above...",
    label_visibility="collapsed",
)
if doc_text_input != st.session_state.document_text:
    st.session_state.document_text = doc_text_input

btn_col1, btn_col2 = st.columns([2, 1])
with btn_col1:
    if st.button("🚀 Verify Job Offer", type="primary", use_container_width=True):
        run_investigation()
        st.rerun()
with btn_col2:
    if st.button("Clear Document", type="secondary", use_container_width=True):
        st.session_state.document_text = ""
        st.session_state.extracted_offer = None
        st.session_state.audit_findings = []
        st.session_state.final_report = None
        st.session_state.human_reviewed = False
        st.session_state.uploader_key += 1
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STEP 2: Extracted Information (Full Width Clean Porcelain Tiles)
# -----------------------------------------------------------------------------
if st.session_state.extracted_offer:
    offer: ExtractedOffer = st.session_state.extracted_offer

    fee_badge = (
        '<span class="badge-fail">Advance Payment Demanded</span>'
        if offer.upfront_payment_requested
        else '<span class="badge-pass">No Advance Fees</span>'
    )

    st.markdown('<div class="tr-card">', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-header">📋 Step 2: Extracted Offer Information</div>', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-caption">Structured contract entities parsed according to the validated schema.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="tr-info-grid">
          <div class="tr-info-tile">
            <div class="tr-info-label">Hiring Employer</div>
            <div class="tr-info-value">{offer.employer_name or 'Not specified'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Location & Registry ID</div>
            <div class="tr-info-value">{offer.location_city or 'City unlisted'}, {offer.commercial_register_id or 'No ID'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Designation</div>
            <div class="tr-info-value">{offer.job_title or 'Not specified'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Offered Base Salary</div>
            <div class="tr-info-value">{f'€{offer.gross_annual_salary_eur:,.2f} per year' if offer.gross_annual_salary_eur else 'Not stated'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Recruiter / Intermediary</div>
            <div class="tr-info-value">{offer.recruiter_agency_name or 'Direct Application'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Pakistani OEP License</div>
            <div class="tr-info-value">{offer.oep_license_number or 'No license cited'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Visa Route</div>
            <div class="tr-info-value">{offer.stated_visa_type or 'General Visa'}</div>
          </div>
          <div class="tr-info-tile">
            <div class="tr-info-label">Advance Processing Fee</div>
            <div class="tr-info-value">{fee_badge}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# STEP 3: Verification Verdict & 4-Pillar Score
# -----------------------------------------------------------------------------
if st.session_state.audit_findings:
    score_val, score_color, score_summary = calculate_score(st.session_state.audit_findings)

    pillars = {
        "Employer Registry": ("Verified Active", "#0b3b2a"),
        "Recruiter Agency": ("Licensed", "#0b3b2a"),
        "Statutory Salary": ("Compliant", "#0b3b2a"),
        "Payment Security": ("No Upfront Fee", "#0b3b2a"),
    }
    for f in st.session_state.audit_findings:
        if "Employer" in f.category and f.status != RiskLevel.VERIFIED:
            pillars["Employer Registry"] = ("Discrepancy", "#991b1b")
        elif "Recruiter" in f.category and f.status != RiskLevel.VERIFIED:
            pillars["Recruiter Agency"] = ("Unlicensed/Suspended", "#991b1b")
        elif "Compensation" in f.category and f.status != RiskLevel.VERIFIED:
            pillars["Statutory Salary"] = ("Below Threshold", "#854d0e")
        elif "Payment" in f.category and f.status != RiskLevel.VERIFIED:
            pillars["Payment Security"] = ("Illegal Advance Fee", "#991b1b")

    st.markdown(
        f"""
        <div class="tr-score-box" style="border-left-color: {score_color};">
          <div class="tr-score-header">
            <div>
              <div style="font-size: 1.25rem; font-weight: 800; color: #0a261b;">Authenticity & Due Diligence Score</div>
              <div style="font-size: 0.94rem; color: #5d7065; margin-top: 0.25rem; font-weight: 600;">{score_summary}</div>
            </div>
            <div class="tr-score-number" style="color: {score_color};">
              {score_val}<span style="font-size: 1.3rem; opacity: 0.7;">/100</span>
            </div>
          </div>
          <div class="tr-pillar-grid">
            <div class="tr-pillar-card">
              <div class="tr-pillar-title">German Registry</div>
              <div class="tr-pillar-status" style="color: {pillars['Employer Registry'][1]};">{pillars['Employer Registry'][0]}</div>
            </div>
            <div class="tr-pillar-card">
              <div class="tr-pillar-title">BEOE Recruiter License</div>
              <div class="tr-pillar-status" style="color: {pillars['Recruiter Agency'][1]};">{pillars['Recruiter Agency'][0]}</div>
            </div>
            <div class="tr-pillar-card">
              <div class="tr-pillar-title">German Minimum Wage</div>
              <div class="tr-pillar-status" style="color: {pillars['Statutory Salary'][1]};">{pillars['Statutory Salary'][0]}</div>
            </div>
            <div class="tr-pillar-card">
              <div class="tr-pillar-title">Payment Route</div>
              <div class="tr-pillar-status" style="color: {pillars['Payment Security'][1]};">{pillars['Payment Security'][0]}</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Detailed Findings Grid
    st.markdown('<div class="tr-card">', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-header">⚖️ Step 3: Official Verification Findings</div>', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-caption">Detailed findings generated by querying government authorities deterministically.</div>', unsafe_allow_html=True)

    badge_map = {
        RiskLevel.VERIFIED: '<span class="badge-pass">Verified Safe</span>',
        RiskLevel.UNVERIFIED: '<span class="badge-warn">Cannot Confirm</span>',
        RiskLevel.INCONSISTENCY: '<span class="badge-warn">Discrepancy</span>',
        RiskLevel.WARNING: '<span class="badge-fail">Violation Flagged</span>',
    }

    grid_cols = st.columns(2, gap="medium")
    for i, finding in enumerate(st.session_state.audit_findings):
        with grid_cols[i % 2]:
            st.markdown(
                f"""
                <div class="tr-finding-card">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.45rem;">
                    <span style="font-weight: 800; font-size: 0.95rem; color: #0a261b;">{finding.category}</span>
                    {badge_map.get(finding.status, '')}
                  </div>
                  <div style="font-size: 0.88rem; margin: 0.4rem 0; color: #0a261b; font-weight: 600;">
                    <b>Finding:</b> {finding.finding_summary}
                  </div>
                  <div class="tr-evidence-snippet">
                    <b>Document proof:</b><br/>{finding.evidence_snippet}
                  </div>
                  <div style="font-size: 0.78rem; color: #5d7065; margin-top: 0.4rem; font-weight: 600;">
                    <b>Authority checked:</b> {finding.source_checked}
                  </div>
                  <div style="font-size: 0.85rem; color: #0b3b2a; font-weight: 800; margin-top: 0.4rem;">
                    <b>Action for candidate:</b> {finding.action_for_candidate}
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # STEP 4: Human Reviewer Adjudication Gate
    # -------------------------------------------------------------------------
    st.markdown('<div class="tr-card">', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-header">👤 Step 4: Reviewer Sign-Off and Release</div>', unsafe_allow_html=True)
    st.markdown('<div class="tr-card-caption">Case reviewer confirms evidence and stamps approval before authoring the final dossier.</div>', unsafe_allow_html=True)

    col_note, col_auth = st.columns([2.5, 1], gap="medium")
    with col_note:
        rev_note = st.text_input(
            "Officer Verification Statement:",
            value=st.session_state.reviewer_notes,
        )
        st.session_state.reviewer_notes = rev_note

    with col_auth:
        st.write("")
        st.write("")
        if not st.session_state.human_reviewed:
            if st.button("Authorize Report", type="primary", use_container_width=True):
                st.session_state.human_reviewed = True
                st.rerun()
        else:
            st.success("Authorized by Case Reviewer")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Final Dossier Output
# -----------------------------------------------------------------------------
if st.session_state.human_reviewed and st.session_state.final_report:
    report: DueDiligenceReport = st.session_state.final_report

    color_accent = "#0b3b2a"
    if "Caution" in report.overall_risk_profile:
        color_accent = "#991b1b"
    elif "Verification" in report.overall_risk_profile:
        color_accent = "#854d0e"

    st.markdown(
        f"""
        <div class="tr-card" style="border-top: 6px solid {color_accent};">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.9rem;">
            <h3 style="margin: 0; font-size: 1.25rem; font-weight: 800; color: #0a261b;">Official Case Summary</h3>
            <span style="font-size: 0.95rem; font-weight: 800; color: {color_accent}; background: #fdfaf4; padding: 5px 14px; border-radius: 8px; border: 1.5px solid #ebdcc5;">
              {report.overall_risk_profile}
            </span>
          </div>
          <p style="font-size: 0.88rem; margin-bottom: 0.8rem; color: #0a261b;"><b>Reviewer Statement:</b> {st.session_state.reviewer_notes}</p>
          <h4 style="font-size: 0.95rem; font-weight: 800; margin-top: 1rem; color: #0a261b;">Candidate Safety Checklist:</h4>
        """,
        unsafe_allow_html=True,
    )

    for item in report.recommended_checklist:
        st.markdown(f"- [ ] **{item}**")

    st.markdown(
        f"""
          <div style="background: #fdfaf4; border: 1.5px solid #ebdcc5; border-radius: 8px; padding: 0.85rem 1rem; margin-top: 1.2rem; font-size: 0.8rem; color: #5d7065; line-height: 1.5; font-weight: 600;">
            <b>Notice:</b> {report.disclaimer}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    report_md = f"""# TRUSTROUTE AI — EMPLOYMENT DUE DILIGENCE REPORT
Case Assessment: {report.overall_risk_profile}
Reviewer Note: {st.session_state.reviewer_notes}

## OFFICIAL FINDINGS:
"""
    for f in report.findings:
        report_md += f"\n- [{f.status.value}] {f.category}\n  Finding: {f.finding_summary}\n  Proof: {f.evidence_snippet}\n  Registry: {f.source_checked}\n  Action: {f.action_for_candidate}\n"

    report_md += f"\n## CANDIDATE SAFETY CHECKLIST:\n"
    for c in report.recommended_checklist:
        report_md += f"- {c}\n"

    report_md += f"\n---\n{report.disclaimer}\n"

    st.download_button(
        label="📥 Download Official Dossier (.md)",
        data=report_md,
        file_name="TrustRoute_Official_Report.md",
        mime="text/markdown",
        use_container_width=True,
    )

# -----------------------------------------------------------------------------
# Clean Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="tr-footer">
      <b>TrustRoute AI</b> • Built with dedication by <b>Team TrustRoute</b> to protect international job seekers through verified, evidence-backed AI due diligence.
    </div>
    """,
    unsafe_allow_html=True,
)