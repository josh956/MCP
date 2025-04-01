from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import re
import asyncio
import sys
import os

class LLMSelector:
    def __init__(self):
        # Initialize parameters for both servers
        self.gpt4_params = StdioServerParameters(
            command="python3",
            args=["gpt4o_server.py"],
            env=os.environ.copy()
        )
        self.claude_params = StdioServerParameters(
            command="python3",
            args=["claude_server.py"],
            env=os.environ.copy()
        )

    def select_llm(self, query: str) -> tuple[str, StdioServerParameters]:
        """Determine the most suitable LLM based on the query."""
        if re.search(r'\b(code|programming|algorithm)\b', query, re.IGNORECASE):
            return 'generate_gpt4_response', self.gpt4_params
        else:
            return 'generate_claude_response', self.claude_params

    async def process_query(self, query: str):
        # Select the appropriate server and tool
        tool_name, server_params = self.select_llm(query)
        
        # Connect to the selected server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # List available prompts and resources
                prompts = await session.list_prompts()
                resources = await session.list_resources()
                
                # Process the query using the appropriate tool
                response = await session.call_tool(tool_name, {'prompt': query})
                return response

if __name__ == "__main__":
    client = LLMSelector()
    while True:
        user_query = input("Enter your query (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        response = asyncio.run(client.process_query(user_query))
        print("Response:", response)
