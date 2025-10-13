from mcp.server.fastmcp import FastMCP

mcp=FastMCP("weather")


@mcp.tool()
async def get_weather(city: str) -> str:
    """Gets the current weather for a given city.
    Args:
        city (str): The city to get the weather for.
    Returns:
        str: The current weather in the city.
    """
    # For demonstration purposes, we'll return a dummy weather report.
    # In a real implementation, you would call a weather API here.
    return f"The current weather in {city} is sunny with a temperature of 25°C."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")