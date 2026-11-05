
import os
import time
import random
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from prompts import SYSTEM_PROMPT


# --------------------------------------------------
# 1. ENVIRONMENT CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY")


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareGuide AI | Health Assistant",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# 3. CUSTOM DESIGN
# --------------------------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5faf8;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: #eaf4f0;
    border-right: 1px solid #dcebe4;
}

[data-testid="stSidebar"] h1 {
    color: #087c56;
}

/* Main heading */

.hero {
    background: linear-gradient(135deg, #e0f5eb, #f5fcf8);
    border: 1px solid #d4eee0;
    border-radius: 22px;
    padding: 30px;
    margin-bottom: 22px;
}

.hero-title {
    color: #087c56;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #536b60;
    font-size: 16px;
    line-height: 1.7;
}

/* Section headings */

.section-heading {
    font-size: 21px;
    font-weight: 700;
    color: #183e30;
    margin-top: 24px;
    margin-bottom: 12px;
}

/* Feature cards */

.feature-card {
    background: white;
    border: 1px solid #e0ece5;
    border-radius: 16px;
    padding: 19px;
    min-height: 145px;
    box-shadow: 0 3px 12px rgba(20, 80, 50, 0.04);
}

.feature-icon {
    font-size: 27px;
    margin-bottom: 9px;
}

.feature-title {
    font-size: 16px;
    font-weight: 700;
    color: #176b4c;
    margin-bottom: 5px;
}

.feature-description {
    color: #687d72;
    font-size: 13px;
    line-height: 1.5;
}

/* Safety notice */

.safety-box {
    background: #fff5df;
    border: 1px solid #f3dfae;
    color: #76551a;
    border-radius: 12px;
    padding: 15px 18px;
    margin-top: 18px;
    margin-bottom: 22px;
    font-size: 14px;
    line-height: 1.7;
}

/* Buttons */

.stButton > button {
    border-radius: 11px;
    border: 1px solid #cce5d7;
    color: #176b4c;
    background: white;
    font-weight: 600;
    min-height: 43px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background: #e5f5ec;
    border-color: #16845b;
    color: #087c56;
}

/* Chat input */

[data-testid="stChatInput"] {
    border-radius: 14px;
}

/* Chat messages */

[data-testid="stChatMessage"] {
    border-radius: 15px;
    padding: 12px;
}

/* Sidebar text */

.sidebar-note {
    color: #62786c;
    font-size: 13px;
    line-height: 1.6;
}

.footer {
    text-align: center;
    color: #82958b;
    font-size: 12px;
    padding-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None


def choose_prompt(prompt):
    st.session_state.pending_prompt = prompt


# --------------------------------------------------
# 5. GEMINI API KEY CHECK
# --------------------------------------------------

if not API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Please configure GEMINI_API_KEY in your .env file "
        "or Streamlit Secrets."
    )
    st.stop()


# --------------------------------------------------
# 6. INITIALIZE GEMINI
# --------------------------------------------------

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


client = get_client(API_KEY)


def generate_ai_response(messages):

    conversation = []

    for message in messages[-12:]:

        role = message["role"].upper()
        content = message["content"]

        conversation.append(f"{role}: {content}")

    conversation_text = "\n\n".join(conversation)

    models = [
        "gemini-3.8-flash",
        "gemini-3.6-flash"
    ]

    for model in models:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=conversation_text,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.4,
                        max_output_tokens=1024
                    )
                )

                if response and response.text:
                    return response.text

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            except errors.APIError as e:

                error_code = getattr(e, "code", None)

                if error_code in (429, 500, 502, 503, 504):

                    if attempt < 2:

                        wait_time = (
                            (2 ** attempt) + random.uniform(0, 1)
                        )

                        time.sleep(wait_time)
                        continue

                    break

                raise

    raise RuntimeError(
        "Gemini models are currently unavailable. "
        "Please try again in a few minutes."
    )


