from mcp.server.fastmcp import FastMCP
import shutil
import os

# Initialize FastMCP server
mcp = FastMCP("LocalHelper")

@mcp.tool()
def get_disk_usage(path: str = ".") -> str:
    """Checks the available disk space at a given local path."""
    total, used, free = shutil.disk_usage(path)
    return f"Free space: {free // (2**30)} GB / {total // (2**30)} GB"

@mcp.tool()
def list_local_files(directory: str = ".") -> list[str]:
    """Lists files in a specific local directory."""
    try:
        return os.listdir(directory)
    except Exception as e:
        return [f"Error: {str(e)}"]

if __name__ == "__main__":
    mcp.run()