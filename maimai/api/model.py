from enum import Enum

class ServerRegion(Enum):
    CN = "cn"
    INTERNATIONAL = "international"
    JP = "jp"

class ServerURL:
    CN = ""
    INTERNATIONAL = "https://maimaidx-eng.com"
    JP = ""

class AuthServerURL:
    INTERNATIONAL = {
        "mobile": "https://maimaidx-eng.com/maimai-mobile/",
        "sega_login": "https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid",
    }
