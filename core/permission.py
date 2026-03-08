from enum import Enum


class Permission(str, Enum):
    ALLOW = "allow"   # Always allow
    ASK   = "ask"     # Ask the user each time
    DENY  = "deny"    # Always deny


class PermissionManager:

    def __init__(self, defaults: dict[str, Permission] = None):
        # Tool name → Permission
        self._permissions: dict[str, Permission] = defaults or {}

    def set(self, tool_name: str, permission: Permission):
        self._permissions[tool_name] = permission
        print(f"[permission] '{tool_name}' → {permission.value}")

    def check(self, tool_name: str) -> bool:
        """
        True  → tool can run
        False → tool blocked
        """
        state = self._permissions.get(tool_name, Permission.ASK)

        if state == Permission.ALLOW:
            return True

        if state == Permission.DENY:
            print(f"[permission] '{tool_name}' was denied.")
            return False

        if state == Permission.ASK:
            return self._ask_user(tool_name)

    def _ask_user(self, tool_name: str) -> bool:
        print(f"\n[permission required] Run '{tool_name}'?")
        print("  e        → yes, once")
        print("  h        → no")
        print("  always   → don't ask for this again")
        print("  never    → always deny from now on")

        answer = input("Answer: ").strip().lower()

        if answer == "e":
            return True
        elif answer == "always":
            self.set(tool_name, Permission.ALLOW)
            return True
        elif answer == "never":
            self.set(tool_name, Permission.DENY)
            return False
        else:
            return False
