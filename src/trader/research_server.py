"""Research tools exposed over a local stdio MCP server."""

from mcp.server.fastmcp import FastMCP

from .tools import search_financial_news as search_financial_news_tool

mcp = FastMCP("research-tools")


@mcp.tool()
def search_financial_news(query: str) -> str:
    """Search current financial news and return concise source snippets."""
    return search_financial_news_tool(query)


if __name__ == "__main__":
    mcp.run()
