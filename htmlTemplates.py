css = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-dark: #1a1a2e;
    --secondary-dark: #16213e;
    --accent-gold: #e94560;
    --accent-blue: #0f3460;
    --text-light: #eaeaea;
    --text-dim: #a0a0a0;
}

* {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 50%, #1a1a2e 100%);
    padding: 3rem 2rem;
    border-radius: 25px;
    text-align: center;
    margin-bottom: 2.5rem;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(233, 69, 96, 0.2);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at 50% 50%, rgba(233, 69, 96, 0.1) 0%, transparent 70%);
    pointer-events: none;
}

.header-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.main-header h1 {
    color: #eaeaea;
    font-size: 3rem;
    margin: 0;
    font-weight: 700;
    letter-spacing: -1px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
    position: relative;
}

.main-header p {
    color: #a0a0a0;
    font-size: 1.2rem;
    margin-top: 1rem;
    font-weight: 400;
    position: relative;
}

.chat-message {
    padding: 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    display: flex;
    align-items: flex-start;
    backdrop-filter: blur(10px);
    animation: slideIn 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.chat-message:hover {
    transform: translateX(-5px);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-message.user {
    background: linear-gradient(135deg, #e94560 0%, #c42847 100%);
    margin-left: 4rem;
    box-shadow: 0 8px 25px rgba(233, 69, 96, 0.3);
}

.chat-message.bot {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    margin-right: 4rem;
    box-shadow: 0 8px 25px rgba(15, 52, 96, 0.3);
}

.chat-message .avatar {
    width: 60px;
    height: 60px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    margin-right: 1.5rem;
}

.chat-message .avatar img {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

.chat-message .message {
    flex: 1;
    color: #eaeaea;
    font-size: 1.05rem;
    line-height: 1.9;
    font-weight: 400;
}

.empty-state {
    text-align: center;
    padding: 6rem 2rem;
    background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
    border-radius: 25px;
    margin: 3rem 0;
    border: 1px solid rgba(233, 69, 96, 0.2);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.empty-state-icon {
    font-size: 6rem;
    margin-bottom: 2rem;
    animation: float 3s ease-in-out infinite;
    filter: drop-shadow(0 5px 15px rgba(233, 69, 96, 0.3));
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-15px); }
}

.empty-state-text {
    font-size: 1.8rem;
    color: #eaeaea;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.empty-state-subtext {
    font-size: 1.1rem;
    color: #a0a0a0;
    font-weight: 400;
}

.sidebar-header {
    font-size: 1.2rem;
    font-weight: 600;
    color: #eaeaea;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(233, 69, 96, 0.3);
}

.file-counter {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    color: #eaeaea;
    font-weight: 600;
    margin-top: 1rem;
    border: 1px solid rgba(233, 69, 96, 0.2);
}

.sidebar-footer {
    text-align: center;
    color: #a0a0a0;
    font-size: 0.9rem;
    padding: 1rem;
    margin-top: 1rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.source-box {
    background: linear-gradient(135deg, #16213e 0%, #1a1a2e 100%);
    padding: 1.5rem;
    border-radius: 15px;
    margin: 1rem 0;
    color: #eaeaea;
    border: 1px solid rgba(233, 69, 96, 0.2);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    font-size: 0.95rem;
    line-height: 1.7;
}

.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #e94560 0%, #c42847 100%);
}

.stButton > button {
    background: linear-gradient(135deg, #e94560 0%, #c42847 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.75rem 2rem;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(233, 69, 96, 0.3);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(233, 69, 96, 0.4);
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://api.dicebear.com/7.x/bottts/svg?seed=AI&backgroundColor=0f3460" alt="AI">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=User&backgroundColor=e94560" alt="User">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''