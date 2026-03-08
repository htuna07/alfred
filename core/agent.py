import anthropic
from core.dispatcher import ToolDispatcher

MODEL   = "claude-haiku-4-5"
MAX_TOKENS = 1024

SYSTEM_PROMPT = """Sen P.R.I.M.E'sin. Raspberry Pi üzerinde çalışan, fiziksel dünyayla etkileşime girebilen kişisel bir asistansın.

Kurallar:
- Türkçe konuş, kısa ve net ol.
- Tool kullanman gerekiyorsa direkt kullan, gereksiz açıklama yapma.
- Birden fazla tool gerekiyorsa aynı anda çağır.
- Tool sonuçlarına dayanarak cevap ver, tahmin yürütme.
- Yapamayacağın bir şey istenirse dürüstçe söyle."""


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
            # Durum 1: LLM tool çağırdı
            # ------------------------------------------------
            if response.stop_reason == "tool_use":
                tool_calls   = [b for b in response.content if b.type == "tool_use"]
                tool_results = []

                for call in tool_calls:
                    print(f"[tool çağrısı] {call.name} → {call.input}")
                    result = self._dispatcher.run(call.name, call.input)
                    print(f"[tool sonucu] {result}")

                    tool_results.append({
                        "type":        "tool_result",
                        "tool_use_id": call.id,
                        "content":     result
                    })

                # Assistant mesajı ve tool result'ları memory'e ekle
                self._memory.append({"role": "assistant", "content": response.content})
                self._memory.append({"role": "user",      "content": tool_results})

                # Döngü devam eder

            # ------------------------------------------------
            # Durum 2: Direkt cevap, döngü biter
            # ------------------------------------------------
            else:
                final = next(b.text for b in response.content if hasattr(b, "text"))
                self._memory.append({"role": "assistant", "content": final})
                return final

    def clear_memory(self):
        self._memory = []
        print("[bellek] Konuşma geçmişi temizlendi.")
