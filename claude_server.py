from mcp.server.fastmcp import FastMCP
import anthropic
import os

# Set your Anthropic API key using the ANTHROPIC_GENERAL environment variable
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_GENERAL")
if not ANTHROPIC_API_KEY:
    raise ValueError("Please set the ANTHROPIC_GENERAL environment variable")

# Initialize the Anthropic client using the key from ANTHROPIC_GENERAL
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

claude_server = FastMCP("Anthropic Claude Server")

@claude_server.tool()
def generate_claude_response(prompt: str) -> str:
    """Generate a response using Anthropic's Claude model."""
    message = client.messages.create(
        model="claude-3-sonnet-20240229",  # Use the correct model name
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

if __name__ == "__main__":
    claude_server.run()
