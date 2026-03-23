# 🧠 NeuroChat AI

An intelligent AI assistant built with Python and Streamlit, featuring memory, hybrid reasoning, and adaptive response modes.

---

## 🚀 Features

- 💬 Chat with LLM (real-time responses)
- 🧠 Structured Memory System (name, goals, preferences)
- ⚡ Hybrid AI (direct answers from memory + LLM fallback)
- 🎯 Intent Detection (translation, coding, general)
- 🎛 Multiple Modes (default, teacher, coder, translator)
- 🖥 Streamlit Dashboard UI (custom styled)
- 📊 Metrics + Cards UI
- 📁 Persistent storage (chat + user facts)
- 🧾 Logging system

---

## 🧠 Architecture

```
User Input
   ↓
Intent Detection
   ↓
Hybrid Router
   ├── Memory → direct answer
   └── LLM → generated response
   ↓
UI (Streamlit)
```

---

## 📂 Project Structure

```
simple-llm-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── llm_client.py
│   ├── memory.py
│   ├── router.py
│   ├── intent.py
│   ├── logger.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .env.example
├── logs/
└── user_facts.json
```

---

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/neurochat-ai.git
cd neurochat-ai

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## 🔑 Environment Variables

```env
API_KEY=your_api_key
API_URL=https://api.groq.com/openai/v1/chat/completions
MODEL_NAME=llama-3.1-8b-instant
```

---

## ▶️ Run the Project

### Terminal Version:

```bash
python -m app.main
```

### Streamlit Dashboard:

```bash
streamlit run streamlit_app.py
```

---

## 📸 Demo

Add screenshots here after running the app

---

## 🧩 Future Improvements

- 📄 RAG (PDF / document understanding)
- 🧠 Vector database (FAISS / Chroma)
- 🌐 FastAPI backend
- 👥 Multi-user support
- 🔐 Authentication system
- 📊 Analytics dashboard

---

## 🧠 Author

Built as part of an AI Engineering learning journey.