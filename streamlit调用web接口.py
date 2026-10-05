# 导入streamlit模块为st
import streamlit as st
from PIL import Image


# 配置页面设置
st.set_page_config(
    page_title="人工智能统辖",
    page_icon="AI大模型调用/PRC_png/PRC_towards_a_digital_world.png",
    initial_sidebar_state="expanded",
    menu_items={}
)

# 设置标题
st.title("一")

# 读取文本并写入段落
f = open("D:/长征.txt", "r" ,encoding="utf-8")
lines = f.readlines()

# 把列表拼接成完整字符串
content = "".join(lines)
st.write(content)

# 插入处理好的图片
col1, col2, col3 = st.columns([3,2,3])
with col2:
    st.image("AI大模型调用/PRC_png/shake.gif",width=180)

# 插入音频
# st.audio("AI大模型调用/OedoSoldier - 无人智胜进行曲 (TFR Remix).mp3")

# 导入logo
st.logo("AI大模型调用/PRC_png/PRC_towards_a_digital_world.png")
logo = Image.open("AI大模型调用/PRC_png/loji_lol_xd.png")
st.sidebar.image(logo, width=180)


# 在终端中运行指令-streamlit run xxx.py