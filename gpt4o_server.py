from mcp.server.fastmcp import FastMCP
from openai import OpenAI
import os

# Get API key from environment variable
OPENAI_API_KEY = os.getenv("General")
if not OPENAI_API_KEY:
    raise ValueError("Please set the General environment variable")

client = OpenAI(api_key=OPENAI_API_KEY)

gpt4_server = FastMCP("OpenAI GPT-4o Server")

@gpt4_server.tool()
def generate_gpt4_response(prompt: str) -> str:
    """Generate a response using OpenAI's GPT-4 model."""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    gpt4_server.run()
