import html
import streamlit as st

from app.llm_client import ask_llm
from app.memory import load_facts, save_facts, update_fact, extract_facts_from_message
from app.router import answer_from_facts
from app.intent import detect_intent


st.set_page_config(
    page_title="NeuroChat AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
    :root {
        --bg: #0e1117;
        --panel: #151a23;
        --panel-2: #1b2230;
        --text: #f3f5f7;
        --muted: #a9b2c3;
        --accent: #4f7cff;
        --accent-2: #3a5ee0;
        --border: #2a3447;
        --accent: #6c5cff;
        --accent-2: #4f7cff;
    }

    .stApp {
        background-color: var(--bg);
        color: var(--text);
    }

    section[data-testid="stSidebar"] {
        background-color: var(--panel);
        border-right: 1px solid var(--border);
    }

    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: var(--text);
    }

    .stCaption {
        color: var(--muted) !important;
    }

    div[data-baseweb="select"] > div {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    .stTextInput input, .stChatInput input {
        background-color: var(--panel-2) !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
    }

    .stButton > button {
        background-color: var(--accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }

    .stButton > button:hover {
        opacity: 0.92;
    }

    div[data-testid="stInfo"] {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        color: var(--text) !important;
    }

    hr {
        border-color: var(--border) !important;
    }

    .hero-advanced {
        padding: 30px 32px;
        border-radius: 22px;
        background: linear-gradient(135deg, #1b2230 0%, #111826 100%);
        border: 1px solid #2a3447;
        margin-bottom: 20px;
    }

    .hero-title-advanced {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero-subtitle-advanced {
        color: #a9b2c3;
        margin-bottom: 16px;
        font-size: 1.05rem;
    }

    .hero-features {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    .hero-badge {
        padding: 6px 12px;
        border-radius: 999px;
        background-color: #151a23;
        border: 1px solid #2a3447;
        font-size: 0.85rem;
        color: #cfd6e4;
    }

    .card {
        padding: 20px;
        border-radius: 18px;
        background: linear-gradient(135deg, #151a23 0%, #1b2230 100%);
        border: 1px solid #2a3447;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
        transition: 0.2s ease;
        margin-bottom: 12px;
    }

    .card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .card-title {
        font-size: 0.9rem;
        color: #a9b2c3;
        margin-bottom: 6px;
    }

    .card-value {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f3f5f7;
    }

    .chat-shell {
        padding: 18px;
        border-radius: 20px;
        background: linear-gradient(135deg, #151a23 0%, #111826 100%);
        border: 1px solid #2a3447;
        min-height: 220px;
        margin-bottom: 12px;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #6c5cff 0%, #4f7cff 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 6px 18px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        width: fit-content;
        text-align: left;
        box-shadow: 0 10px 25px rgba(108, 92, 255, 0.35);
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .chat-bubble-bot {
        background-color: #6c5cff;
        border: 1px solid #2a3447;
        color: #f3f5f7;
        padding: 12px 16px;
        border-radius: 16px 16px 16px 4px;
        margin: 8px auto 8px 0;
        max-width: 75%;
        width: fit-content;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.18);
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    .chat-empty {
        color: #a9b2c3;
        padding: 12px 2px 4px 2px;
    }
</style>
""", unsafe_allow_html=True)


def render_bubble(role: str, content: str) -> None:
    safe_content = html.escape(content).replace("\n", "<br>")
    bubble_class = "chat-bubble-user" if role == "user" else "chat-bubble-bot"
    st.markdown(
        f'<div class="{bubble_class}">{safe_content}</div>',
        unsafe_allow_html=True
    )


# -------- Session State --------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "facts" not in st.session_state:
    st.session_state.facts = load_facts()

if "mode" not in st.session_state:
    st.session_state.mode = "default"

# -------- Sidebar --------
with st.sidebar:
    st.title("Control Panel")
    st.markdown("---")

    selected_mode = st.selectbox(
        "Select Mode",
        ["default", "teacher", "coder", "translator"],
        index=["default", "teacher", "coder", "translator"].index(st.session_state.mode),
        key="mode_selector"
    )
    st.session_state.mode = selected_mode

    st.markdown("---")
    st.subheader("User Facts")

    if st.session_state.facts:
        for k, v in st.session_state.facts.items():
            st.markdown(f"**{k.replace('_', ' ').title()}**")
            st.caption(v)
    else:
        st.info("No facts stored yet.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    with col2:
        if st.button("Clear Facts", use_container_width=True):
            st.session_state.facts = {}
            save_facts({})
            st.rerun()

# -------- Hero --------
st.markdown("""
<div class="hero-advanced">
    <div class="hero-title-advanced">🤖 🧠 NeuroChat AI</div>
    <div class="hero-subtitle-advanced">
        An intelligent AI assistant powered by memory, hybrid reasoning, and adaptive response modes.
    </div>
    <div class="hero-features">
        <div class="hero-badge">Memory System</div>
        <div class="hero-badge">Hybrid AI</div>
        <div class="hero-badge">Intent Detection</div>
        <div class="hero-badge">Multi-Mode</div>
        <div class="hero-badge">Streamlit UI</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------- Metrics --------
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Mode", st.session_state.mode)

with m2:
    st.metric("Messages", len(st.session_state.messages))

with m3:
    st.metric("Facts", len(st.session_state.facts))

with m4:
    last_input = "N/A"
    if st.session_state.messages:
        for item in reversed(st.session_state.messages):
            if item["role"] == "user":
                last_input = item["content"][:20]
                break
    st.metric("Last Input", last_input)

# -------- Top Cards --------
top_col1, top_col2, top_col3 = st.columns(3)

with top_col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Mode</div>
        <div class="card-value">{st.session_state.mode}</div>
    </div>
    """, unsafe_allow_html=True)

with top_col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Messages</div>
        <div class="card-value">{len(st.session_state.messages)}</div>
    </div>
    """, unsafe_allow_html=True)

with top_col3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Stored Facts</div>
        <div class="card-value">{len(st.session_state.facts)}</div>
    </div>
    """, unsafe_allow_html=True)

# -------- Chat Area --------
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        '<div class="chat-empty">Start the conversation by typing a message below.</div>',
        unsafe_allow_html=True
    )

for msg in st.session_state.messages:
    render_bubble(msg["role"], msg["content"])

st.markdown('</div>', unsafe_allow_html=True)

# -------- Chat Input --------
user_input = st.chat_input("Type your message...")

if user_input:
    # show user message instantly
    render_bubble("user", user_input)

    # 1) extract and save facts
    new_facts = extract_facts_from_message(user_input)
    for k, v in new_facts.items():
        st.session_state.facts = update_fact(st.session_state.facts, k, v)

    # 2) save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 3) hybrid answer from facts
    direct_answer = answer_from_facts(user_input, st.session_state.facts)
    if direct_answer is not None:
        render_bubble("assistant", direct_answer)
        st.session_state.messages.append({"role": "assistant", "content": direct_answer})
        st.stop()

    # 4) intent
    intent = detect_intent(user_input)

    active_mode = st.session_state.mode
    if intent == "translation":
        active_mode = "translator"
    elif intent == "coding":
        active_mode = "coder"

    # 5) llm
    response = ask_llm(
        st.session_state.messages,
        mode=active_mode,
        facts=st.session_state.facts
    )

    render_bubble("assistant", response)
    st.session_state.messages.append({"role": "assistant", "content": response})