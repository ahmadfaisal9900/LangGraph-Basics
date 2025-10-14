from mcp.server.fastmcp import FastMCP

mcp=FastMCP("math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Adds two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.
    Returns:
        int: The sum of the two numbers.
    """
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers.
    Args:
        a (int): The first number.
        b (int): The second number.
    Returns:
        int: The product of the two numbers.
    """
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")