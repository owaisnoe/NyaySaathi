import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. PRE-DEFINED LEGAL TEMPLATES ---
# These are standard formats used in India.

RENTAL_TEMPLATE = """
RENTAL AGREEMENT

This Rental Agreement is made on this {date} at {city}, between:

1. LANDLORD:
   {landlord_name}, residing at {landlord_address} (hereinafter referred to as the "LESSOR").

   AND

2. TENANT:
   {tenant_name}, residing at {tenant_address} (hereinafter referred to as the "LESSEE").

WHEREAS the Lessor is the absolute owner of the property situated at:
{property_address}

NOW THIS AGREEMENT WITNESSETH AS FOLLOWS:

1. RENT: The Lessee shall pay a monthly rent of Rs. {rent_amount} on or before the 5th of every month.
2. DEPOSIT: The Lessee has paid a refundable security deposit of Rs. {deposit}.
3. TERM: This lease shall be valid for a period of {duration}, starting from {start_date}.
4. NOTICE: Either party can terminate this agreement by giving 1 month notice.
5. USE: The premises shall be used for residential purposes only.

IN WITNESS WHEREOF, the parties have signed this agreement on the date first mentioned above.

_________________                       _________________
(Landlord Signature)                    (Tenant Signature)
"""

NDA_TEMPLATE = """
NON-DISCLOSURE AGREEMENT (NDA)

This Agreement is entered into on {date} BY AND BETWEEN:

1. DISCLOSING PARTY: {disclosing_party}
   AND
2. RECEIVING PARTY: {receiving_party}

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" includes, but is not limited to:
{confidential_info}

2. OBLIGATIONS
The Receiving Party agrees to hold the Confidential Information in strict confidence and not to disclose it to any third party without prior written consent.

3. DURATION
This Agreement shall remain in effect for a period of {duration}.

4. JURISDICTION
This Agreement shall be governed by the laws of India and subject to the jurisdiction of courts in {jurisdiction}.

IN WITNESS WHEREOF, the parties have executed this Agreement.

_________________                       _________________
(Disclosing Party)                      (Receiving Party)
"""

AFFIDAVIT_TEMPLATE = """
AFFIDAVIT / SELF-DECLARATION

I, {deponent_name}, S/o or W/o {father_name}, aged about {age} years, residing at:
{address}

Do hereby solemnly affirm and declare as follows:

1. That I am a citizen of India.
2. {statement}
3. That the facts stated above are true and correct to the best of my knowledge and belief.

VERIFICATION

Verified at {place} on this {date}, that the contents of this affidavit are true and correct.

_________________
(Deponent Signature)
"""

# --- 2. CUSTOM CSS (Dark Mode Fix) ---
def inject_custom_css():
    st.markdown("""
    <style>
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        .stForm h1, .stForm h2, .stForm h3, .stForm p, .stForm label, .stForm div {
            color: #1a1a1a !important;
        }
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #f9f9f9 !important;
            color: #000000 !important;
            border: 1px solid #cccccc;
        }
        .preview-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            color: #000000 !important;
            white-space: pre-wrap;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- 3. PDF GENERATOR ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Nyay-Saathi Legal Draft', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_pdf_bytes(doc_text, doc_type):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Use latin-1 encoding to prevent crashes with special chars
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, safe_text)
    return bytes(pdf.output())

# --- 4. MAIN UI FUNCTION ---
def show_document_generator(llm_model=None): # llm_model is unused now, but kept for compatibility
    inject_custom_css()
    
    st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>Legal Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # We only offer the templates we have defined
    document_type = st.selectbox(
        "Select Document Type:",
        ("Rental/Lease Agreement", "Non-Disclosure Agreement (NDA)", "Affidavit/Self-Declaration")
    )

    inputs = {}
    
    # --- FORM LOGIC ---
    with st.form("doc_gen_form"):
        st.subheader(f"{document_type} Details")
        
        if document_type == "Rental/Lease Agreement":
            c1, c2 = st.columns(2)
            inputs["landlord_name"] = c1.text_input("Landlord Name")
            inputs["tenant_name"] = c2.text_input("Tenant Name")
            inputs["landlord_address"] = st.text_area("Landlord Address", height=70)
            inputs["tenant_address"] = st.text_area("Tenant Address", height=70)
            inputs["property_address"] = st.text_area("Rented Property Address", height=70)
            c3, c4 = st.columns(2)
            inputs["rent_amount"] = c3.number_input("Monthly Rent (Rs.)", min_value=0, step=500)
            inputs["deposit"] = c4.number_input("Deposit (Rs.)", min_value=0, step=1000)
            inputs["duration"] = st.text_input("Duration (e.g., 11 months)")
            inputs["start_date"] = st.date_input("Start Date", datetime.date.today())
            inputs["city"] = st.text_input("City/Place")

        elif document_type == "Non-Disclosure Agreement (NDA)":
            c1, c2 = st.columns(2)
            inputs["disclosing_party"] = c1.text_input("Disclosing Party Name")
            inputs["receiving_party"] = c2.text_input("Receiving Party Name")
            inputs["confidential_info"] = st.text_area("Description of Confidential Information")
            inputs["duration"] = st.text_input("Duration (e.g., 2 years)")
            inputs["jurisdiction"] = st.text_input("Jurisdiction (City)")
            
        elif document_type == "Affidavit/Self-Declaration":
            c1, c2 = st.columns(2)
            inputs["deponent_name"] = c1.text_input("Your Name (Deponent)")
            inputs["father_name"] = c2.text_input("Father's Name")
            inputs["age"] = st.number_input("Age", min_value=18)
            inputs["address"] = st.text_area("Address")
            inputs["statement"] = st.text_area("Statement to Declare (e.g., My name is spelled...)")
            inputs["place"] = st.text_input("Place")

        st.markdown("---")
        generate_btn = st.form_submit_button("Generate Document (Instant)", type="primary")

    # --- GENERATION LOGIC (NO AI) ---
    if generate_btn:
        # Add today's date to inputs automatically
        inputs["date"] = datetime.date.today().strftime("%B %d, %Y")
        
        # 1. Select the template
        template = ""
        if document_type == "Rental/Lease Agreement":
            template = RENTAL_TEMPLATE
        elif document_type == "Non-Disclosure Agreement (NDA)":
            template = NDA_TEMPLATE
        elif document_type == "Affidavit/Self-Declaration":
            template = AFFIDAVIT_TEMPLATE
            
        # 2. Fill the template (Python Format String)
        try:
            final_doc = template.format(**inputs)
            
            st.success("Document generated successfully!")
            
            # Preview
            st.markdown("### Document Preview")
            st.markdown(f'<div class="preview-box">{final_doc}</div>', unsafe_allow_html=True)
            
            # PDF
            pdf_bytes = create_pdf_bytes(final_doc, document_type)
            
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{document_type.replace(' ', '_')}_Draft.pdf",
                mime="application/pdf",
                type="primary"
            )
            
        except KeyError as e:
            st.error(f"Please fill in all fields. Missing: {e}")
        except Exception as e:
            st.error(f"Error: {e}")