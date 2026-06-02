from . import api
from . import config
from . import database
try:
    from ..common import utils
except ImportError:
    from common import utils

import json
import string

class SafeTemplate(string.Template):
    delimiter = "$$"

def get_api_processor(user_profile: dict) -> api.processor.Processor:
    server_code = user_profile.get("serverCode", user_profile.get("server", None))
    if server_code == "cn":
        region = api.model.ServerRegion.CN
    elif server_code == "global":
        region = api.model.ServerRegion.GLOBAL
    else:
        raise ValueError("Invalid region")
    return api.processor.Processor(region=region, user_profile=user_profile)

def get_best30(user_profile: dict, just_data: bool = False, just_html: bool = False) -> str | dict:
    processor = get_api_processor(user_profile)
    
    latest_summary = processor.get_latest_summary()

    song_datas = processor.get_game_record(summary=latest_summary)
    song_datas.sort(key=lambda x: x["rating"], reverse=True)
    
    ap_song_datas = [song_data for song_data in song_datas if song_data["status"] == "AP"]
    ap_song_datas.sort(key=lambda x: x["rating"], reverse=True)
    
    best30_song_datas = ap_song_datas[:3]
    for song_data in song_datas:
        if len(best30_song_datas) - len(ap_song_datas[:3]) >= 27: break
        if song_data not in best30_song_datas:
            best30_song_datas.append(song_data)
    
    if just_data: return best30_song_datas
    
    user_info = processor.get_user_info(summary=latest_summary)
    
    result = {
        "user_info": user_info,
        "song_data": best30_song_datas
    }

    with open(f"{config.HTML_ASSETS_DIR}/best30.html", "r", encoding="utf-8") as f:
        html = SafeTemplate(f.read()).safe_substitute({"data": json.dumps(result, indent=4, ensure_ascii=False)})

    if just_html: return html

    return utils.render_html_to_jpg(window_size=(1100, 1350), html=html)
