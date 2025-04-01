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

    def select_llm(self, query: str) -> tuple[str, StdioServerParameters, str]:
        """Let user choose which model to use."""
        print("\nWhich model would you like to use?")
        print("1. GPT-4 (Better for technical queries)")
        print("2. Claude (Better for general queries)")
        
        while True:
            choice = input("Enter 1 or 2: ").strip()
            if choice == "1":
                return 'generate_gpt4_response', self.gpt4_params, "GPT-4 selected by user preference"
            elif choice == "2":
                return 'generate_claude_response', self.claude_params, "Claude selected by user preference"
            else:
                print("Please enter 1 or 2")

    async def process_query(self, query: str):
        # Select the appropriate server and tool
        tool_name, server_params, reason = self.select_llm(query)
        
        # Connect to the selected server
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # List available prompts and resources
                prompts = await session.list_prompts()
                resources = await session.list_resources()
                
                # Process the query using the appropriate tool
                response = await session.call_tool(tool_name, {'prompt': query})
                
                # Extract the actual response text
                if hasattr(response, 'content') and response.content:
                    response_text = response.content[0].text
                else:
                    response_text = str(response)
                
                # Return the model selection reason and response
                return f"\nModel Used: {reason}\n\nResponse:\n{response_text}"

if __name__ == "__main__":
    client = LLMSelector()
    while True:
        user_query = input("\nEnter your query (type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        response = asyncio.run(client.process_query(user_query))
        print(response)
