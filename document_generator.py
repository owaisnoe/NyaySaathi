import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. CONFIGURATION & DATA ---
st.set_page_config(page_title="Nyay-Saathi Drafts", layout="wide", page_icon="⚖️")

DOC_CONFIG = {
    "Rental Agreement": {
        "icon": "🏠",
        "filename": "Rental_Agreement_Draft",
        "sections": {
            "Party Details": [
                {"id": "landlord_name", "label": "Landlord Name (Lessor)", "placeholder": "e.g., Amit Sharma"},
                {"id": "landlord_addr", "label": "Landlord's Residence Address", "type": "textarea", "placeholder": "Full permanent address of landlord..."},
                {"id": "tenant_name", "label": "Tenant Name (Lessee)", "placeholder": "e.g., Rahul Verma"},
                {"id": "tenant_addr", "label": "Tenant's Permanent Address", "type": "textarea", "placeholder": "Permanent address of tenant (not the rental property)..."},
            ],
            "Property Details": [
                {"id": "property_address", "label": "Rental Property Address", "type": "textarea", "placeholder": "Complete address of the property being rented..."},
                {"id": "city", "label": "City of Execution", "placeholder": "e.g., Bangalore"},
            ],
            "Financial Terms": [
                {"id": "rent_amount", "label": "Monthly Rent (₹)", "type": "number"},
                {"id": "deposit_amount", "label": "Security Deposit (₹)", "type": "number"},
                {"id": "payment_day", "label": "Rent Payment Day (e.g., 5th)", "placeholder": "5th"},
                {"id": "notice_period", "label": "Notice Period (Months)", "type": "number", "placeholder": "1"},
            ],
            "Lease Terms": [
                {"id": "lease_duration", "label": "Duration (Months)", "type": "number", "placeholder": "11"},
                {"id": "start_date", "label": "Lease Start Date", "type": "date"},
                {"id": "purpose", "label": "Purpose", "placeholder": "Residential Use Only"},
            ]
        },
        # EXPANDED LEGAL TEMPLATE
        "template": """<b>RESIDENTIAL RENTAL AGREEMENT</b>

THIS RENTAL AGREEMENT is made and executed at <b>{city}</b> on this <b>{date}</b>, BY AND BETWEEN:

<b>1. {landlord_name}</b>, residing at {landlord_addr} (hereinafter referred to as the "<b>LESSOR</b>", which expression shall include his/her heirs, successors, and assigns) of the ONE PART.

AND

<b>2. {tenant_name}</b>, having permanent address at {tenant_addr} (hereinafter referred to as the "<b>LESSEE</b>", which expression shall include his/her heirs, successors, and assigns) of the OTHER PART.

<b>WHEREAS</b> the Lessor is the absolute owner of the property situated at:
{property_address}
(hereinafter referred to as the "<b>SCHEDULED PREMISES</b>").

AND WHEREAS the Lessee has requested the Lessor to grant the lease of the said Scheduled Premises for <b>{purpose}</b>, and the Lessor has agreed to the same on the following terms and conditions:

<b>NOW THIS AGREEMENT WITNESSETH AS FOLLOWS:</b>

<b>1. RENT:</b> The Lessee shall pay a monthly rent of <b>Rs. {rent_amount}/-</b> on or before the <b>{payment_day} day</b> of every English calendar month.

<b>2. SECURITY DEPOSIT:</b> The Lessee has paid an interest-free refundable security deposit of <b>Rs. {deposit_amount}/-</b> to the Lessor. This amount shall be refunded at the time of vacating the premises, subject to deductions for damages, unpaid rent, or electricity/water dues.

<b>3. DURATION:</b> This lease shall be in force for a period of <b>{lease_duration} months</b>, commencing from <b>{start_date}</b>.

<b>4. TERMINATION & NOTICE:</b> Either party may terminate this agreement by giving <b>{notice_period} month(s)</b> prior notice in writing. If the Lessee vacates without notice, the Lessor is entitled to deduct the rent for the notice period from the security deposit.

<b>5. MAINTENANCE & REPAIRS:</b>
   a) The Lessee shall keep the premises in good tenantable condition.
   b) Minor repairs such as fusing of bulbs, leaking taps, etc., shall be borne by the Lessee.
   c) Major structural repairs shall be the responsibility of the Lessor.

<b>6. UTILITIES:</b> The Lessee shall punctually pay the electricity and water charges as per the meter reading/bills to the concerned authorities.

<b>7. SUB-LETTING:</b> The Lessee shall NOT sub-let, assign, or part with the possession of the Scheduled Premises or any part thereof to any third party.

<b>8. INSPECTION:</b> The Lessor or their authorized agent shall have the right to enter the premises at a reasonable time to inspect the condition of the property.

<b>9. ILLEGAL ACTIVITIES:</b> The Lessee shall not use the premises for any illegal or immoral purposes or any purpose other than residential use.

IN WITNESS WHEREOF, the Lessor and the Lessee have set their hands to this Agreement on the day, month, and year first above written.

__________________          __________________
<b>LESSOR</b>                      <b>LESSEE</b>

<b>Witnesses:</b>
1. _____________________
2. _____________________"""
    },
    "NDA": {
        "icon": "🔒",
        "filename": "Non_Disclosure_Agreement",
        "sections": {
            "Parties": [
                {"id": "disclosing_party", "label": "Disclosing Party Name", "placeholder": "Company/Individual sharing info"},
                {"id": "receiving_party", "label": "Receiving Party Name", "placeholder": "Company/Individual receiving info"},
            ],
            "Scope": [
                {"id": "confidential_info", "label": "Description of Confidential Info", "type": "textarea", "placeholder": "e.g., Trade secrets, client lists, software code..."},
                {"id": "purpose", "label": "Purpose of Disclosure", "placeholder": "e.g., Evaluating a potential partnership"},
                {"id": "duration", "label": "Duration (Years)", "type": "number", "placeholder": "2"},
                {"id": "jurisdiction", "label": "Jurisdiction (City/State)", "placeholder": "Delhi"},
            ]
        },
        "template": """<b>NON-DISCLOSURE AGREEMENT (NDA)</b>

This Non-Disclosure Agreement ("Agreement") is entered into on <b>{date}</b> BY AND BETWEEN:

<b>1. {disclosing_party}</b> (hereinafter referred to as the "<b>DISCLOSING PARTY</b>")
AND
<b>2. {receiving_party}</b> (hereinafter referred to as the "<b>RECEIVING PARTY</b>")

(Collectively referred to as the "Parties").

<b>WHEREAS</b>, in connection with <b>{purpose}</b> (the "Purpose"), the Disclosing Party may disclose certain confidential and proprietary information to the Receiving Party.

<b>NOW, THEREFORE, the Parties agree as follows:</b>

<b>1. DEFINITION OF CONFIDENTIAL INFORMATION</b>
"Confidential Information" means all non-public information disclosed by the Disclosing Party, whether written, oral, or digital, including but not limited to:
{confidential_info}

<b>2. OBLIGATIONS OF THE RECEIVING PARTY</b>
The Receiving Party agrees to:
   a) Hold the Confidential Information in strict confidence and take reasonable precautions to protect it.
   b) Not disclose such information to any third party without prior written consent from the Disclosing Party.
   c) Use the information <b>solely</b> for the Purpose stated above.

<b>3. EXCLUSIONS</b>
Confidential Information does not include information that:
   a) Is or becomes public knowledge through no breach of this Agreement.
   b) Is already known to the Receiving Party at the time of disclosure.
   c) Is independently developed by the Receiving Party without use of the Confidential Information.

<b>4. TERM</b>
The obligations of confidentiality under this Agreement shall survive for a period of <b>{duration} years</b> from the date of disclosure.

<b>5. RETURN OF MATERIALS</b>
Upon termination of discussions or written request, the Receiving Party shall immediately return or destroy all copies of the Confidential Information.

<b>6. GOVERNING LAW</b>
This Agreement shall be governed by the laws of India, and the courts in <b>{jurisdiction}</b> shall have exclusive jurisdiction over any disputes.

IN WITNESS WHEREOF, the parties have executed this Agreement.

__________________          __________________
<b>Disclosing Party</b>            <b>Receiving Party</b>"""
    }
}

