import asyncio
import os

import streamlit as st
from dotenv import load_dotenv

try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from finance_agent_team import ask_finance_team

load_dotenv()

st.set_page_config(
    page_title="AI Finance Agent Team",
    page_icon="$",
    layout="wide",
)

st.title("AI Finance Agent Team")
st.caption("DashScope/Qwen + Web Agent + Finance Agent + Team Coordinator")

with st.sidebar:
    st.subheader("Model")
    st.code(os.getenv("DASHSCOPE_MODEL", "qwen-max"))
    st.subheader("Examples")
    examples = [
        "分析英伟达 NVDA 最近的股价、公司新闻和分析师建议",
        "Compare Apple and Microsoft from stock price, company news, and analyst recommendations.",
        "请用表格总结 Tesla TSLA 当前股价、公司信息和近期新闻",
    ]
    selected_example = st.radio("Try one", examples, label_visibility="collapsed")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("输入你想分析的公司或股票，例如：分析阿里巴巴 BABA 最近的市场表现")

if st.button("使用示例问题"):
    prompt = selected_example

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("多智能体正在检索网页信息和金融数据..."):
            try:
                answer = ask_finance_team(prompt)
            except Exception as exc:
                answer = (
                    "运行失败，请检查 DashScope API Key、网络连接和依赖安装。\n\n"
                    f"错误信息：`{exc}`"
                )
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
