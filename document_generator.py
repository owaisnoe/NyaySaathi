import streamlit as st
from fpdf import FPDF
import datetime

# --- 1. CONFIGURATION & DATA ---
st.set_page_config(page_title="Nyay-Saathi Premium Drafts", layout="wide", page_icon="⚖️")

def get_date():
    return datetime.date.today().strftime("%B %d, %Y")

DOC_CONFIG = {
    "Memorandum of Understanding": {
        "icon": "🤝",
        "filename": "MOU_Agreement",
        "sections": {
            "Parties": [
                {"id": "party_a", "label": "First Party Name", "placeholder": "e.g., Alpha Tech Solutions"},
                {"id": "party_b", "label": "Second Party Name", "placeholder": "e.g., Beta Innovations"},
                {"id": "place", "label": "Place of Execution", "placeholder": "e.g., New Delhi"},
            ],
            "Core Terms": [
                {"id": "purpose", "label": "Purpose", "type": "textarea"},
                {"id": "duration", "label": "Duration (Months)", "type": "number", "placeholder": "12"},
            ]
        },
        "template": """MEMORANDUM OF UNDERSTANDING

This MEMORANDUM OF UNDERSTANDING (the "MOU") is entered into on <b>{date}</b> at <b>{place}</b>.

<b>BY AND BETWEEN:</b>

<b>1. {party_a}</b> (Hereinafter "Party A")
   AND
<b>2. {party_b}</b> (Hereinafter "Party B")

<b>RECITALS:</b>

A. The Parties share a common interest in collaborating for mutual benefit.
B. The Parties wish to set out the framework for their cooperation.

<b>NOW, THEREFORE, IT IS AGREED:</b>

<b>ARTICLE 1: OBJECTIVE</b>
The primary objective of this MOU is:
{purpose}

<b>ARTICLE 2: TERM</b>
This MOU shall be effective for a period of <b>{duration} months</b> from the date of signing.

<b>ARTICLE 3: CONFIDENTIALITY</b>
Each Party agrees to keep all technical and commercial information exchanged strictly confidential.

<b>ARTICLE 4: GOVERNING LAW</b>
This MOU shall be governed by the laws of India.

IN WITNESS WHEREOF, the Parties have executed this MOU.

_________________________              _________________________
<b>{party_a}</b>                          <b>{party_b}</b>
(Authorized Signatory)                 (Authorized Signatory)"""
    },
    "Rental Agreement": {
        "icon": "🏠",
        "filename": "Rental_Agreement",
        "sections": {
            "Parties": [
                {"id": "landlord", "label": "Landlord Name", "placeholder": "Owner Name"},
                {"id": "tenant", "label": "Tenant Name", "placeholder": "Renter Name"},
                {"id": "address", "label": "Property Address", "type": "textarea"},
            ],
            "Money": [
                {"id": "rent", "label": "Rent (₹)", "type": "number"},
                {"id": "deposit", "label": "Deposit (₹)", "type": "number"},
            ]
        },
        "template": """RESIDENTIAL RENTAL AGREEMENT

This AGREEMENT is made on <b>{date}</b> BETWEEN:

<b>{landlord}</b> ("LESSOR")
AND
<b>{tenant}</b> ("LESSEE")

<b>WHEREAS</b> the Lessor is the owner of the property:
{address}

<b>TERMS AND CONDITIONS:</b>

1. <b>GRANT:</b> The Lessor grants the Lessee the right to occupy the premises.
2. <b>RENT:</b> Monthly rent is <b>Rs. {rent}/-</b>.
3. <b>DEPOSIT:</b> Security deposit is <b>Rs. {deposit}/-</b>.
4. <b>MAINTENANCE:</b> Lessee shall maintain the premises in good condition.

IN WITNESS WHEREOF, the parties have signed below.

__________________          __________________
<b>LESSOR</b>                      <b>LESSEE</b>"""
    }
}

# --- 2. "OP" PDF ENGINE (Manually Drawn Design) ---
class PremiumPDF(FPDF):
    def header(self):
        # 1. The "Legal Border" (Double Line)
        self.set_draw_color(0, 0, 0) # Black
        self.set_line_width(0.5)
        self.rect(5, 5, 200, 287) # Outer Box
        self.set_line_width(0.2)
        self.rect(7, 7, 196, 283) # Inner Box

        # 2. The "Stamp" (Simulated)
        self.set_xy(165, 10)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(200, 0, 0) # Dark Red
        self.cell(30, 8, "E-STAMP VERIFIED", 1, 0, 'C')
        
        # 3. Watermark (Diagonal)
        self.set_font('Arial', 'B', 60)
        self.set_text_color(245, 245, 245) # Very faint grey
        with self.rotation(45, 105, 148):
            self.text(60, 180, "NYAY-SAATHI")

    def footer(self):
        self.set_y(-20)
        self.set_font('Times', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Drafted via Nyay-Saathi Legal AI • Page {self.page_no()}', 0, 0, 'C')

def generate_premium_pdf(raw_text):
    pdf = PremiumPDF()
    pdf.add_page()
    
    # Parse text for formatting
    lines = raw_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(4)
            continue
            
        # Title Handling (Centered, Bold, Underlined look)
        if line.isupper() and len(line) < 60 and "AGREEMENT" in line:
            pdf.set_font("Times", 'B', 16)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 10, line, 0, 1, 'C')
            pdf.ln(5)
        
        # Clause Headers (e.g., "ARTICLE 1:")
        elif "<b>" in line and ":" in line:
            clean = line.replace("<b>", "").replace("</b>", "")
            pdf.set_font("Times", 'B', 11)
            pdf.cell(0, 8, clean, 0, 1, 'L')
            
        # Signatures
        elif "___" in line:
            pdf.ln(15)
            pdf.set_font("Times", 'B', 11)
            pdf.cell(0, 8, line, 0, 1, 'C')
            
        # Normal Text
        else:
            clean = line.replace("<b>", "").replace("</b>", "")
            pdf.set_font("Times", '', 11)
            pdf.multi_cell(0, 6, clean)
            
    return bytes(pdf.output())

