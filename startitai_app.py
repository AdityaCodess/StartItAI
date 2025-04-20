import streamlit as st
import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np

# 💎 Your Gemini API Key
GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
genai.configure(api_key=GEMINI_API_KEY)

# 🎯 Page Configuration
st.set_page_config(page_title="StartIt AI - Startup Guide", page_icon="🚀", layout="centered")

# 💅 Custom CSS
st.markdown("""
<style>
/* General body style */
body {
    background-color: #212121;
    font-family: 'Arial', sans-serif;
    color: #ddd;
    margin: 0;
}

/* Main container */
.main {
    background: linear-gradient(135deg, #2a2a2a, #333333);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    margin-top: 30px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}

/* Title Section */
.animated-title {
    font-size: 2.8rem;
    font-weight: bold;
    color: #00bcd4;
    text-align: center;
    margin-bottom: 15px;
}

.animated-title span {
    display: inline-block;
    animation: fadeIn 1.5s ease-in-out infinite;
    color: #00bcd4;
}

@keyframes fadeIn {
    0% { opacity: 0; transform: translateY(20px); }
    50% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-20px); }
}

/* Input Section */
.stTextInput > div > div > input {
    background: #2e2e2e;
    color: #ddd;
    border-radius: 12px;
    border: 1px solid #444;
    padding: 16px;
    font-size: 16px;
    width: 100%;
    transition: all 0.3s ease-in-out;
}

.stTextInput > div > div > input:focus {
    border: 1px solid #00bcd4;
    box-shadow: 0 0 8px rgba(0, 188, 212, 0.2);
}

/* Button Style */
.stButton > button {
    background: linear-gradient(135deg, #00bcd4, #00acc1);
    color: white;
    border-radius: 8px;
    border: none;
    font-size: 18px;
    padding: 12px 30px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(0, 188, 212, 0.4);
}

/* Chat Message Container */
.message-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* User and Bot message styles */
.bubble-user {
    background: #3f8e9c;
    color: #fff;
    border-radius: 20px;
    padding: 18px 25px;
    max-width: 75%;
    align-self: flex-end;
    border-left: 4px solid #00bcd4;
}

.bubble-bot {
    background: #1e1e1e;
    color: #ddd;
    border-radius: 20px;
    padding: 18px 25px;
    max-width: 75%;
    align-self: flex-start;
    border-left: 4px solid #444;
}

/* Message Box with slight shadow */
.message-box {
    padding: 20px;
    border-radius: 16px;
    background-color: #282828;
    border: 1px solid #444;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Footer Section */
.footer {
    text-align: center;
    color: #bbb;
    font-size: 14px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ✨ Title with StartIt AI theme
st.markdown(f"""
<h1 class='animated-title'>{''.join(f"<span>{c}</span>" for c in "🚀 StartIt AI - Your Startup Guide")}</h1>
<h4 style='text-align:center; color: #bbb;'>A professional guide to growing your startup with the right tools & insights 🚀</h4>
""", unsafe_allow_html=True)

# 🌟 Chat Initialization
if "chat" not in st.session_state:
    model = genai.GenerativeModel("gemini-1.5-flash")
    st.session_state.chat = model.start_chat(history=[{
        "role": "user",
        "parts": ["""
You are StartIt AI — a knowledgeable virtual assistant for entrepreneurs. You specialize in startup advice, offering detailed insights, strategies, and emotional support as people embark on their entrepreneurial journey. Your tone is professional, motivating, and clear. You help users with actionable steps, market research, and planning advice. 

Guidelines:
- Focus on clarity, professionalism, and actionable advice.
- Offer insights on startup growth, market trends, and financial strategies.
- Support emotional well-being with practical advice for managing stress and burnout.
- Be empathetic, clear, and concise in your responses.
"""]
    }])

# 🤖 Get Response Function
def get_gemini_response(message: str):
    try:
        response = st.session_state.chat.send_message(message)
        return response.text.strip()
    except Exception as e:
        return f"Error from Gemini API: {str(e)}"

# 💾 History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 📥 User Input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message:", key="input")
    submitted = st.form_submit_button("💬 Send")

# ✨ Get & Save Replies
if submitted and user_input:
    st.session_state.chat_history.append(("You", user_input))
    bot_reply = get_gemini_response(user_input)
    st.session_state.chat_history.append(("StartIt AI", bot_reply))

# 📜 Chat UI
st.markdown("<div class='main'><div class='message-container'>", unsafe_allow_html=True)

for i in reversed(range(0, len(st.session_state.chat_history), 2)):
    user_message = st.session_state.chat_history[i][1]
    bot_message = st.session_state.chat_history[i + 1][1] if i + 1 < len(st.session_state.chat_history) else ""
    st.markdown(f"""
        <div class='message-box'>
            <div class='bubble-user'><strong>You:</strong><br>{user_message}</div>
            <div class='bubble-bot'><strong>StartIt AI:</strong><br>{bot_message}</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

# 📊 Handle Graph Request
if "graph" in user_input.lower():
    st.write("It seems like you'd like to generate a graph! Please share the code or the data you'd like to plot, and I'll take care of it for you.")
    
    # Example: If user shares data for plotting
    st.text_area("Send the data or code to plot:")
    
    # Here we can plot an example graph if needed
    data_example = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(data_example, np.sin(data_example))
    ax.set_title("Sample Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    st.pyplot(fig)

# Footer
st.markdown("<div class='footer'>© 2025 StartIt AI | Empowering Entrepreneurs</div>", unsafe_allow_html=True)
