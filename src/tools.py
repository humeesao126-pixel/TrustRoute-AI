import sqlite3
import os
from typing import Optional
from src.schemas import RiskLevel, AuditFinding

DB_PATH = os.path.join("data", "registries.db")

def verify_oep_recruiter(license_no: Optional[str], agency_name: Optional[str]) -> AuditFinding:
    if not license_no and not agency_name:
        return AuditFinding(
            category="Recruiter License",
            status=RiskLevel.UNVERIFIED,
            source_checked="Pakistan BEOE Directory",
            evidence_snippet="No OEP agency name or license number provided in document.",
            finding_summary="Offer did not disclose a Pakistani Overseas Employment Promoter license.",
            action_for_candidate="Ask the recruiter for their official 4-digit BEOE license number."
        )

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT agency_name, status FROM beoe_oep WHERE license_no = ?", (license_no,))
    row = cur.fetchone()
    conn.close()

    if row:
        name, status = row
        if status == "ACTIVE":
            return AuditFinding(
                category="Recruiter License",
                status=RiskLevel.VERIFIED,
                source_checked="Pakistan BEOE Directory",
                evidence_snippet=f"License {license_no} registered to '{name}', Status: {status}.",
                finding_summary="Recruiter is verified as an active licensed OEP in Pakistan.",
                action_for_candidate="Ensure all contract signings occur directly through the registered agency office."
            )
        else:
            return AuditFinding(
                category="Recruiter License",
                status=RiskLevel.WARNING,
                source_checked="Pakistan BEOE Directory",
                evidence_snippet=f"License {license_no} status is currently '{status}'.",
                finding_summary=f"The stated agency license is {status.lower()}.",
                action_for_candidate="Do not proceed until confirming active status with the Bureau of Emigration."
            )

    return AuditFinding(
        category="Recruiter License",
        status=RiskLevel.INCONSISTENCY,
        source_checked="Pakistan BEOE Directory",
        evidence_snippet=f"License number '{license_no}' not found in registry records.",
        finding_summary="The provided license number does not match registered OEP records.",
        action_for_candidate="Verify whether the recruiter is operating through an unlisted intermediary."
    )

def verify_german_employer(company_name: Optional[str], reg_id: Optional[str]) -> AuditFinding:
    if not company_name and not reg_id:
        return AuditFinding(
            category="Employer Registry",
            status=RiskLevel.UNVERIFIED,
            source_checked="German Handelsregister",
            evidence_snippet="Missing employer legal identity in document.",
            finding_summary="Employer corporate entity could not be determined.",
            action_for_candidate="Request an official letterhead showing the registered HRB/HRA number and legal seat."
        )

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT legal_form, court_city, status FROM handelsregister WHERE company_name LIKE ? OR register_id = ?",
        (f"%{company_name}%", reg_id)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        legal_form, court_city, status = row
        if status == "ACTIVE":
            return AuditFinding(
                category="Employer Registry",
                status=RiskLevel.VERIFIED,
                source_checked="German Handelsregister",
                evidence_snippet=f"Entity '{company_name}' found. Form: {legal_form}, Court: {court_city}, Status: {status}.",
                finding_summary="Employer is registered as an active corporate entity in Germany.",
                action_for_candidate="Cross-check that correspondence comes from the company's verified corporate domain."
            )
        else:
            return AuditFinding(
                category="Employer Registry",
                status=RiskLevel.WARNING,
                source_checked="German Handelsregister",
                evidence_snippet=f"Entity status: {status}.",
                finding_summary=f"Employer found but marked as {status}.",
                action_for_candidate="Clarify current business operations with the employer directly."
            )

    return AuditFinding(
        category="Employer Registry",
        status=RiskLevel.UNVERIFIED,
        source_checked="German Handelsregister",
        evidence_snippet=f"'{company_name}' (Reg: {reg_id or 'N/A'}) not found in registered records.",
        finding_summary="Company record could not be matched in standard commercial registry entries.",
        action_for_candidate="Search company registration independently via handelsregister.de."
    )

