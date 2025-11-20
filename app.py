import streamlit as st
import google.generativeai as genai
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from operator import itemgetter
from PIL import Image 
from langchain_core.messages import HumanMessage 
import base64
import json
import io
from gtts import gTTS 
import random # Added for random lawyer selection

# --- IMPORT DOCUMENT GENERATOR ---
from document_generator import show_document_generator 

# --- CONFIGURATION & PAGE SETUP ---
st.set_page_config(
    page_title="Nyay-Saathi", 
    page_icon="🤝", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
:root {
    --primary-color: #00FFD1;
    --background-color: #08070C;
    --secondary-background-color: #1B1C2A;
    --text-color: #FAFAFA;
}
body { font-family: 'sans serif'; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stButton > button {
    border: 2px solid var(--primary-color); background: transparent; color: var(--primary-color);
    padding: 12px 24px; border-radius: 8px; font-weight: bold; transition: all 0.3s ease-in-out;
}
.stButton > button:hover {
    background: var(--primary-color); color: var(--background-color); box-shadow: 0 0 15px var(--primary-color);
}
.stTextArea textarea {
    background-color: var(--secondary-background-color); color: var(--text-color);
    border: 1px solid var(--primary-color); border-radius: 8px;
}
div[data-testid="chat-message-container"] {
    background-color: var(--secondary-background-color);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent; color: var(--text-color); padding: 10px; transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover { background: var(--secondary-background-color); }
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: var(--secondary-background-color); color: var(--primary-color); border-bottom: 3px solid var(--primary-color);
}
/* Lawyer Card CSS */
.lawyer-card {
    background-color: #262730;
    border: 1px solid #00FFD1;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# --- API KEY CONFIGURATION ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"Error configuring: {e}. Please check your API key in Streamlit Secrets.")
    st.stop()

DB_FAISS_PATH = "vectorstores/db_faiss"
MODEL_NAME = "gemini-2.5-flash" 

# --- MOCK LAWYER DATABASE (For Tab 5) ---
LAWYER_DIRECTORY = [
    {"name": "Adv. Priya Sharma", "location": "Delhi/NCR", "specialization": "Family Law", "experience": "12 Years", "languages": "Hindi, English", "phone": "+91-98765XXXXX"},
    {"name": "Adv. Rajesh Kumar", "location": "Mumbai", "specialization": "Property Dispute", "experience": "15 Years", "languages": "Marathi, Hindi, English", "phone": "+91-91234XXXXX"},
    {"name": "Adv. Sneha Reddy", "location": "Bangalore", "specialization": "Corporate Law", "experience": "8 Years", "languages": "Kannada, Telugu, English", "phone": "+91-99887XXXXX"},
    {"name": "Adv. Amit Verma", "location": "Lucknow", "specialization": "Criminal Law", "experience": "20 Years", "languages": "Hindi, Urdu", "phone": "+91-98712XXXXX"},
    {"name": "Adv. Kavita Iyer", "location": "Chennai", "specialization": "Consumer Rights", "experience": "10 Years", "languages": "Tamil, English", "phone": "+91-94455XXXXX"},
    {"name": "Adv. Vikram Singh", "location": "Chandigarh", "specialization": "Cyber Crime", "experience": "7 Years", "languages": "Punjabi, Hindi, English", "phone": "+91-98140XXXXX"}
]


# --- RAG PROMPT TEMPLATE ---
rag_prompt_template = """
You are 'Nyay-Saathi,' a kind legal friend.
A common Indian citizen is asking for help.
You have two sources of information. Prioritize the MOST relevant one.
1. CONTEXT_FROM_GUIDES: (General guides from a database)
{context}

2. DOCUMENT_CONTEXT: (Specific text from a document the user uploaded)
{document_context}

Answer the user's 'new question' based on the most relevant context.
If the 'new question' is a follow-up, use the 'chat history' to understand it.
Do not use any legal jargon.
Give a simple, step-by-step action plan in the following language: {language}.
If no context is relevant, just say "I'm sorry, I don't have enough information on that. Please contact NALSA."

CHAT HISTORY:
{chat_history}

NEW QUESTION:
{question}

Your Simple, Step-by-Step Action Plan (in {language}):
"""

# --- LOAD THE MODEL & VECTOR STORE ---
@st.cache_resource
def get_models_and_db():
    try:
        embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                           model_kwargs={'device': 'cpu'})
        db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.5)
        
        retriever = db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 3,
                "score_threshold": 0.3 
            }
        )
        
        return retriever, llm
    except Exception as e:
        st.error(f"Error loading models or vector store: {e}")
        st.error("Did you run 'ingest.py' and push the 'vectorstores' folder to GitHub?")
        st.stop()

