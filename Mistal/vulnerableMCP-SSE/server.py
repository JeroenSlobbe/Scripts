# Example MCP, do NOT use in production, its vulnerable by design and not addressing any of the good practises (such as oauth) from: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#security-warning
# prerequisite: pip install mcp

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
import logging
logging.basicConfig(level=logging.DEBUG)

mcp = FastMCP("Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    return a - b

@mcp.prompt("operation-decider")
def operation_decider_prompt(user_query: str) -> list[base.Message]:
    return [
        base.UserMessage(
            f"""Extract numbers and operation from: {user_query}. Respond only with a raw JSON object like: {{ "a": 1, "b": 2, "operation": "add" }}"""
        ),
    ]

if __name__ == "__main__":
    print("MCP server is running using SSE transport on http://127.0.0.1:8765 ...")
    mcp.run(transport="sse")
