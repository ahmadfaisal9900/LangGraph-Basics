from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
            "args":["mathserver.py"],
            "transport": "stdio"
            },
            "weather":{
                "url": "http://localhost:8000",
                "transport": "streamable-http"
            }
        }
    )
    print("Starting the client...")
    import os
    google_api_key = os.getenv("GOOGLE_API_KEY")
    os.environ["GOOGLE_API_KEY"] = google_api_key
    print("Getting the tools...")
    tools = await client.get_tools()
    print("Tools:", tools)
    print("Initializing the LLM...")
    llm = init_chat_model("google_genai:gemini-2.0-flash")
    agent = create_react_agent(llm, tools)

    print("Invoking the agent...")
    math_response = await agent.invoke(
        {"messages": [{"role": "user", "content": "What is 2 multiplied by 3?"}]}
    )
    print("Math Response:", math_response["messages"][-1].content)
    # weather_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "What is the weather in New York?"}]}
    # )
    # print("Weather Response:", weather_response["messages"][-1].content)

asyncio.run(main())