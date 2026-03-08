from core.tool import Tool
from core.permission import PermissionManager


class ToolDispatcher:

    def __init__(self, permission_manager: PermissionManager):
        self._tools: dict[str, Tool] = {}
        self._permission_manager = permission_manager

    def register(self, tool: Tool):
        self._tools[tool.name] = tool
        print(f"[tool] '{tool.name}' registered.")

    def run(self, tool_name: str, params: dict) -> str:
        if tool_name not in self._tools:
            return f"[error] No tool named '{tool_name}' found."

        tool = self._tools[tool_name]

        # Only ask for tools that have requires_permission=True
        if tool.requires_permission:
            allowed = self._permission_manager.check(tool_name)
            if not allowed:
                return f"Permission denied for '{tool_name}'."

        try:
            result = tool.run(params)
            return result
        except Exception as e:
            return f"[error] An error occurred while running '{tool_name}': {str(e)}"

    def get_api_schemas(self) -> list[dict]:
        """List of all tools' schemas in Claude API format."""
        return [tool.to_api_schema() for tool in self._tools.values()]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
