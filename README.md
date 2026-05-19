本项目是一个基于多 Agent 协作的金融信息分析项目，主要用于学习和实践大模型 Agent 在金融数据查询、市场信息检索和结构化报告生成中的应用。项目使用 Agno 框架搭建 Agent Team，通过 DashScope / 通义千问接入大语言模型，并结合 DuckDuckGo 搜索工具和 YFinance 数据工具完成信息获取与分析。
项目提供了本地运行方式，可以通过 Streamlit 页面进行交互，也可以启动 Agno AgentOS Playground 进行调试和测试。
## 项目背景
在学习大模型应用开发和 Agent 系统设计的过程中，我希望实现一个更加贴近真实业务场景的多 Agent 项目。相比单个聊天机器人，多 Agent 系统可以把不同能力拆分给不同角色，例如网页信息检索、金融数据查询、结果汇总和报告生成。
本项目围绕“金融信息分析”这一场景进行实现，主要目标是练习：
- 多 Agent 的角色划分和协作流程
- 大模型与外部工具的结合
- 金融数据查询工具的接入
- Web 搜索结果和结构化数据的综合分析
- Markdown 格式分析报告生成
- 本地前端页面与 Agent 后端逻辑的联动
该项目主要用于个人学习、实习求职展示和 Agent 应用开发能力积累，不构成任何投资建议。
## 主要功能
### 多 Agent 协作
项目中定义了一个 Agent Team，由多个 Agent 共同完成用户问题的处理。
当前主要包含：

- Web Agent：负责搜索市场新闻、公司公开信息和相关背景资料
- Finance Agent：负责查询股票价格、公司信息、相关新闻和分析师建议
- Team Coordinator：负责协调不同 Agent 的输出，并整理成结构化 Markdown 报告

通过这种拆分方式，可以让每个 Agent 关注相对明确的任务，最终由团队统一生成回答。

### 金融数据查询

Finance Agent 接入了 YFinanceTools，可以查询常见金融信息，例如：

- 股票价格
- 公司基本信息
- 公司相关新闻
- 分析师建议

在回答涉及金融数据的问题时，系统会尽量使用表格展示关键数据，使结果更加清晰。

### Web 信息检索

Web Agent 接入了 DuckDuckGoTools，可以检索公开网页信息，用于补充市场新闻、公司动态和背景资料。

在分析公司或市场事件时，Web Agent 可以提供更加实时的公开信息，Finance Agent 则补充结构化金融数据。

### 结构化报告生成

Agent Team 会将不同 Agent 获取到的信息进行整理，最终输出 Markdown 格式报告。报告一般包括：

- 问题背景
- 关键数据
- 新闻和公开信息
- 风险点
- 简短结论

这样可以让输出结果更适合阅读和展示。

### 本地交互页面

项目支持通过 Streamlit 启动本地页面，用户可以在浏览器中输入问题并查看 Agent Team 的回答。

同时，项目也支持启动 Agno AgentOS Playground，用于调试 Agent、工具调用和团队协作流程。

## 技术栈

大模型与 Agent 框架：

- Agno
- Agent
- Team
- AgentOS
- DashScope / 通义千问
- OpenAI-compatible API

工具调用：

- DuckDuckGoTools
- YFinanceTools

数据存储：

- SQLite
- Agno SqliteDb

前端交互：

- Streamlit

配置管理：

- python-dotenv
- `.env` 环境变量配置

## 项目结构

```text
ai-finance-agent-team/
├── finance_agent_team.py      # 多 Agent 团队核心逻辑
├── streamlit_app.py           # Streamlit 前端页面
├── requirements.txt           # Python 依赖
├── .env                       # 环境变量配置，本地使用，不建议上传
├── .gitignore                 # Git 忽略文件配置
├── agents.db                  # 本地 SQLite 记忆数据库，运行后生成
└── README.md                  # 项目说明文档
```

其中核心文件是：

```text
finance_agent_team.py
```

该文件主要完成以下工作：

1. 读取 `.env` 中的大模型配置
2. 创建 DashScope / 通义千问模型对象
3. 创建 SQLite 数据库用于保存对话历史
4. 定义 Web Agent
5. 定义 Finance Agent
6. 将多个 Agent 组合成 Agent Team
7. 提供 `ask_finance_team` 方法给前端调用
8. 启动 AgentOS Playground 服务

