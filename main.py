import os
from core.agent      import AgentCore
from core.dispatcher import ToolDispatcher
from core.permission import PermissionManager, Permission
from tools.example_tools import GetTimeTool, ScanNetworkTool

# .env dosyasından okumak istersen:
# from dotenv import load_dotenv; load_dotenv()


def build_agent() -> AgentCore:

    # 1. İzin yöneticisi — varsayılan izinleri burada tanımla
    permissions = PermissionManager(defaults={
        "get_time":     Permission.ALLOW,   # Saat sormak için izin gerekmez
        "scan_network": Permission.ASK,     # Her seferinde sor
    })

    # 2. Dispatcher
    dispatcher = ToolDispatcher(permissions)
    dispatcher.register(GetTimeTool())
    dispatcher.register(ScanNetworkTool())
    # Yeni tool → dispatcher.register(YeniTool())

    # 3. Agent
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable'ı set edilmemiş.")

    return AgentCore(dispatcher, api_key)


def main():
    print("Prime başlatılıyor...\n")
    agent = build_agent()
    print("\nHazır. Çıkmak için 'q' yaz.\n")

    while True:
        try:
            user_input = input("Sen: ").strip()

            if not user_input:
                continue
            if user_input.lower() == "q":
                print("Prime kapatılıyor.")
                break
            if user_input.lower() == "belleği temizle":
                agent.clear_memory()
                continue

            response = agent.run(user_input)
            print(f"\nPrime: {response}\n")

        except KeyboardInterrupt:
            print("\nPrime kapatılıyor.")
            break


if __name__ == "__main__":
    main()
