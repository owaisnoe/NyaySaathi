import streamlit as st
from fpdf import FPDF
import datetime

def create_pdf_bytes(doc_text, doc_type):
    """Generates a PDF from text and returns the bytes."""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, f'Nyay-Saathi Draft: {doc_type}', 0, 1, 'C')
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, f'Generated on: {datetime.date.today().strftime("%d %B, %Y")}', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Clean the text to prevent encoding errors (basic FPDF supports Latin-1)
    # For a hackathon, this ensures emojis or Hindi chars don't crash the app
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 6, safe_text)
    return pdf.output(dest='S').encode('latin-1')

def show_document_generator(llm_model):
    """
    Renders the Document Generator UI.
    Args:
        llm_model: The ChatGoogleGenerativeAI object passed from app.py
    """
    st.header("📝 Generate Legal Agreements")
    st.write("Select a document type, fill in the details, and AI will draft a legal version compliant with Indian laws.")

    # 1. Document Selection
    document_type = st.selectbox(
        "Select Agreement Type:",
        (
            "Rental/Lease Agreement", 
            "Non-Disclosure Agreement (NDA)", 
            "Affidavit/Self-Declaration", 
            "Employment Offer Letter", 
            "Legal Notice (Demand)", 
            "Memorandum of Understanding (MOU)", 
            "Gift Deed", 
            "Power of Attorney (Special)", 
            "Simple Will"
        )
    )

    # 2. The Input Form
    with st.form("doc_gen_form"):
        st.info(f"**Instructions:** Provide specific details for the {document_type}.")
        
        user_inputs = st.text_area(
            "Enter Names, Addresses, Amounts, Dates, and Terms:",
            height=150,
            placeholder="Example: Landlord Name: Rahul Sharma, Tenant: Anita Roy, Address: Flat 402, Indiranagar, Bangalore. Rent: 20,000. Start Date: 1st April 2025."
        )
        
        # Disclaimer inside the form
        st.warning("⚠️ Disclaimer: This is an AI-generated draft. It is NOT a substitute for a lawyer. Review carefully.")
        
        generate_btn = st.form_submit_button("Draft Document", type="primary")

    # 3. Generation Logic
    if generate_btn and user_inputs:
        with st.spinner("Drafting your document based on Indian Code..."):
            try:
                # The Prompt
                prompt = f"""
                You are an expert Indian Legal Drafter.
                Task: Draft a legally sound '{document_type}' based on Indian Law (e.g., Indian Contract Act 1872, Transfer of Property Act, etc.).
                
                Context Provided by User:
                {user_inputs}
                
                Instructions:
                1. Use formal, legal language appropriate for India.
                2. Include standard clauses (Jurisdiction, Dispute Resolution, Indemnity).
                3. Fill in the user details. If details are missing, use [Bracketed Placeholders].
                4. Output ONLY the agreement text. No conversational filler.
                """
                
                # Generate Text
                response = llm_model.invoke(prompt)
                draft_text = response.content
                
                # Show Preview
                st.subheader("📄 Draft Preview")
                st.text_area("Editable Text", value=draft_text, height=300)
                
                # Generate PDF
                pdf_data = create_pdf_bytes(draft_text, document_type)
                
                # Download Button
                st.download_button(
                    label="⬇️ Download PDF",
                    data=pdf_data,
                    file_name=f"{document_type.replace(' ', '_')}_Draft.pdf",
                    mime="application/pdf"
                )
                
            except Exception as e:
                st.error(f"Error generating document: {e}")