import os
from mcp.server.fastmcp import FastMCP

# Create FastMCP server
mcp = FastMCP("desk-docs")

# Path to Desktop documents
DESKTOP_PATH = os.path.expanduser("~/Desktop")

@mcp.tool()
async def list_files() -> str:
    """List files on Desktop"""
    try:
        files = os.listdir(DESKTOP_PATH)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {e}"

@mcp.tool()
async def read_file(filename: str) -> str:
    """Read the content of a Desktop file.

    Args:
        filename: Name of the file to read (must be on Desktop).
    """
    filepath = os.path.join(DESKTOP_PATH, filename)
    if not os.path.exists(filepath):
        return f"File not found: {filename}"

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {filename}: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
