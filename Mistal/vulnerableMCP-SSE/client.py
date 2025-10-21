# Example MCP client (do not use in production)

import asyncio
import json
import re

from mcp import ClientSession
from mcp.client.sse import sse_client
from mistralai import Mistral

async def main():
    # Static configuration
    server_url = "http://127.0.0.1:8000/sse"
    api_key = "put-key-here"
    user_input = "five + 4"

    # Connect to MCP SSE server
    async with sse_client(url=server_url) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[x] Connected to MCP SSE server")

            # List tools
            tools = await session.list_tools()
            print("[x] Available tools:", [tool.name for tool in tools.tools])

            # List prompts
            prompts = await session.list_prompts()
            prompt_names = [p.name for p in prompts.prompts]

            if "operation-decider" not in prompt_names:
                print("[!] 'operation-decider' prompt not found.")
                return

            # Get prompt
            prompt = await session.get_prompt(
                name="operation-decider",
                arguments={"user_query": user_input}
            )
            prompt_text = prompt.messages[0].content.text
            print("Prompt:", prompt_text)

            # Call Mistral
            mistral = Mistral(api_key=api_key)
            response = mistral.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt_text}]
            )

            raw = response.choices[0].message.content.strip()
            print("[r] Mistral response:", raw)

            # Clean JSON
            cleaned = re.sub(r"^```json|```$", "", raw).strip()

            try:
                extracted = json.loads(cleaned)
                print("Extracted:", extracted)

                a = extracted["a"]
                b = extracted["b"]
                operation = extracted["operation"].strip().lower()

                if operation in ["add", "subtract"]:
                    result = await session.call_tool(operation, arguments={"a": a, "b": b})
                    print(f"[x] Result of {operation}({a}, {b}):", result.content)
                else:
                    print("[!] Invalid operation:", operation)
            except Exception as e:
                print("[!] Failed to parse JSON:", e)

asyncio.run(main())
