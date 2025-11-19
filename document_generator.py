import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. PROFESSIONAL DOCUMENT TEMPLATES (Indian Legal Standard) ---
DOC_CONFIG = {
    "Rental/Lease Agreement": {
        "fields": [
            {"id": "landlord_name", "label": "Landlord Name (Lessor)"},
            {"id": "tenant_name", "label": "Tenant Name (Lessee)"},
            {"id": "property_address", "label": "Complete Property Address", "type": "textarea"},
            {"id": "rent_amount", "label": "Monthly Rent (Rs.)", "type": "number"},
            {"id": "deposit_amount", "label": "Security Deposit (Rs.)", "type": "number"},
            {"id": "lease_duration", "label": "Lease Duration (e.g., 11 months)"},
            {"id": "start_date", "label": "Lease Start Date", "type": "date"},
            {"id": "city", "label": "City of Execution"}
        ],
        "template": """RESIDENTIAL RENTAL AGREEMENT

THIS RENTAL AGREEMENT is made and executed at {city} on this {date}, by and between:

1. {landlord_name}, residing at [Landlord's Address], hereinafter referred to as the "LESSOR" (which expression shall unless repugnant to the context include his/her heirs, executors, administrators, and assigns) of the ONE PART.

AND

2. {tenant_name}, having permanent address at [Tenant's Permanent Address], hereinafter referred to as the "LESSEE" (which expression shall unless repugnant to the context include his/her heirs, executors, administrators, and assigns) of the OTHER PART.

WHEREAS the Lessor is the absolute owner of the property situated at:
{property_address}
(hereinafter referred to as the "SCHEDULED PREMISES").

AND WHEREAS the Lessee has requested the Lessor to grant the lease of the said Scheduled Premises for residential purposes, and the Lessor has agreed to the same.

NOW THIS AGREEMENT WITNESSETH AS FOLLOWS:

1. RENT: The Lessee shall pay a monthly rent of Rs. {rent_amount}/- (Rupees in words) on or before the 5th day of every English calendar month.

2. DEPOSIT: The Lessee has paid an interest-free refundable security deposit of Rs. {deposit_amount}/- to the Lessor. This amount shall be refunded at the time of vacating the premises, subject to deductions for damages or unpaid dues.

3. DURATION: This lease shall be in force for a period of {lease_duration}, commencing from {start_date}.

4. MAINTENANCE: The Lessee shall maintain the premises in good condition and shall not cause any structural damages. Minor repairs (tap leakage, fused bulbs) shall be borne by the Lessee.

5. UTILITIES: The Lessee shall pay the electricity and water charges as per the meter reading/bills directly to the concerned authorities.

6. TERMINATION: Either party can terminate this agreement by giving one (1) month's prior notice in writing.

7. PURPOSE: The premises shall be used strictly for residential purposes only and not for any commercial activity.

IN WITNESS WHEREOF, the Lessor and the Lessee have set their hands to this Agreement on the day, month, and year first above written.

_________________                              _________________
LESSOR                                         LESSEE

Witnesses:
1. _________________
2. _________________"""
    },

    "Non-Disclosure Agreement (NDA)": {
        "fields": [
            {"id": "disclosing_party", "label": "Disclosing Party Name"},
            {"id": "receiving_party", "label": "Receiving Party Name"},
            {"id": "confidential_info", "label": "Description of Confidential Information", "type": "textarea"},
            {"id": "duration", "label": "Duration of Agreement (e.g., 2 years)"},
            {"id": "jurisdiction", "label": "Jurisdiction (City/State)"}
        ],
        "template": """NON-DISCLOSURE AGREEMENT (NDA)

This Non-Disclosure Agreement ("Agreement") is entered into on {date} BY AND BETWEEN:

1. {disclosing_party}, hereinafter referred to as the "DISCLOSING PARTY".
   AND
2. {receiving_party}, hereinafter referred to as the "RECEIVING PARTY".

(Collectively referred to as the "Parties").

WHEREAS the Disclosing Party possesses certain non-public, confidential, and proprietary information and wishes to share it with the Receiving Party for the purpose of potential business collaboration.

NOW, THEREFORE, the Parties agree as follows:

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" refers to any information disclosed by the Disclosing Party, including but not limited to:
{confidential_info}

2. OBLIGATIONS OF THE RECEIVING PARTY
The Receiving Party agrees to:
   a) Hold the Confidential Information in strict confidence.
   b) Not disclose such information to any third party without prior written consent.
   c) Use the information solely for the intended business purpose.

3. EXCLUSIONS
Confidential Information does not include info that is public knowledge, already known to the Receiving Party, or independently developed.

4. TERM
This Agreement shall remain in effect for a period of {duration} from the date of execution.

5. JURISDICTION
This Agreement shall be governed by the laws of India, and the courts in {jurisdiction} shall have exclusive jurisdiction.

IN WITNESS WHEREOF, the parties have executed this Agreement.

_________________                              _________________
(Disclosing Party)                             (Receiving Party)"""
    },

    "Affidavit/Self-Declaration": {
        "fields": [
            {"id": "deponent_name", "label": "Your Name (Deponent)"},
            {"id": "father_name", "label": "Father's/Husband's Name"},
            {"id": "age", "label": "Age", "type": "number"},
            {"id": "address", "label": "Full Residential Address", "type": "textarea"},
            {"id": "statement", "label": "Statement/Facts to Declare", "type": "textarea"},
            {"id": "place", "label": "Place of Verification"}
        ],
        "template": """AFFIDAVIT / SELF-DECLARATION

I, {deponent_name}, S/o or W/o {father_name}, aged about {age} years, residing at:
{address}

Do hereby solemnly affirm and declare as follows:

1. That I am a citizen of India and the deponent herein.
2. That I am well conversant with the facts and circumstances of the matter.
3. {statement}
4. That the contents of this affidavit are true and correct to the best of my knowledge and belief, and nothing material has been concealed therefrom.

VERIFICATION

Verified at {place} on this {date}, that the contents of the above affidavit are true and correct. No part of it is false.

_________________
DEPONENT"""
    },

    "Employment Offer Letter": {
        "fields": [
            {"id": "company_name", "label": "Company Name"},
            {"id": "candidate_name", "label": "Candidate Name"},
            {"id": "job_title", "label": "Job Title"},
            {"id": "salary", "label": "Annual CTC (Rs.)"},
            {"id": "start_date", "label": "Joining Date", "type": "date"},
            {"id": "location", "label": "Work Location"}
        ],
        "template": """OFFER OF EMPLOYMENT

Date: {date}

To,
{candidate_name}

Subject: Offer for the post of {job_title}

Dear {candidate_name},

We are pleased to offer you the position of {job_title} at {company_name}, based in {location}. We were impressed by your skills and believe you will be a valuable asset to our team.

TERMS OF OFFER:
1. Position: You will serve as {job_title} and report to the designated manager.
2. Compensation: Your Annual Cost to Company (CTC) will be Rs. {salary}, subject to standard statutory deductions (PF, Tax, etc.).
3. Commencement: Your employment will commence on {start_date}.
4. Probation: You will be on a probation period of 6 months from the date of joining.

Please sign the duplicate copy of this letter as a token of your acceptance and return it to us.

We look forward to welcoming you to {company_name}.

Sincerely,

HR Manager
{company_name}

ACCEPTED BY:
_________________
(Signature of Candidate)"""
    },

    "Legal Notice (General)": {
        "fields": [
            {"id": "sender_name", "label": "Sender Name (Client)"},
            {"id": "recipient_name", "label": "Recipient Name"},
            {"id": "recipient_address", "label": "Recipient Address", "type": "textarea"},
            {"id": "issue_details", "label": "Details of Grievance/Issue", "type": "textarea"},
            {"id": "demand", "label": "Demand/Action Required", "type": "textarea"},
            {"id": "days_to_reply", "label": "Notice Period (e.g., 15 days)"}
        ],
        "template": """REGD. POST WITH A/D
LEGAL NOTICE

Date: {date}

To,
{recipient_name}
{recipient_address}

Subject: Legal Notice regarding {issue_details}

Sir/Madam,

Under instructions from and on behalf of my client, {sender_name}, I do hereby serve you with this Legal Notice:

1. That my client states that: {issue_details}

2. That due to your aforesaid acts/omissions, my client has suffered significant mental agony/financial loss.

3. I, therefore, call upon you to {demand} within {days_to_reply} days from the receipt of this notice.

TAKE NOTICE that if you fail to comply with the above demand within the stipulated period, my client shall be constrained to initiate appropriate civil/criminal legal proceedings against you at your sole risk, cost, and consequences.

Yours faithfully,

_________________
Advocate for {sender_name}"""
    },
    
    "Memorandum of Understanding (MOU)": {
        "fields": [
            {"id": "party_a", "label": "First Party Name"},
            {"id": "party_b", "label": "Second Party Name"},
            {"id": "purpose", "label": "Purpose of Collaboration", "type": "textarea"},
            {"id": "roles", "label": "Roles & Responsibilities", "type": "textarea"},
            {"id": "place", "label": "Place of Execution"}
        ],
        "template": """MEMORANDUM OF UNDERSTANDING (MOU)

This MOU is made on {date} at {place}, BY AND BETWEEN:

1. {party_a}, hereinafter referred to as the "FIRST PARTY".
   AND
2. {party_b}, hereinafter referred to as the "SECOND PARTY".

PREAMBLE:
The parties share a common interest and wish to collaborate to achieve mutual goals.

1. PURPOSE:
The purpose of this MOU is:
{purpose}

2. ROLES AND RESPONSIBILITIES:
The parties agree to the following roles:
{roles}

3. NATURE OF AGREEMENT:
This MOU is a statement of intent and is not legally binding unless followed by a definitive agreement. Either party may terminate this MOU by giving written notice.

IN WITNESS WHEREOF, the parties have signed this MOU on the date first mentioned above.

_________________          _________________
(First Party)              (Second Party)"""
    },

    "Simple Will": {
        "fields": [
            {"id": "testator_name", "label": "Your Name (Testator)"},
            {"id": "beneficiary_name", "label": "Beneficiary Name"},
            {"id": "executor_name", "label": "Executor Name"},
            {"id": "assets", "label": "Details of Assets/Property", "type": "textarea"},
            {"id": "place", "label": "Place"}
        ],
        "template": """LAST WILL AND TESTAMENT

I, {testator_name}, currently residing at {place}, being of sound mind and memory, do hereby declare this to be my Last Will and Testament.

1. I hereby revoke all former Wills and Codicils made by me.

2. I appoint {executor_name} as the sole Executor of this Will.

3. I hereby bequeath, devise, and grant my assets/property described below:
   {assets}
   
   TO MY BENEFICIARY: {beneficiary_name}.

4. I declare that this Will is made by me without any pressure or undue influence.

IN WITNESS WHEREOF, I have signed this Will on {date} at {place}.

_________________
(Testator Signature)

Witnesses:
1. _________________
2. _________________"""
    },
    
    "Gift Deed": {
        "fields": [
            {"id": "donor_name", "label": "Donor Name (Giver)"},
            {"id": "donee_name", "label": "Donee Name (Receiver)"},
            {"id": "relationship", "label": "Relationship (e.g., Son/Daughter)"},
            {"id": "property_desc", "label": "Description of Gifted Property", "type": "textarea"},
            {"id": "value", "label": "Approx. Market Value (Rs.)", "type": "number"},
            {"id": "place", "label": "Place of Execution"}
        ],
        "template": """GIFT DEED

This Deed of Gift is executed on {date} at {place}, BETWEEN:

1. {donor_name} (hereinafter called the "DONOR")
   AND
2. {donee_name} (hereinafter called the "DONEE")

WHEREAS the Donor is the absolute owner of the property described below.
AND WHEREAS the Donor bears natural love and affection for the Donee, who is his/her {relationship}.

NOW THIS DEED WITNESSETH:

1. That out of natural love and affection, the Donor hereby transfers, assigns, and gifts the schedule property to the Donee, free from all encumbrances.
2. The estimated value of the property is Rs. {value}.
3. The Donee accepts this Gift and has taken possession of the property.

SCHEDULE OF PROPERTY:
{property_desc}

IN WITNESS WHEREOF, the Donor has executed this Gift Deed.

_________________          _________________
(Donor)                    (Donee - Accepted)

Witnesses:
1. _________________
2. _________________"""
    },
    
    "Power of Attorney (Special)": {
        "fields": [
            {"id": "principal_name", "label": "Principal Name (You)"},
            {"id": "attorney_name", "label": "Attorney/Agent Name"},
            {"id": "specific_act", "label": "Specific Act Authorized (e.g., to sell car)", "type": "textarea"},
            {"id": "place", "label": "Place of Execution"}
        ],
        "template": """SPECIAL POWER OF ATTORNEY

KNOW ALL MEN BY THESE PRESENTS that I, {principal_name}, residing at {place}, do hereby nominate, constitute, and appoint {attorney_name} as my true and lawful Attorney.

WHEREAS I am unable to personally attend to the matter described below due to personal reasons.

NOW, I authorize my Attorney to do the following specific acts/deeds on my behalf:
{specific_act}

I hereby agree to ratify and confirm all acts done by my said Attorney under this power.

IN WITNESS WHEREOF, I have signed this deed on {date}.

_________________
(Principal Signature)

Accepted by:
_________________
(Attorney Signature)"""
    }
}

