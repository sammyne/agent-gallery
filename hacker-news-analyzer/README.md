# HackerNews 分析代理

一个使用 LangChain 框架构建的强大 AI 代理，用于分析和提供有关 HackerNews 内容的见解。该代理使用 OpenAI 兼容的模型来提供对科技新闻、趋势和讨论的智能分析。

## 功能特性

- 🔍 **智能分析**：深度分析 HackerNews 内容，包括热门话题、用户参与度和科技趋势
- 💡 **上下文洞察**：提供故事之间的有意义的上下文和联系
- 📊 **参与度分析**：跟踪用户参与模式并识别有趣的讨论
- 🤖 **交互式界面**：易于使用的命令行界面，支持自然对话
- ⚡ **实时更新**：获取最新的科技新闻和趋势

## 依赖

- python >= 3.10
- uv >= 0.9
- LangChain >= 1.0

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/sammyne/agent-gallery.git
cd hacker-news-analyzer
```

### 2. 安装依赖

```bash
uv sync
```

### 3. 配置大语言模型
创建 `.env` 文件，并添加如下配置

配置项 | 说明 | 样例
-------|-----|-----
`OPENAI_API_BASE_URL` | 访问模型的 url | https://dashscope.aliyuncs.com/compatible-mode/v1 | 
`OPENAI_API_KEY` | 访问模型服务的密钥 | 
`OPENAI_MODEL` | OpenAI 兼容的模型名称 | qwen3-max-2025-09-23

### 4. 运行

```bash
uv run src/main.py
```

代理将显示欢迎消息和可用功能。你可以通过输入问题或命令与它交互。

### 示例查询

- "今天 HackerNews 上讨论最多的主题是什么？"
- "分析热门故事中的参与模式"
- "从最近的讨论中出现了哪些科技趋势？"
- "比较本周和上周的热门故事"
- "显示今天最有争议的故事"
