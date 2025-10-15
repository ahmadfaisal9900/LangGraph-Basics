import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import Optional

class SimpleMCPClient:
    """Simple MCP client for web search and summary tools"""
    
    def __init__(self):
        self.search_session: Optional[ClientSession] = None
        self.summary_session: Optional[ClientSession] = None
        self._search_context = None
        self._summary_context = None
    
    async def connect(self):
        """Connect to both MCP servers"""
        await asyncio.gather(
            self._connect_search_server(),
            self._connect_summary_server()
        )
    
    async def _connect_search_server(self):
        """Connect to web search MCP server"""
        try:
            server_params = StdioServerParameters(
                command="python",
                args=["websearch.py"],
                env=None  # Add TAVILY_API_KEY if needed
            )
            
            self._search_context = stdio_client(server_params)
            read, write = await self._search_context.__aenter__()
            
            self.search_session = ClientSession(read, write)
            await self.search_session.__aenter__()
            await self.search_session.initialize()
            
            print("✓ Connected to web_search MCP server")
            
        except Exception as e:
            print(f"✗ Failed to connect to web_search server: {e}")
    
    async def _connect_summary_server(self):
        """Connect to summary MCP server"""
        try:
            server_params = StdioServerParameters(
                command="python",
                args=["summary.py"],
                env=None
            )
            
            self._summary_context = stdio_client(server_params)
            read, write = await self._summary_context.__aenter__()
            
            self.summary_session = ClientSession(read, write)
            await self.summary_session.__aenter__()
            await self.summary_session.initialize()
            
            print("✓ Connected to summary_writing MCP server")
            
        except Exception as e:
            print(f"✗ Failed to connect to summary server: {e}")
    
    async def search_web(self, query: str) -> str:
        """Call search_web tool on MCP server"""
        if not self.search_session:
            return f"Error: Search server not connected"
        
        try:
            result = await self.search_session.call_tool(
                "search_web",
                arguments={"query": query}
            )
            # Extract content from MCP response
            if hasattr(result, 'content'):
                if isinstance(result.content, list):
                    return "\n".join([str(item.text) if hasattr(item, 'text') else str(item) 
                                     for item in result.content])
                return str(result.content)
            return str(result)
        except Exception as e:
            return f"Search error: {str(e)}"
    
    async def write_summary(self, content: str) -> str:
        """Call write_summary tool on MCP server"""
        if not self.summary_session:
            return f"Error: Summary server not connected"
        
        try:
            result = await self.summary_session.call_tool(
                "write_summary",
                arguments={"content": content}
            )
            # Extract content from MCP response
            if hasattr(result, 'content'):
                if isinstance(result.content, list):
                    return "\n".join([str(item.text) if hasattr(item, 'text') else str(item) 
                                     for item in result.content])
                return str(result.content)
            return str(result)
        except Exception as e:
            return f"Summary error: {str(e)}"
    
    async def cleanup(self):
        """Cleanup connections"""
        if self.search_session:
            try:
                await self.search_session.__aexit__(None, None, None)
                await self._search_context.__aexit__(None, None, None)
            except:
                pass
        
        if self.summary_session:
            try:
                await self.summary_session.__aexit__(None, None, None)
                await self._summary_context.__aexit__(None, None, None)
            except:
                pass


# Global MCP client instance
_mcp_client: Optional[SimpleMCPClient] = None

def get_mcp_client() -> SimpleMCPClient:
    """Get or create the global MCP client"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = SimpleMCPClient()
        # Initialize in the event loop
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, we'll connect later
                pass
            else:
                loop.run_until_complete(_mcp_client.connect())
        except RuntimeError:
            # Create new event loop if needed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(_mcp_client.connect())
    return _mcp_client


# ============================================================================
# Synchronous wrappers for LangGraph integration
# ============================================================================

def search_web_sync(query: str) -> str:
    """Synchronous wrapper for web search via MCP"""
    client = get_mcp_client()
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create new loop
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(client.search_web(query))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(client.search_web(query))


def write_summary_sync(content: str) -> str:
    """Synchronous wrapper for summary via MCP"""
    client = get_mcp_client()
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create new loop
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(client.write_summary(content))
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(client.write_summary(content))


# ============================================================================
# Initialize MCP client on module import
# ============================================================================

def initialize_mcp():
    """Initialize MCP client connection"""
    client = get_mcp_client()
    
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if not client.search_session or not client.summary_session:
        loop.run_until_complete(client.connect())


# ============================================================================
# Test the MCP integration
# ============================================================================

async def test_mcp_tools():
    """Test the MCP tools"""
    client = SimpleMCPClient()
    await client.connect()
    
    print("\n" + "="*60)
    print("Testing Web Search")
    print("="*60)
    search_result = await client.search_web("LangGraph tutorial")
    print(search_result)
    
    print("\n" + "="*60)
    print("Testing Summary")
    print("="*60)
    summary_result = await client.write_summary(search_result)
    print(summary_result)
    
    await client.cleanup()


if __name__ == "__main__":
    asyncio.run(test_mcp_tools())
