def my_tool(param: str) -> dict:
    return {"success": True, "result": param}

def register(tool_interface):
    tool_interface.my_tool = my_tool
    return True

METADATA = {
    "name": "my_plugin",
    "version": "1.0.0",
    "description": "My custom tool"
}