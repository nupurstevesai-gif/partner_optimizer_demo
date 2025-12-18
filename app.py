import streamlit as st
from llm import answer_query

st.set_page_config(
    page_title="PartnerOptimizer ChatBot", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean, modern look
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e3f 0%, #8b2c47 50%, #ff6b35 100%);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom chat container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Message bubbles */
    .message {
        margin-bottom: 20px;
        padding: 20px 24px;
        border-radius: 12px;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        font-size: 15px;
        line-height: 1.6;
    }
    
    .user-message {
        background: rgba(30, 50, 70, 0.9);
        color: white;
        border: 1px solid rgba(255, 107, 53, 0.3);
    }
    
    .assistant-message {
        background: rgba(15, 25, 40, 0.95);
        color: white;
        border: 1px solid rgba(100, 150, 200, 0.2);
    }
    
    .message-label {
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
        color: rgba(255, 255, 255, 0.8);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Input styling - Force dark from start */
    .stTextInput > div > div > input {
        background-color: rgba(30, 50, 70, 0.9) !important;
        color: white !important;
        border: 2px solid rgba(255, 107, 53, 0.5) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff6b35 !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.3) !important;
        background-color: rgba(30, 50, 70, 0.95) !important;
    }
    
    /* Button styling - Bright and visible */
    .stButton > button {
        background: #ffffff !important;
        color: #1e1e3f !important;
        border: 3px solid #ffffff !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(255, 255, 255, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        background: #ff6b35 !important;
        color: #ffffff !important;
        border: 3px solid #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 30px rgba(255, 107, 53, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
    }
    
    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(20, 20, 40, 0.95);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-top: 2px solid rgba(255, 107, 53, 0.3);
        z-index: 999;
    }
    
    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: flex-end;
    }
    
    /* Spacing for fixed input */
    .main .block-container {
        padding-bottom: 120px;
    }
</style>
""", unsafe_allow_html=True)

# Custom styled heading
st.markdown("<h1 style='color: #ffffff; text-align: center; text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5); margin-bottom: 10px; font-size: 2.5rem;'> PartnerOptimizer ChatBot</h1>", unsafe_allow_html=True)

# Custom styled subtitle
st.markdown("<p style='color: rgba(255, 255, 255, 0.8); text-align: center; font-size: 1.1rem; margin-bottom: 30px;'>Ask questions about PartnerOptimizer products, solutions, and partner intelligence.</p>", unsafe_allow_html=True)

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display chat messages with custom HTML
chat_html = ""
for role, msg in st.session_state.chat:
    # Escape HTML and convert newlines to <br>
    msg_escaped = msg.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')
    
    if role == "user":
        chat_html += f"""
        <div class="message user-message">
            <div class="message-label">You:</div>
            <div>{msg_escaped}</div>
        </div>
        """
    else:
        chat_html += f"""
        <div class="message assistant-message">
            <div class="message-label">PartnerOptimizer:</div>
            <div>{msg_escaped}</div>
        </div>
        """

st.markdown(chat_html, unsafe_allow_html=True)

# Add some spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Custom input area at bottom
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "message",
        placeholder="Ask questions about PartnerOptimizer products, solutions, and partner intelligence",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# Handle input
if send_button and user_input:
    # Add user message
    st.session_state.chat.append(("user", user_input))
    
    # Get assistant response
    with st.spinner("Thinking..."):
        response = answer_query(user_input)
    
    # Add assistant response
    st.session_state.chat.append(("assistant", response))
    
    # Rerun to update chat and clear input
    st.rerun()