retriever, llm = get_models_and_db()

@st.cache_resource
def get_genai_model():
    return genai.GenerativeModel(MODEL_NAME)

# --- HELPER FUNCTION: Text to Speech ---
def text_to_speech(text, language):
    """Converts text to audio bytes using gTTS."""
    try:
        lang_code_map = {
            "Simple English": "en",
            "Hindi (in Roman script)": "hi", 
            "Kannada": "kn",
            "Tamil": "ta",
            "Telugu": "te",
            "Marathi": "mr"
        }
        lang_code = lang_code_map.get(language, "en")
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        return fp
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# --- THE RAG CHAIN ---
rag_prompt = PromptTemplate.from_template(rag_prompt_template)

rag_chain_with_sources = RunnableParallel(
    {
        "context": itemgetter("question") | retriever,
        "question": itemgetter("question"),
        "language": itemgetter("language"),
        "chat_history": itemgetter("chat_history"),
        "document_context": itemgetter("document_context")
    }
) | {
    "answer": (
        {
            "context": (lambda x: format_docs(x["context"])),
            "question": itemgetter("question"),
            "language": itemgetter("language"),
            "chat_history": itemgetter("chat_history"),
            "document_context": itemgetter("document_context")
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    ),
    "sources": itemgetter("context")
}

# --- SESSION STATE INITIALIZATION ---
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_context" not in st.session_state:
    st.session_state.document_context = "No document uploaded."
if "uploaded_file_bytes" not in st.session_state:
    st.session_state.uploaded_file_bytes = None
if "uploaded_file_type" not in st.session_state:
    st.session_state.uploaded_file_type = None
if "samjhao_explanation" not in st.session_state:
    st.session_state.samjhao_explanation = None
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0
# Initialize AI Brief
if "case_brief" not in st.session_state:
    st.session_state.case_brief = None
if "recommended_lawyer_type" not in st.session_state:
    st.session_state.recommended_lawyer_type = "General"


# --- "START NEW SESSION" BUTTON ---
def clear_session():
    st.session_state.messages = []
    st.session_state.document_context = "No document uploaded."
    st.session_state.uploaded_file_bytes = None
    st.session_state.uploaded_file_type = None
    st.session_state.samjhao_explanation = None
    st.session_state.case_brief = None # Clear brief
    st.session_state.file_uploader_key += 1 


# --- THE APP UI ---

# --- LANDING PAGE ---
if not st.session_state.app_started:
    st.title("Welcome to 🤝 Nyay-Saathi")
    st.subheader("Your AI legal friend, built for India.")
    st.markdown("This tool helps you understand complex legal documents and get clear, simple action plans.")
    st.markdown("---")
    
    if st.button("Click here to start", type="primary"):
        st.session_state.app_started = True
        st.rerun()

# --- MAIN APP ---
else:
    st.title("🤝 Nyay-Saathi (Justice Companion)")
    st.markdown("Your legal friend, in your pocket. Built for India.")

    col1, col2 = st.columns([3, 1])
    with col1:
        language = st.selectbox(
            "Choose your language:",
            ("Simple English", "Hindi (in Roman script)", "Kannada", "Tamil", "Telugu", "Marathi")
        )
    with col2:
        st.write("") 
        st.write("")
        st.button("Start New Session ♻️", on_click=clear_session, type="primary")


    st.divider()

    # --- THE TAB-BASED LAYOUT ---
    # Updated tabs list
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "**Ask** (Explain)", 
        "**What to do** (Plan)", 
        "**Draft Documents** (Create)", 
        "**Voice Mode** (Talk)",
        "**Find Lawyer** (Connect)"
    ])

    # --- TAB 1: ASK (EXPLAIN) ---
    with tab1:
        st.header("Upload a Legal Document to Explain")
        st.write("Take a photo (or upload a PDF) of your legal notice or agreement.")
        
        uploaded_file = st.file_uploader(
            "Choose a file...", 
            type=["jpg", "jpeg", "png", "pdf"], 
            key=st.session_state.file_uploader_key 
        )
        
        if uploaded_file is not None:
            new_file_bytes = uploaded_file.getvalue()
            if new_file_bytes != st.session_state.uploaded_file_bytes:
                st.session_state.uploaded_file_bytes = new_file_bytes
                st.session_state.uploaded_file_type = uploaded_file.type
                st.session_state.samjhao_explanation = None 
                st.session_state.document_context = "No document uploaded." 
        
        if st.session_state.uploaded_file_bytes is not None:
            file_bytes = st.session_state.uploaded_file_bytes
            file_type = st.session_state.uploaded_file_type
            
            if "image" in file_type:
                image = Image.open(io.BytesIO(file_bytes)) 
                st.image(image, caption="Your Uploaded Document", use_column_width=True)
            elif "pdf" in file_type:
                st.info("PDF file uploaded. Click 'Ask!' to explain.")
            
            if st.button("Explain!", type="primary", key="samjhao_button"):
                
                spinner_text = "Your friend is reading and explaining..."
                if "image" in file_type:
                    spinner_text = "Reading your image... (this can take 15-30s)"

                with st.spinner(spinner_text):
                    try:
                        model = get_genai_model()

                        prompt_text_multi = f"""
                        You are an AI assistant. The user has uploaded a document (MIME type: {file_type}).
                        Perform two tasks:
                        1. Extract all raw text from the document.
                        2. Explain the document in simple, everyday {language}.

                        Respond with ONLY a JSON object in this format:
                        {{
                          "raw_text": "The raw extracted text...",
                          "explanation": "Your simple {language} explanation..."
                        }}
                        """

                        data_part = {'mime_type': file_type, 'data': file_bytes}
                        response = model.generate_content([prompt_text_multi, data_part])
                        clean_response_text = response.text.strip().replace("```json", "").replace("```", "")

                        try:
                            response_json = json.loads(clean_response_text)
                            st.session_state.samjhao_explanation = response_json.get("explanation", "Unable to extract explanation.")
                            st.session_state.document_context = response_json.get("raw_text", "Unable to extract text.")
                        except json.JSONDecodeError:
                            st.error("The AI response was not in the expected format. Please try again.")
                            st.session_state.samjhao_explanation = None
                            st.session_state.document_context = "No document uploaded."

                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.warning("Please try uploading the document again.")

        if st.session_state.samjhao_explanation:
            st.subheader(f"Here's what it means in {language}:")
            st.markdown(st.session_state.samjhao_explanation)
            
            st.markdown("---")
            st.write("🔊 **Listen to this explanation:**")
            audio_bytes = text_to_speech(st.session_state.samjhao_explanation, language)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
        
        if st.session_state.document_context != "No document uploaded." and st.session_state.samjhao_explanation:
            st.success("Context Saved! You can now ask questions about this document in the 'What to do' tab.")


    # --- TAB 2: WHAT TO DO (ASK) ---
    with tab2:
        st.header("Ask for a simple action plan")
        
        col1, col2 = st.columns([3,1])
        with col1:
             st.write("Scared? Confused? Ask a question and get a simple 3-step plan **based on real guides.**")
        with col2:
            if st.button("Clear Chat ♻️"):
                st.session_state.messages = []
                st.rerun()

        if st.session_state.document_context != "No document uploaded.":
            with st.container():
                st.info(f"**Context Loaded:** I have your uploaded document in memory. Feel free to ask questions about it!")

        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                guides_sources = message.get("sources_from_guides")
                doc_context_used = message.get("source_from_document")

                if (guides_sources and len(guides_sources) > 0) or doc_context_used:
                    st.subheader("Sources I used:")
                    
                    if doc_context_used:
                        st.warning(f"**From Your Uploaded Document:**\n\n...{st.session_state.document_context[:500]}...")
                    
                    if guides_sources:
                        for doc in guides_sources:
                            st.info(f"**From {doc.metadata.get('source', 'Unknown Guide')}:**\n\n...{doc.page_content}...")
                
                if message["role"] == "assistant":
                    feedback_key = f"feedback_{i}"
                    c1, c2, _ = st.columns([1, 1, 5])
                    with c1:
                        if st.button("👍", key=f"{feedback_key}_up"):
                            st.toast("Thanks for your feedback!")
                    with c2:
                        if st.button("👎", key=f"{feedback_key}_down"):
                            st.toast("Thanks for your feedback!")

        if prompt := st.chat_input(f"Ask your follow-up question in {language}..."):

            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.spinner("Your friend is checking the guides..."):
                try:
                    chat_history_str = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-5:-1]])
                    current_doc_context = st.session_state.document_context

                    invoke_payload = {
                        "question": prompt,
                        "language": language,
                        "chat_history": chat_history_str,
                        "document_context": current_doc_context
                    }

                    response_dict = rag_chain_with_sources.invoke(invoke_payload)
                    response = response_dict["answer"]
                    docs = response_dict["sources"]

                    used_document = False
                    if not docs and current_doc_context != "No document uploaded.":
                        audit_model = get_genai_model()
                        audit_prompt = f"""
                        You are an auditor.
                        Question: "{prompt}"
                        Answer: "{response}"
                        Context: "{current_doc_context[:2000]}" 
                        
                        Did the "Answer" come primarily from the "Context"?
                        Respond with ONLY the word 'YES' or 'NO'.
                        """
                        try:
                            audit_response = audit_model.generate_content(audit_prompt)
                            if "YES" in audit_response.text.upper():
                                used_document = True
                        except:
                            pass 

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "sources_from_guides": docs,
                        "source_from_document": used_document
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"An error occurred during RAG processing: {e}")
                    st.session_state.messages.pop() 

    # --- TAB 3: DOCUMENT GENERATOR ---
    with tab3:
        show_document_generator()

    # --- TAB 4: VOICE MODE ---
    with tab4:
        st.header("Voice Chat (Web Compatible)")
        st.write("Record a voice note, and Nyay-Saathi will reply with audio!")
        
        audio_value = st.audio_input("Record your legal question")

        if audio_value:
            st.audio(audio_value) 
            
            if st.button("Get Answer"):
                with st.spinner("Listening and thinking..."):
                    try:
                        model = get_genai_model()
                        audio_bytes = audio_value.getvalue()
                        prompt_text = f"Listen to this user audio. You are 'Nyay-Saathi', a helpful Indian legal assistant. Answer the user's question in simple {language}. Keep the answer short, helpful, and friendly."
                        
                        response = model.generate_content([prompt_text, {"mime_type": "audio/wav", "data": audio_bytes}])
                        response_text = response.text
                        
                        st.success("Nyay-Saathi says:")
                        st.markdown(response_text)
                        
                        st.write("🔊 **Listen to the answer:**")
                        tts_audio = text_to_speech(response_text, language)
                        if tts_audio:
                            st.audio(tts_audio, format="audio/mp3")
                    except Exception as e:
                        st.error(f"Error processing audio: {e}")

    # --- TAB 5: FIND LAWYER (INNOVATION) ---
    with tab5:
        st.header("👩‍⚖️ Find the Right Lawyer (Smart Match)")
        st.markdown("""
        **The Innovation:** Instead of blindly calling lawyers, Nyay-Saathi analyzes your conversation and documents to:
        1. **Summarize your case** into a professional legal brief.
        2. **Identify the category** (Family, Property, Criminal, etc.).
        3. **Match you** with the right expert.
        """)
        st.divider()

        # Check if we have any context to work with
        has_context = len(st.session_state.messages) > 0 or st.session_state.document_context != "No document uploaded."

        if not has_context:
            st.info("Please chat with Nyay-Saathi in the 'What to do' tab or upload a document first. We need information to match you with a lawyer!")
        else:
            col_match, col_display = st.columns([1, 2])
            
            with col_match:
                st.subheader("Step 1: AI Analysis")
                if st.button("Generate Case Brief & Find Match", type="primary"):
                    with st.spinner("AI is analyzing your case details..."):
                        try:
                            # Gather Context
                            chat_summary = "\n".join([m["content"] for m in st.session_state.messages])
                            doc_summary = st.session_state.document_context[:2000] # Limit length
                            
                            model = get_genai_model()
                            match_prompt = f"""
                            Analyze this user's legal situation based on their chat and documents.
                            
                            Chat History: {chat_summary}
                            Document Context: {doc_summary}
                            
                            Output a JSON object with these 2 fields:
                            1. "summary": A 3-sentence professional summary of the legal issue for a lawyer to read.
                            2. "category": ONE of these exact categories: "Family Law", "Property Dispute", "Criminal Law", "Consumer Rights", "Corporate Law", "Cyber Crime". If unsure, use "General".

                            JSON:
                            """
                            
                            response = model.generate_content(match_prompt)
                            cleaned_json = response.text.strip().replace("```json", "").replace("```", "")
                            data = json.loads(cleaned_json)
                            
                            st.session_state.case_brief = data["summary"]
                            st.session_state.recommended_lawyer_type = data["category"]
                            
                        except Exception as e:
                            st.error(f"AI Analysis failed: {e}")
                            # Fallback
                            st.session_state.case_brief = "User needs legal assistance based on recent inquiries."
                            st.session_state.recommended_lawyer_type = "General"

            with col_display:
                if st.session_state.case_brief:
                    st.success(f"**Match Found: {st.session_state.recommended_lawyer_type}**")
                    
                    st.markdown("### 📄 Your AI Legal Brief")
                    st.info(f"*{st.session_state.case_brief}*")
                    st.caption("Show this summary to the lawyer to save time and money.")
                    
                    st.markdown("---")
                    st.subheader(f"Recommended {st.session_state.recommended_lawyer_type} Lawyers")
                    
                    # Filter Mock Database
                    found_lawyers = [l for l in LAWYER_DIRECTORY if l["specialization"] == st.session_state.recommended_lawyer_type]
                    
                    # If no exact match, show random ones (Fallback)
                    if not found_lawyers:
                        found_lawyers = random.sample(LAWYER_DIRECTORY, 2)
                        st.warning(f"No specific {st.session_state.recommended_lawyer_type} experts in our demo database. Showing top rated lawyers:")

                    for lawyer in found_lawyers:
                        st.markdown(f"""
                        <div class="lawyer-card">
                            <h4>{lawyer['name']} <span style="font-size:0.8em; color:#00FFD1;">({lawyer['location']})</span></h4>
                            <p><strong>Specialization:</strong> {lawyer['specialization']} | <strong>Exp:</strong> {lawyer['experience']}</p>
                            <p><strong>Languages:</strong> {lawyer['languages']}</p>
                            <a href="tel:{lawyer['phone']}" style="text-decoration:none;">
                                <button style="background-color:#00FFD1; color:black; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;">📞 Call Now</button>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

# --- DISCLAIMER ---
st.divider()
st.error("""
**Note:** If you cannot afford legal services like hiring a lawyer or paying the court fees then please contact your local **NALSA (National Legal Services Authority)** for free legal aid or fee Waiver.
""")