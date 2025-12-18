# Twitter Generator

这个智能体能够抓取一个指定 url 对应的网页，并将其转化为 Twitter 消息列表。

## 1. 依赖
- uv >= v0.9
- python >= 3.12

## 2. 概览

核心流程如下
1. 调用 Frawcrawl 服务抓取网页
1. LLM 分析网页生成 Twitter 消息

## 3. 快速开始

### 3.1. 准备 .env 配置文件
配置项 | 说明
------|--------
OPENAI_API_KEY | 兼容 OpenAI 协议的服务提供商的 API 密钥
OPENAI_API_BASE_URL | 兼容 OpenAI 协议的服务地址
OPENAI_MODEL | 兼容 OpenAI 的模型名称
FIRECRAWL_API_KEY | Firecrawl 工具依赖的 API 密钥

### 3.2. 初始化依赖
```bash
uv sync
```

### 3.3. 运行服务
```bash
uv run main.py
```

样例输出如下
```json
{
  "thread": [
    {
      "tweet_number": 1,
      "content": "LangChain: The #1 agent framework powering the world's top companies! 🚀\n\nFrom startups to enterprises like Klarna, LinkedIn, and Cloudflare, teams are building reliable AI agents at scale.\n\n90M+ monthly downloads and 100k+ GitHub stars say it all!\n\nLet me break down why it's dominating the agent space 👇\n\n(1/6)"
    },
    {
      "tweet_number": 2,
      "content": "Building AI agents is hard... 😅\n\n• Dense outputs make debugging impossible\n• LLMs are non-deterministic (random!)\n• Standard infrastructure can't handle long-running workloads\n• Vendor lock-in kills flexibility\n\nLangChain solves ALL of these problems with visibility, control, and model neutrality!\n\nCheck it out👇\n\n(2/6)"
    },
    {
      "tweet_number": 3,
      "content": "Two powerful frameworks for different needs:\n\n🔹 LangChain - Ship FAST with pre-built agent architecture\n\n🔹 LangGraph - Full control with low-level primitives for custom workflows\n\nBoth work seamlessly with 1000+ integrations and any LLM you choose!\n\nNo vendor lock-in = future-proof your stack 🛡️\n\n(3/6)"
    },
    {
      "tweet_number": 4,
      "content": "LangSmith Platform: Your agent engineering super-tool! 🛠️\n\n📊 Observability - See exactly what your agent is doing step-by-step\n\n🎯 Evaluation - Build test sets, score performance, iterate to greatness\n\n🚀 Deployment - One-click deploy with memory, auto-scaling, enterprise security\n\nBuilt for agents that run for hours or days!\n\n(4/6)"
    },
    {
      "tweet_number": 5,
      "content": "Real-world impact across industries:\n\n• Copilots (Rippling) • Enterprise GPT (Rakuten)\n• Customer Support (Klarna) • Research (Morningstar)\n• Code Generation • AI Search (Home Depot)\n\nThese aren't demos - they're production systems serving millions!\n\n(5/6)"
    },
    {
      "tweet_number": 6,
      "content": "Ready to ship reliable agents faster? ⚡\n\nJoin 1M+ developers building the future with LangChain!\n\nIf you're into:\n- AI Agents 🤖\n- LLM Development 🧠\n- Python/TypeScript 🐍\n- MLOps 🛠️\n- Production AI 🚀\n\nFollow me for more AI engineering insights! 💡\n\nGet started free → smith.langchain.com\n\n(6/6)"
    }
  ],
  "total_tweets": 6
}
```

## 4. 参考文献
- [Build a Multi-agent Content Creation System](https://blog.dailydoseofds.com/p/build-a-multi-agent-content-creation)
- https://github.com/patchy631/ai-engineering-hub/tree/main/motia-content-creation
