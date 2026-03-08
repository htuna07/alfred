# P.R.I.M.E (Pi Robotic Intelligence & Monitoring Engine)

Raspberry Pi üzerinde çalışan kişisel agent.

## Kurulum

```bash
pip3 install -r requirements.txt
export ANTHROPIC_API_KEY="sk-..."
python3 main.py
```

## Yeni Tool Eklemek

`tools/` altına yeni bir dosya oluştur:

```python
from core.tool import Tool

class YeniSensorTool(Tool):
    name                = "yeni_sensor"
    description         = "LLM bunu okur — ne yaptığını açıkla."
    requires_permission = True          # False → izin sormaz
    parameters_schema   = {
        "type": "object",
        "properties": {
            "parametre": {
                "type":        "string",
                "description": "Parametrenin açıklaması"
            }
        },
        "required": ["parametre"]
    }

    def run(self, params: dict) -> str:
        # Donanımı burada çağır
        # Ham veri (görüntü, binary) burada işle
        # LLM'e sadece string döndür
        return "Sensor değeri: 42"
```

`main.py` içinde register et:

```python
from tools.yeni_sensor import YeniSensorTool
dispatcher.register(YeniSensorTool())
```

## İzin Sistemi

| Değer   | Davranış                      |
| ------- | ----------------------------- |
| `allow` | Her zaman izin ver            |
| `ask`   | Her seferinde kullanıcıya sor |
| `deny`  | Her zaman reddet              |

Runtime'da değiştirmek için:

```
Sen: bundan sonra ağ taraması için izin isteme
```

Agent bunu `permission_manager.set("scan_network", Permission.ALLOW)` şeklinde çalıştıracak. (Faz 2'de eklenecek)

## Proje Yapısı

```
Prime/
├── main.py
├── requirements.txt
├── core/
│   ├── agent.py        # ReAct döngüsü, LLM bağlantısı
│   ├── dispatcher.py   # Tool yönetimi
│   ├── permission.py   # İzin sistemi
│   └── tool.py         # Base Tool sınıfı
└── tools/
    └── example_tools.py
```
