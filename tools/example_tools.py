import subprocess
import datetime
from core.tool import Tool


class GetTimeTool(Tool):
    """Simple tool example that does not require permission."""
    name                = "get_time"
    description         = "Returns the current date and time."
    requires_permission = False
    parameters_schema   = {
        "type": "object",
        "properties": {},
        "required": []
    }

    def run(self, params: dict) -> str:
        now = datetime.datetime.now()
        return now.strftime("%d %B %Y, %H:%M:%S")


class ScanNetworkTool(Tool):
    """Scans devices on the network. Requires permission."""
    name                = "scan_network"
    description         = "Scans the local network for devices, returns IP and MAC addresses."
    requires_permission = True
    parameters_schema   = {
        "type": "object",
        "properties": {
            "subnet": {
                "type":        "string",
                "description": "Subnet to scan, e.g.: 192.168.1.0/24"
            }
        },
        "required": ["subnet"]
    }

    def run(self, params: dict) -> str:
        subnet = params.get("subnet", "192.168.1.0/24")

        try:
            # nmap must be installed: sudo apt install nmap
            result = subprocess.run(
                ["nmap", "-sn", subnet],
                capture_output=True,
                text=True,
                timeout=30
            )
            # Simplify raw nmap output, send to LLM
            lines    = result.stdout.splitlines()
            devices  = [l for l in lines if "Nmap scan" in l or "MAC" in l or "report" in l]
            return "\n".join(devices) if devices else "No devices found."

        except FileNotFoundError:
            return "[error] nmap is not installed. Install with 'sudo apt install nmap'."
        except subprocess.TimeoutExpired:
            return "[error] Scan timed out."
