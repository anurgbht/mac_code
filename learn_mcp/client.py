import asyncio, os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AzureOpenAI


def build_client():
    """Build and return an `AzureOpenAI` client and deployment name.

    Reads configuration from the following environment variables
    (loaded via `python-dotenv`):

    - `API_ENDPOINT`
    - `API_VERSION`
    - `API_DEPLOYMENT`
    - `API_KEY`

    Returns:
        A tuple of `(client, deployment_name)` where `client` is an
        initialized `AzureOpenAI` instance.
    """

    api_base = os.getenv("API_ENDPOINT", "")
    api_version = os.getenv("API_VERSION", "")
    deployment_name = os.getenv("API_DEPLOYMENT", "")
    api_key = os.getenv("API_KEY", "")
    client = AzureOpenAI(
        azure_endpoint=api_base,
        api_key=api_key,
        api_version=api_version,
    )    

    return client, deployment_name

# 1. Setup LLM Client (pointing to your API)
ai_client, model_name = build_client()

async def run_agent():
    # 2. Define how to start your local server
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"], # Path to your server script
    )

    # 3. Connect to the server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()
            
            # List available tools from your local server
            tools = await session.list_tools()
            print(f"Connected! Available tools: {[t.name for t in tools.tools]}")

            # 4. Simple Chat Loop
            query = "How much disk space is left on my machine?"
            
            # Ask the LLM (passing it the tool definitions)
            response = ai_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": query}],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": t.name,
                        "description": t.description,
                        "parameters": t.inputSchema
                    }
                } for t in tools.tools]
            )

            # 5. Execute Tool if LLM requested it
            tool_call = response.choices[0].message.tool_calls[0]
            if tool_call:
                import json
                result = await session.call_tool(
                    tool_call.function.name, 
                    json.loads(tool_call.function.arguments)
                )
                print(f"Tool Result: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_agent())