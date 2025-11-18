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
    
    # Clean the text to prevent encoding errors
    safe_text = doc_text.encode('latin-1', 'replace').decode('latin-1')
    
    pdf.multi_cell(0, 6, safe_text)
    
    # --- FIXED: Return bytes directly for fpdf2 compatibility ---
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
        
        # --- SPECIFIC FORM FOR RENTAL AGREEMENT ---
        if document_type == "Rental/Lease Agreement":
            col1, col2 = st.columns(2)
            inputs["Landlord Name"] = col1.text_input("Landlord (Owner) Name")
            inputs["Tenant Name"] = col2.text_input("Tenant Name")
            
            inputs["Property Address"] = st.text_input("Full Property Address")
            
            c1, c2, c3 = st.columns(3)
            inputs["Monthly Rent"] = c1.number_input("Monthly Rent (₹)", min_value=0, step=500)
            inputs["Security Deposit"] = c2.number_input("Security Deposit (₹)", min_value=0, step=1000)
            inputs["Lease Duration"] = c3.text_input("Duration (e.g., 11 Months)")
            
            inputs["Lease Start Date"] = st.date_input("Lease Start Date", datetime.date.today())

        # --- SPECIFIC FORM FOR NDA ---
        elif document_type == "Non-Disclosure Agreement (NDA)":
            col1, col2 = st.columns(2)
            inputs["Disclosing Party"] = col1.text_input("Disclosing Party Name")
            inputs["Receiving Party"] = col2.text_input("Receiving Party Name")
            
            inputs["Confidential Information Description"] = st.text_area("What information is confidential?", placeholder="e.g., Business plans, trade secrets, customer lists...")
            inputs["Duration of Confidentiality"] = st.text_input("Duration (e.g., 2 years, Indefinite)")
            inputs["Jurisdiction"] = st.text_input("Jurisdiction (City/State)", value="Bangalore, Karnataka")

        # --- SPECIFIC FORM FOR AFFIDAVIT ---
        elif document_type == "Affidavit/Self-Declaration":
            col1, col2 = st.columns(2)
            inputs["Deponent Name"] = col1.text_input("Deponent Name (Your Name)")
            inputs["Father/Husband Name"] = col2.text_input("Father's/Husband's Name")
            
            inputs["Age"] = st.number_input("Age", min_value=18, max_value=100)
            inputs["Address"] = st.text_input("Residential Address")
            
            inputs["Statement of Fact"] = st.text_area("What are you declaring?", placeholder="e.g., I declare that my name is spelled correctly as...")

        # --- SPECIFIC FORM FOR WILL ---
        elif document_type == "Simple Will":
            inputs["Testator Name"] = st.text_input("Testator Name (Person making the will)")
            inputs["Executor Name"] = st.text_input("Executor Name (Person managing the will)")
            inputs["Beneficiaries"] = st.text_area("Who gets what? (Beneficiaries)", placeholder="e.g., My wife receives the house. My son receives the car.")
            
        # --- GENERIC FORM FOR OTHERS ---
        else:
            inputs["Party A Name"] = st.text_input("First Party Name")
            inputs["Party B Name"] = st.text_input("Second Party Name")
            inputs["Key Terms & Details"] = st.text_area("Enter all other details, terms, and conditions:")

        # Common Disclaimer
        st.warning("⚠️ Disclaimer: This is an AI-generated draft. It is NOT a substitute for a lawyer. Review carefully.")
        
        generate_btn = st.form_submit_button("Draft Document", type="primary")

    # 3. Generation Logic
    if generate_btn:
        # Validate that at least the first field is filled
        if list(inputs.values())[0]:
            with st.spinner(f"Drafting your {document_type} based on Indian Code..."):
                try:
                    # Construct a structured string from the inputs
                    details_text = "\n".join([f"{key}: {value}" for key, value in inputs.items()])
                    
                    # The Prompt
                    prompt = f"""
                    You are an expert Indian Legal Drafter.
                    Task: Draft a legally sound '{document_type}' based on Indian Law (e.g., Indian Contract Act 1872, Transfer of Property Act, etc.).
                    
                    USE THESE SPECIFIC DETAILS:
                    {details_text}
                    
                    Instructions:
                    1. Use formal, legal language appropriate for India.
                    2. Include standard clauses (Jurisdiction, Dispute Resolution, Indemnity) relevant to this document type.
                    3. Ensure the layout is clean and professional.
                    4. Output ONLY the agreement text. No conversational filler.
                    """
                    
                    # Generate Text
                    response = llm_model.invoke(prompt)
                    draft_text = response.content
                    
                    # Show Preview
                    st.subheader("📄 Draft Preview")
                    st.text_area("Editable Text", value=draft_text, height=400)
                    
                    # Generate PDF
                    pdf_data = create_pdf_bytes(draft_text, document_type)
                    
                    # Download Button
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