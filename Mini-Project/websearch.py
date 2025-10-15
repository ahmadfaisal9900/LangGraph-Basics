from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key 

langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_API_KEY"] = langsmith_api_key
os.environ["LANGSMITH_TRACING"] = "true" 

mcp=FastMCP("web_search")

@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for information"""
    search = TavilySearch(max_results=2)
    results = search.invoke(query)
    return str(results)

if __name__ == "__main__":
    mcp.run(transport="stdio")