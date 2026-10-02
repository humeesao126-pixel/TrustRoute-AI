from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class RiskLevel(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    INCONSISTENCY = "INCONSISTENCY"
    WARNING = "WARNING"

class ExtractedOffer(BaseModel):
    employer_name: Optional[str] = Field(None, description="Name of hiring organization")
    commercial_register_id: Optional[str] = Field(None, description="HRB/HRA registration number if stated")
    location_city: Optional[str] = Field(None, description="City of employment")
    job_title: Optional[str] = Field(None, description="Stated job role")
    gross_annual_salary_eur: Optional[float] = Field(None, description="Annual gross salary in EUR")
    stated_visa_type: Optional[str] = Field(None, description="Visa category e.g. EU Blue Card, Work Visa, Opportunity Card")
    recruiter_agency_name: Optional[str] = Field(None, description="Local or intermediary agency name")
    oep_license_number: Optional[str] = Field(None, description="Pakistani BEOE license number e.g. 1234/LHR")
    upfront_payment_requested: bool = Field(False, description="Whether advance fees or payments are requested")
    payment_amount_pkr: Optional[float] = Field(None, description="Amount demanded in PKR")
    payment_channel: Optional[str] = Field(None, description="Payment method requested e.g. Personal Bank IBAN, Cash, JazzCash")
    contact_email: Optional[str] = Field(None, description="Contact email address in document")

class AuditFinding(BaseModel):
    category: str  # e.g., 'Employer Registry', 'Recruiter License', 'Compensation Benchmarks', 'Payment Security'
    status: RiskLevel
    source_checked: str  # e.g., 'German Handelsregister', 'Pakistan BEOE Directory'
    evidence_snippet: str
    finding_summary: str
    action_for_candidate: str

class DueDiligenceReport(BaseModel):
    overall_risk_profile: str  # "Low Friction", "Requires Verification", "Elevated Risk"
    findings: List[AuditFinding]
    recommended_checklist: List[str]
    disclaimer: str = (
        "This AI Due-Diligence Report is an informational risk assessment compiled "
        "from available public registries and deterministic rule checks. It does not "
        "constitute an official visa clearance, legal counsel, or government guarantee."
    )