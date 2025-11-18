import streamlit as st
from fpdf import FPDF, HTMLMixin
import datetime

# --- PDF CLASS WITH HTML SUPPORT ---
class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(100, 100, 100) # Grey color for header
        self.cell(0, 10, 'Nyay-Saathi Generated Draft', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def clean_text_for_pdf(text):
    """
    Replaces incompatible characters for standard PDF fonts.
    FPDF (standard) doesn't support Unicode symbols like ₹ or smart quotes.
    """
    replacements = {
        "₹": "Rs. ",
        "“": '"', "”": '"', "‘": "'", "’": "'", # Smart quotes
        "–": "-", "—": "-", # Dashes
        "…": "..."
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Encode to Latin-1 to catch any other errors, ignoring unprintable chars
    return text.encode('latin-1', 'ignore').decode('latin-1')

def create_pdf_bytes(doc_html, doc_type):
    """Generates a PDF from HTML text."""
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Sanitize the text to prevent crashes
    safe_html = clean_text_for_pdf(doc_html)

    # 2. Wrap in basic styling for the PDF engine
    # We use inline CSS to ensure the PDF engine understands it
    styled_html = f"""
    <font face="Arial" size="11">
    <h1 align="center"><b>{doc_type.upper()}</b></h1>
    <br>
    {safe_html}
    </font>
    """
    
    try:
        # 3. Write HTML
        pdf.write_html(styled_html)
    except Exception as e:
        # Fallback: If HTML structure fails, write plain text so user gets SOMETHING
        print(f"HTML Render Error: {e}")
        pdf = PDF() # Reset
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 6, "Error rendering format. Here is the plain text version:\n\n" + safe_html.replace("<br>", "\n").replace("<b>", "").replace("</b>", ""))

    return bytes(pdf.output())

def show_document_generator(llm_model):
    st.header("📝 Generate Legal Agreements")
    st.write("Select a document type, fill in the specific details, and AI will draft a legal version compliant with Indian laws.")

    # 1. Document Selection
    document_type = st.selectbox(
        "Select Agreement Type:",
        (
            "Rental/Lease Agreement", 
            "Non-Disclosure Agreement (NDA)", 
            "Affidavit/Self-Declaration", 
            "Simple Will",
            "Employment Offer Letter",
            "Legal Notice"
        )
    )

    # 2. Dynamic Form
    inputs = {}
    with st.form("doc_gen_form"):
        st.subheader("Enter Agreement Details")
        
        if document_type == "Rental/Lease Agreement":
            c1, c2 = st.columns(2)
            inputs["Landlord Name"] = c1.text_input("Landlord Name")
            inputs["Tenant Name"] = c2.text_input("Tenant Name")
            inputs["Property Address"] = st.text_input("Property Address")
            inputs["Rent Amount"] = st.number_input("Monthly Rent (Rs.)", min_value=0)
            
        elif document_type == "Non-Disclosure Agreement (NDA)":
            inputs["Disclosing Party"] = st.text_input("Disclosing Party")
            inputs["Receiving Party"] = st.text_input("Receiving Party")
            inputs["Confidential Info"] = st.text_area("Description of Confidential Info")
            
        elif document_type == "Affidavit/Self-Declaration":
            inputs["Deponent Name"] = st.text_input("Your Name (Deponent)")
            inputs["Father's Name"] = st.text_input("Father's Name")
            inputs["Statement"] = st.text_area("Statement to Declare")
            
        else:
            inputs["Party Names"] = st.text_input("Party Names")
            inputs["Key Details"] = st.text_area("Enter Key Terms/Details")

        st.warning("⚠️ Disclaimer: This is an AI-generated draft. Review with a lawyer.")
        generate_btn = st.form_submit_button("Draft Document", type="primary")

    # 3. Generation Logic
    if generate_btn:
        if list(inputs.values())[0]: # Check if at least one field is filled
            with st.spinner("Drafting your document..."):
                try:
                    details_text = "\n".join([f"{key}: {value}" for key, value in inputs.items()])
                    
                    # --- PROMPT FOR HTML OUTPUT ---
                    prompt = f"""
                    You are an expert Indian Legal Drafter.
                    Task: Draft a legally sound '{document_type}' based on Indian Law.
                    
                    USER DETAILS:
                    {details_text}
                    
                    INSTRUCTIONS:
                    1. Output the document in **Clean HTML Format**.
                    2. Use <b> tags for bolding Party Names and Titles.
                    3. Use <br><br> for paragraph breaks.
                    4. Use <h3> tags for section headers (e.g., <h3>WHEREAS</h3>).
                    5. Do NOT use Markdown (** or ##). Use ONLY HTML tags.
                    6. Do NOT include <html> or <body> tags, just the content.
                    """
                    
                    response = llm_model.invoke(prompt)
                    draft_html = response.content.replace("```html", "").replace("```", "")
                    
                    # Preview (Streamlit handles Markdown/HTML mixed well)
                    st.subheader("📄 Draft Preview")
                    st.markdown(draft_html, unsafe_allow_html=True)
                    
                    # Generate PDF
                    pdf_bytes = create_pdf_bytes(draft_html, document_type)
                    
                    st.download_button(
                        label="⬇️ Download Final PDF",
                        data=pdf_bytes,
                        file_name=f"{document_type.replace(' ', '_')}_Draft.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating document: {e}")
        else:
            st.error("Please fill in the details.")