import os
from typing import List
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from src.schemas import ExtractedOffer, DueDiligenceReport, AuditFinding

load_dotenv()

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts raw textual clauses from a provided PDF document."""
    try:
        reader = PdfReader(pdf_path)
        extracted_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)
        return "\n".join(extracted_text)
    except Exception as e:
        return f"Error reading PDF: {e}"

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

# Using the active gemini-3.5-flash model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0,
    api_key=api_key,
)

structured_extractor = llm.with_structured_output(ExtractedOffer)
structured_reporter = llm.with_structured_output(DueDiligenceReport)

def extraction_agent(document_text: str) -> ExtractedOffer:
    """Parses raw text into the Pydantic ExtractedOffer schema."""
    prompt = f"""You are an expert employment legal investigator specializing in immigration to Germany.
Analyze the following job offer or appointment contract text and extract the required contractual entities accurately.

If a field is missing, ambiguous, or not stated, leave it null or False as per the schema.
Ensure you check whether advance fees, security bonds, or candidate charges are demanded.

Document Content:
\"\"\"{document_text}\"\"\"
"""
    return structured_extractor.invoke(prompt)

def report_synthesis_agent(*args, **kwargs) -> DueDiligenceReport:
    """Synthesizes verified audit findings into a formal DueDiligenceReport."""
    if len(args) == 2:
        extracted_offer, audit_findings = args
    elif len(args) == 1 and isinstance(args[0], dict):
        extracted_offer = args[0].get("extracted_offer")
        audit_findings = args[0].get("audit_findings", [])
    else:
        extracted_offer = kwargs.get("extracted_offer")
        audit_findings = kwargs.get("audit_findings", [])

    findings_str = "\n".join(
        [
            f"- [{f.status.value if hasattr(f.status, 'value') else f.status}] {f.category}: {f.finding_summary} "
            f"(Evidence: {f.evidence_snippet} | Source: {f.source_checked} | Action: {f.action_for_candidate})"
            for f in (audit_findings or [])
        ]
    )

    prompt = f"""You are the Chief Immigration Compliance Officer at TrustRoute AI.
Compile an authoritative Due Diligence Dossier summarizing the employment verification.

Extracted Offer Details:
- Employer: {getattr(extracted_offer, 'employer_name', 'Unknown')}
- Job Title: {getattr(extracted_offer, 'job_title', 'Unknown')}
- Salary: EUR {getattr(extracted_offer, 'gross_annual_salary_eur', 'Not stated')}
- City: {getattr(extracted_offer, 'location_city', 'Unknown')}
- Agency: {getattr(extracted_offer, 'recruiter_agency_name', 'None')}
- Advance Fee Demanded: {getattr(extracted_offer, 'upfront_payment_requested', False)}

Audit Findings:
{findings_str}

Formulate:
1. overall_risk_profile (e.g., 'Safe / Verified Standard', 'Caution / Discrepancies Noted', or 'High Risk / Severe Violations')
2. recommended_checklist: Concrete sequential steps the candidate should follow.
3. findings: Retain the full list of validated findings.
4. disclaimer: Formal statutory advisory notice.
"""
    return structured_reporter.invoke(prompt)