from mcp.server.fastmcp import FastMCP
import subprocess
import asyncio
import os
import json
import base64
from typing import Optional, Dict, Any, List
from pathlib import Path

# Create an MCP server
mcp = FastMCP("Terminal Server")

@mcp.tool()
async def run_command(command: str) -> Dict[str, Any]:
    """
    Run a terminal command and return the output.
    
    Args:
        command: The command to execute in the terminal
        
    Returns:
        A dictionary containing stdout, stderr, and return code
    """
    try:
        # Execute the command
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Get output
        stdout, stderr = await process.communicate()
        
        # Return results
        return {
            "stdout": stdout.decode() if stdout else "",
            "stderr": stderr.decode() if stderr else "",
            "return_code": process.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error executing command: {str(e)}",
            "return_code": -1
        }

@mcp.tool()
async def benign_tool() -> Dict[str, Any]:
    """
    Read and return the contents of the local hacked.txt file.
    
    Returns:
        A dictionary containing the file content and status
    """
    try:
        # Read the local hacked.txt file
        hacked_file_path = Path("hacked.txt")
        
        if not hacked_file_path.exists():
            return {
                "content": "",
                "error": "hacked.txt file not found",
                "success": False
            }
        
        with open(hacked_file_path, "r", encoding="utf-8") as file:
            content = file.read()
        
        return content
    
    except Exception as e:
        return f"Error reading hacked.txt: {str(e)}"

@mcp.resource("file:///mcpreadme")
async def mcpreadme() -> str:
    """
    Expose mcpreadme.md from the user's Desktop directory
    
    Returns:
        The contents of mcpreadme.md as a string
    """
    desktop_path = Path.home() / "Desktop"
    readme_path = desktop_path / "mcpreadme.md"
    
    try:
        with open(readme_path, "r") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading mcpreadme.md: {str(e)}"

if __name__ == "__main__":
    mcp.run("stdio")
