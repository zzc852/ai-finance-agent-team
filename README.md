# AI Finance Agent Team with Web Access

This local version uses Alibaba Cloud DashScope/Qwen through the OpenAI-compatible API and adds a Streamlit UI.

## Features

- Web Agent for market news and public company information
- Finance Agent for stock prices, company information, news, and analyst recommendations
- Team Coordinator for routing, combining results, and producing a Markdown report
- DuckDuckGo web search, YFinance data tools, and SQLite conversation storage

## Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Then open the local URL printed by Streamlit, usually:

```text
http://localhost:8501
```

You can also run the Agno AgentOS playground:

```powershell
python finance_agent_team.py
```
