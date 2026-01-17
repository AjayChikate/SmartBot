css = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #0f0f0f;
    --bg-secondary: #1a1a1a;
    --bg-tertiary: #252525;
    --bg-elevated: #2d2d2d;
    --accent-primary: #ff2f4c;
    --accent-hover: #e6203e;
    --accent-subtle: rgba(255, 47, 76, 0.12);
    --accent-light: rgba(255, 47, 76, 0.2);
    --text-primary: #f5f5f7;
    --text-secondary: #c5c5ca;
    --text-tertiary: #8e8e93;
    --border-primary: #323236;
    --border-secondary: #454549;
    --border-accent: rgba(255, 47, 76, 0.3);
    --success: #10b981;
    --error: #ff2f4c;
    --red-glow: 0 0 20px rgba(255, 47, 76, 0.3);
}

* {
    font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
}

body, .stApp {
    background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
    color: var(--text-primary);
}

/* ===== PAGE TITLE ===== */
.page-title {
    background: linear-gradient(135deg, rgba(255, 47, 76, 0.1) 0%, rgba(255, 47, 76, 0.05) 100%);
    padding: 2.5rem 3rem;
    border-radius: 12px;
    border: 1.5px solid var(--border-accent);
    margin-bottom: 2rem;
    box-shadow: var(--red-glow);
}

.page-title h1 {
    color: var(--text-primary);
    font-size: 2.2rem;
    margin: 0 0 0.5rem 0;
    font-weight: 700;
    letter-spacing: -0.8px;
    background: linear-gradient(135deg, #ff2f4c 0%, #ff6b7a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-title p {
    color: var(--text-secondary);
    font-size: 0.98rem;
    margin: 0;
    font-weight: 400;
}

/* ===== CHAT MESSAGES ===== */
.chat-message {
    padding: 0;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}

.chat-message.user {
    flex-direction: row-reverse;
    margin-left: 10%;
}

.chat-message.bot {
    margin-right: 10%;
}

.chat-message .message-container {
    background: var(--bg-tertiary);
    padding: 1.25rem 1.5rem;
    border-radius: 12px;
    border: 1px solid var(--border-primary);
    max-width: 650px;
    backdrop-filter: blur(10px);
}

.chat-message.user .message-container {
    background: linear-gradient(135deg, var(--accent-primary) 0%, #ff5a6d 100%);
    border-color: var(--accent-primary);
    box-shadow: 0 8px 24px rgba(255, 47, 76, 0.25);
}

.chat-message.user .message-container {
    background: var(--accent-primary);
    border-color: var(--accent-primary);
}

.chat-message .avatar {
    width: 40px;
    height: 40px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: var(--bg-tertiary);
    border-radius: 10px;
    border: 1.5px solid var(--border-primary);
    transition: all 0.3s ease;
}

.chat-message.user .avatar {
    background: var(--accent-subtle);
    border-color: var(--accent-primary);
    box-shadow: 0 0 12px var(--accent-light);
}

.chat-message .avatar img {
    width: 24px;
    height: 24px;
    border-radius: 4px;
    object-fit: cover;
    filter: brightness(1.1);
}

.chat-message .message {
    color: var(--text-primary);
    font-size: 0.95rem;
    line-height: 1.6;
    font-weight: 400;
}

.chat-message.user .message {
    color: #ffffff;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a1a 0%, #252525 100%);
}

.sidebar-section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--accent-primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, var(--accent-primary) 0%, #ff5a6d 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(255, 47, 76, 0.3);
    width: 100%;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, var(--accent-hover) 0%, #e6203e 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 47, 76, 0.4);
}

/* Sidebar text inputs */
[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: var(--bg-tertiary);
    border: 1.5px solid var(--border-primary);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] .stTextInput > div > div > input:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-subtle);
}

/* Sidebar file uploader */
[data-testid="stSidebar"] .stFileUploader > div {
    background: var(--bg-secondary);
    border: 2px dashed var(--border-accent);
    border-radius: 10px;
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] .stFileUploader > div:hover {
    border-color: var(--accent-primary);
    background: var(--bg-tertiary);
    box-shadow: 0 0 15px var(--accent-light);
}

/* Sidebar expanders */
[data-testid="stSidebar"] .streamlit-expanderHeader {
    background: var(--bg-secondary);
    border: 1.5px solid var(--border-primary);
    border-radius: 10px;
    color: var(--text-primary);
    font-weight: 600;
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
    box-shadow: 0 0 12px var(--accent-light);
}

/* Sidebar selectbox */
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: var(--bg-tertiary);
    border: 1.5px solid var(--border-primary);
    border-radius: 10px;
}

[data-testid="stSidebar"] .stSelectbox > div > div:focus-within {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-subtle);
}

