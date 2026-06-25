import os
import re
import base64
import streamlit as st
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# GLOBAL INITIALIZATION & CONFIG 
st.set_page_config(page_title="Resume Genie Workspace", page_icon="🧞‍♂️", layout="wide")

# Standardize your API Key across all modular components
GOOGLE_API_KEY = "API_KEY" 
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["GEMINI_API_KEY"] = GOOGLE_API_KEY

# Helper function to extract text and convert PDF to Base64 safely
def process_uploaded_pdf(file_buffer):
    pdf_reader = PdfReader(file_buffer)
    extracted_text = ""
    for page in pdf_reader.pages:
        extracted_text += page.extract_text() + "\n\n"
    
    file_buffer.seek(0)
    base64_string = base64.b64encode(file_buffer.read()).decode('utf-8')
    return extracted_text, base64_string


# SIDEBAR MULTI-SERVICE NAVIGATION ---
with st.sidebar:
    st.markdown("## 🧞‍♂️ Resume Genie Menu")
    st.write("Select a dynamic optimization service:")
    
    # Persistent page selection variable inside Session State
    if "active_service" not in st.session_state:
        st.session_state.active_service = "📊 Resume Scorer & Analyzer"
        
    if st.button("📊 Resume Scorer & Analyzer", use_container_width=True, type="primary" if st.session_state.active_service == "📊 Resume Scorer & Analyzer" else "secondary"):
        st.session_state.active_service = "📊 Resume Scorer & Analyzer"
    if st.button("📝 Tailored Cover Letter Generator", use_container_width=True, type="primary" if st.session_state.active_service == "📝 Tailored Cover Letter Generator" else "secondary"):
        st.session_state.active_service = "📝 Tailored Cover Letter Generator"
    if st.button("🎯 ATS Job Match Scorer & Pie Chart", use_container_width=True, type="primary" if st.session_state.active_service == "🎯 ATS Job Match Scorer & Pie Chart" else "secondary"):
        st.session_state.active_service = "🎯 ATS Job Match Scorer & Pie Chart"
    if st.button("💬 Live AI Career Coach Chatbot", use_container_width=True, type="primary" if st.session_state.active_service == "💬 Live AI Career Coach Chatbot" else "secondary"):
        st.session_state.active_service = "💬 Live AI Career Coach Chatbot"

    st.markdown("---")
    st.caption("Engineered using Gemini-2.5-Flash Framework Architecture.")

# 1: RESUME SCORER & ANALYZER 

if st.session_state.active_service == "📊 Resume Scorer & Analyzer":
    st.title("📊 Standard Resume Scorer & Profiler")
    st.write("Get an instant industry-standard grading metric matrix breakdown along with next steps recommendations.")
    
    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    
    resume_template = """You are an expert career coach and senior technical recruiter. 
    Analyze the resume provided in the context below against professional industry standards.

    Provide a highly structured evaluation including a total score out of 100 based on the following 4 rubrics (each worth 25 points):
    1. Impact & Metrics: Are achievements quantified using action verbs and data/results?
    2. Structure & Formatting: Is the content logical, clean, and scannable?
    3. Core Competencies: Are technical and soft skills clearly defined and well-positioned?
    4. Relevance & Language: Is the tone professional, concise, and free of fluff?

    ---
    CONTEXT (RESUME TEXT):
    {context}

    QUESTION/USER REQUEST:
    {question}
    ---

    Please return your response using the following markdown format:

    ## 📊 Resume Score: [Insert Total Score]/100
    * **Impact & Metrics:** [Score]/25
    * **Structure & Formatting:** [Score]/25
    * **Core Competencies:** [Score]/25
    * **Relevance & Language:** [Score]/25

    ---

    ### 💪 Key Strengths
    * [Strength 1 with a brief note why]
    * [Strength 2]
    * [Strength 3]

    ### ❌ Key Weaknesses
    * [Weakness 1 with a brief note why]
    * [Weakness 2]
    * [Weakness 3]

    ### 🛠️ Skills
    * **Current Skills found:** [List main skills in seperate points]
    * **Recommended Skills to Add:** [Suggest 3-5 high-value skills or keywords that would strengthen this specific profile]

    ### 🎯 Next Career Path
    * [Based on the resume, suggest a specific job role or industry that would be a strong fit for this candidate, with a brief rationale. Put the suggested career paths in points]
    """
    
    prompt = PromptTemplate(input_variables=["context", "question"], template=resume_template)
    uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"], key="s1_file")
    
    if uploaded_file is not None:
        if st.button("Evaluate Resume Profile", type="primary"):
            with st.spinner("Analyzing profile metrics... Please wait..."):
                parsed_text, _ = process_uploaded_pdf(uploaded_file)
                if not parsed_text.strip():
                    st.error("Could not parse character maps from this PDF structure.")
                else:
                    formatted_prompt = prompt.format(
                        context=parsed_text,
                        question="Please evaluate this resume thoroughly and provide the structured score breakdown."
                    )
                    response = chat.invoke(formatted_prompt)
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown(response.content)

