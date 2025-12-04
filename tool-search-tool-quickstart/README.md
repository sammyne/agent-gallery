# 可搜索工具的工具示例程序

此项目演示实现 [Introducing advanced tool use on the Claude Developer Platform] 一文介绍的 Tool Search Tool 特性，支持智能
体在运行过程中按需加载工具，而不是一开始就将所有工具的描述加载到会话上下文。

## 环境依赖
- python >= 3.12
- uv >= 0.9

## 快速开始

### 1. 准备 .env 文件
添加以下配置

配置项 | 说明
------|------
`GITHUB_PERSONAL_ACCESS_TOKEN` | 在 [github](https://github.com/settings/tokens) 页面创建的 Personal Access Token，具备 `read:project+read:user+repo+user:email` 等权限即可
`GOOGLE_API_KEY` | [google AI studio 页面](https://aistudio.google.com/api-keys?hl=zh-cn) 创建的 API 密钥
`GOOGLE_GEMINI_MODEL` | Gemini 模型名称。可用列表参考 [Gemini 模型](https://ai.google.dev/gemini-api/docs/models?hl=zh-cn) 介绍页

> 如需替换为其他大模型，在 .env 文件添加大模型配置项，并替换掉 src/main.py 里面的 `ChatGoogleGenerativeAI` 即可。
### 2. 初始化 python 虚拟环境

  ```bash
  uv sync
  ```

### 3. 运行程序

```bash
uv run src/main.py
```

样例输出片段如下
```bash
================================ System Message ================================

You are an agent. Your internal name is "GitHubManager".
================================ Human Message =================================

Get details for issue https://github.com/SaschaHeyer/gen-ai-livestream/issues/6
================================== Ai Message ==================================
Tool Calls:
  search_tools (222ded73-dd54-49ce-8f4c-c32f4496f8f7)
Call ID: 222ded73-dd54-49ce-8f4c-c32f4496f8f7
  Args:
    query: github issues
================================= Tool Message =================================

['search_issues Search for issues in GitHub repositories using issues search syntax already scoped to is:issue', 'search_pull_requests Search for pull requests in GitHub repositories using issues search syntax already scoped to is:pr', "list_issues List issues in a GitHub repository. For pagination, use the 'endCursor' from the previous response's 'pageIn", 'list_releases List releases in a GitHub repository', 'list_branches List branches in a GitHub repository']
================================== Ai Message ==================================
Tool Calls:
  load_tool (ad2a6d21-c075-4cff-8571-0954169ea685)
Call ID: ad2a6d21-c075-4cff-8571-0954169ea685
  Args:
    name: search_issues
================================= Tool Message =================================

Tool 'search_issues' is now loaded and ready to use.
================================== Ai Message ==================================
Tool Calls:
  search_issues (6aa2d1fc-1318-48d1-b736-619913ff4ba6)
Call ID: 6aa2d1fc-1318-48d1-b736-619913ff4ba6
  Args:
    owner: SaschaHeyer
    query: 6
    repo: gen-ai-livestream
================================= Tool Message =================================

{"total_count":1,"incomplete_results":false,"items":[{"id":3640181196,"number":6,"state":"open","locked":false,"title":"Video in Bidi","body":"Awesome demo! \n\nWas anyone able to get Audio+Video bidi streaming to work outside of the adk web UI?\n\nThe adk sample/example github provided a webUI that was a separate package, so I could not see how video was getting passed. The webUI is a separate repo. I cloned that, but couldn't find how it communicates video with Bidi streaming.","author_association":"NONE","user":{"login":"mkorn1","id":22860498,"node_id":"MDQ6VXNlcjIyODYwNDk4","avatar_url":"https://avatars.githubusercontent.com/u/22860498?v=4","html_url":"https://github.com/mkorn1","gravatar_id":"","type":"User","site_admin":false,"url":"https://api.github.com/users/mkorn1","events_url":"https://api.github.com/users/mkorn1/events{/privacy}","following_url":"https://api.github.com/users/mkorn1/following{/other_user}","followers_url":"https://api.github.com/users/mkorn1/followers","gists_url":"https://api.github.com/users/mkorn1/gists{/gist_id}","organizations_url":"https://api.github.com/users/mkorn1/orgs","received_events_url":"https://api.github.com/users/mkorn1/received_events","repos_url":"https://api.github.com/users/mkorn1/repos","starred_url":"https://api.github.com/users/mkorn1/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/mkorn1/subscriptions"},"comments":2,"created_at":"2025-11-18T22:13:04Z","updated_at":"2025-11-26T09:57:21Z","url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream/issues/6","html_url":"https://github.com/SaschaHeyer/gen-ai-livestream/issues/6","comments_url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream/issues/6/comments","events_url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream/issues/6/events","labels_url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream/issues/6/labels{/name}","repository_url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream","reactions":{"total_count":0,"+1":0,"-1":0,"laugh":0,"confused":0,"heart":0,"hooray":0,"rocket":0,"eyes":0,"url":"https://api.github.com/repos/SaschaHeyer/gen-ai-livestream/issues/6/reactions"},"node_id":"I_kwDOMnTBG87Y-MHM"}]}
================================== Ai Message ==================================


Here are the details for the issue:

**Title**: Video in Bidi
**State**: open
**Body**: Awesome demo! 

Was anyone able to get Audio+Video bidi streaming to work outside of the adk web UI?

The adk sample/example github provided a webUI that was a separate package, so I could not see how video was getting passed. The webUI is a separate repo. I cloned that, but couldn't find how it communicates video with Bidi streaming.
**Created At**: 2025-11-18T22:13:04Z
**Updated At**: 2025-11-26T09:57:21Z
**Comments**: 2
**URL**: https://github.com/SaschaHeyer/gen-ai-livestream/issues/6
```

## TODO
- 修复 `@tool` 修饰的工具函数用于 LangGraph 时无法识别 `ToolRuntime` 的问题
  - 相关 issue 参见 https://github.com/langchain-ai/langgraph/issues/6318

## 参考文献
- [Introducing advanced tool use on the Claude Developer Platform]
- [LangChain Docs / Workflows + agent](https://docs.langchain.com/oss/python/langgraph/workflows-agents#agents)

[Introducing advanced tool use on the Claude Developer Platform]: https://www.anthropic.com/engineering/advanced-tool-use