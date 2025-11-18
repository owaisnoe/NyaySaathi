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
        /* Main Form Container */
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        
        /* Typography inside form (Force Dark Text) */
        .stForm h1, .stForm h2, .stForm h3, .stForm p, .stForm label, .stForm div {
            color: #333333 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            background-color: #f9f9f9 !important;
            color: #000000 !important;
            border: 1px solid #cccccc;
            border-radius: 8px;
            padding: 10px;
        }
        
        /* Input Focus Effect */
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus {
            border-color: #00FFD1;
            box-shadow: 0 0 5px rgba(0, 255, 209, 0.4);
        }

        /* Paper Preview Box */
        .preview-box {
            background-color: #ffffff;
            color: #000000; /* Black text */
            padding: 40px;
            margin-top: 20px;
            border: 1px solid #dcdcdc;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            border-radius: 2px; /* Sharp corners for paper look */
            font-family: 'Times New Roman', Times, serif; /* Legal Font */
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap; /* Respects newlines */
        }
        
        /* Header Styling */
        .doc-header {
            color: #FAFAFA;
            text-align: center;
            font-weight: bold;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .doc-subheader {
            color: #cccccc;
            text-align: center;
            margin-bottom: 30px;
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