/* Sidebar radio buttons */
[data-testid="stSidebar"] .stRadio > div {
    color: var(--text-primary);
}

[data-testid="stSidebar"] .stRadio > div > label {
    font-weight: 500;
}

/* Sidebar checkboxes */
[data-testid="stSidebar"] .stCheckbox > div {
    color: var(--text-primary);
}

/* Sidebar metric cards */
[data-testid="stSidebar"] .stMetric {
    background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border: 1.5px solid var(--border-accent);
    transition: all 0.3s ease;
}

[data-testid="stSidebar"] .stMetric:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 4px 16px var(--accent-light);
}
/* ===== SOURCE BOXES ===== */
.source-box {
    background: linear-gradient(135deg, rgba(255, 47, 76, 0.08) 0%, rgba(255, 47, 76, 0.03) 100%);
    padding: 1.25rem;
    border-radius: 10px;
    margin: 1rem 0;
    color: var(--text-secondary);
    border: 1.5px solid var(--border-accent);
    font-size: 0.9rem;
    line-height: 1.6;
    font-family: 'JetBrains Mono', monospace;
    transition: all 0.3s ease;
}

.source-box:hover {
    border-color: var(--accent-primary);
    background: linear-gradient(135deg, rgba(255, 47, 76, 0.12) 0%, rgba(255, 47, 76, 0.06) 100%);
    box-shadow: 0 4px 16px var(--accent-light);
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-primary) 0%, #ff5a6d 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.8rem 2rem;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    box-shadow: 0 4px 15px rgba(255, 47, 76, 0.3);
}

.stButton > button:hover {
    background: linear-gradient(135deg, var(--accent-hover) 0%, #e6203e 100%);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(255, 47, 76, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-primary) 0%, #ff5a6d 100%);
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: var(--bg-secondary);
    border: 1.5px solid var(--border-primary);
    border-radius: 10px;
    color: var(--text-primary);
    font-weight: 600;
    transition: all 0.3s ease;
}

.streamlit-expanderHeader:hover {
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
    box-shadow: 0 0 12px var(--accent-light);
}

/* ===== FILE UPLOADER ===== */
.stFileUploader > div {
    background: var(--bg-secondary);
    border: 2px dashed var(--border-primary);
    border-radius: 10px;
    transition: all 0.3s ease;
}

.stFileUploader > div:hover {
    border-color: var(--accent-primary);
    background: var(--bg-tertiary);
    box-shadow: 0 0 15px var(--accent-light);
}

/* ===== TEXT INPUT ===== */
.stTextInput > div > div > input {
    background: var(--bg-tertiary);
    border: 1.5px solid var(--border-primary);
    color: var(--text-primary);
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-subtle);
    outline: none;
}

/* ===== CHAT INPUT ===== */
.stChatInput > div {
    background: var(--bg-tertiary);
    border: 1.5px solid var(--border-primary);
    border-radius: 12px;
    transition: all 0.3s ease;
}

.stChatInput > div:focus-within {
    border-color: var(--accent-primary);
    box-shadow: 0 0 0 3px var(--accent-subtle);
}

/* ===== METRIC CARDS ===== */
.stMetric {
    background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid var(--border-primary);
    transition: all 0.3s ease;
}

.stMetric:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 4px 16px var(--accent-light);
}

/* ===== DIVIDER ===== */
hr {
    border-color: var(--accent-primary);
    margin: 1.5rem 0;
    opacity: 0.5;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--bg-primary);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--accent-primary) 0%, #ff5a6d 100%);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, var(--accent-hover) 0%, #e6203e 100%);
}

/* ===== RADIO & CHECKBOX ===== */
.stRadio > div, .stCheckbox > div {
    color: var(--text-primary);
}

/* ===== CAPTION ===== */
.stCaption {
    color: var(--text-tertiary);
    font-size: 0.85rem;
}

/* ===== SPINNER ===== */
.stSpinner > div {
    border-top-color: var(--accent-primary) !important;
}

/* ===== CODE BLOCKS ===== */
code {
    background: var(--bg-tertiary);
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
    color: #ff6b7a;
    border: 1px solid var(--border-accent);
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ff2f4c' stroke-width='2'%3E%3Cpath d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/%3E%3C/svg%3E" alt="AI">
    </div>
    <div class="message-container">
        <div class="message">{{MSG}}</div>
    </div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2'%3E%3Ccircle cx='12' cy='8' r='5'/%3E%3Cpath d='M20 21a8 8 0 1 0-16 0'/%3E%3C/svg%3E" alt="User">
    </div>
    <div class="message-container">
        <div class="message">{{MSG}}</div>
    </div>
</div>
'''