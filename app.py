import streamlit as st
from fpdf import FPDF, HTMLMixin
import datetime
import re

# --- CUSTOM CSS FOR ENHANCED UI ---
def inject_custom_css():
    st.markdown("""
    <style>
        /* --- FORM CONTAINER (Light Background) --- */
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        /* --- CRITICAL FIX: FORCE DARK TEXT INSIDE FORM --- */
        /* This overrides the global Dark Mode white text settings */
        
        /* Fix for Headers (Subheaders/Titles inside form) */
        .stForm h1, .stForm h2, .stForm h3, .stForm h4 {
            color: #1a1a1a !important;
            font-family: 'Arial', sans-serif;
        }

        /* Fix for Input Labels */
        .stForm label p {
            color: #333333 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
        }
        
        /* Fix for Standard Text/Paragraphs inside form */
        .stForm p {
            color: #333333 !important;
        }

        /* --- INPUT FIELDS --- */
        .stTextInput > div > div > input, 
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            border-radius: 8px;
            border: 1px solid #cccccc;
            padding: 12px;
            color: #000000 !important; /* Force black text input */
            background-color: #f9f9f9 !important;
            transition: all 0.3s ease;
        }

        /* Input Focus State */
        .stTextInput > div > div > input:focus, 
        .stTextArea > div > div > textarea:focus,
        .stNumberInput > div > div > input:focus {
            border-color: #00FFD1;
            background-color: #ffffff !important;
            box-shadow: 0 0 0 2px rgba(0, 255, 209, 0.2);
        }

        /* --- BUTTONS --- */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            width: 100%;
        }

        /* --- PREVIEW BOX --- */
        .preview-box {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 10px;
            border: 1px solid #e0e0e0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin: 20px 0;
            color: #000000 !important; /* Force black text in preview */
        }
        
        /* Make sure preview text is visible */
        .preview-box p, .preview-box h1, .preview-box h2, .preview-box h3 {
             color: #000000 !important;
        }

        /* --- DOWNLOAD BUTTON --- */
        .stDownloadButton > button {
            background-color: #4CAF50 !important;
            color: white !important;
            border: none;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        }
        
        /* --- ALERTS/WARNINGS --- */
        .stAlert {
            color: #000000 !important; /* Ensure alert text is readable */
        }
        
    </style>
    """, unsafe_allow_html=True)

# --- PDF CLASS WITH HTML SUPPORT ---
class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_font('Arial', 'B', 11)
        self.set_text_color(60, 60, 60) # Grey color for header
        self.cell(0, 10, 'Nyay-Saathi Legal Document', 0, 1, 'R')
        self.set_draw_color(200, 200, 200)
        self.line(10, 18, 200, 18)
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.datetime.now().strftime("%B %d, %Y")}', 0, 0, 'C')

