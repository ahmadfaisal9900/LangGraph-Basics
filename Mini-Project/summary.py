from mcp.server.fastmcp import FastMCP

mcp = FastMCP("summary_writing")

@mcp.tool()
def write_summary(content: str) -> str:
    """Write a concise summary of the content"""
    summary = f"Summary: {content[:500]}..."
    return summary

if __name__ == "__main__":
    mcp.run(transport="stdio")
