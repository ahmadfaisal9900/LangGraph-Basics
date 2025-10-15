from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch

mcp=FastMCP("web_search")

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for information"""
    search = TavilySearch(max_results=2)
    results = search.invoke(query)
    return str(results)

if __name__ == "__main__":
    mcp.run(transport="stdio")