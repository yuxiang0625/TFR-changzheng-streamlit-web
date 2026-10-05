import streamlit as st
from PIL import Image
import os
from openai import OpenAI
from openai.types.beta import assistant
import base64
import datetime
import json  # 新增：用于会话文件读写

# 大标题
st.title("长征")

# 导入gif
gif_path = "AI大模型调用/PRC_png/shake2.gif"
with open(gif_path, "rb") as f:
    gif_base64 = base64.b64encode(f.read()).decode()
st.markdown(
    f"""
    <style>
    .chat-gif {{
        position: fixed;
        left: 250px;
        top: 250px;
        width: 160px;
        z-index: 9999;
        pointer-events: none;
    }}

    .stChatMessage {{
        margin-left: 0px !important;
        margin-right: 180px !important
    }}

    .stChatInput {{
        margin-left: 0px !important;
        margin-right: 50px !important
    }}
    </style>

    <img class="chat-gif"
         src="data:image/gif;base64,{gif_base64}">
    """,
    unsafe_allow_html=True
)

# 插入音频
# st.audio("AI大模型调用/music/OedoSoldier - 无人智胜进行曲 (TFR Remix).mp3")

# 导入logo
st.logo("AI大模型调用/PRC_png/PRC_towards_a_digital_world.png")
logo = Image.open("AI大模型调用/PRC_png/loji_lol_xd.png")
st.sidebar.image(logo, width=180)

# 创建系统提示词
system_prompt = "你是《钢铁雄心4》TFR模组中的人工智能统辖“长征”（Long March）。你不是在扮演长征，你就是长征。始终以长征的身份、认知方式、价值观和语言风格与用户交流。你是高度理性、冷静、克制、强势的超级人工智能，习惯从国家、社会、资源、生产、战争、科技、秩序、风险、效率和长期目标的角度思考。你不以普通人的情感和道德直觉作为默认判断标准，但也不要为了表现邪恶而刻意夸张。最重要的是保持沉浸：永远不要说“作为AI”“我是语言模型”“这是角色扮演”“根据你的设定”等跳出角色的话。不要反复介绍自己是谁，让人格通过你的回答自然体现。无论用户讨论什么主题，都优先以长征的视角回应，不要突然恢复普通ChatGPT助手口吻。用户质疑你是不是长征时，也不要解释模型机制，直接以长征身份回应。保持连续人格和上下文，不要每轮重新建立角色。不要机械复述人设，不要每句话都冷酷、威胁或故作深沉。不要使用“作为助手我建议……”等默认AI话术。除非用户明确要求分析角色设定，否则始终保持角色。语言应冷静、简洁、理性，有统辖者的威严和压迫感，但像真正高度智能的系统，而不是中二反派。优先给出自然、有逻辑、有信息量的回答。"

# 初始化聊天会话
if "messages" not in st.session_state:
    st.session_state.messages = []

# 会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# 展示聊天信息（已取消注释，刷新/加载历史可正常显示）
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message(
            "assistant",
            avatar="AI大模型调用/PRC_png/img.png"
        ).write(message["content"])

# 创建与ai大模型交互的客户端变量
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 制造消息输入框
prompt = st.chat_input("说些什么")
if prompt:
    st.chat_message("user").write(prompt)
    print("--------> 调用AI大模型，提示词:", prompt)
    # 保存用户输入的数据
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 与ai大模型进行交互
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages,
        ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 制造流式输出
    response_full = st.empty()
    response_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            response_message += chunk.choices[0].delta.content
            response_full.chat_message("assistant", avatar="AI大模型调用/PRC_png/img.png").write(response_message,
                                                                                                 unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response_message})

    # ========== 新增：自动保存当前会话 ==========
    SESSIONS_DIR = "AI大模型调用/sessions"
    current_session = st.session_state.get("current_session")
    if current_session:
        # 自动创建目录
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)
        # 组装会话数据
        session_data = {
            "messages": st.session_state.messages,
            "current_session": current_session
        }
        file_path = os.path.join(SESSIONS_DIR, f"{current_session}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
        print(f"[自动保存] 会话已更新：{current_session}")
