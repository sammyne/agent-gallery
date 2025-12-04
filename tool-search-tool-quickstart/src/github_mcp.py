"""
基于 mcp 客户端连接到 GitHub Copilot MCP 服务器的客户端示例。

参考：
1. https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable_basic.py
2. https://github.com/github/github-mcp-server/tree/main?tab=readme-ov-file#install-in-vs-code
3. https://github.com/modelcontextprotocol/python-sdk/issues/998#issue-3164301675
"""

import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def new_client(
    url: str = "https://api.githubcopilot.com/mcp/",
    pat: str | None = None,
) -> MultiServerMCPClient:
    if not pat:
        pat = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not pat:
        raise ValueError(
            "GitHub Personal Access Token not provided and "
            "GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set."
        )

    out = MultiServerMCPClient(
        {
            "github": {
                "transport": "streamable_http",
                "url": url,
                "headers": {
                    "Authorization": f"Bearer {pat}",
                },
            }
        }
    )

    return out


async def get_tools(
    url: str = "https://api.githubcopilot.com/mcp/",
    pat: str | None = None,
):
    if not pat:
        pat = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not pat:
        raise ValueError(
            "GitHub Personal Access Token not provided and "
            "GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set."
        )

    headers = {"Authorization": f"Bearer {pat}"}

    # # Connect to a streamable HTTP server
    async with streamablehttp_client(url, headers=headers) as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tools = await session.list_tools()
            return tools.tools


if __name__ == "__main__":
    import dotenv

    dotenv.load_dotenv()

    # asyncio.run(main())
    tools = asyncio.run(get_tools())
    # for v in tools:
    #     print('----')
    #     print(f'name: {v.name}')
    #     print(f'desc: {v.description}')
    # break
    print(f"Available tools: {[tool.name for tool in tools]}")

    tools = asyncio.run(new_client().get_tools())
    print(f"\nAvailable tools: {[tool.name for tool in tools]}")
