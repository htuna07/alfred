import os
from core.agent      import AgentCore
from core.dispatcher import ToolDispatcher
from core.permission import PermissionManager, Permission
from tools.example_tools import GetTimeTool, ScanNetworkTool

# If you want to read from a .env file:
# from dotenv import load_dotenv; load_dotenv()


def build_agent() -> AgentCore:

    # 1. Permission manager — define default permissions here
    permissions = PermissionManager(defaults={
        "get_time":     Permission.ALLOW,   # No permission needed to ask time
        "scan_network": Permission.ASK,     # Ask each time
    })

    # 2. Dispatcher
    dispatcher = ToolDispatcher(permissions)
    dispatcher.register(GetTimeTool())
    dispatcher.register(ScanNetworkTool())
    # New tool → dispatcher.register(NewTool())

    # 3. Agent
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

    return AgentCore(dispatcher, api_key)


def main():
    print("Starting Prime...\n")
    agent = build_agent()
    print("\nReady. Type 'q' to quit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue
            if user_input.lower() == "q":
                print("Shutting down Prime.")
                break
            if user_input.lower() == "clear memory":
                agent.clear_memory()
                continue

            response = agent.run(user_input)
            print(f"\nPrime: {response}\n")

        except KeyboardInterrupt:
            print("\nShutting down Prime.")
            break


if __name__ == "__main__":
    main()
