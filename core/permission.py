from enum import Enum


class Permission(str, Enum):
    ALLOW = "allow"   # Her zaman izin ver
    ASK   = "ask"     # Her seferinde kullanıcıya sor
    DENY  = "deny"    # Her zaman reddet


class PermissionManager:

    def __init__(self, defaults: dict[str, Permission] = None):
        # Tool adı → Permission
        self._permissions: dict[str, Permission] = defaults or {}

    def set(self, tool_name: str, permission: Permission):
        self._permissions[tool_name] = permission
        print(f"[izin] '{tool_name}' → {permission.value}")

    def check(self, tool_name: str) -> bool:
        """
        True  → tool çalışabilir
        False → tool engellendi
        """
        state = self._permissions.get(tool_name, Permission.ASK)

        if state == Permission.ALLOW:
            return True

        if state == Permission.DENY:
            print(f"[izin] '{tool_name}' engellendi.")
            return False

        if state == Permission.ASK:
            return self._ask_user(tool_name)

    def _ask_user(self, tool_name: str) -> bool:
        print(f"\n[izin gerekli] '{tool_name}' çalıştırılsın mı?")
        print("  e        → evet, bir kere")
        print("  h        → hayır")
        print("  her zaman → bundan sonra izin isteme")
        print("  asla      → bundan sonra hep reddet")

        answer = input("Cevap: ").strip().lower()

        if answer == "e":
            return True
        elif answer == "her zaman":
            self.set(tool_name, Permission.ALLOW)
            return True
        elif answer == "asla":
            self.set(tool_name, Permission.DENY)
            return False
        else:
            return False
