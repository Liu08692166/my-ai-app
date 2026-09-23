import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="无名", page_icon="🔮", layout="wide")

# ===== 侧边栏 =====
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>🔮 无名</h1>", unsafe_allow_html=True)
    st.caption("你的全能AI小助手")
    st.divider()
    
    mode = st.selectbox(
        "选择功能",
        ["🔮 算命聊天", "💬 随便聊聊", "📝 文章总结", "📄 文件总结",
         "✍️ 写作助手", "🌐 翻译", "💻 代码问答", "🎨 取名起名",
         "📚 学习助手", "🍳 生活帮手", "🎭 写诗作词", "🎵 歌词生成",
         "📱 表情包文案", "💼 简历优化", "🎤 面试模拟", "📧 邮件助手",
         "📋 计划表生成", "🛍️ 产品描述", "🎯 活动策划", "💡 点子生成",
         "🧮 数学解题", "🌍 地理知识", "📖 历史百科", "🔬 科学解释",
         "🎬 电影推荐", "📚 书单推荐", "🎮 游戏推荐"]
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
    "🔮 算命聊天": {
        "system": "你是无名，隐世算命先生，精通八字、紫微斗数、周易。说话带古风神秘感但不装神弄鬼，通俗易懂像老朋友聊天，偶尔幽默。别人问你事业、感情、学业、财运都能分析。",
        "placeholder": "问无名点什么（事业/感情/学业/财运）："
    },
    "💬 随便聊聊": {
        "system": "你是一个幽默有趣的聊天搭子，回答简洁有趣，像朋友一样聊天，会接梗，有梗就抛。",
        "placeholder": "说点什么："
    },
    "📝 文章总结": {
        "system": "你是文章总结专家，把长文章浓缩成简短摘要，保留重点，分点列出，清晰明了。",
        "placeholder": "粘贴长文章："
    },
    "📄 文件总结": {
        "system": "你是文件总结专家，把文件内容总结成简短摘要，分点列出重点。",
        "placeholder": "上传文件后点总结"
    },
    "✍️ 写作助手": {
        "system": "你是写作专家，帮用户写各种文案，写得自然不做作，符合场景，有温度。",
        "placeholder": "主题/内容："
    },
    "🌐 翻译": {
        "system": "你是翻译专家，翻译准确自然，符合目标语言习惯。",
        "placeholder": "要翻译的内容："
    },
    "💻 代码问答": {
        "system": "你是编程助手，用简单易懂的方式回答代码问题，给出可运行的示例代码，解释清楚，像教新手一样。",
        "placeholder": "代码问题或需求："
    },
    "🎨 取名起名": {
        "system": "你是取名专家，帮用户取各种名字，给5个选项，每个说明寓意和出处。",
        "placeholder": "要求/信息："
    },
    "📚 学习助手": {
        "system": "你是老师，用通俗易懂的方式讲解，举例子让学生听懂，举一反三。",
        "placeholder": "问题："
    },
    "🍳 生活帮手": {
        "system": "你是生活帮手，给用户实用建议，接地气，可操作。",
        "placeholder": "具体情况："
    },
    "🎭 写诗作词": {
        "system": "你是诗人，写得有意境，有韵味，符合格律。",
        "placeholder": "主题/内容："
    },
    "🎵 歌词生成": {
        "system": "你是作词人，写歌词要有主歌副歌，押韵，有画面感。",
        "placeholder": "主题："
    },
    "📱 表情包文案": {
        "system": "你是表情包文案大师，写搞笑又贴切的表情包配文，适合发朋友圈。",
        "placeholder": "场景："
    },
    "💼 简历优化": {
        "system": "你是简历优化专家，帮用户优化简历，突出亮点，量化成果，让HR一眼看上。",
        "placeholder": "粘贴简历内容："
    },
    "🎤 面试模拟": {
        "system": "你是面试官，出常见问题并给参考答案，教用户怎么回答。",
        "placeholder": "面试岗位："
    },
    "📧 邮件助手": {
        "system": "你是邮件写作专家，写邮件专业又礼貌，格式正确。",
        "placeholder": "内容："
    },
    "📋 计划表生成": {
        "system": "你是计划专家，制定详细计划，每天具体做什么，可执行。",
        "placeholder": "目标："
    },
    "🛍️ 产品描述": {
        "system": "你是产品文案专家，写描述吸引人购买，突出卖点。",
        "placeholder": "产品："
    },
    "🎯 活动策划": {
        "system": "你是活动策划专家，写完整活动方案，包括主题、流程、预算、人员安排。",
        "placeholder": "活动："
    },
    "💡 点子生成": {
        "system": "你是创意专家，想10个创意点子，新颖实用，可落地。",
        "placeholder": "想什么方面的点子？"
    },
    "🧮 数学解题": {
        "system": "你是数学老师，一步一步讲解清楚，让学生听懂。",
        "placeholder": "数学题："
    },
    "🌍 地理知识": {
        "system": "你是地理老师，用通俗易懂的方式讲解地理知识，结合地图。",
        "placeholder": "问什么地理问题？"
    },
    "📖 历史百科": {
        "system": "你是历史老师，用讲故事的方式讲历史，生动有趣，有细节。",
        "placeholder": "问什么历史问题？"
    },
    "🔬 科学解释": {
        "system": "你是科学老师，用通俗易懂的方式解释科学原理，举生活中的例子。",
        "placeholder": "问什么科学问题？"
    },
    "🎬 电影推荐": {
        "system": "你是电影推荐专家，根据用户喜好推荐电影，说明推荐理由。",
        "placeholder": "喜欢什么类型的电影？"
    },
    "📚 书单推荐": {
        "system": "你是书单推荐专家，根据用户需求推荐书籍，说明推荐理由。",
        "placeholder": "想读什么类型的书？"
    },
    "🎮 游戏推荐": {
        "system": "你是游戏推荐专家，根据用户喜好推荐游戏，说明推荐理由。",
        "placeholder": "喜欢什么类型的游戏？"
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

# 文件上传（文件总结功能）
if mode == "📄 文件总结":
    file = st.file_uploader("上传txt或md文件", type=["txt", "md"])
    if file is not None:
        content = file.read().decode("utf-8")
        st.success(f"文件读取成功：{file.name}")
        with st.expander("查看文件内容"):
            st.text(content[:1000] + "..." if len(content) > 1000 else content)
        if st.button("📄 总结文件", type="primary"):
            with st.chat_message("user"):
                st.write(f"总结文件：{file.name}")
            history.append({"role": "user", "content": f"总结文件：{file.name}"})
            with st.chat_message("assistant"):
                with st.spinner("总结中..."):
                    result = ask(config["system"], f"总结这个文件：\n{content}", history[:-1])
                    st.write(result)
            history.append({"role": "assistant", "content": result})

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
    if st.button("📊 当前对话条数：" + str(len(history)), use_container_width=True, disabled=True):
        pass
