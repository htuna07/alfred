# A.L.F.R.E.D.(A Little Friendly Robot for Everday Duties)

A personal agent designed to run on a Raspberry Pi.

## Installation

```bash
pip3 install -r requirements.txt
export ANTHROPIC_API_KEY="sk-..."
python3 main.py
```

## Adding a New Tool

Create a new file under `tools/`:

```python
from core.tool import Tool

class NewSensorTool(Tool):
    name                = "new_sensor"
    description         = "Describe what the tool does for the LLM."
    requires_permission = True          # False → won't ask for permission
    parameters_schema   = {
        "type": "object",
        "properties": {
            "parameter": {
                "type":        "string",
                "description": "Description of the parameter"
            }
        },
        "required": ["parameter"]
    }

    def run(self, params: dict) -> str:
        # Call hardware here
        # Process raw data (image, binary) here
        # Return only strings to the LLM
        return "Sensor value: 42"
```

Register it in `main.py`:

```python
from tools.new_sensor import NewSensorTool
dispatcher.register(NewSensorTool())
```

## Permission System

| Value   | Behavior               |
| ------- | ---------------------- |
| `allow` | Always allow           |
| `ask`   | Ask the user each time |
| `deny`  | Always deny            |

To change permissions at runtime, send a command like:

```
You: don't ask for network scans anymore
```

The agent will call `permission_manager.set("scan_network", Permission.ALLOW)` to apply the change.

## Project Structure

```
Prime/
├── main.py
├── requirements.txt
├── core/
│   ├── agent.py        # ReAct loop, LLM integration
  │   ├── dispatcher.py   # Tool management
  │   ├── permission.py   # Permission system
  │   └── tool.py         # Base Tool class
└── tools/
    └── example_tools.py
```