def check_statutory_benchmarks(salary_eur: Optional[float], visa_type: Optional[str]) -> AuditFinding:
    MIN_MONTHLY_WAGE = 2409.33  # baseline ~€13.90/hr @ 40h/wk
    MIN_ANNUAL_WAGE = MIN_MONTHLY_WAGE * 12
    BLUE_CARD_SHORTAGE = 45934.20

    if not salary_eur:
        return AuditFinding(
            category="Compensation Benchmarks",
            status=RiskLevel.UNVERIFIED,
            source_checked="German Statutory Labor Standards",
            evidence_snippet="No explicit compensation figure found in document.",
            finding_summary="Compensation was not stated in the parsed document.",
            action_for_candidate="Request an itemized breakdown of gross salary in Euros before proceeding."
        )

    if salary_eur < MIN_ANNUAL_WAGE:
        return AuditFinding(
            category="Compensation Benchmarks",
            status=RiskLevel.INCONSISTENCY,
            source_checked="Mindestlohngesetz (Statutory Minimum Wage)",
            evidence_snippet=f"Offered salary €{salary_eur:,.2f}/yr is below statutory full-time minimum (~€{MIN_ANNUAL_WAGE:,.2f}/yr).",
            finding_summary="Stated remuneration is below current German statutory minimum wage thresholds.",
            action_for_candidate="Clarify contractual weekly working hours or revised gross pay."
        )

    if visa_type and "blue card" in visa_type.lower():
        if salary_eur < BLUE_CARD_SHORTAGE:
            return AuditFinding(
                category="Compensation Benchmarks",
                status=RiskLevel.INCONSISTENCY,
                source_checked="BAMF EU Blue Card Thresholds",
                evidence_snippet=f"Offered €{salary_eur:,.2f}/yr vs. minimum Blue Card reference threshold €{BLUE_CARD_SHORTAGE:,.2f}/yr.",
                finding_summary="Salary appears below the standard reference threshold required for direct EU Blue Card issuance.",
                action_for_candidate="Confirm whether the intended visa pathway is a general work permit instead of an EU Blue Card."
            )

    return AuditFinding(
        category="Compensation Benchmarks",
        status=RiskLevel.VERIFIED,
        source_checked="German Wage & Blue Card Benchmarks",
        evidence_snippet=f"Salary of €{salary_eur:,.2f}/yr aligns with referenced qualification bands.",
        finding_summary="Salary figure meets relevant statutory reference levels.",
        action_for_candidate="Ensure tax deductions and net salary expectations are calculated via standard German wage tables."
    )

def evaluate_payment_terms(upfront_req: bool, amount_pkr: Optional[float], channel: Optional[str]) -> AuditFinding:
    if upfront_req and channel and any(term in channel.lower() for term in ["personal", "jazzcash", "easypaisa", "cash"]):
        return AuditFinding(
            category="Payment Security",
            status=RiskLevel.WARNING,
            source_checked="BEOE & Ethical Recruitment Directives",
            evidence_snippet=f"Requested upfront transfer of PKR {amount_pkr or 0:,.2f} via {channel}.",
            finding_summary="Upfront fee transfer requested via informal or personal account rails.",
            action_for_candidate="Exercise caution. Official visa fees are paid directly to embassy-authorized centers, never personal accounts."
        )

    if upfront_req:
        return AuditFinding(
            category="Payment Security",
            status=RiskLevel.WARNING,
            source_checked="Fair Recruitment Principles",
            evidence_snippet="Document indicates advance charges or deposits.",
            finding_summary="Upfront payments required before contract formalization.",
            action_for_candidate="Verify whether fees represent legitimate government attestation receipts."
        )

    return AuditFinding(
        category="Payment Security",
        status=RiskLevel.VERIFIED,
        source_checked="Standard Employment Norms",
        evidence_snippet="No unverified upfront candidate-side fees identified.",
        finding_summary="No upfront placement fee demands detected.",
        action_for_candidate="Confirm whether relocation or travel costs are employer-covered or self-funded."
    )