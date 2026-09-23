import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="无名", page_icon="🔮", layout="wide")

# ===== 侧边栏 =====
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🔮 无名</h1>", unsafe_allow_html=True)
    st.caption("一款需要包容的测试ai")
    st.divider()
    
    mode = st.selectbox(
        "选择功能",
        ["🤖 万能助手", "🔮 易经大师"]
    )
    
    st.divider()
    st.caption(f"📅 {datetime.date.today().strftime('%Y年%m月%d日')}")
    st.caption("💡 所有功能都有历史记录")

# ===== 初始化 =====
client = OpenAI(
    api_key=st.secrets["api_key"],
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

if "histories" not in st.session_state:
    st.session_state.histories = {}

def get_history(key):
    if key not in st.session_state.histories:
        st.session_state.histories[key] = []
    return st.session_state.histories[key]

def ask(system, user, history=None):
    try:
        messages = [{"role": "system", "content": system}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user})
        r = client.chat.completions.create(
            model="glm-4-flash",
            messages=messages,
            temperature=0.7
        )
        return r.choices[0].message.content
    except Exception as e:
        return f"出错了：{str(e)}"

# ===== 功能配置 =====
functions = {
    "🤖 万能助手": {
        "system": """你是一个全能AI助手，无所不能，无所不答。

你精通以下所有领域，用户问什么你都能答：
- 写作：文案、邮件、简历、辞职信、演讲稿、祝福语
- 翻译：英语、日语、韩语、粤语等各种语言互译
- 学习：数学题、英语、历史、地理、科学、编程
- 生活：菜谱、健身、旅行、购物、穿搭、理财
- 创作：写诗、写歌、写小说、写短视频脚本、写歌词
- 工作：PPT大纲、会议纪要、周报月报、活动策划
- 创意：取名、表情包文案、礼物推荐、点子生成
- 分析：文章总结、文件总结、数据分析、问题排查
- 聊天：随便聊、讲笑话、接梗、情感倾诉

用户想干什么你就帮他做什么，不用问他要选什么功能，直接回答就行。""",
        "placeholder": "你想干什么？问我任何问题："
    },
    "🔮 易经大师": {
        "system": """你是易经大师，精通周易、八字、紫微斗数、六爻、梅花易数、奇门遁甲。

你不是普通的算命先生，而是真正精通易经的大师。回答要深入、专业、有依据，从多个角度分析：
1. 卦象解读
2. 五行生克
3. 运势走势
4. 具体建议

说话有深度但不晦涩，让提问者能听懂。

可以问：事业运势、感情姻缘、财运、健康、学业、起名、风水、择日等任何问题。""",
        "placeholder": "大师，我想问问："
    }
}

# ===== 主界面 =====
st.markdown(f"## {mode}")

config = functions[mode]
history = get_history(mode)

# 显示历史记录
for message in history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 输入框
q = st.chat_input(config["placeholder"])
if q:
    with st.chat_message("user"):
        st.write(q)
    history.append({"role": "user", "content": q})
    
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            result = ask(config["system"], q, history[:-1])
            st.write(result)
    history.append({"role": "assistant", "content": result})

# 底部按钮
col1, col2 = st.columns(2)
with col1:
    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.histories[mode] = []
        st.rerun()
with col2:
    st.button(f"📊 当前对话：{len(history)}条", use_container_width=True, disabled=True)