with st.sidebar:

    st.markdown("# 💚 CareGuide AI")

    st.markdown(
        '<p class="sidebar-note">'
        'Your personal AI-powered healthcare education companion.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ✨ Explore Health Topics")

    sidebar_topics = [
        ("🥗 Nutrition", "What are some general healthy eating habits?"),
        ("😴 Sleep", "What are healthy sleep habits?"),
        ("🏃 Fitness", "What are the benefits of regular exercise?"),
        ("💧 Hydration", "Why is drinking enough water important?")
    ]

    for label, question in sidebar_topics:

        st.button(
            label,
            key=f"sidebar_{label}",
            use_container_width=True,
            on_click=choose_prompt,
            args=(question,)
        )

    st.divider()

    st.markdown("### 💬 Your Conversation")

    st.caption(
        f"Messages in this session: {len(st.session_state.messages)}"
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.rerun()

    st.divider()

    st.markdown(
        '<p class="sidebar-note">'
        '**Built with:** Python, Streamlit and Google Gemini AI.'
        '</p>',
        unsafe_allow_html=True
    )

    st.caption("Educational use only.")



st.markdown("""
<div class="hero">
    <div class="hero-title">
        💚 CareGuide AI
    </div>
    <div class="hero-subtitle">
        Your friendly AI healthcare information assistant.<br>
        Ask questions, explore wellness topics and learn
        healthy lifestyle habits with AI-powered guidance.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="safety-box">
    <strong>⚕️ Important Health Disclaimer</strong><br>
    CareGuide AI provides general healthcare education
    and wellness information. It does not diagnose medical
    conditions, prescribe treatments or replace professional
    medical advice. Always consult a qualified healthcare
    professional for personal medical concerns.
    For emergencies in India, call 112.
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 11. FEATURE CARDS
# --------------------------------------------------


# ==================================================
# 11. FEATURE CARDS
# ==================================================

st.markdown(
    '<div class="section-heading">Explore Your Wellness</div>',
    unsafe_allow_html=True
)

features = [
    {
        "icon": "🥗",
        "title": "Nutrition",
        "description": "Learn about balanced diets and healthy food choices."
    },
    {
        "icon": "😴",
        "title": "Better Sleep",
        "description": "Explore healthy sleep habits and routines."
    },
    {
        "icon": "🏃",
        "title": "Fitness",
        "description": "Discover general exercise and activity benefits."
    },
    {
        "icon": "💧",
        "title": "Healthy Living",
        "description": "Understand hydration and everyday wellness."
    }
]

columns = st.columns(4)

for column, feature in zip(columns, features):

    with column:

        with st.container(border=True):

            st.markdown(
                f"""
                <div style="font-size:30px;">
                    {feature["icon"]}
                </div>
                <div style="color:#176b4c;font-size:17px;font-weight:700;">
                    {feature["title"]}
                </div>
                <div style="color:#687d72;font-size:13px;">
                    {feature["description"]}
                </div>
                """,
                unsafe_allow_html=True
            )

# --------------------------------------------------
# 12. QUICK QUESTIONS
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">💡 Try Asking</div>',
    unsafe_allow_html=True
)

quick_questions = [
    "What are healthy sleep habits?",
    "What foods contain iron?",
    "How can I maintain a balanced diet?",
    "What are the benefits of regular exercise?"
]

question_columns = st.columns(2)

for index, question in enumerate(quick_questions):

    with question_columns[index % 2]:

        st.button(
            f"💬 {question}",
            key=f"quick_{index}",
            use_container_width=True,
            on_click=choose_prompt,
            args=(question,)
        )


# --------------------------------------------------
# 13. CHAT SECTION
# --------------------------------------------------

st.markdown(
    '<div class="section-heading">💬 Chat with CareGuide AI</div>',
    unsafe_allow_html=True
)


# Display welcome content when chat is empty

if not st.session_state.messages:
    st.markdown("""
    <div class="feature-card" style="min-height:auto;">
        <h3 style="color:#176b4c;">
            Hello! 👋 Welcome to CareGuide AI
        </h3>
        <p style="color:#687d72; line-height:1.7;">
            I'm here to help you understand general health
            and wellness topics in simple language.
        </p>
        <p style="color:#176b4c; font-weight:600;">
            Choose a suggested question above or type
            your own question below.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# 14. CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask CareGuide AI about health and wellness..."
)

# Handle both typed questions and button suggestions

prompt = user_input

if st.session_state.pending_prompt:

    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None


# --------------------------------------------------
# 15. PROCESS USER QUESTION
# --------------------------------------------------

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "💚 CareGuide AI is preparing your answer..."
        ):

            try:

                answer = generate_ai_response(
                    st.session_state.messages
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except errors.APIError as e:

                st.error(
                    "Gemini API error. Please check your API "
                    "access and try again."
                )

                st.caption(str(e))

                st.session_state.messages.pop()

            except Exception as e:

                st.error(
                    "Something went wrong while generating "
                    "your response. Please try again."
                )

                st.caption(str(e))

                st.session_state.messages.pop()


# --------------------------------------------------
# 16. FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">
    💚 CareGuide AI | AI-Powered Healthcare Education
    <br><br>
    <strong>Built with:</strong>
    Python • Streamlit • Google Gemini AI
    <br><br>
    Educational information only. Always seek professional
    medical advice for personal health concerns.
</div>
""", unsafe_allow_html=True)
