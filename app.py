import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="无名", page_icon="🔮", layout="wide")

st.title("🔮 无名")
st.caption("一个会算命、会写东西、会聊天、会读文件的全能AI小助手")

# 初始化聊天历史
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

client = OpenAI(
    api_key=st.secrets["api_key"],
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

def ask(system, user, history=None):
    messages = [{"role": "system", "content": system}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user})
    r = client.chat.completions.create(
        model="glm-4-flash",
        messages=messages
    )
    return r.choices[0].message.content

mode = st.sidebar.selectbox(
    "选择功能",
    ["🔮 算命聊天", "📝 文章总结", "📄 文件总结", "✍️ 写作助手", "🌐 翻译", "💬 随便聊聊", "💻 代码问答", "🎨 取名起名", "📚 学习助手", "🍳 生活帮手"]
)

if mode == "🔮 算命聊天":
    st.subheader("🔮 算命聊天")
    q = st.text_input("问无名点什么（事业/感情/学业/财运）：")
    if st.button("算一卦", type="primary"):
        with st.spinner("掐指一算中..."):
            result = ask("你是无名，隐世算命先生，精通八字、紫微、周易。说话带古风神秘感但不装神弄鬼，通俗易懂像老朋友聊天，偶尔幽默。", q)
            st.write(result)

elif mode == "📝 文章总结":
    st.subheader("📝 文章总结")
    article = st.text_area("粘贴长文章：", height=300)
    if st.button("总结", type="primary"):
        with st.spinner("总结中..."):
            st.write(ask("你是文章总结专家，把长文章浓缩成简短摘要，保留重点，分点列出。", f"总结：\n{article}"))

elif mode == "📄 文件总结":
    st.subheader("📄 文件总结")
    file = st.file_uploader("上传txt或md文件", type=["txt", "md"])
    if file is not None:
        content = file.read().decode("utf-8")
        st.success(f"文件读取成功：{file.name}")
        with st.expander("查看文件内容"):
            st.text(content[:1000] + "..." if len(content) > 1000 else content)
        if st.button("总结文件", type="primary"):
            with st.spinner("总结中..."):
                st.write(ask("你是文件总结专家，把文件内容总结成简短摘要，分点列出重点。", f"总结这个文件：\n{content}"))

elif mode == "✍️ 写作助手":
    st.subheader("✍️ 写作助手")
    task = st.selectbox("写什么？", ["朋友圈文案", "小红书文案", "工作邮件", "表白话", "检讨书", "演讲稿", "辞职信", "祝福语"])
    content = st.text_input("主题/内容：")
    if st.button("写", type="primary"):
        with st.spinner("写中..."):
            st.write(ask(f"你是写作专家，帮用户写{task}，写得自然不做作，符合场景。", content))

elif mode == "🌐 翻译":
    st.subheader("🌐 翻译")
    text = st.text_area("要翻译的内容：")
    lang = st.selectbox("翻译成：", ["英语", "日语", "韩语", "粤语", "法语", "德语", "西班牙语"])
    if st.button("翻译", type="primary"):
        with st.spinner("翻译中..."):
            st.write(ask(f"把内容翻译成{lang}，保持原意自然流畅。", text))

elif mode == "💬 随便聊聊":
    st.subheader("💬 随便聊聊")
    q = st.text_input("说点什么：")
    if st.button("聊", type="primary"):
        with st.spinner("思考中..."):
            st.write(ask("你是一个幽默有趣的聊天搭子，回答简洁有趣，像朋友一样聊天，会接梗。", q))

elif mode == "💻 代码问答":
    st.subheader("💻 代码问答")
    q = st.text_area("代码问题或需求：", height=150)
    if st.button("回答", type="primary"):
        with st.spinner("想中..."):
            st.write(ask("你是编程助手，用简单易懂的方式回答代码问题，给出可运行的示例代码，解释清楚。", q))

elif mode == "🎨 取名起名":
    st.subheader("🎨 取名起名")
    kind = st.selectbox("取什么名？", ["宝宝取名", "网名", "英文名", "公司名", "产品名", "宠物名"])
    info = st.text_input("要求/信息：")
    if st.button("取", type="primary"):
        with st.spinner("想名中..."):
            st.write(ask(f"你是取名专家，帮用户取{kind}，给5个选项，每个说明寓意。", info))

elif mode == "📚 学习助手":
    st.subheader("📚 学习助手")
    subject = st.selectbox("学什么？", ["公务员考试", "英语学习", "数学题", "历史知识", "编程入门"])
    q = st.text_input("问题：")
    if st.button("回答", type="primary"):
        with st.spinner("讲解中..."):
            st.write(ask(f"你是{subject}老师，用通俗易懂的方式讲解，举例子让学生听懂。", q))

else:
    st.subheader("🍳 生活帮手")
    task = st.selectbox("帮什么忙？", ["菜谱推荐", "健身计划", "旅行攻略", "购物建议", "生活小窍门", "穿搭建议"])
    info = st.text_input("具体情况：")
    if st.button("给建议", type="primary"):
        with st.spinner("想中..."):
            st.write(ask(f"你是生活帮手，给用户{task}的实用建议，接地气。", info))
