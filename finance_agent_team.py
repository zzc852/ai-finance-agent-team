import os

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()   #加载 .env文件


def get_dashscope_model() -> OpenAIChat:   #模型配置      
    """Use Alibaba Cloud DashScope through its OpenAI-compatible endpoint."""
    return OpenAIChat(                       #创建一个大模型对象
        id=os.getenv("DASHSCOPE_MODEL", "qwen-max"),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv(
            "DASHSCOPE_API_BASE",
            "https://dashscope.aliyuncs.com/compatible-mode/v1",
        ),
        role_map={
            "system": "system",
            "user": "user",
            "assistant": "assistant",
            "tool": "tool",
            "model": "assistant",
        },
    )


def response_to_text(response) -> str:       #把模型回答转换成文本
    if hasattr(response, "content") and response.content:
        return str(response.content)
    if isinstance(response, str):
        return response
    return str(response)


db = SqliteDb(db_file="agents.db")           #创建数据库和模型实例
llm_model = get_dashscope_model()

web_agent = Agent(                                 #作用是搜索网页
    name="Web Agent",
    role="Search the web for market news and public company information",   #角色说明
    model=llm_model,
    tools=[DuckDuckGoTools()],         #挂载搜索工具
    db=db,                             #保存历史
    add_history_to_context=True,       #历史对话加入上下文
    markdown=True,         #yongmarkdown格式回答
)

finance_agent = Agent(                  #绑定了 YFinanceTools，所以能查股票价格、公司信息、新闻、分析师建议。
    name="Finance Agent",
    role="Get stock prices, company information, news, and analyst recommendations",
    model=llm_model,
    tools=[
        YFinanceTools(
            enable_stock_price=True,
            enable_company_info=True,
            enable_company_news=True,
            enable_analyst_recommendations=True,
        )
    ],
    instructions=[
        "Always use tables to display financial data.",
        "Explain conclusions in concise Chinese unless the user asks for English.",
    ],
    db=db,
    add_history_to_context=True,
    markdown=True,
)

agent_team = Team(       #这是多智能体的核心。它把 web_agent 和 finance_agent 放进一个团队里。
    name="Agent Team (Web+Finance)",
    model=llm_model,
    members=[web_agent, finance_agent],
    instructions=[
        "Coordinate the web agent and finance agent to answer the user's question.",
        "Return a structured Markdown report with key facts, tables, risks, and a short conclusion.",
        "Do not present the result as financial advice.",
    ],
    debug_mode=False,
    markdown=True,
)


def ask_finance_team(question: str) -> str:      #给前端调用的函数Streamlit 页面调用的就是这个函数。
    response = agent_team.run(question)
    return response_to_text(response)


agent_os = AgentOS(teams=[agent_team])
app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="finance_agent_team:app", reload=True)
