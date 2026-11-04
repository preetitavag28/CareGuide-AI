
# 💚 CareGuide AI – Healthcare Information Assistant

CareGuide AI is an AI-powered healthcare information assistant developed using Python, Streamlit, and Google's Gemini API.

The application provides general healthcare education and wellness information in simple, easy-to-understand language. It is designed to help users learn about topics such as hydration, nutrition, sleep, exercise, and preventive healthcare.

**Note:** CareGuide AI is an educational prototype. It does not diagnose medical conditions, prescribe medicines, or replace professional medical advice.

---

## 🌐 Live Demo

[Open CareGuide AI](https://careguide-ai-8asnm59v5r4ikuo92q9obs.streamlit.app/)

## 📌 GitHub Repository

[View Source Code](https://github.com/preetitavag28/CareGuide-AI)

---

## ✨ Features

- AI-powered healthcare information assistant.
- Interactive chat interface.
- General health and wellness information.
- Simple and understandable AI-generated responses.
- Medical safety instructions through prompt engineering.
- Emergency guidance for potentially life-threatening symptoms.
- Chat history during the application session.
- Gemini API integration.
- Automatic retry handling for temporary API errors.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| Streamlit | Web application interface |
| Google Gemini API | AI-generated responses |
| Google GenAI SDK | Gemini API integration |
| Python-dotenv | Environment variable management |
| Prompt Engineering | AI instructions and safety guidelines |
| Git & GitHub | Version control and project hosting |
| Streamlit Community Cloud | Application deployment |

---

## 📂 Project Structure

```text
CareGuide-AI/
│
├── app.py
├── prompts.py
├── prompts_documentation.md
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
└── test_env.py
```

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/preetitavag28/CareGuide-AI.git
```

### 2. Open the project folder

```bash
cd CareGuide-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the Gemini API key

Create a `.env` file in the project root directory.

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Get an API key from:

https://aistudio.google.com/apikey

Never upload your actual `.env` file or API key to GitHub.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧠 Prompt Engineering

Prompt engineering was used to define the assistant's role, response style, and safety restrictions.

The system prompt instructs CareGuide AI to:

- Provide general healthcare education.
- Explain topics in simple language.
- Avoid medical diagnosis.
- Avoid prescribing medicines or dosages.
- Encourage consultation with healthcare professionals.
- Provide emergency guidance when necessary.

Prompt iterations and improvements are documented in:

`prompts_documentation.md`

---

## 🔍 Example Questions

Users can ask questions such as:

1. What are the benefits of drinking water?
2. What are healthy sleep habits?
3. What foods are rich in iron?
4. What are the benefits of regular exercise?
5. How can I maintain a balanced diet?

---

## 🔐 Safety and Limitations

- This application is for educational purposes only.
- It does not provide medical diagnosis or treatment.
- AI-generated information may be inaccurate.
- Always consult a qualified healthcare professional.
- For potentially life-threatening emergencies in India, seek immediate medical assistance by calling 112.

---

## 🚀 Future Enhancements

- Voice-based interaction.
- Multilingual healthcare information.
- Improved response validation.
- Additional wellness education resources.
- Enhanced user interface.
- More comprehensive automated testing.

---

## 👩‍💻 Developer

**Preeti Tavag**

MCA Graduate | Software Developer | AI Enthusiast

GitHub: https://github.com/preetitavag28

LinkedIn: https://www.linkedin.com/in/preetitavag/

---

## 📄 License

This project is developed for educational and demonstration purposes.