# --- 2. PDF GENERATOR ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Nyay-Saathi Legal Draft', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_bytes(doc_text, doc_type):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, doc_type.upper(), 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Arial", size=11)
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    return bytes(pdf.output())

# --- 3. UI HELPERS (CSS) ---
def inject_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800;900&display=swap');

        /* ===== GLOBAL STYLES ===== */
        * {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        /* Main App Background with Gradient */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            background-attachment: fixed;
        }

        /* ===== HEADER SECTION ===== */
        .doc-header {
            color: #ffffff;
            text-align: center;
            font-family: 'Playfair Display', serif;
            font-weight: 900;
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #f8fafc 0%, #cbd5e1 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: fadeInDown 0.8s ease-out;
        }

        .doc-subheader {
            color: #94a3b8;
            text-align: center;
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            font-weight: 400;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 3rem;
            animation: fadeInUp 0.8s ease-out 0.2s backwards;
        }

        /* ===== SELECTBOX STYLING ===== */
        .stSelectbox {
            margin-bottom: 2rem;
        }

        .stSelectbox > div > div {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: #1e293b !important;
            padding: 0.75rem 1rem !important;
        }

        .stSelectbox > div > div:hover {
            border-color: #0ea5e9 !important;
            box-shadow: 0 6px 25px rgba(14, 165, 233, 0.15) !important;
            transform: translateY(-2px) !important;
        }

        .stSelectbox [role="option"] {
            color: #1e293b !important;
            background-color: #ffffff !important;
        }

        .stSelectbox [role="option"][aria-selected="true"] {
            background-color: #0ea5e9 !important;
            color: #ffffff !important;
        }

        .stSelectbox [role="listbox"] {
            background-color: #ffffff !important;
        }

        .stSelectbox svg {
            color: #1e293b !important;
        }

        .stSelectbox > div > div > div {
            color: #1e293b !important;
        }

        .stSelectbox input {
            color: #1e293b !important;
        }

        .stSelectbox [data-baseweb="select"] input {
            color: #1e293b !important;
        }

        .stSelectbox .baseweb__select__value {
            color: #1e293b !important;
        }

        /* ===== FORM CONTAINER ===== */
        .stForm {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            padding: 3rem;
            border-radius: 24px;
            border: 2px solid #e2e8f0;
            box-shadow:
                0 20px 60px rgba(0, 0, 0, 0.12),
                0 0 0 1px rgba(255, 255, 255, 0.5) inset;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
            animation: slideUp 0.6s ease-out 0.3s backwards;
        }

        .stForm::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #0ea5e9 0%, #06b6d4 50%, #0ea5e9 100%);
            background-size: 200% 100%;
            animation: shimmer 3s linear infinite;
        }

        /* Form Headers */
        .stForm h1, .stForm h2, .stForm h3 {
            color: #0f172a !important;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            margin-top: 0;
        }

        .stForm h3 {
            font-size: 1.5rem;
            letter-spacing: -0.01em;
            margin-bottom: 1.5rem;
        }

        .stForm p, .stForm label, .stForm div {
            color: #475569 !important;
            font-family: 'Inter', sans-serif;
        }

        /* Caption Styling */
        .stForm [data-testid="stCaptionContainer"] {
            color: #64748b !important;
            font-size: 0.9rem;
            margin-bottom: 1.5rem;
        }

        /* ===== INPUT FIELDS ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            background-color: #ffffff !important;
            color: #0f172a !important;
            border: 2px solid #e2e8f0;
            border-radius: 10px;
            padding: 0.875rem 1rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        .stTextInput > div > div > input:hover,
        .stTextArea > div > div > textarea:hover,
        .stNumberInput > div > div > input:hover,
        .stDateInput > div > div > input:hover {
            border-color: #cbd5e1;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
        }

        /* Input Focus Effect */
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus,
        .stDateInput > div > div > input:focus {
            border-color: #0ea5e9 !important;
            box-shadow:
                0 0 0 3px rgba(14, 165, 233, 0.1),
                0 4px 16px rgba(14, 165, 233, 0.15) !important;
            outline: none;
            transform: translateY(-1px);
        }

        /* Textarea Specific */
        .stTextArea > div > div > textarea {
            min-height: 120px;
            resize: vertical;
        }

        /* Labels */
        label {
            font-weight: 600 !important;
            color: #1e293b !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
            display: block;
            letter-spacing: 0.01em;
        }

        /* ===== BUTTONS ===== */
        .stButton > button {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 1rem 2.5rem;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.02em;
            box-shadow:
                0 10px 30px rgba(14, 165, 233, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .stButton > button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0 15px 40px rgba(14, 165, 233, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        }

        .stButton > button:hover::before {
            width: 300px;
            height: 300px;
        }

        .stButton > button:active {
            transform: translateY(0);
        }

        /* Download Button */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #ffffff;
            border: none;
            border-radius: 12px;
            padding: 1rem 2.5rem;
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            box-shadow:
                0 10px 30px rgba(16, 185, 129, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.2) inset;
            width: 100%;
        }

        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0 15px 40px rgba(16, 185, 129, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.3) inset;
        }

        /* ===== PAPER PREVIEW BOX ===== */
        .preview-box {
            background-color: #ffffff;
            color: #1e293b;
            padding: 4rem 3.5rem;
            margin: 2rem 0;
            border: 1px solid #d1d5db;
            box-shadow:
                0 25px 50px rgba(0, 0, 0, 0.15),
                0 0 0 1px rgba(0, 0, 0, 0.05),
                0 -2px 15px rgba(0, 0, 0, 0.05) inset;
            border-radius: 4px;
            font-family: 'Georgia', 'Times New Roman', Times, serif;
            font-size: 15px;
            line-height: 1.8;
            white-space: pre-wrap;
            position: relative;
            animation: fadeIn 0.6s ease-out;
        }

        .preview-box::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background:
                repeating-linear-gradient(
                    transparent,
                    transparent 1.8rem,
                    rgba(14, 165, 233, 0.03) 1.8rem,
                    rgba(14, 165, 233, 0.03) calc(1.8rem + 1px)
                );
            pointer-events: none;
        }

        /* ===== SUCCESS/ERROR MESSAGES ===== */
        .stSuccess {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
            border-left: 4px solid #10b981;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            color: #065f46;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);
            animation: slideInRight 0.4s ease-out;
        }

        .stError {
            background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
            border-left: 4px solid #ef4444;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            color: #991b1b;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(239, 68, 68, 0.15);
            animation: shake 0.4s ease-out;
        }

        /* ===== ANIMATIONS ===== */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(40px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(-30px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }

        @keyframes shimmer {
            0% { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }

        /* ===== SCROLLBAR STYLING ===== */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }

        ::-webkit-scrollbar-track {
            background: #f1f5f9;
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            border-radius: 10px;
            border: 2px solid #f1f5f9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #0284c7 0%, #0891b2 100%);
        }

        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 768px) {
            .doc-header {
                font-size: 2.5rem;
            }

            .doc-subheader {
                font-size: 0.95rem;
            }

            .stForm {
                padding: 2rem 1.5rem;
            }

            .preview-box {
                padding: 2.5rem 2rem;
                font-size: 14px;
            }
        }

        /* ===== PRINT STYLES ===== */
        @media print {
            .stApp {
                background: white;
            }

            .preview-box {
                box-shadow: none;
                border: 1px solid #000;
                page-break-inside: avoid;
            }

            .stButton, .stDownloadButton, .doc-header, .doc-subheader, .stForm {
                display: none;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN FUNCTION ---
def show_document_generator():
    inject_custom_css()
    
    st.markdown("<h1 class='doc-header'>📝 Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='doc-subheader'>Instant. Professional. Compliant.</p>", unsafe_allow_html=True)

    # Document Selector
    doc_type = st.selectbox("Select Document Type:", list(DOC_CONFIG.keys()))
    config = DOC_CONFIG[doc_type]
    
    user_inputs = {}
    
    # --- FORM START ---
    with st.form("doc_form"):
        st.markdown(f"<h3 style='color:#333; border-bottom: 2px solid #eee; padding-bottom: 10px;'>{doc_type} Details</h3>", unsafe_allow_html=True)
        st.caption("Please fill in the details below.")
        
        # Layout Logic: Pairs of fields in columns, Textareas full width
        current_col = 0
        cols = st.columns(2)
        
        for field in config["fields"]:
            label = field["label"]
            key = field["id"]
            ftype = field.get("type", "text")
            
            # If textarea, break out of columns
            if ftype == "textarea":
                user_inputs[key] = st.text_area(label, height=100)
                current_col = 0 # Reset column counter
            else:
                # Place in current column
                with cols[current_col]:
                    if ftype == "text":
                        user_inputs[key] = st.text_input(label)
                    elif ftype == "number":
                        user_inputs[key] = st.number_input(label, min_value=0, step=1000)
                    elif ftype == "date":
                        user_inputs[key] = st.date_input(label, value=datetime.date.today())
                
                # Toggle column index (0 -> 1 -> 0)
                current_col = 1 - current_col

        st.markdown("---")
        submitted = st.form_submit_button("Generate Draft (Instant)", type="primary")
    # --- FORM END ---

    if submitted:
        user_inputs["date"] = datetime.date.today().strftime("%B %d, %Y")
        
        # Simple validation
        empty_fields = [k for k, v in user_inputs.items() if str(v).strip() == ""]
        
        if not empty_fields:
            try:
                # Fill Template
                final_text = config["template"].format(**user_inputs)
                
                st.success(f"✅ {doc_type} Generated Successfully!")
                
                # Preview
                st.markdown("### 📄 Document Preview")
                st.markdown(f'<div class="preview-box">{final_text}</div>', unsafe_allow_html=True)
                
                # PDF
                pdf_data = create_pdf_bytes(final_text, doc_type)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.download_button(
                        label="⬇️ Download PDF Document",
                        data=pdf_data,
                        file_name=f"{doc_type.replace(' ', '_')}_Draft.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"Error filling template: {e}")
        else:
            st.error("⚠️ Please fill in all fields to generate the document.")