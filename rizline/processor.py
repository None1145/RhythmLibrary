from . import api
from . import config
from ..common import utils

import json
import string

class SafeTemplate(string.Template):
    delimiter = "$$"

def get_api_processor(user_profile: dict) -> api.processor.Processor:
    if user_profile["serverCode"] == "cn": region = api.model.ServerRegion.CN
    elif user_profile["serverCode"] == "global": region = api.model.ServerRegion.GLOBAL
    return api.processor.Processor(region=region, user_profile=user_profile)

def get_data(user_profile: dict) -> dict:
    data = get_api_processor(user_profile).get_login_data()
    return data

def get_best40(user_profile: dict, just_data: bool = False, just_html: bool = False) -> str | dict:
    player_info, _, song_datas = get_api_processor(user_profile).get_data()
    best40 = song_datas[:40]

    if just_data: return best40

    with open(f"{config.ASSETS_DIR}/html/b40.html", "r", encoding="utf-8") as f:
        html = SafeTemplate(f.read()).safe_substitute({"data": json.dumps({"playerInfo": player_info, "songDatas": best40}, indent=4, ensure_ascii=False)})
    
    if just_html: return html
    
    return utils.render_html_to_jpg(window_size=(1400, 600), html=html)
