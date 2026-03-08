from core.tool import Tool
from core.permission import PermissionManager


class ToolDispatcher:

    def __init__(self, permission_manager: PermissionManager):
        self._tools: dict[str, Tool] = {}
        self._permission_manager = permission_manager

    def register(self, tool: Tool):
        self._tools[tool.name] = tool
        print(f"[tool] '{tool.name}' kaydedildi.")

    def run(self, tool_name: str, params: dict) -> str:
        if tool_name not in self._tools:
            return f"[hata] '{tool_name}' adında bir tool bulunamadı."

        tool = self._tools[tool_name]

        # Sadece requires_permission=True olan tool'lar için sor
        if tool.requires_permission:
            allowed = self._permission_manager.check(tool_name)
            if not allowed:
                return f"'{tool_name}' için izin verilmedi."

        try:
            result = tool.run(params)
            return result
        except Exception as e:
            return f"[hata] '{tool_name}' çalışırken hata oluştu: {str(e)}"

    def get_api_schemas(self) -> list[dict]:
        """Tüm tool'ların Claude API formatındaki schema listesi."""
        return [tool.to_api_schema() for tool in self._tools.values()]

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())