# --- 2. PDF GENERATOR ---
class PDF(FPDF):
    def header(self):
        self.set_font('Times', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'Drafted via Nyay-Saathi', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(content):
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_font("Times", size=12)
    
    # Basic parsing to remove HTML tags for the PDF text
    clean_text = content.replace("<b>", "").replace("</b>", "")
    
    # Using multi_cell for text wrapping
    pdf.multi_cell(0, 6, clean_text)
    return bytes(pdf.output())

# --- 3. CSS STYLING ---
st.markdown("""
<style>
    /* General App Styling */
    .stApp { background-color: #f8f9fa; }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #dee2e6;
    }
    
    /* Preview Paper Styling */
    .a4-paper {
        background-color: white;
        width: 100%;
        min-height: 800px;
        padding: 50px 60px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
        font-family: 'Times New Roman', Times, serif;
        font-size: 15px;
        line-height: 1.7;
        color: #212529;
        white-space: pre-wrap;
    }

    /* Highlight Styling */
    .highlight {
        background-color: #e8f0fe;
        color: #1a73e8;
        font-weight: 600;
        padding: 0 2px;
        border-bottom: 1px dashed #1a73e8;
    }
    
    /* Section Header in Sidebar */
    .section-label {
        text-transform: uppercase;
        font-size: 0.75rem;
        font-weight: 700;
        color: #6c757d;
        margin-top: 20px;
        margin-bottom: 5px;
        letter-spacing: 0.5px;
    }

    /* Download Card Styling */
    .download-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .file-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .file-icon {
        font-size: 2rem;
    }
    .file-details h4 {
        margin: 0;
        font-size: 1rem;
        color: #333;
    }
    .file-details p {
        margin: 0;
        font-size: 0.8rem;
        color: #777;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. MAIN APP LOGIC ---

# --- SIDEBAR: INPUTS ---
with st.sidebar:
    st.title("📝 Legal Drafter")
    selected_doc = st.selectbox("Document Type", list(DOC_CONFIG.keys()))
    config = DOC_CONFIG[selected_doc]
    
    st.markdown("---")
    
    user_data = {}
    
    # Dynamic Form Generation
    with st.form("drafting_form"):
        for section, fields in config["sections"].items():
            st.markdown(f"<div class='section-label'>{section}</div>", unsafe_allow_html=True)
            
            for field in fields:
                ftype = field.get("type", "text")
                fid = field["id"]
                flabel = field["label"]
                fplace = field.get("placeholder", "")
                
                if ftype == "textarea":
                    user_data[fid] = st.text_area(flabel, placeholder=fplace, height=80)
                elif ftype == "date":
                    user_data[fid] = st.date_input(flabel, value=datetime.date.today())
                elif ftype == "number":
                    user_data[fid] = st.number_input(flabel, min_value=0, step=1)
                else:
                    user_data[fid] = st.text_input(flabel, placeholder=fplace)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Update Preview", type="primary", use_container_width=True)

# --- MAIN AREA: PREVIEW ---
col1, col2 = st.columns([4, 1])
with col1:
    st.subheader(f"{config['icon']} {selected_doc}")
with col2:
    st.markdown(f"<div style='text-align:right; color:gray; padding-top:10px;'>{datetime.date.today().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)

# 1. Prepare Data for Display
formatted_data = {}
user_data["date"] = datetime.date.today().strftime("%B %d, %Y")

for key, value in user_data.items():
    display_value = str(value) if value else f"[{key.replace('_', ' ').upper()}]"
    formatted_data[key] = f'<span class="highlight">{display_value}</span>'

# 2. Render HTML Preview (Paper Look)
html_content = config["template"].format(**formatted_data)
st.markdown(f'<div class="a4-paper">{html_content}</div>', unsafe_allow_html=True)

# 3. Download Section (Professional Card UI)
st.markdown("---")
st.subheader("📥 Export Document")

# Prepare Clean Data for PDF
clean_data = {k: str(v) if v else "____________" for k, v in user_data.items()}
clean_text = config["template"].replace("<b>", "").replace("</b>", "").format(**clean_data)
pdf_bytes = generate_pdf(clean_text)
file_name = f"{config['filename']}.pdf"

# The "Download Card" Layout
download_col1, download_col2, download_col3 = st.columns([0.1, 3, 1])

with download_col1:
    st.markdown("<div style='font-size: 2.5rem; padding-top:10px;'>📄</div>", unsafe_allow_html=True)

with download_col2:
    st.markdown(f"""
    <div style="padding-top: 10px;">
        <h4 style="margin:0; color:#333;">{selected_doc} (Ready to Print)</h4>
        <p style="margin:0; color:#777; font-size:0.9rem;">PDF Format • A4 Size • Standard Legal Font</p>
    </div>
    """, unsafe_allow_html=True)

with download_col3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=file_name,
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )