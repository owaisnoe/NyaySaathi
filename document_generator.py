import streamlit as st
from fpdf import FPDF
import datetime

# --- CUSTOM CSS FOR ENHANCED UI (DARK MODE FIX) ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* Form Container - White Background */
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        /* FORCE BLACK TEXT INSIDE FORM */
        .stForm h1, .stForm h2, .stForm h3, .stForm p, .stForm label, .stForm div {
            color: #1a1a1a !important;
        }
        
        /* Input Fields */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background-color: #f9f9f9 !important;
            color: #000000 !important;
            border: 1px solid #cccccc;
        }
        
        /* Preview Box */
        .preview-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #ddd;
            color: #000000 !important;
            white-space: pre-wrap; /* Preserves formatting */
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
        }
    </style>
    """, unsafe_allow_html=True)

# --- ROBUST PDF CLASS ---
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
    """Generates a PDF from text instantly."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, doc_type.upper(), 0, 1, 'C')
    pdf.ln(5)
    
    # Body
    pdf.set_font("Arial", size=11)
    
    # Clean text to prevent crashes with special characters
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    
    # Write text (multi_cell handles wrapping automatically)
    pdf.multi_cell(0, 6, safe_text)
    
    return bytes(pdf.output())

def get_document_fields(document_type):
    """Returns form fields based on document type."""
    if document_type == "Rental/Lease Agreement":
        return {
            "columns": True,
            "fields": [
                {"name": "Landlord Name", "type": "text", "required": True},
                {"name": "Tenant Name", "type": "text", "required": True},
                {"name": "Property Address", "type": "textarea", "required": True},
                {"name": "Rent Amount (Rs.)", "type": "number", "required": True},
                {"name": "Lease Duration", "type": "text", "placeholder": "e.g., 11 months"},
                {"name": "Security Deposit (Rs.)", "type": "number"}
            ]
        }
    elif document_type == "Non-Disclosure Agreement (NDA)":
        return {
            "columns": True,
            "fields": [
                {"name": "Disclosing Party", "type": "text", "required": True},
                {"name": "Receiving Party", "type": "text", "required": True},
                {"name": "Confidential Info Description", "type": "textarea", "required": True},
                {"name": "Duration", "type": "text", "placeholder": "e.g., 2 years"}
            ]
        }
    elif document_type == "Affidavit/Self-Declaration":
        return {
            "columns": False,
            "fields": [
                {"name": "Deponent Name", "type": "text", "required": True},
                {"name": "Father's Name", "type": "text", "required": True},
                {"name": "Address", "type": "textarea"},
                {"name": "Statement to Declare", "type": "textarea", "required": True}
            ]
        }
    else:
        return {
            "columns": False,
            "fields": [
                {"name": "Party Names", "type": "text"},
                {"name": "Key Details & Terms", "type": "textarea", "required": True}
            ]
        }

def render_form_fields(field_config):
    inputs = {}
    if field_config["columns"]:
        fields = field_config["fields"]
        for i in range(0, len(fields), 2):
            c1, c2 = st.columns(2)
            with c1:
                if i < len(fields): inputs.update(render_single_field(fields[i]))
            with c2:
                if i + 1 < len(fields): inputs.update(render_single_field(fields[i+1]))
    else:
        for field in field_config["fields"]:
            inputs.update(render_single_field(field))
    return inputs

def render_single_field(field):
    label = field["name"] + (" *" if field.get("required") else "")
    if field["type"] == "text":
        val = st.text_input(label, placeholder=field.get("placeholder", ""))
    elif field["type"] == "textarea":
        val = st.text_area(label, placeholder=field.get("placeholder", ""), height=100)
    elif field["type"] == "number":
        val = st.number_input(label, min_value=0, step=1000)
    else:
        val = st.text_input(label)
    return {field["name"]: val}

def show_document_generator(llm_model):
    inject_custom_css()
    
    st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>Legal Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("---")

    document_type = st.selectbox(
        "Select Document Type:",
        ("Rental/Lease Agreement", "Non-Disclosure Agreement (NDA)", 
         "Affidavit/Self-Declaration", "Simple Will", "Employment Offer Letter", "Legal Notice")
    )

    field_config = get_document_fields(document_type)

    with st.form("doc_gen_form"):
        st.subheader(f"{document_type} Details")
        inputs = render_form_fields(field_config)
        st.markdown("---")
        generate_btn = st.form_submit_button("Generate Document", type="primary")

    if generate_btn:
        # Check if required fields are filled
        if any(inputs.values()):
            with st.spinner("Drafting document... (This will take 5-10 seconds)"):
                try:
                    details_text = "\n".join([f"{key}: {value}" for key, value in inputs.items()])
                    
                    # --- ROBUST TEXT PROMPT (NO HTML) ---
                    prompt = f"""
                    You are an expert Indian Legal Drafter.
                    Task: Draft a legally sound '{document_type}' based on Indian Law.
                    
                    USER DETAILS:
                    {details_text}
                    
                    INSTRUCTIONS:
                    1. Output the document in **CLEAN PLAIN TEXT**.
                    2. Use UPPERCASE for section headers (e.g., WHEREAS, NOW THIS DEED WITNESSETH).
                    3. Ensure clear paragraph spacing.
                    4. Include signature blocks at the bottom.
                    5. Do NOT use Markdown, HTML, or special formatting. Just clean, professional text.
                    """
                    
                    response = llm_model.invoke(prompt)
                    draft_text = response.content
                    
                    st.success("Draft generated!")
                    
                    # Preview
                    st.markdown("### Document Preview")
                    st.markdown(f'<div class="preview-box">{draft_text}</div>', unsafe_allow_html=True)
                    
                    # Generate PDF
                    pdf_bytes = create_pdf_bytes(draft_text, document_type)
                    
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name=f"{document_type.replace(' ', '_')}_Draft.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please fill in the details.")