from enum import Enum

class ServerRegion(Enum):
    CN = "cn"
    GLOBAL = "global"

class ServerURL:
    CN = "https://rizserver.pigeongames.net"
    GLOBAL = "https://service.rhyths.net"

class ServerSecret:
    AES = {
        "iv": bytes.fromhex("31255b4f422e3c5953773f296f3a7251"),
        "key": bytes.fromhex("537640482c2b53562d552a56456a43572c6e3757412d406e7d6a333b553b5846")
    }
