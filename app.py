import streamlit as st
from openai import OpenAI

st.title("无名")

client = OpenAI(
    api_key=st.secrets["api_key"],
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

q = st.text_input("问无名点什么：")
if st.button("发送"):
    r = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": q}]
    )
    st.write(r.choices[0].message.content)