# 
# 2: TAILORED COVER LETTER GENERATOR 
#
elif st.session_state.active_service == "📝 Tailored Cover Letter Generator":
    st.title("📝 Tailored Cover Letter Generator")
    st.write("Generate a contextually aligned 350-400 word value proposition letter mapping directly onto your target job requirements.")
    
    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    cover_letter_template = """You are an elite executive career coach and professional copywriter. 
    Your task is to write a highly professional, tailored, compelling, and persuasive cover letter based on the candidate's resume and the target job description.

    STRICT CONSTRAINTS & FORMATTING RULES:
    1. **Word Count:** The entire cover letter must be strictly between 350 to 400 words total. Be concise and make every sentence impactful.
    2. **No Redundancy:** Do not stack identical metrics. Select the strongest matching accomplishments from the resume that prove core capabilities.

    ---
    STRUCTURE EXPECTED:
    - **Contact Block:** You MUST start with the specific contact details and name of the candidate found in the resume (e.g., [Candidate Name], [Phone Number], [Email Address], [LinkedIn Profile URL], [Current Date]). Place each of these details on their own separate line, aligned perfectly to the left. Leave a clean empty line gap before the salutation.
    - **Salutation:** Open with a professional salutation (e.g., Dear [Hiring Manager Name], or Dear Selection Committee,).
    - **The Hook:** Start with a strong opening paragraph highlighting 6+ years of analytics experience transforming data into optimization strategies.
    - **Technical Alignment:** Explicitly map backend data architecture capabilities (SQL, automated ETL pipelines) to their need for database design and management (e.g., matching past warehouse optimization to data solutions like Snowflake).
    - **Dashboards & Cross-Functional Impact:** Focus on the creation of business intelligence reporting solutions (like Power BI dashboards) and cross-functional collaboration to optimize business experiences.
    - **Polished Close:** Reiterate alignment and invite a conversation.
    - **Signature:** End cleanly with a professional sign-off exactly like this:

    Sincerely,
    [Candidate's Name]

    ---
    CANDIDATE RESUME:
    {context}

    TARGET JOB DESCRIPTION:
    {job_description}
    ---

    Generate the letter following these exact rules. Focus purely on high-impact value delivery.
    """
    
    prompt = PromptTemplate(input_variables=["context", "job_description"], template=cover_letter_template)
    uploaded_file = st.file_uploader("Step 1: Upload your Resume (PDF format)", type=["pdf"], key="s2_file")
    job_description_input = st.text_area("Step 2: Paste the Target Job Description here:", height=200, key="s2_jd")
    
    if uploaded_file and job_description_input:
        if st.button("Generate Cover Letter", type="primary"):
            with st.spinner("Drafting copy solutions... Please wait..."):
                parsed_text, _ = process_uploaded_pdf(uploaded_file)
                if not parsed_text.strip():
                    st.error("Could not parse character data maps.")
                else:
                    formatted_prompt = prompt.format(context=parsed_text, job_description=job_description_input)
                    st.markdown("### 📋 Generated Cover Letter")
                    st.markdown("---")
                    output_placeholder = st.empty()
                    full_response = ""
                    for m in chat.stream(formatted_prompt):
                        full_response += m.content
                        output_placeholder.markdown(full_response + "▌")
                    output_placeholder.markdown(full_response)
                    st.success("Cover Letter Generated Successfully!")


