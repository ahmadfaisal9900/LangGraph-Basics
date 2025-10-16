# Agentic AI Modules — LangGraph, DSPy, MCP

This repository contains modular explorations of agentic AI frameworks including **LangGraph**, **DSPy**, **LangSmith**, and **MCP**. Each folder demonstrates a specific capability or architectural pattern.

---

## Modules

### BasicChatBot
Implements core LangGraph concepts:
- Tools and function calling
- Memory and custom states
- Human-in-the-loop control
- Time travel for state replay
- ReAct-style agents

### Context Engineering
Introduces DSPy fundamentals:
- Declarative prompt design
- Context and reasoning optimization
- Also added experiment tracking via MLFlow

### LangSmith Debugging
Integrates LangSmith with LangGraph:
- Execution tracing
- State inspection and visualization
- Agent debugging workflow

### Lovable Clone - AI Coding Assistant
A LangGraph-based chatbot using:
- GROQ API for inference  
- Tavily Search for retrieval  

### MCP Server
Covers the basics of the Model Context Protocol (MCP):
- Server setup and API exposure  
- Tool schema registration  
- Inter-agent communication  

### Mini-Project
Implements a hierarchical workflow:
- CEO agent coordinating writer and researcher teams  
- Research team: data and market researchers  
- Writing team: summary and technical writers  
- Built with LangGraph + DSPy + MCP  

### Multi-Agent
Demonstrates advanced LangGraph setups:
- Standard multi-agent workflows  
- Supervisory (controller-agent) workflows  

---

## Dependencies
- LangGraph  
- DSPy  
- LangSmith  
- MCP  
- GROQ API  
- Tavily Search  


