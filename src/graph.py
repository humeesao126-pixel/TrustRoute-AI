from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END
from src.schemas import ExtractedOffer, AuditFinding, DueDiligenceReport
from src.agents import extraction_agent, report_synthesis_agent
from src.tools import (
    verify_oep_recruiter,
    verify_german_employer,
    check_statutory_benchmarks,
    evaluate_payment_terms
)

class WorkflowState(TypedDict):
    document_text: str
    extracted_offer: Optional[ExtractedOffer]
    audit_findings: List[AuditFinding]
    final_report: Optional[DueDiligenceReport]
    human_approved: bool

def extract_node(state: WorkflowState) -> dict:
    text = state.get("document_text", "")
    extracted = extraction_agent(text)
    return {"extracted_offer": extracted}

def verify_node(state: WorkflowState) -> dict:
    offer = state.get("extracted_offer")
    findings: List[AuditFinding] = []

    if offer:
        findings.append(verify_german_employer(offer.employer_name, offer.commercial_register_id))
        findings.append(verify_oep_recruiter(offer.oep_license_number, offer.recruiter_agency_name))
        findings.append(check_statutory_benchmarks(offer.gross_annual_salary_eur, offer.stated_visa_type))
        findings.append(evaluate_payment_terms(
            offer.upfront_payment_requested,
            offer.payment_amount_pkr,
            offer.payment_channel
        ))

    return {"audit_findings": findings}

def synthesize_node(state: WorkflowState) -> dict:
    findings = state.get("audit_findings", [])
    report = report_synthesis_agent(findings)
    return {"final_report": report}

def build_trustroute_graph():
    builder = StateGraph(WorkflowState)

    builder.add_node("extract", extract_node)
    builder.add_node("verify", verify_node)
    builder.add_node("synthesize", synthesize_node)

    builder.add_edge(START, "extract")
    builder.add_edge("extract", "verify")
    builder.add_edge("verify", "synthesize")
    builder.add_edge("synthesize", END)

    return builder.compile()

pipeline = build_trustroute_graph()