# 3: ATS JOB MATCH SCORER & PIE CHART 
elif st.session_state.active_service == "🎯 ATS Job Match Scorer & Pie Chart":
    st.title("🎯 ATS Job Match Scorer & Dashboard")
    st.write("Run deep analytical compliance checks complete with missing keyword logs and a visual rubric pie chart dashboard tool.")
    
    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.15)
    
    template = """You are an expert ATS (Applicant Tracking System) optimizer, elite technical recruiter, and executive career coach.
    Your task is to critically analyze the candidate's resume against the provided Job Description (JD).

    ---
    CANDIDATE RESUME:
    {context}

    TARGET JOB DESCRIPTION:
    {job_description}
    ---

    CRITICAL INITIAL STEP:
    You must output a raw comma-separated data block on the absolute first line of your response containing exactly 4 integers out of 100 representing your rubric assessment. Do not put any markdown or labels on this first line. Format it exactly like this example line:
    DATA_SCORES:85,70,90,75

    After that data line, leave a line gap and return your complete response using the following structured markdown format:

    # 📊 ATS Evaluation Dashboard

    ## 🎯 Match Summary
    * **Overall Job Match:** [Score]/ 100
    * **ATS Compatibility Score:** [Score] / 100
    * **Readability Score:** [Score] / 100

    * **Keywords Matched:**
      * Point 1
      * Point 2
      * Point 3

    * **Missing Keywords:** essential keywords/tools found in both the resume and JD
      * Keyword 1
      * Keyword 2
      * Keyword 3

    * **Missing Critical Keywords:** [Identify 3-5 crucial technical or procedural keywords found in the JD that are completely missing from the resume]
      * Keyword 1
      * Keyword 2
      * Keyword 3

    ---

    ## 🛠️ Gap & Format Analysis

    ### 📐 Structural & Formatting Review
    [Provide exactly a 2-sentence crisp analysis of the resume's layout, font clarity, scannability, and structural file parsing limits.]

    ### 🚨 Skills Gap Analysis : in points
    * **Hard Skills Gaps:** [Identify specific missing software, database systems, mathematical modeling, or engineering platforms demanded by the JD and put it in points. format-* Point 1: Missing/weak: represented skills that are critical for this role based on the JD]
    * **Methodology/Process Gaps:** [Identify missing processes, such as Agile/Scrum structures, specific governance models, or enterprise-wide optimization methods and put it in points]

    ---

    ## 🚀 Optimization & Feedback

    ### 🎯 Industry-Specific Feedback
    * [Provide 1 tailored, strategic insight into what competitive companies in this specific industry are looking for on a resume right now based on this job profile]

    ### 💡 Overall Improvement Action Items
    * [Action Item 1: Provide a highly specific, actionable instruction to immediately increase the score]
    * [Action Item 2]
    * [Action Item 3]
    """
    
    prompt = PromptTemplate(input_variables=["context", "job_description"], template=template)
    uploaded_file = st.file_uploader("Step 1: Upload your Resume (PDF format)", type=["pdf"], key="s3_file")
    job_desc_input = st.text_area("Step 2: Paste the Target Job Description here:", height=200, key="s3_jd")
    
    if uploaded_file and job_desc_input:
        if st.button("Evaluate Match Scores", type="primary"):
            with st.spinner("Processing structural parsing loops... Please wait..."):
                parsed_text, _ = process_uploaded_pdf(uploaded_file)
                if not parsed_text.strip():
                    st.error("Could not parse file structure maps accurately.")
                else:
                    formatted_prompt = prompt.format(context=parsed_text, job_description=job_desc_input)
                    response = chat.invoke(formatted_prompt)
                    raw_content = response.content
                    
                    scores = [70, 70, 70, 70]
                    data_match = re.search(r"DATA_SCORES:(\d+),(\d+),(\d+),(\d+)", raw_content)
                    if data_match:
                        scores = [int(x) for x in data_match.groups()]
                        display_content = re.sub(r"DATA_SCORES:\d+,\d+,\d+,\d+", "", raw_content).strip()
                    else:
                        display_content = raw_content

                    st.markdown("---")
                    st.subheader("🎯 Visual Rubrics Score Explorer")
                    
                    st.components.v1.html(f"""
                    <div style="font-family: sans-serif; background-color: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px;">
                        <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
                            <div style="position: relative; width: 180px; height: 180px;">
                                <svg width="100%" height="100%" viewBox="0 0 42 42" class="donut">
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="#f8f9fa"></circle>
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#e9ecef" stroke-width="3"></circle>
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#dc3545" stroke-width="4" stroke-dasharray="{scores[0]/4} {100 - (scores[0]/4)}" stroke-dashoffset="25"></circle>
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#007bff" stroke-width="4" stroke-dasharray="{scores[1]/4} {100 - (scores[1]/4)}" stroke-dashoffset="{25 - (scores[0]/4)}"></circle>
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#28a745" stroke-width="4" stroke-dasharray="{scores[2]/4} {100 - (scores[2]/4)}" stroke-dashoffset="{25 - (scores[0]/4) - (scores[1]/4)}"></circle>
                                    <circle cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#ffc107" stroke-width="4" stroke-dasharray="{scores[3]/4} {100 - (scores[3]/4)}" stroke-dashoffset="{25 - (scores[0]/4) - (scores[1]/4) - (scores[2]/4)}"></circle>
                                </svg>
                                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                                    <span style="font-size: 24px; font-weight: bold; color: #333;">{int(sum(scores)/4)}%</span><br>
                                    <span style="font-size: 11px; color: #6c757d; font-weight: 600;">OVERALL</span>
                                </div>
                            </div>
                            <div style="min-width: 220px; font-size: 13px;">
                                <div style="margin-bottom: 8px;"><span style="display:inline-block; width:12px; height:12px; background:#dc3545; margin-right:8px; border-radius:2px;"></span><strong>Technical Alignment:</strong> {scores[0]}/100</div>
                                <div style="margin-bottom: 8px;"><span style="display:inline-block; width:12px; height:12px; background:#007bff; margin-right:8px; border-radius:2px;"></span><strong>Impact Metrics:</strong> {scores[1]}/100</div>
                                <div style="margin-bottom: 8px;"><span style="display:inline-block; width:12px; height:12px; background:#28a745; margin-right:8px; border-radius:2px;"></span><strong>Experience Relevance:</strong> {scores[2]}/100</div>
                                <div><span style="display:inline-block; width:12px; height:12px; background:#ffc107; margin-right:8px; border-radius:2px;"></span><strong>Soft Skills & Leadership:</strong> {scores[3]}/100</div>
                            </div>
                        </div>
                    </div>
                    """, height=230)
                    
                    st.markdown("---")
                    st.markdown(display_content)
                    st.success("Analysis Complete!")

