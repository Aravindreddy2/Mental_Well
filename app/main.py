import sys, os
import streamlit as st
import re

# Ensure the app can find the local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.rag_engine import get_response
from app.emotion_detector import detect_emotion
from app.notifier import send_alert

# ---------------------------------------------------------
# 🔧 PAGE CONFIGURATION & TOTAL UI OVERRIDE
# ---------------------------------------------------------
st.set_page_config(page_title="Youth Wellness Agent", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0E0E10 !important; color: #FFFFFF !important; }
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #000000 !important;
    color: #FFFFFF !important;
    padding: 15px 20px;
    font-size: 1.4rem;
    font-weight: 700;
    border-bottom: 1px solid #2D2D30;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 60px;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0) !important;
    top: 60px !important;
    height: 40px !important;
}
.chat-wrapper {
    max-width: 850px;
    margin: auto;
    padding: 20px 20px 150px 20px;
}
.content-spacer { height: 100px; }
.user-bubble {
    background-color: #1E1F20;
    color: #FFFFFF;
    padding: 1.2rem;
    border-radius: 1.2rem;
    margin-bottom: 1.5rem;
    border: 1px solid #3C4043;
}
.agent-bubble {
    background-color: transparent;
    color: #F0F0F0;
    padding: 1.2rem;
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    line-height: 1.7;
}
.gradient-text {
    background: linear-gradient(to right, #4285F4, #9B72CB, #D96570);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: bold;
    font-size: 3.5rem;
}
[data-testid="stSidebar"] {
    background-color: #171719 !important;
    border-right: 1px solid #2D2D30 !important;
    padding-top: 20px;
}
.stTextInput input {
    background-color: #1E1F20 !important;
    color: #FFFFFF !important;
    border: 1px solid #3C4043 !important;
    border-radius: 32px !important;
    padding: 18px 25px !important;
}
footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 🧩 STATE MANAGEMENT
# ---------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "parent_email" not in st.session_state:
    st.session_state.parent_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_page" not in st.session_state:
    st.session_state.current_page = "Chat"

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

access_ready = is_valid_email(st.session_state.parent_email) and len(st.session_state.user_name) > 1

# ---------------------------------------------------------
# 🏙️ TOP NAV BAR
# ---------------------------------------------------------
st.markdown('<div class="fixed-header">🧠 Youth Wellness AI Agent</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# ⬅️ SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-top: 60px;'>Menu</h2>", unsafe_allow_html=True)
    if st.button("💬 Chat"):
        st.session_state.current_page = "Chat"
        st.rerun()
    if st.button("⚙️ Settings"):
        st.session_state.current_page = "Settings"
        st.rerun()
    st.markdown("---")
    if st.button("🗑️ New Chat"):
        st.session_state.chat_history = []
        st.session_state.current_page = "Chat"
        st.rerun()

# ---------------------------------------------------------
# ⚙️ SETTINGS PAGE
# ---------------------------------------------------------
if st.session_state.current_page == "Settings":
    st.markdown("<div class='chat-wrapper'><div class='content-spacer'></div>", unsafe_allow_html=True)
    st.markdown("<h1 class='gradient-text'>Settings</h1>", unsafe_allow_html=True)

    name_input = st.text_input(
        "Your Name",
        value=st.session_state.user_name,
        placeholder="Enter your name"
    )

    email_input = st.text_input(
        "Trusted Contact Email",
        value=st.session_state.parent_email,
        placeholder="parent@example.com"
    )

    # ✅ NEW BUTTON (ONLY ADDITION)
    if st.button("➡️ Proceed to Chat"):
        if name_input and email_input and is_valid_email(email_input):
            st.session_state.user_name = name_input
            st.session_state.parent_email = email_input
            st.session_state.current_page = "Chat"
            st.rerun()
        else:
            st.error("❌ Please enter a valid name and email.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 💬 CHAT PAGE
# ---------------------------------------------------------
else:
    st.markdown("<div class='chat-wrapper'><div class='content-spacer'></div>", unsafe_allow_html=True)

    if not st.session_state.chat_history:
        greeting_name = st.session_state.user_name if st.session_state.user_name else ""
        st.markdown(f"<h1 class='gradient-text'>Hello {greeting_name}.</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #C4C7C5;'>How can I help you today?</h2>", unsafe_allow_html=True)

    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(
                f"<div class='user-bubble'><b>{st.session_state.user_name}</b><br>{entry['content']}</div>",
                unsafe_allow_html=True
            )
        elif entry["role"] == "agent":
            st.markdown(
                f"<div class='agent-bubble'><b>Agent</b><br>{entry['content']}</div>",
                unsafe_allow_html=True
            )
        elif entry["role"] == "emotion":
            st.markdown(
                f"<span style='color:#8AB4F8;font-size:0.8rem;'>✨ {entry['content']}</span>",
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='position: fixed; bottom: 0; width: 100%; background: #0E0E10; padding: 20px;'>",
        unsafe_allow_html=True
    )

    _, center_col, _ = st.columns([0.15, 0.7, 0.15])
    with center_col:
        if not access_ready:
            st.warning("⚠️ Go to Settings and enter your Name and Email.")

        with st.form("chat_form", clear_on_submit=True):
            cols = st.columns([0.92, 0.08])
            user_input = cols[0].text_input(
                "",
                placeholder="Enter here ...",
                label_visibility="collapsed",
                disabled=not access_ready
            )
            submit = cols[1].form_submit_button("↑", disabled=not access_ready)

        if submit and user_input and access_ready:
            emotion, score = detect_emotion(user_input)
            agent_reply = get_response(user_input)

            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append(
                {"role": "emotion", "content": f"{emotion} ({int(score*100)}%)"}
            )
            st.session_state.chat_history.append({"role": "agent", "content": agent_reply})

            if emotion.lower() in ["sadness", "fear", "anger"] and score > 0.8:
                alert_msg = (
                    f"USER NAME: {st.session_state.user_name}\n"
                    f"EMOTION: {emotion} ({int(score*100)}%)\n"
                    f"MESSAGE: {user_input}"
                )
                send_alert("⚠️ Wellness Alert", alert_msg, st.session_state.parent_email)

            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    
