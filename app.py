
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
# 1. LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env", override=True)

API_KEY = os.getenv("GEMINI_API_KEY")


# --------------------------------------------------
# 2. STREAMLIT PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CareGuide AI",
    page_icon="💚",
    layout="centered"
)


# --------------------------------------------------
# 3. CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .main {
        background-color: #f7fbf8;
    }

    .title {
        text-align: center;
        color: #16845b;
        font-size: 40px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: #555;
        font-size: 16px;
    }

    .safety {
        background-color: #fff4df;
        padding: 12px;
        border-radius: 10px;
        color: #664400;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 4. APPLICATION HEADER
# --------------------------------------------------

st.markdown(
    '<div class="title">💚 CareGuide AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your friendly AI healthcare information assistant</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "CareGuide AI provides general healthcare education "
    "and wellness information."
)

st.markdown("""
<div class="safety">
<strong>Important:</strong> This application does not diagnose
medical conditions or prescribe treatments. Always consult
a qualified healthcare professional for medical advice.
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# 5. CHECK API KEY
# --------------------------------------------------

if not API_KEY:
    st.error(
        "Gemini API key is missing. "
        "Please add GEMINI_API_KEY to your .env file."
    )
    st.stop()


# --------------------------------------------------
# 6. INITIALIZE GEMINI CLIENT
# --------------------------------------------------

@st.cache_resource
def get_client(api_key):
    return genai.Client(api_key=api_key)


client = get_client(API_KEY)


# --------------------------------------------------
# 7. GENERATE AI RESPONSE WITH RETRIES
# --------------------------------------------------

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

    # Try each model, with up to 3 attempts
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

                # Retry temporary server or rate-limit errors
                if error_code in (429, 500, 502, 503, 504):

                    if attempt < 2:
                        wait_time = (
                            (2 ** attempt) + random.uniform(0, 1)
                        )

                        time.sleep(wait_time)
                        continue

                    # Move to the next model
                    break

                # Other API errors should be shown to the user
                raise

    raise RuntimeError(
        "Both Gemini models are currently unavailable. "
        "Please wait a few minutes and try again."
    )


# --------------------------------------------------
# 8. CHAT SESSION
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# --------------------------------------------------
# 9. DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 10. USER CHAT INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask a healthcare or wellness question..."
)


if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("CareGuide AI is preparing your answer..."):

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
                    f"Gemini API error: {e}. "
                    "Please check your API access and try again."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# --------------------------------------------------
# 11. SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("💚 CareGuide AI")

    st.write(
        "An AI-powered healthcare education project."
    )

    st.divider()

    st.subheader("Example Questions")

    examples = [
        "What are healthy sleep habits?",
        "Why is drinking enough water important?",
        "What are the benefits of regular exercise?",
        "What foods contain iron?",
        "How can I maintain a balanced diet?"
    ]

    for example in examples:
        st.write("• " + example)

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built using Python, Streamlit and Gemini AI.")

    st.caption(
        "Educational use only. Not a substitute for professional care."
    )