# --- 3. "OP" CSS (The Bond Paper Look) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora:wght@400;600&display=swap');

    .stApp {
        background-color: #f0f2f6;
        background-image: radial-gradient(#cfd9df 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* The "Bond Paper" Container */
    .bond-paper {
        background-color: #fffaf0; /* Cream/Bond color */
        padding: 60px 80px;
        width: 100%;
        min-height: 900px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
        border: 1px solid #d4c5b0;
        font-family: 'Lora', serif; /* High-end serif font */
        font-size: 16px;
        color: #2c3e50;
        line-height: 1.8;
        position: relative;
        margin-bottom: 30px;
    }

    /* The "Legal Border" inside HTML */
    .bond-paper::before {
        content: "";
        position: absolute;
        top: 15px; left: 15px; right: 15px; bottom: 15px;
        border: 2px solid #333;
        pointer-events: none;
    }
    .bond-paper::after {
        content: "";
        position: absolute;
        top: 18px; left: 18px; right: 18px; bottom: 18px;
        border: 1px solid #333;
        pointer-events: none;
    }

    /* Typography */
    .bond-paper h1 {
        font-family: 'Playfair Display', serif;
        text-align: center;
        text-transform: uppercase;
        font-size: 24px;
        text-decoration: underline;
        text-underline-offset: 5px;
        margin-bottom: 40px;
        color: #000;
    }

    .highlight-field {
        background-color: rgba(0, 255, 209, 0.2);
        border-bottom: 2px solid #00aa90;
        padding: 0 5px;
        font-weight: 600;
        border-radius: 3px;
    }

    /* Sidebar Polish */
    [data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #e0e0e0;
    }
    .stTextInput input, .stTextArea textarea, .stNumberInput input {
        background-color: #f8f9fa;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- 4. APP LOGIC ---

with st.sidebar:
    st.title("⚖️ Nyay-Saathi Drafts")
    st.caption("Premium AI-Assisted Legal Drafting")
    st.markdown("---")
    
    selected_doc = st.selectbox("Choose Document", list(DOC_CONFIG.keys()))
    config = DOC_CONFIG[selected_doc]
    
    user_data = {}
    with st.form("input_form"):
        for section, fields in config["sections"].items():
            st.subheader(section)
            for field in fields:
                ftype = field.get("type", "text")
                if ftype == "textarea":
                    user_data[field["id"]] = st.text_area(field["label"], height=80)
                elif ftype == "number":
                    user_data[field["id"]] = st.number_input(field["label"], min_value=0)
                else:
                    user_data[field["id"]] = st.text_input(field["label"], placeholder=field.get("placeholder"))
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.form_submit_button("Update Draft", type="primary", use_container_width=True)

# --- MAIN PREVIEW ---
col1, col2 = st.columns([1, 4]) # Centering trick
with col2:
    # Prepare Data
    user_data["date"] = get_date()
    display_data = {}
    
    for key, value in user_data.items():
        val = str(value) if value else f"[{key.upper()}]"
        # This applies the 'highlight-field' CSS class
        display_data[key] = f'<span class="highlight-field">{val}</span>'
    
    # Render HTML
    # We use some basic string manipulation to convert the template into HTML
    html_body = config["template"].format(**display_data)
    # Convert newlines to <br> and bold tags for HTML
    html_body = html_body.replace("\n", "<br>").replace("<b>", "<strong>").replace("</b>", "</strong>")
    
    # Inject into the "Bond Paper" div
    st.markdown(f"""
    <div class="bond-paper">
        {html_body}
    </div>
    """, unsafe_allow_html=True)

    # --- DOWNLOAD CARD ---
    clean_data = {k: str(v) if v else "___________" for k, v in user_data.items()}
    clean_text = config["template"].format(**clean_data)
    pdf_bytes = generate_premium_pdf(clean_text)
    
    st.download_button(
        label="🔒 Download Signed PDF (Watermarked)",
        data=pdf_bytes,
        file_name=f"{config['filename']}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )