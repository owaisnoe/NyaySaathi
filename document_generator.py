import streamlit as st
from fpdf import FPDF, HTMLMixin # Import HTMLMixin for formatting

def create_pdf_bytes(doc_html, doc_type):
    """Generates a PDF from HTML text and returns the bytes."""
    
    # We inherit from HTMLMixin to enable write_html
    class PDF(FPDF, HTMLMixin):
        def header(self):
            self.set_font('Arial', 'B', 16)
            # FIXED: Clean title, no "Nyay-Saathi" prefix
            self.cell(0, 10, doc_type.upper(), 0, 1, 'C') 
            self.ln(10) # Add some space after title

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # We use write_html to render bolding (<b>) and breaks (<br>)
    # We wrap the text in a body tag to ensure font consistency
    html_content = f"""
    <body style="font-family: Arial; font-size: 11pt; line-height: 1.5;">
    {doc_html}
    </body>
    """
    
    # Attempt to write HTML. If symbols fail, we fall back to clean text.
    try:
        pdf.write_html(html_content)
    except Exception as e:
        # Fallback: If HTML fails (rare), write plain text
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 6, doc_html.replace("<b>", "").replace("</b>", "").replace("<br>", "\n"))

    return bytes(pdf.output())

def show_document_generator(llm_model):
    """
    Renders the Document Generator UI with interactive forms.
    """
    st.header("📝 Generate Legal Agreements")
    st.write("Select a document type, fill in the specific details, and AI will draft a compliant legal version.")

    # 1. Document Selection
    document_type = st.selectbox(
        "Select Agreement Type:",
        (
            "Rental/Lease Agreement", 
            "Non-Disclosure Agreement (NDA)", 
            "Affidavit/Self-Declaration", 
            "Simple Will",
            "General Document (Other)" 
        )
    )

    # 2. Dynamic Form Generation based on selection
    inputs = {}
    
    with st.form("doc_gen_form"):
        st.subheader("Enter Agreement Details")
        
        if document_type == "Rental/Lease Agreement":
            col1, col2 = st.columns(2)
            inputs["Landlord Name"] = col1.text_input("Landlord (Owner) Name")
            inputs["Tenant Name"] = col2.text_input("Tenant Name")
            inputs["Property Address"] = st.text_input("Full Property Address")
            c1, c2, c3 = st.columns(3)
            inputs["Monthly Rent"] = c1.number_input("Monthly Rent (₹)", min_value=0, step=500)
            inputs["Security Deposit"] = c2.number_input("Security Deposit (₹)", min_value=0, step=1000)
            inputs["Lease Duration"] = c3.text_input("Duration (e.g., 11 Months)")
            
        elif document_type == "Non-Disclosure Agreement (NDA)":
            col1, col2 = st.columns(2)
            inputs["Disclosing Party"] = col1.text_input("Disclosing Party Name")
            inputs["Receiving Party"] = col2.text_input("Receiving Party Name")
            inputs["Confidential Information"] = st.text_area("Description of Confidential Info")
            inputs["Jurisdiction"] = st.text_input("Jurisdiction (City/State)", value="Bangalore, Karnataka")

        elif document_type == "Affidavit/Self-Declaration":
            inputs["Deponent Name"] = st.text_input("Deponent Name (Your Name)")
            inputs["Father/Husband Name"] = st.text_input("Father's/Husband's Name")
            inputs["Age"] = st.number_input("Age", min_value=18)
            inputs["Address"] = st.text_input("Residential Address")
            inputs["Statement"] = st.text_area("What are you declaring?", height=100)

        elif document_type == "Simple Will":
            inputs["Testator Name"] = st.text_input("Testator Name")
            inputs["Beneficiaries"] = st.text_area("Beneficiaries & Distribution Details")

        else:
            inputs["Party Names"] = st.text_input("Party Names")
            inputs["Details"] = st.text_area("Enter Agreement Details")

        st.warning("⚠️ Disclaimer: This is an AI-generated draft. It is NOT a substitute for a lawyer. Review carefully.")
        
        generate_btn = st.form_submit_button("Draft Document", type="primary")

    # 3. Generation Logic
    if generate_btn:
        if list(inputs.values())[0]:
            with st.spinner(f"Drafting your {document_type} based on Indian Code..."):
                try:
                    details_text = "\n".join([f"{key}: {value}" for key, value in inputs.items()])
                    
                    # --- UPDATED PROMPT FOR HTML OUTPUT ---
                    prompt = f"""
                    You are an expert Indian Legal Drafter.
                    Task: Draft a legally sound '{document_type}' based on Indian Law.
                    
                    USER DETAILS:
                    {details_text}
                    
                    INSTRUCTIONS:
                    1. Output the document in **HTML Format** for PDF generation.
                    2. Use <b> tags for bolding Party Names, key terms, and headers.
                    3. Use <br> tags for line breaks. Use <br><br> for paragraph breaks.
                    4. Use <h3> tags for section headers (like "WHEREAS" or "NOW THIS DEED WITNESSETH").
                    5. Do NOT use Markdown (like ** or ##). Use only HTML.
                    6. Output ONLY the HTML code inside the <body> content. Do not include ```html``` blocks.
                    """
                    
                    response = llm_model.invoke(prompt)
                    # Clean up potential code blocks
                    draft_html = response.content.replace("```html", "").replace("```", "")
                    
                    # Show Preview (We render HTML as markdown for preview, it looks okay)
                    st.subheader("📄 Draft Preview")
                    st.markdown(draft_html, unsafe_allow_html=True)
                    
                    # Generate PDF
                    pdf_data = create_pdf_bytes(draft_html, document_type)
                    
                    st.download_button(
                        label="⬇️ Download Final PDF",
                        data=pdf_data,
                        file_name=f"{document_type.replace(' ', '_')}_Draft.pdf",
                        mime="application/pdf",
                        type="primary"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating document: {e}")
        else:
            st.error("Please fill in the required details.")