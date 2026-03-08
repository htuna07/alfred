import subprocess
import datetime
from core.tool import Tool


class GetTimeTool(Tool):
    """İzin gerektirmeyen basit tool örneği."""
    name                = "get_time"
    description         = "Şu anki tarih ve saati döner."
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
    """Ağa bağlı cihazları tarar. İzin gerektirir."""
    name                = "scan_network"
    description         = "Yerel ağa bağlı cihazları tarar, IP ve MAC adreslerini döner."
    requires_permission = True
    parameters_schema   = {
        "type": "object",
        "properties": {
            "subnet": {
                "type":        "string",
                "description": "Taranacak subnet, örn: 192.168.1.0/24"
            }
        },
        "required": ["subnet"]
    }

    def run(self, params: dict) -> str:
        subnet = params.get("subnet", "192.168.1.0/24")

        try:
            # nmap kurulu olmalı: sudo apt install nmap
            result = subprocess.run(
                ["nmap", "-sn", subnet],
                capture_output=True,
                text=True,
                timeout=30
            )
            # Ham nmap çıktısını sadeleştir, LLM'e gönder
            lines    = result.stdout.splitlines()
            devices  = [l for l in lines if "Nmap scan" in l or "MAC" in l or "report" in l]
            return "\n".join(devices) if devices else "Cihaz bulunamadı."

        except FileNotFoundError:
            return "[hata] nmap kurulu değil. 'sudo apt install nmap' ile kur."
        except subprocess.TimeoutExpired:
            return "[hata] Tarama zaman aşımına uğradı."