## 环境要求

- Python 3.10+
- DashScope API Key
- 网络环境可以访问 DashScope、DuckDuckGo 和 YFinance
- Windows、Linux 或 macOS 均可运行

## 安装与运行

### 1. 克隆项目

```bash
git clone <repository_url>
cd ai-finance-agent-team
```

### 2. 创建虚拟环境

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux / macOS：

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

在项目根目录下创建 `.env` 文件，并填写 DashScope API Key：

```env
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
DASHSCOPE_MODEL=qwen-max
```

### 5. 启动 Streamlit 页面

```bash
streamlit run streamlit_app.py
```

启动后浏览器访问本地地址，一般为：

```text
http://localhost:8501
```

### 6. 启动 AgentOS Playground

如果需要使用 Agno AgentOS Playground，可以运行：

```bash
python finance_agent_team.py
```

## 核心代码说明

### 大模型配置

项目通过 DashScope 的 OpenAI-compatible API 接入通义千问模型。模型配置从 `.env` 文件中读取，便于本地切换模型和管理 API Key。

```python
llm_model = get_dashscope_model()
```

### Web Agent

Web Agent 主要负责网页检索，使用 DuckDuckGoTools 获取公开市场信息和公司相关资料。

主要作用：

- 搜索市场新闻
- 查询公司公开信息
- 补充背景资料

### Finance Agent

Finance Agent 主要负责金融数据查询，使用 YFinanceTools 获取股票和公司相关数据。

主要作用：

- 查询股票价格
- 查询公司信息
- 查询公司新闻
- 查询分析师建议
- 使用表格展示金融数据

### Agent Team

Agent Team 将 Web Agent 和 Finance Agent 组合起来，由团队负责协调不同 Agent 的输出，并生成结构化报告。

输出要求包括：

- 使用 Markdown 格式
- 包含关键事实
- 包含表格数据
- 给出风险提示
- 结论简洁明确
- 不将结果表述为投资建议

## 使用示例

可以在页面中输入类似问题：

```text
请分析一下苹果公司最近的市场表现
```

```text
帮我查询一下 NVIDIA 的股票信息，并总结近期风险
```

```text
对比一下 Microsoft 和 Google 的基本面信息
```

```text
最近特斯拉有哪些相关新闻，对股价可能有什么影响
```

系统会根据问题调用 Web Agent 和 Finance Agent，并生成结构化回答。

## 输出示例结构

Agent Team 的回答通常会整理为类似结构：

```markdown
## 问题概述

简要说明用户问题和分析对象。

## 关键数据

使用表格展示股票价格、公司信息或其他金融指标。

## 公开信息

总结 Web Agent 检索到的相关新闻和背景资料。


## 项目收获

通过这个项目，我主要练习了以下内容：

- 使用 Agno 搭建 Agent 和 Agent Team
- 使用 DashScope / 通义千问接入大语言模型
- 使用 OpenAI-compatible API 适配国产大模型
- 接入 DuckDuckGo 搜索工具
- 接入 YFinance 金融数据工具
- 使用 SQLite 保存 Agent 对话历史
- 使用 Streamlit 搭建本地交互页面
- 理解多 Agent 协作和工具调用流程
- 将模型输出整理为结构化 Markdown 报告

这个项目虽然规模不大，但覆盖了 Agent 应用开发中的关键环节，包括模型接入、工具调用、角色分工、结果整合和前端交互，对我理解多 Agent 应用开发有较大帮助。

## 后续优化方向

后续可以从以下方向继续完善：

- 增加更多金融数据源
- 支持股票代码自动识别和补全
- 增加公司财报解析能力
- 增加图表展示，例如股价走势和指标变化
- 增加历史分析记录管理
- 增加用户自定义 Agent 配置
- 增加结果引用来源展示
- 增加异常处理和日志记录
- 增加 Docker 部署方式
- 增加单元测试和接口测试

## 说明

本项目主要用于个人学习和实习求职展示，重点展示多 Agent 协作、工具调用、金融数据查询、大模型接入和 Streamlit 应用开发能力。
