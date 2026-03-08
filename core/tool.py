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
        Runs the tool.
        Always returns a string — raw data (image, binary) should never be returned from here.
        """
        raise NotImplementedError

    def to_api_schema(self) -> dict:
        """Convert to Claude function calling API format."""
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": self.parameters_schema
        }
