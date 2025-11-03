import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.rag_engine import get_response
from app.emotion_detector import detect_emotion
from app.notifier import send_alert  # ✅ Import notifier

# -------------------------------#
# 🔧 Page Setup
# -------------------------------#
st.set_page_config(page_title="🧠 Youth Wellness Agent", layout="centered")

# 🧠 Header
st.markdown("""
    <style>
        body {
            background-color: #f9fafc;
        }
        .chat-container {
            background: #ffffff;
            border-radius: 1rem;
            padding: 1rem 1.2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        }
        .user-bubble {
            background-color: #e8f0fe;
            padding: 0.8rem 1rem;
            border-radius: 1rem;
            margin-bottom: 0.5rem;
        }
        .agent-bubble {
            background-color: #d1f7c4;
            padding: 0.8rem 1rem;
            border-radius: 1rem;
            margin-bottom: 0.5rem;
        }
        .emotion-bubble {
            background-color: #fff3cd;
            padding: 0.7rem 1rem;
            border-radius: 0.8rem;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }
        .title {
            text-align: center;
            font-size: 2rem;
            color: #1e3a8a;
            margin-bottom: 0.3rem;
        }
        .subtitle {
            text-align: center;
            font-size: 1rem;
            color: #555;
            margin-bottom: 1.2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title">🧠 Youth Wellness AI Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Talk freely — I’ll listen and respond with kindness 💬</p>', unsafe_allow_html=True)

# -------------------------------#
# 🧩 Session States
# -------------------------------#
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "parent_email" not in st.session_state:
    st.session_state.parent_email = ""

# -------------------------------#
# 📧 Email Section
# -------------------------------#
st.markdown("### 👨‍👩‍👧 Trusted Contact Email (optional)")
st.session_state.parent_email = st.text_input(
    "Enter a trusted person’s email:",
    value=st.session_state.parent_email,
    placeholder="e.g. parent@example.com"
)

st.divider()

# -------------------------------#
# 💬 Chat Input
# -------------------------------#
user_input = st.text_area("💬 What’s on your mind today?")

if st.button("Send"):
    if user_input.strip():
        with st.spinner("Thinking empathetically..."):
            emotion, score = detect_emotion(user_input)
            agent_reply = get_response(user_input)

            st.session_state.chat_history.append(("user", user_input))
            st.session_state.chat_history.append(("agent", agent_reply))
            st.session_state.chat_history.append(("emotion", f"{emotion} ({score:.2f})"))

            # 🚨 Alert if distress detected
            if emotion.lower() in ["sadness", "depression", "fear", "anger"] and score > 0.8:
                if st.session_state.parent_email:
                    subject = "⚠️ Mental Health Alert - Youth Wellness Agent"
                    message = (
                        f"The user expressed signs of {emotion} (confidence {score:.2f}).\n\n"
                        f"🧍‍♂️ User said:\n{user_input}\n\n"
                        f"🤖 Agent replied:\n{agent_reply}\n\n"
                        f"Please reach out to check on them."
                    )
                    send_alert(subject, message, to_email=st.session_state.parent_email)
                    st.warning(f"⚠️ Alert sent to {st.session_state.parent_email}.")
                else:
                    st.warning("⚠️ Detected distress, but no email was provided for alerting.")

# -------------------------------#
# 🧾 Chat History Display
# -------------------------------#
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div class='chat-container user-bubble'>🧍‍♂️ <b>You:</b> {msg}</div>", unsafe_allow_html=True)
    elif sender == "agent":
        st.markdown(f"<div class='chat-container agent-bubble'>🤖 <b>Agent:</b> {msg}</div>", unsafe_allow_html=True)
    elif sender == "emotion":
        st.markdown(f"<div class='chat-container emotion-bubble'>❤️ <b>Detected Emotion:</b> {msg}</div>", unsafe_allow_html=True)