# 4: LIVE AI CAREER COACH CHATBOT (SPLIT VIEW)

elif st.session_state.active_service == "💬 Live AI Career Coach Chatbot":
    st.title("💬 Live Chatbot Workspace Matrix")
    st.write("Review your visual document formatting on the left half while talking in real-time to your coach on the right.")
    
    chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    # Use localized unique tracking keys for Service 4 state persistence
    if "s4_chat_history" not in st.session_state:
        st.session_state.s4_chat_history = []
    if "s4_resume_context" not in st.session_state:
        st.session_state.s4_resume_context = ""
    if "s4_pdf_base64" not in st.session_state:
        st.session_state.s4_pdf_base64 = None

    uploaded_file = st.file_uploader("Upload your Resume (PDF format) to anchor the chatbot context:", type=["pdf"], key="s4_file")
    
    if uploaded_file:
        parsed_text, base64_str = process_uploaded_pdf(uploaded_file)
        st.session_state.s4_resume_context = parsed_text
        st.session_state.s4_pdf_base64 = base64_str

    if st.session_state.s4_resume_context:
        st.markdown("---")
        left_col, right_col = st.columns(2)
        
        with left_col:
            st.subheader("📄 Connected Resume Profile")
            if st.session_state.s4_pdf_base64:
                pdf_iframe = f'<iframe src="data:application/pdf;base64,{st.session_state.s4_pdf_base64}" width="100%" height="650px" style="border:1px solid #dee2e6; border-radius:8px;"></iframe>'
                st.markdown(pdf_iframe, unsafe_allow_html=True)
                
        with right_col:
            st.subheader("💬 Active Coaching Session")
            chat_container = st.container(height=550)
            
            with chat_container:
                for message in st.session_state.s4_chat_history:
                    if isinstance(message, HumanMessage):
                        with st.chat_message("user"): st.markdown(message.content)
                    elif isinstance(message, AIMessage):
                        with st.chat_message("assistant"): st.markdown(message.content)
                        
            if user_query := st.chat_input("Ask about structural improvements, interviews, or career pivots...", key="s4_input"):
                with chat_container:
                    with st.chat_message("user"): st.markdown(user_query)
                
                st.session_state.s4_chat_history.append(HumanMessage(content=user_query))
                
                system_message = SystemMessage(content=f"""
                    You are a professional career coach and mentor.
                    You help with career guidance, resume improvement, interview preparation, 
                    job search strategies, professional development advice, networking strategies, and skill gap analysis.
                    
                    Candidate Resume Content Context: 
                    {st.session_state.s4_resume_context}
                """)
                
                payload = [system_message] + st.session_state.s4_chat_history
                
                with chat_container:
                    with st.chat_message("assistant"):
                        output_placeholder = st.empty()
                        full_reply = ""
                        for chunk in chat.stream(payload):
                            full_reply += chunk.content
                            output_placeholder.markdown(full_reply + "▌")
                        output_placeholder.markdown(full_reply)
                        
                st.session_state.s4_chat_history.append(AIMessage(content=full_reply))
                st.rerun()
    else:
        st.info("Sync your resume file structure above to activate the side-by-side terminal coach environment.")