def clean_text_for_pdf(text):
    """
    Replaces incompatible characters for standard PDF fonts.
    """
    replacements = {
        "₹": "Rs. ",
        "“": '"', "”": '"', "‘": "'", "’": "'", 
        "–": "-", "—": "-", 
        "…": "...",
        "•": "*"
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_pdf_bytes(doc_html, doc_type):
    """Generates a professional PDF from HTML text."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    safe_html = clean_text_for_pdf(doc_html)

    styled_html = f"""
    <font face="Arial" size="11">
    <h1 align="center"><b>{doc_type.upper()}</b></h1>
    <br><br>
    {safe_html}
    </font>
    """
    
    try:
        pdf.write_html(styled_html)
    except Exception as e:
        pdf = PDF() # Reset
        pdf.add_page()
        pdf.set_font("Arial", size=11)
        plain_text = safe_html.replace("<br>", "\n").replace("<b>", "").replace("</b>", "")
        plain_text = re.sub('<.*?>', '', plain_text)
        pdf.multi_cell(0, 6, f"Error rendering format.\n\nPlain text version:\n\n{plain_text}")

    return bytes(pdf.output())

def validate_inputs(inputs):
    """Validates that required fields are filled."""
    filled_values = [v for v in inputs.values() if v and str(v).strip()]
    return len(filled_values) > 0

def get_document_fields(document_type):
    """Returns the appropriate form fields for each document type."""
    if document_type == "Rental/Lease Agreement":
        return {
            "columns": True,
            "fields": [
                {"name": "Landlord Name", "type": "text", "required": True},
                {"name": "Tenant Name", "type": "text", "required": True},
                {"name": "Property Address", "type": "textarea", "required": True},
                {"name": "Rent Amount", "type": "number", "required": True},
                {"name": "Lease Duration", "type": "text", "placeholder": "e.g., 11 months"},
                {"name": "Security Deposit", "type": "number"},
                {"name": "Agreement Date", "type": "date"}
            ]
        }
        
    elif document_type == "Non-Disclosure Agreement (NDA)":
        return {
            "columns": True,
            "fields": [
                {"name": "Disclosing Party", "type": "text", "required": True},
                {"name": "Receiving Party", "type": "text", "required": True},
                {"name": "Confidential Info", "type": "textarea", "required": True},
                {"name": "Agreement Duration", "type": "text", "placeholder": "e.g., 2 years"},
                {"name": "Agreement Date", "type": "date"}
            ]
        }
        
    elif document_type == "Affidavit/Self-Declaration":
        return {
            "columns": False,
            "fields": [
                {"name": "Deponent Name", "type": "text", "required": True},
                {"name": "Father's Name", "type": "text", "required": True},
                {"name": "Address", "type": "textarea"},
                {"name": "Statement", "type": "textarea", "required": True},
                {"name": "Place", "type": "text"},
                {"name": "Date", "type": "date"}
            ]
        }

    elif document_type == "Simple Will":
        return {
            "columns": False,
            "fields": [
                {"name": "Testator Name", "type": "text", "required": True},
                {"name": "Address", "type": "textarea", "required": True},
                {"name": "Beneficiaries", "type": "textarea", "required": True, "placeholder": "List all beneficiaries and their shares"},
                {"name": "Executor Name", "type": "text"},
                {"name": "Date", "type": "date"}
            ]
        }

    elif document_type == "Employment Offer Letter":
        return {
            "columns": True,
            "fields": [
                {"name": "Company Name", "type": "text", "required": True},
                {"name": "Candidate Name", "type": "text", "required": True},
                {"name": "Position", "type": "text", "required": True},
                {"name": "Annual Salary", "type": "number", "required": True},
                {"name": "Start Date", "type": "date"},
                {"name": "Department", "type": "text"},
                {"name": "Reporting Manager", "type": "text"}
            ]
        }
        
    else:  # Legal Notice
        return {
            "columns": False,
            "fields": [
                {"name": "Sender Name", "type": "text", "required": True},
                {"name": "Recipient Name", "type": "text", "required": True},
                {"name": "Recipient Address", "type": "textarea", "required": True},
                {"name": "Issue Description", "type": "textarea", "required": True},
                {"name": "Demand/Relief Sought", "type": "textarea", "required": True},
                {"name": "Date", "type": "date"}
            ]
        }

def render_form_fields(field_config):
    """Renders dynamic form fields based on configuration."""
    inputs = {}
    
    if field_config["columns"]:
        fields = field_config["fields"]
        for i in range(0, len(fields), 2):
            if i + 1 < len(fields):
                c1, c2 = st.columns(2)
                with c1:
                    inputs.update(render_single_field(fields[i]))
                with c2:
                    inputs.update(render_single_field(fields[i+1]))
            else:
                inputs.update(render_single_field(fields[i]))
    else:
        for field in field_config["fields"]:
            inputs.update(render_single_field(field))
            
    return inputs

def render_single_field(field):
    """Renders a single form field."""
    label = field["name"] + (" *" if field.get("required") else "")
    placeholder = field.get("placeholder", "")
    
    if field["type"] == "text":
        value = st.text_input(label, placeholder=placeholder)
    elif field["type"] == "textarea":
        value = st.text_area(label, placeholder=placeholder, height=100)
    elif field["type"] == "number":
        value = st.number_input(label, min_value=0, step=1)
    elif field["type"] == "date":
        value = st.date_input(label, value=datetime.date.today())
    else:
        value = st.text_input(label)
        
    return {field["name"]: value}

def show_document_generator(llm_model):
    """Main function to display the document generator interface."""
    inject_custom_css()
    
    # Using HTML for header to ensure color consistency
    st.markdown("<h1 style='text-align: center; color: #FAFAFA;'>Legal Document Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #CCCCCC; font-size: 16px;'>Create professional legal documents compliant with Indian laws</p>", unsafe_allow_html=True)
    st.markdown("---")

    document_type = st.selectbox(
        "Select Document Type:",
        (
            "Rental/Lease Agreement",
            "Non-Disclosure Agreement (NDA)",
            "Affidavit/Self-Declaration",
            "Simple Will",
            "Employment Offer Letter",
            "Legal Notice"
        )
    )

    field_config = get_document_fields(document_type)

    with st.form("doc_gen_form", clear_on_submit=False):
        # Force dark text for the form subheader using HTML
        st.markdown(f"<h3 style='color: #1a1a1a;'>{document_type} Details</h3>", unsafe_allow_html=True)
        st.caption("Fields marked with * are required")
        
        inputs = render_form_fields(field_config)
        
        st.markdown("---")
        st.warning("Disclaimer: This is an AI-generated draft. Please review with a qualified lawyer.")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_btn = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

    if generate_btn:
        if validate_inputs(inputs):
            with st.spinner("Drafting your document..."):
                try:
                    details_text = "\n".join([f"{key}: {value}" for key, value in inputs.items() if value])
                    
                    prompt = f"""
                    You are an expert Indian Legal Drafter specializing in {document_type}.
                    Task: Draft a comprehensive, legally sound '{document_type}' based on Indian Law.
                    USER DETAILS:
                    {details_text}
                    INSTRUCTIONS:
                    1. Output the document in Clean HTML Format.
                    2. Use <b> tags for bolding.
                    3. Use <br><br> for paragraph breaks.
                    4. Use <h3> tags for section headers.
                    5. Use proper legal terminology and structure.
                    6. Do NOT use Markdown. Use ONLY HTML tags.
                    7. Do NOT include <html> or <body> tags.
                    """
                    
                    response = llm_model.invoke(prompt)
                    draft_html = response.content.replace("```html", "").replace("```", "").strip()
                    
                    st.success("Document generated successfully!")
                    
                    # Preview Box
                    st.markdown("---")
                    st.markdown('<div class="preview-box">', unsafe_allow_html=True)
                    st.markdown(f"<h3 style='color: black;'>Document Preview</h3>", unsafe_allow_html=True)
                    # Render the HTML content inside the white preview box
                    st.markdown(f"<div style='color: black;'>{draft_html}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    pdf_bytes = create_pdf_bytes(draft_html, document_type)
                    
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="Download PDF Document",
                            data=pdf_bytes,
                            file_name=f"{document_type.replace(' ', '_')}_{datetime.datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    
                except Exception as e:
                    st.error(f"Error generating document: {str(e)}")
        else:
            st.error("Please fill in at least the required fields marked with *")