# 🛡️ TrustRoute AI

> **Evidence-based employment offer verification for Germany-bound job seekers**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-orange.svg)](https://github.com/langchain-ai/langgraph)
[![Gemini](https://img.shields.io/badge/Gemini-3.5_Flash-4285F4.svg?logo=google&logoColor=white)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-Registry%20Data-003B57.svg?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

TrustRoute AI is an employment due diligence system built to help job seekers identify suspicious or unverified job offers for employment in Germany.

The system takes an employment offer as a PDF or text, extracts important contract details, checks those details against available company and recruitment records, evaluates salary and payment-related risks, and presents the results in a structured verification report.

The goal is simple: **help candidates understand what they are being offered before they pay money, sign a contract, or continue with a potentially risky recruitment process.**

---

## 🎯 Why TrustRoute AI?

International job seekers can face recruitment offers containing fake companies, unlicensed intermediaries, unrealistic salary claims, or requests for advance payments.

Checking an offer manually can be difficult because the relevant information is usually spread across different parts of the contract and different verification sources.

TrustRoute AI brings these checks into one workflow.

Instead of only generating a general AI response, the system:

- Extracts structured information from the offer
- Separates extracted contract data from verification results
- Checks employer and recruiter information against available records
- Reviews salary and payment-related concerns
- Produces evidence-backed findings
- Gives the candidate practical next steps
- Requires human review before the final report is released

---

## 🔍 What TrustRoute AI Checks

The investigation focuses on four main areas.

### 🏢 1. German Employer Verification

The system checks the employer information provided in the offer against available German commercial registry records.

It looks at information such as:

- Employer name
- Commercial registration details
- Registry ID when available
- Company status
- Potential inconsistencies in the provided information

### 🇵🇰 2. Pakistani Recruiter Verification

When a Pakistani recruitment agency or intermediary is mentioned, TrustRoute AI checks the available BEOE records.

The system can identify situations such as:

- Active recruiter license
- Missing license information
- Unverified recruiter
- Suspended or problematic license status

### 💶 3. Salary & Employment Terms

The offered salary is reviewed against the applicable salary requirements used by the system.

The investigation can highlight:

- Salary information that is missing
- Salary below the relevant threshold
- Possible inconsistencies between the stated job and salary
- Issues related to the declared visa route

### 💳 4. Payment & Recruitment Fee Risks

TrustRoute AI looks for payment-related warning signs in the employment offer.

Examples include:

- Advance processing fees
- Security deposits
- Personal bank account payment requests
- Mobile wallet payment requests
- Other suspicious candidate charges

These findings are presented as risk indicators for further verification.

---

## 🏗️ How It Works

The system follows a multi-step workflow from document intake to final report.

```text
                    ┌──────────────────────────┐
                    │   Job Offer PDF / Text   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Information Extraction  │
                    │     Gemini + Pydantic     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Verification Workflow │
                    │         LangGraph         │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
               Employer      Recruiter     Salary &
               Registry       License       Payment
                    │            │            │
                    └────────────┼────────────┘
                                 ▼
                    ┌──────────────────────────┐
                    │   Findings & Risk Score  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │      Human Review Gate   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Final Due Diligence   │
                    │         Dossier           │
                    └──────────────────────────┘
```

The workflow is designed so that AI is used for language understanding and report generation, while structured verification checks are handled through defined application logic and registry data.

---

## 📊 Investigation Output

When TrustRoute AI completes an investigation, the dashboard presents the results in three clear steps. Each step gives the user more detail about the employment offer, the verification results, and the final case report.

### Step 2: Extracted Offer Information

First, TrustRoute AI extracts the important details from the uploaded PDF or pasted offer text and displays them in a structured format.

| Field | What It Shows |
|---|---|
| **Hiring Employer** | The company name mentioned in the employment offer. |
| **Location & Registry ID** | The employer's city and commercial register information, when available. |
| **Designation** | The job title mentioned in the offer. |
| **Offered Base Salary** | The stated gross annual salary in euros. |
| **Recruiter / Intermediary** | The recruitment agency or intermediary involved in the offer. |
| **Pakistani OEP License** | The license number provided for the Pakistani recruitment agency, if available. |
| **Visa Route** | The visa or immigration route mentioned in the offer. |
| **Advance Processing Fee** | Shows whether the offer contains an upfront payment or processing fee request. |

This information is then used by the verification workflow for the next stage.

---

### Step 3: Verification Score & Findings

The extracted information is checked against the available registry records and verification rules in the system.

#### Authenticity & Due Diligence Score

TrustRoute AI calculates a score from **0 to 100** based on the findings.

- **80 to 100:** Lower risk and major checks passed
- **50 to 79:** Moderate risk and some issues require clarification
- **Below 50:** High risk with serious concerns identified

The score is only a risk indicator. It does not guarantee that an employment offer is genuine.

#### Four Verification Pillars

The dashboard summarizes the investigation through four main areas:

- **German Registry:** Checks the employer information against available German company records.
- **BEOE Recruiter License:** Checks the recruitment agency's license information against available BEOE records.
- **German Minimum Wage:** Reviews the offered salary against the applicable salary requirements used by the system.
- **Payment Security:** Identifies suspicious advance fees or payment requests mentioned in the offer.

#### Detailed Findings

Each verification finding provides the information needed to understand the result:

- **Status:** Shows whether the check was verified, could not be confirmed, has a discrepancy, or contains a violation.
- **Finding:** Explains what the system found.
- **Document Proof:** Shows the relevant text or evidence from the uploaded offer.
- **Authority Checked:** Shows which registry or verification source was checked.
- **Action for Candidate:** Provides a practical next step based on the finding.

This makes it possible to see not only the final score, but also the evidence behind each result.

---

### Step 4: Human Review & Final Dossier

Before the final report is released, the case goes through a human review step.

The reviewer can inspect the extracted information, verification findings, evidence, and recommended actions before authorizing the report.

After authorization, TrustRoute AI provides:

- **Reviewer Statement:** A final note recorded by the case reviewer.
- **Risk Profile:** The overall assessment of the employment offer.
- **Candidate Safety Checklist:** Practical steps the candidate should take based on the findings.
- **Downloadable Dossier:** A complete Markdown report containing the case assessment, findings, document evidence, verification sources, recommended actions, checklist, and disclaimer.

The final dossier gives the candidate a clear record of what was checked, what was found, and what should be considered before moving forward.

---

## 🤖 AI and Verification Workflow

TrustRoute AI uses AI where language understanding is useful, while keeping important verification steps structured.

### Document Understanding

The extraction workflow reads the uploaded employment offer and converts relevant information into a structured `ExtractedOffer` schema.

This allows the rest of the application to work with consistent fields instead of relying on unstructured text.

### Structured Verification

The extracted information is passed through verification nodes that perform defined checks against the available registry data and application rules.

This helps keep registry-based checks separate from AI-generated interpretation.

### Report Synthesis

After the investigation is complete, the system combines the findings into a structured due diligence report.

The report includes:

- Overall risk profile
- Verification findings
- Supporting evidence
- Candidate actions
- Safety checklist
- Disclaimer

### Human Review Gate

The final report is not immediately released after the automated investigation.

A reviewer can inspect the case and authorize the report through the dashboard.

This adds a human decision point before the final dossier is generated.

---

## 🧠 Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and verification logic |
| **Streamlit** | Interactive web dashboard |
| **LangGraph** | Investigation workflow and agent orchestration |
| **Gemini** | Document extraction and report synthesis |
| **Pydantic** | Structured data validation |
| **SQLite** | Local registry and verification data |
| **PyPDF** | Employment offer PDF text extraction |
| **python-dotenv** | Environment variable management |

---

## 📁 Project Structure

```text
TrustRoute-AI/
│
├── data/
│   └── registries.db
│
├── src/
│   ├── agents.py
│   ├── graph.py
│   └── schemas.py
│
├── tests/
│
├── app.py
├── requirements.txt
├── .gitignore
├── generate_test_pdfs.py
└── README.md
```

### Main Components

**`app.py`**

Contains the Streamlit dashboard, user interaction, case management, verification controls, reviewer gate, and final report export.

**`src/agents.py`**

Contains the document extraction and report synthesis logic used by the investigation workflow.

**`src/graph.py`**

Defines the LangGraph workflow and connects the different investigation stages.

**`src/schemas.py`**

Contains the Pydantic models and risk-related enums used to keep extracted information and findings structured.

**`data/registries.db`**

Contains the local registry data used by the verification workflow.

**`tests/`**

Contains project tests for validating application behavior.

**`generate_test_pdfs.py`**

Utility for generating test employment offer PDFs.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hamxashoaib/TrustRoute-AI.git
cd TrustRoute-AI
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scriptsctivate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY="your_google_ai_studio_api_key_here"
```

Keep your API key private and do not commit the `.env` file to GitHub.

### 5. Start the Application

```bash
streamlit run app.py
```

Streamlit will provide a local URL where you can open the TrustRoute AI dashboard.

---

## 🧪 Testing the Application

You can test the system using either:

- A PDF employment offer
- Plain text pasted directly into the dashboard
- Test documents generated with `generate_test_pdfs.py`

A typical test flow is:

```text
Upload Offer
     ↓
Extract Contract Information
     ↓
Run Verification
     ↓
Review Findings
     ↓
Inspect Evidence
     ↓
Human Authorization
     ↓
Download Final Dossier
```

For a meaningful test, use offers containing different combinations of employer information, recruiter details, salary information, visa routes, and payment terms.

---

## 🔐 Safety & Design Considerations

TrustRoute AI is designed around the idea that an employment verification system should show **why** it reached a conclusion.

The dashboard therefore keeps important evidence visible instead of presenting only a final AI-generated answer.

Key design decisions include:

- Structured extraction instead of working directly with raw contract text
- Registry-based checks for available verification data
- Explicit finding statuses
- Document evidence attached to individual findings
- Candidate-focused actions
- Human review before final report release
- A clear disclaimer on the final dossier

The system is intended to support better decisions, not replace professional legal or immigration advice.

---

## ⚠️ Disclaimer

TrustRoute AI is an independent software project for employment due diligence and risk awareness.

The information presented by the system depends on the employment document, available registry data, and the verification rules implemented in the application. A verified result does not guarantee that an employer, recruiter, contract, visa process, or job offer is completely genuine.

The system does not replace legal advice, immigration advice, official embassy decisions, or decisions made by competent German or Pakistani authorities.

Users should independently confirm important employment, visa, salary, and recruitment information with the relevant official authorities before making financial or legal commitments.

---

## 🌍 Project Purpose

TrustRoute AI was built around a practical problem faced by international job seekers: **how to check an overseas employment offer before trusting it.**

The project combines document understanding, structured verification, evidence-based findings, and human review into one workflow.

Rather than treating an LLM response as the final answer, TrustRoute AI uses AI as one part of a larger verification system where extracted information, structured checks, evidence, and human authorization all contribute to the final result.

---

## 👨‍💻 Author

**Hamza Shoaib**

*AI & ML Engineer & AI Automation Specialist*

## Connect

- 🌐 [**Portfolio**](https://hamzashoaib.dev/)
- 💼 [**LinkedIn**](https://linkedin.com/in/ch-hamza-shoaib)
- 🐙 [**GitHub**](https://github.com/hamxashoaib)

## ⭐ Project

If you find TrustRoute AI useful or interesting, consider giving the repository a ⭐ on GitHub.
