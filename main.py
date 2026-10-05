import streamlit as st
import json
import os
import datetime

# ========== 配置项 ==========
SESSIONS_DIR = "AI大模型调用/sessions"  # 会话文件保存目录

# ========== 全局初始化（保证变量一定存在，不会报KeyError） ==========
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_session" not in st.session_state:
    # 时间精度改到秒，彻底避免文件名重复覆盖
    st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# ========== 核心功能函数 ==========
def save_session():
    """保存当前会话到本地JSON文件"""
    current_session = st.session_state.get("current_session")
    messages = st.session_state.get("messages", [])

    # 调试：终端打印保存的内容，方便排查
    print("===== 执行保存 =====")
    print("会话ID:", current_session)
    print("消息条数:", len(messages))

    if not current_session:
        st.toast("没有可保存的会话", icon="⚠️")
        return

    # 自动创建多级目录
    if not os.path.exists(SESSIONS_DIR):
        os.makedirs(SESSIONS_DIR)

    session_data = {
        "messages": messages,
        "current_session": current_session
    }

    file_path = os.path.join(SESSIONS_DIR, f"{current_session}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    st.toast(f"会话已保存：{current_session}", icon="✅")
    print("保存成功，文件路径:", file_path)


def load_session(file_name):
    """加载指定的历史会话"""
    file_path = os.path.join(SESSIONS_DIR, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)

    st.session_state.messages = session_data.get("messages", [])
    st.session_state.current_session = session_data.get(
        "current_session",
        file_name.replace(".json", "")
    )

    st.toast(f"已加载会话：{st.session_state.current_session}", icon="📂")
    st.rerun()


def delete_session(file_name):
    """删除指定的历史会话"""
    file_path = os.path.join(SESSIONS_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        st.toast(f"已删除：{file_name.replace('.json', '')}", icon="🗑️")
        st.rerun()


@st.dialog("确认删除会话")
def confirm_delete(file_name):
    """删除前的二次确认弹窗"""
    session_name = file_name.replace(".json", "")
    st.warning(f"确定要永久删除会话「{session_name}」吗？\n\n此操作无法撤销，删除后记录将无法恢复。")

    col_cancel, col_confirm = st.columns(2)
    with col_cancel:
        if st.button("取消", use_container_width=True):
            st.rerun()
    with col_confirm:
        if st.button("确认删除", type="primary", use_container_width=True):
            delete_session(file_name)


def get_session_list():
    """获取所有历史会话，按时间倒序排列"""
    if not os.path.exists(SESSIONS_DIR):
        return []
    # 只读取json文件
    files = [f for f in os.listdir(SESSIONS_DIR) if f.endswith(".json")]
    # 按文件修改时间排序，最新的在最上面
    files.sort(
        key=lambda x: os.path.getmtime(os.path.join(SESSIONS_DIR, x)),
        reverse=True
    )
    return files


# ========== 多页面导航 ==========
pages = [
    st.Page("streamlit调用web接口.py", title="长征", icon=""),
    st.Page("长征.py", title="迈向数字世界", icon=""),
]
pg = st.navigation(pages)

# 压缩侧边栏删除按钮尺寸，不改变侧边栏总宽度
st.markdown(
    """
    <style>
    /* 压缩侧边栏删除按钮尺寸 */
    [data-testid="stSidebar"] button[kind="secondary"] {
        padding-left: 2px !important;
        padding-right: 2px !important;
        min-width: unset !important;
    }

    /* 写入按钮：背景和侧边栏一致，保留默认边框 */
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: transparent !important;
        border-color: rgba(255, 255, 255, 0.2) !important; /* 和普通按钮同款浅边框 */
        color: #fafafa !important;
        box-shadow: none !important;
    }

    /* 鼠标悬停反馈 */
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background-color: rgba(255,255,255,0.06) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== 侧边栏UI ==========
with st.sidebar:
    st.title("人工智能统辖")

    # 保存并新建按钮
    if st.button("写入", width="stretch", type="primary"):
        # 1. 先保存当前有内容的会话
        save_session()
        # 2. 清空消息，生成新的会话ID（带秒，绝对不会和上一个重名）
        st.session_state.messages = []
        st.session_state.current_session = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

        # 3. 保存新的空会话（不需要可以删掉这行）
        save_session()

    st.divider()

    # 历史会话列表
    st.subheader("归档")
    session_list = get_session_list()

    if not session_list:
        st.caption("暂无归档记录")
    else:
        for idx, file_name in enumerate(session_list):
            session_full_name = file_name.replace(".json", "")
            # 只显示前12个字符，超出用省略号，节省横向空间
            show_name = session_full_name[:12] + "..." if len(session_full_name) > 12 else session_full_name

            # 调整列比例，给删除按钮多分配一点空间
            col_load, col_del = st.columns([3.2, 1])
            with col_load:
                if st.button(
                        show_name,
                        key=f"load_{idx}",
                        help=session_full_name,  # 鼠标悬停显示完整名称
                        use_container_width=True
                ):
                    load_session(file_name)
            with col_del:
                if st.button(
                        "🗑️",
                        key=f"del_{idx}",
                        help="删除",
                        type="secondary",
                        use_container_width=True
                ):
                    confirm_delete(file_name)

# ========== 启动页面 ==========
pg.run()
