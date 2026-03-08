from abc import ABC, abstractmethod


class Tool(ABC):
    name: str
    description: str
    requires_permission: bool = True
    parameters_schema: dict = {
        "type": "object",
        "properties": {},
        "required": []
    }

    @abstractmethod
    def run(self, params: dict) -> str:
        """
        Tool'u çalıştırır.
        Her zaman string döner — ham veri (görüntü, binary) asla buradan çıkmaz.
        """
        raise NotImplementedError

    def to_api_schema(self) -> dict:
        """Claude function calling API formatına çevirir."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters_schema
        }
