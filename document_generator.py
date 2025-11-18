import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. DOCUMENT CONFIGURATION (The "Database") ---
DOC_CONFIG = {
    "Rental/Lease Agreement": {
        "fields": [
            {"id": "landlord_name", "label": "Landlord Name"},
            {"id": "tenant_name", "label": "Tenant Name"},
            {"id": "property_address", "label": "Property Address", "type": "textarea"},
            {"id": "rent_amount", "label": "Monthly Rent (Rs.)", "type": "number"},
            {"id": "deposit_amount", "label": "Security Deposit (Rs.)", "type": "number"},
            {"id": "lease_duration", "label": "Lease Duration (e.g., 11 months)"},
            {"id": "start_date", "label": "Lease Start Date", "type": "date"},
            {"id": "city", "label": "City of Execution"}
        ],
        "template": """RENTAL AGREEMENT\n\nThis Rental Agreement is made on {date} at {city}, BETWEEN:\n\n1. {landlord_name} (hereinafter called the "LESSOR")\n   AND\n2. {tenant_name} (hereinafter called the "LESSEE")\n\nThe Lessor is the absolute owner of the property at:\n{property_address}\n\nNOW THIS DEED WITNESSETH:\n1. RENT: The Lessee pays a monthly rent of Rs. {rent_amount}.\n2. DEPOSIT: The Lessee has paid a refundable security deposit of Rs. {deposit_amount}.\n3. TERM: The lease is for a period of {lease_duration} starting from {start_date}.\n4. NOTICE: The lease can be terminated with 1 month notice.\n\nIN WITNESS WHEREOF, the parties have signed below.\n\n_________________          _________________\n(Landlord)                 (Tenant)"""
    },
    "Non-Disclosure Agreement (NDA)": {
        "fields": [
            {"id": "disclosing_party", "label": "Disclosing Party Name"},
            {"id": "receiving_party", "label": "Receiving Party Name"},
            {"id": "confidential_info", "label": "Description of Confidential Info", "type": "textarea"},
            {"id": "duration", "label": "Duration (e.g., 2 years)"},
            {"id": "jurisdiction", "label": "Jurisdiction (City/State)"}
        ],
        "template": """NON-DISCLOSURE AGREEMENT (NDA)\n\nThis Agreement is entered into on {date} BETWEEN:\n\n1. {disclosing_party} (Disclosing Party)\n2. {receiving_party} (Receiving Party)\n\n1. DEFINITION: "Confidential Information" refers to:\n{confidential_info}\n\n2. OBLIGATIONS: The Receiving Party agrees not to disclose this information to any third party.\n\n3. DURATION: This agreement is valid for {duration}.\n\n4. JURISDICTION: This agreement is subject to the courts in {jurisdiction}.\n\n_________________          _________________\n(Disclosing Party)         (Receiving Party)"""
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
        "template": """AFFIDAVIT / SELF-DECLARATION\n\nI, {deponent_name}, S/o or W/o {father_name}, aged {age}, residing at:\n{address}\n\nDo hereby solemnly affirm and declare:\n\n1. That I am a citizen of India.\n2. {statement}\n3. That the contents of this affidavit are true to the best of my knowledge.\n\nVERIFICATION\nVerified at {place} on {date}.\n\n_________________\n(Deponent Signature)"""
    }
}

# --- 2. PDF GENERATOR (Offline) ---
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
    # Clean text for Latin-1 encoding (Standard FPDF limitation)
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, safe_text)
    
    return bytes(pdf.output())

# --- 3. UI HELPERS ---
def inject_custom_css():
    st.markdown("""
    <style>
        .stForm {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
        .stForm label, .stForm h1, .stForm h2, .stForm p {
            color: #333333 !important;
        }
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #f9f9f9 !important;
            color: #000000 !important;
            border: 1px solid #ccc;
        }
        .preview-box {
            background-color: #fff;
            color: #000;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            white-space: pre-wrap;
            font-family: monospace;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MAIN FUNCTION (No LLM Argument) ---
def show_document_generator():
    inject_custom_css()
    
    st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>Legal Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Select Document
    doc_type = st.selectbox("Select Document Type:", list(DOC_CONFIG.keys()))
    
    config = DOC_CONFIG[doc_type]
    
    # Dynamic Form
    user_inputs = {}
    with st.form("doc_form"):
        st.subheader(f"{doc_type} Details")
        
        # Create 2 columns for layout
        cols = st.columns(2)
        
        for i, field in enumerate(config["fields"]):
            
            label = field["label"]
            key = field["id"]
            ftype = field.get("type", "text")
            
            # --- FIXED LOGIC FOR COLUMN LAYOUT ---
            if ftype == "textarea":
                # If textarea, use full width (no column context)
                user_inputs[key] = st.text_area(label, height=100)
            else:
                # If normal input, put in a column
                col = cols[i % 2]
                with col:
                    if ftype == "text":
                        user_inputs[key] = st.text_input(label)
                    elif ftype == "number":
                        user_inputs[key] = st.number_input(label, min_value=0, step=1000)
                    elif ftype == "date":
                        user_inputs[key] = st.date_input(label, value=datetime.date.today())
            # -------------------------------------

        st.markdown("---")
        submitted = st.form_submit_button("Generate Draft (Instant)", type="primary")

    if submitted:
        # 1. Add automatic date
        user_inputs["date"] = datetime.date.today().strftime("%B %d, %Y")
        
        # 2. Check for empty fields
        # Convert dates and numbers to string for checking
        empty_fields = [k for k, v in user_inputs.items() if str(v).strip() == ""]
        
        if not empty_fields:
            # 3. Fill Template
            try:
                final_text = config["template"].format(**user_inputs)
                
                st.success("Document Generated Successfully!")
                
                st.markdown("### Preview")
                st.markdown(f'<div class="preview-box">{final_text}</div>', unsafe_allow_html=True)
                
                # 4. Create PDF
                pdf_data = create_pdf_bytes(final_text, doc_type)
                
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_data,
                    file_name=f"{doc_type.replace(' ', '_')}_Draft.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                
            except Exception as e:
                st.error(f"Error filling template: {e}")
        else:
            st.error("Please fill in all fields to generate the document.")