from enum import Enum

class ServerRegion(Enum):
    CN = "cn"
    GLOBAL = "global"

class ServerURL:
    CN = "https://rak3ffdi.cloud.tds1.tapapis.cn"
    GLOBAL = "https://kviehlel.cloud.ap-sg.tapapis.com"

class ServerSecret:
    CN = {
        "id": "rAK3FfdieFob2Nn8Am", 
        "key": "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0"
    }
    GLOBAL = {
        "id": "kviehleldgxsagpozb",
        "key": "tG9CTm0LDD736k9HMM9lBZrbeBGRmUkjSfNLDNib"
    }

class AuthServerURL:
    CN = {
        "code": "https://www.taptap.com/oauth2/v1/device/code",
        "token": "https://www.taptap.cn/oauth2/v1/token",
        "account": "https://open.tapapis.cn/account/basic-info/v1",
    }
    GLOBAL = {
        "code": "https://accounts.tapapis.com/oauth2/v1/device/code",
        "token": "https://accounts.tapapis.com/oauth2/v1/token",
        "account": "https://open.tapapis.com/account/profile/v1",
    }
