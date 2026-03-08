import anthropic
from core.dispatcher import ToolDispatcher

MODEL   = "claude-haiku-4-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """You are P.R.I.M.E. A personal assistant running on a Raspberry Pi that can interact with the physical world.

Rules:
- Speak in English, be short and concise.
- If you need to use tools, call them directly and avoid unnecessary explanation.
- If multiple tools are needed, call them together.
- Base your answers on tool results; do not speculate.
- If asked to do something you cannot, say so honestly."""


class AgentCore:

    def __init__(self, dispatcher: ToolDispatcher, api_key: str):
        self._dispatcher = dispatcher
        self._client     = anthropic.Anthropic(api_key=api_key)
        self._memory: list[dict] = []

    def run(self, user_input: str) -> str:
        self._memory.append({"role": "user", "content": user_input})

        while True:
            response = self._client.messages.create(
                model      = MODEL,
                max_tokens = MAX_TOKENS,
                system     = SYSTEM_PROMPT,
                tools      = self._dispatcher.get_api_schemas(),
                messages   = self._memory
            )

            # ------------------------------------------------
            # Case 1: LLM called a tool
            # ------------------------------------------------
            if response.stop_reason == "tool_use":
                tool_calls   = [b for b in response.content if b.type == "tool_use"]
                tool_results = []

                for call in tool_calls:
                    print(f"[tool call] {call.name} → {call.input}")
                    result = self._dispatcher.run(call.name, call.input)
                    print(f"[tool result] {result}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": call.id,
                        "content":     result
                    })

                # Add assistant message and tool results to memory
                self._memory.append({"role": "assistant", "content": response.content})
                self._memory.append({"role": "user",      "content": tool_results})

                # Loop continues

            # ------------------------------------------------
            # Case 2: Direct response, end loop
            # ------------------------------------------------
            else:
                final = next(b.text for b in response.content if hasattr(b, "text"))
                self._memory.append({"role": "assistant", "content": final})
                return final

    def clear_memory(self):
        self._memory = []
        print("[memory] Conversation history cleared.")
