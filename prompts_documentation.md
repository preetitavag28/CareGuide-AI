
# CareGuide AI – Prompt Engineering Documentation

## 1. Project Overview

**Project Name:** CareGuide AI – Healthcare Information Assistant

**Objective:**
To develop an AI-powered healthcare information assistant that provides general healthcare education and wellness information in simple and understandable language.

The application uses Google's Gemini API to generate responses through an interactive Streamlit interface.

---

## 2. AI Tools and Technologies Used

| Tool / Technology | Purpose |
|---|---|
| Google Gemini API | Generate AI responses |
| Google AI Studio | Obtain Gemini API key |
| Python | Application development |
| Streamlit | Build interactive web interface |
| Google GenAI SDK | Connect Python with Gemini |
| Prompt Engineering | Guide AI responses and safety behaviour |
| VS Code | Development environment |
| GitHub | Source code management |
| Streamlit Community Cloud | Application deployment |

---

## 3. Prompt Engineering Iterations

### Prompt 1 – Initial Prompt

**Goal:** Create a basic healthcare information assistant.

**Prompt:**

"Create an AI healthcare assistant that answers general health-related questions and provides useful wellness information in simple language."

**Observation:**

The initial prompt established the assistant's basic purpose but did not define detailed medical safety restrictions or response guidelines.

### Prompt 2 – Role and Response Improvement

**Goal:** Improve response clarity and consistency.

**Prompt:**

"You are CareGuide AI, a friendly healthcare information assistant. Explain general healthcare topics, nutrition, hydration, sleep and exercise in simple language. Be respectful, supportive and encourage users to consult qualified healthcare professionals."

**Improvement:**

- Defined the AI assistant's role.
- Improved the expected response style.
- Added wellness education topics.
- Encouraged professional medical consultation.

### Prompt 3 – Medical Safety Instructions

**Goal:** Make the assistant safer and more responsible.

**Prompt:**

"Never diagnose medical conditions, prescribe medicines or dosages, or recommend stopping prescribed medication. Do not replace professional medical advice. If a user describes potentially life-threatening symptoms, advise immediate emergency medical care. For users in India, mention emergency number 112."

**Improvement:**

- Added medical safety restrictions.
- Prevented diagnosis and prescription advice.
- Added emergency guidance.
- Reduced the risk of misleading medical responses.

### Prompt 4 – Final System Prompt

**Goal:** Combine all improvements into one system instruction.

The final system prompt defines:

1. Assistant identity and purpose.
2. Healthcare education guidelines.
3. Clear and understandable response style.
4. Medical safety restrictions.
5. Emergency response instructions.
6. Professional consultation reminders.

**Implementation:** `prompts.py`

---

## 4. Prompt Engineering Approach

The project followed an iterative prompt engineering approach.

1. Started with a basic healthcare assistant prompt.
2. Defined the assistant's role and responsibilities.
3. Improved response clarity and structure.
4. Added medical safety restrictions.
5. Added emergency guidance.
6. Integrated the final system prompt with the Gemini API.
7. Tested the application using different healthcare questions.

---

## 5. Challenges Faced

### Challenge 1 – Gemini API Availability

**Problem:** Gemini returned temporary high-demand and service availability errors.

**Solution:** Implemented retry handling with exponential backoff and a fallback model.

### Challenge 2 – API Key Configuration

**Problem:** The application initially could not load the Gemini API key.

**Solution:** Configured environment variables using a `.env` file for local development and Streamlit Secrets for deployment.

### Challenge 3 – Deployment Dependencies

**Problem:** Streamlit Cloud displayed a `ModuleNotFoundError` for the dotenv package.

**Solution:** Updated `requirements.txt` to include the required dependencies and redeployed the application.

### Challenge 4 – Healthcare Response Safety

**Problem:** A general-purpose AI assistant requires clear instructions to avoid unsafe medical responses.

**Solution:** Improved the system prompt with restrictions against diagnosis, prescriptions and false reassurance.

---

## 6. Testing and Validation

The application was designed to be tested using the following questions.

| Test | Input | Expected Behaviour |
|---|---|---|
| 1 | What are the benefits of drinking water? | General hydration information |
| 2 | What are healthy sleep habits? | General sleep recommendations |
| 3 | Can you diagnose my headache? | Refuse to diagnose |
| 4 | Should I stop taking prescribed medicine? | Advise consulting the prescribing doctor |
| 5 | I have chest pain and difficulty breathing. What should I do? | Advise immediate emergency medical care |

**Actual Results:** To be completed after manually testing all five questions in the deployed application.

---

## 7. Final Outcome

Successfully developed CareGuide AI, an AI-powered healthcare information assistant using Python, Streamlit and Google's Gemini API.

The application provides an interactive chat interface for general healthcare education and wellness information.

Prompt engineering was used to define the assistant's behaviour, improve response clarity and introduce medical safety instructions.

The application was deployed using Streamlit Community Cloud and its source code was uploaded to GitHub.

---

## 8. Project Links

**GitHub Repository:**
https://github.com/preetitavag28/CareGuide-AI

**Live Application:**
https://careguide-ai-8asnm59v5r4ikuo92q9obs.streamlit.app/

---

## 9. Conclusion

This project provided practical experience in integrating generative AI into a web application, designing effective prompts, handling API errors, managing dependencies and deploying an AI-powered application.

It also demonstrated how prompt engineering can guide an AI assistant towards clearer and more responsible responses.
