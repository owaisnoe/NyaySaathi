import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. DOCUMENT CONFIGURATION (The Expanded Database) ---
DOC_CONFIG = {
    "Rental/Lease Agreement": {
        "fields": [
            {"id": "landlord_name", "label": "Landlord Name"},
            {"id": "tenant_name", "label": "Tenant Name"},
            {"id": "property_address", "label": "Property Address", "type": "textarea"},
            {"id": "rent_amount", "label": "Monthly Rent (Rs.)", "type": "number"},
            {"id": "deposit_amount", "label": "Security Deposit (Rs.)", "type": "number"},
            {"id": "lease_duration", "label": "Lease Duration"},
            {"id": "start_date", "label": "Lease Start Date", "type": "date"},
            {"id": "city", "label": "City of Execution"}
        ],
        "template": """RENTAL AGREEMENT

This Rental Agreement is made on {date} at {city}, BETWEEN:

1. {landlord_name} (hereinafter called the "LESSOR")
   AND
2. {tenant_name} (hereinafter called the "LESSEE")

The Lessor is the absolute owner of the property at:
{property_address}

NOW THIS DEED WITNESSETH:
1. RENT: The Lessee pays a monthly rent of Rs. {rent_amount}.
2. DEPOSIT: The Lessee has paid a refundable security deposit of Rs. {deposit_amount}.
3. TERM: The lease is for a period of {lease_duration} starting from {start_date}.
4. NOTICE: The lease can be terminated with 1 month notice.

IN WITNESS WHEREOF, the parties have signed below.

_________________          _________________
(Landlord)                 (Tenant)"""
    },
    
    "Non-Disclosure Agreement (NDA)": {
        "fields": [
            {"id": "disclosing_party", "label": "Disclosing Party Name"},
            {"id": "receiving_party", "label": "Receiving Party Name"},
            {"id": "confidential_info", "label": "Description of Confidential Info", "type": "textarea"},
            {"id": "duration", "label": "Duration (e.g., 2 years)"},
            {"id": "jurisdiction", "label": "Jurisdiction (City/State)"}
        ],
        "template": """NON-DISCLOSURE AGREEMENT (NDA)

This Agreement is entered into on {date} BETWEEN:

1. {disclosing_party} (Disclosing Party)
2. {receiving_party} (Receiving Party)

1. DEFINITION: "Confidential Information" refers to:
{confidential_info}

2. OBLIGATIONS: The Receiving Party agrees not to disclose this information to any third party.

3. DURATION: This agreement is valid for {duration}.

4. JURISDICTION: This agreement is subject to the courts in {jurisdiction}.

_________________          _________________
(Disclosing Party)         (Receiving Party)"""
    },

    "Affidavit/Self-Declaration": {
        "fields": [
            {"id": "deponent_name", "label": "Your Name (Deponent)"},
            {"id": "father_name", "label": "Father's/Husband's Name"},
            {"id": "age", "label": "Age", "type": "number"},
            {"id": "address", "label": "Full Address", "type": "textarea"},
            {"id": "statement", "label": "Statement to Declare", "type": "textarea"},
            {"id": "place", "label": "Place of Verification"}
        ],
        "template": """AFFIDAVIT / SELF-DECLARATION

I, {deponent_name}, S/o or W/o {father_name}, aged {age}, residing at:
{address}

Do hereby solemnly affirm and declare:

1. That I am a citizen of India.
2. {statement}
3. That the contents of this affidavit are true to the best of my knowledge.

VERIFICATION
Verified at {place} on {date}.

_________________
(Deponent Signature)"""
    },

    "Employment Offer Letter": {
        "fields": [
            {"id": "company_name", "label": "Company Name"},
            {"id": "candidate_name", "label": "Candidate Name"},
            {"id": "job_title", "label": "Job Title"},
            {"id": "salary", "label": "Annual Salary (Rs.)"},
            {"id": "start_date", "label": "Joining Date", "type": "date"},
            {"id": "location", "label": "Work Location"}
        ],
        "template": """EMPLOYMENT OFFER LETTER

Date: {date}

To,
{candidate_name}

Subject: Offer of Employment

Dear {candidate_name},

We are pleased to offer you the position of {job_title} at {company_name}, based in {location}.

Your annual Cost to Company (CTC) will be Rs. {salary}. Your employment will commence on {start_date}.

You will be on probation for a period of 6 months. Please sign the duplicate copy of this letter as a token of your acceptance.

Welcome to the team!

Sincerely,
HR Manager
{company_name}"""
    },

    "Legal Notice (General)": {
        "fields": [
            {"id": "sender_name", "label": "Sender Name"},
            {"id": "recipient_name", "label": "Recipient Name"},
            {"id": "recipient_address", "label": "Recipient Address", "type": "textarea"},
            {"id": "issue_details", "label": "Details of the Issue/Grievance", "type": "textarea"},
            {"id": "demand", "label": "Demand/Action Required", "type": "textarea"},
            {"id": "days_to_reply", "label": "Days to Reply (e.g., 15 days)"}
        ],
        "template": """LEGAL NOTICE

Date: {date}

To,
{recipient_name}
{recipient_address}

Subject: Legal Notice regarding {issue_details}

Sir/Madam,

Under instruction from my client, {sender_name}, I hereby serve you this legal notice:

1. That my client states that: {issue_details}

2. That due to your actions, my client has suffered loss/grievance.

3. I hereby call upon you to {demand} within {days_to_reply} of receipt of this notice.

Failing which, my client shall be constrained to initiate legal proceedings against you at your own risk and cost.

Advocate for {sender_name}"""
    },

    "Memorandum of Understanding (MOU)": {
        "fields": [
            {"id": "party_a", "label": "First Party Name"},
            {"id": "party_b", "label": "Second Party Name"},
            {"id": "purpose", "label": "Purpose of Partnership", "type": "textarea"},
            {"id": "roles", "label": "Roles & Responsibilities", "type": "textarea"},
            {"id": "place", "label": "Place of Execution"}
        ],
        "template": """MEMORANDUM OF UNDERSTANDING (MOU)

This MOU is made on {date} at {place}, BETWEEN:

1. {party_a} (First Party)
AND
2. {party_b} (Second Party)

PURPOSE:
The parties intend to collaborate for:
{purpose}

ROLES & RESPONSIBILITIES:
{roles}

This MOU is a statement of intent and is not legally binding unless a specific agreement is signed.

_________________          _________________
(First Party)              (Second Party)"""
    },

    "Simple Will": {
        "fields": [
            {"id": "testator_name", "label": "Your Name (Testator)"},
            {"id": "beneficiary_name", "label": "Beneficiary Name"},
            {"id": "executor_name", "label": "Executor Name"},
            {"id": "assets", "label": "Details of Assets", "type": "textarea"},
            {"id": "place", "label": "Place"}
        ],
        "template": """LAST WILL AND TESTAMENT

I, {testator_name}, resident of {place}, being of sound mind, hereby declare this to be my last Will.

1. I revoke all previous wills and codicils.
2. I appoint {executor_name} as the Executor of this Will.
3. I bequeath my assets/property described below:
   {assets}
   
   TO: {beneficiary_name}.

Signed on {date} at {place}.

_________________
(Testator Signature)

Witness 1: _________________
Witness 2: _________________"""
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
    
    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, doc_type.upper(), 0, 1, 'C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", size=11)
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    return bytes(pdf.output())

# --- 3. UI STYLING (CSS) ---
def inject_custom_css():
    st.markdown("""
    <style>
        .doc-header {
            font-family: 'Arial', sans-serif;
            color: #FAFAFA;
            text-align: center;
            margin-bottom: 20px;
        }
        .doc-subheader {
            text-align: center;
            color: #B0B0B0;
            margin-bottom: 30px;
        }
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border: 1px solid #e0e0e0;
        }
        .stForm label, .stForm h1, .stForm h2, .stForm p, .stForm div {
            color: #333333 !important;
        }
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #f8f9fa !important;
            color: #000000 !important;
            border: 1px solid #ced4da;
            border-radius: 8px;
        }
        .paper-preview {
            background-color: #ffffff;
            color: #000000;
            padding: 40px;
            margin-top: 20px;
            border: 1px solid #ccc;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            border-radius: 2px;
            font-family: 'Times New Roman', Times, serif;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN FUNCTION ---
def show_document_generator():
    inject_custom_css()
    
    st.markdown("<h1 class='doc-header'>📝 Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p class='doc-subheader'>Create professional legal agreements instantly. Zero wait time.</p>", unsafe_allow_html=True)

    # Document Selector
    doc_type = st.selectbox("Select Document Type:", list(DOC_CONFIG.keys()))
    config = DOC_CONFIG[doc_type]
    
    # --- DYNAMIC FORM ---
    user_inputs = {}
    with st.form("doc_form"):
        st.markdown(f"<h3 style='color:#333;'>{doc_type} Details</h3>", unsafe_allow_html=True)
        
        # Create 2 columns for clean layout
        cols = st.columns(2)
        
        for i, field in enumerate(config["fields"]):
            
            label = field["label"]
            key = field["id"]
            ftype = field.get("type", "text")
            
            # --- THIS IS THE FIX FOR THE CRASH ---
            if ftype == "textarea":
                # Textareas go full width (outside columns)
                user_inputs[key] = st.text_area(label, height=100)
            else:
                # Normal inputs go into columns
                with cols[i % 2]:
                    if ftype == "text":
                        user_inputs[key] = st.text_input(label)
                    elif ftype == "number":
                        user_inputs[key] = st.number_input(label, min_value=0, step=1000)
                    elif ftype == "date":
                        user_inputs[key] = st.date_input(label, value=datetime.date.today())

        st.markdown("---")
        submitted = st.form_submit_button("Generate Draft (Instant)", type="primary")

    # --- OUTPUT SECTION ---
    if submitted:
        # Add automatic date
        user_inputs["date"] = datetime.date.today().strftime("%B %d, %Y")
        
        # Check for empty fields
        empty_fields = [k for k, v in user_inputs.items() if str(v).strip() == ""]
        
        if not empty_fields:
            try:
                # Fill Template
                final_text = config["template"].format(**user_inputs)
                
                st.success(f"✅ {doc_type} Generated Successfully!")
                
                # Preview
                st.markdown("### Document Preview")
                st.markdown(f'<div class="paper-preview">{final_text}</div>', unsafe_allow_html=True)
                
                # PDF Download
                pdf_data = create_pdf_bytes(final_text, doc_type)
                
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