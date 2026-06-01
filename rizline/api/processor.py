from .request import UserAPI
from ..database import song_data as song_data_database

from ...common import utils
from ...common import config

import time
from typing import Tuple

class Processor(UserAPI):
    def get_data(self) -> Tuple[dict, list, list]:
        raw_data = self.get_login_data()
        
        user_id = raw_data["userId"]
        
        save_dir = config.DATA_DIR / "rizline" / user_id / "data"
        save_dir.mkdir(parents=True, exist_ok=True)
        utils.save_data_to_file(raw_data, save_dir / str(time.time()))
        
        player_info = {
            "name": raw_data["username"],
            "coin": raw_data["coin"],
            "dot": raw_data["dot"],
            "avatar": {
                "id": raw_data["rizcard"]["avatarId"],
                "position": raw_data["rizcard"]["avatarPos"],
            },
            "bio": [raw_data["rizcard"]["bioId1"], raw_data["rizcard"]["bioId2"]],
            "background": raw_data["rizcard"]["backgroundId"]
        }
        
        song_datas = [
            {
                "id": song_data["trackAssetId"].replace("track.", ""),
                "level": song_data["difficultyClassName"],
                "score": song_data["score"],
                "complete": song_data["completeRate"],
                "fullcombo": song_data["isFullCombo"],
                "clear": song_data["isClear"],
            } for song_data in raw_data["myBest"]
        ]
        for song_data in song_datas:
            song_info = song_data_database.song_data.get_song(id=song_data["id"])
            song_data["artist"] = song_info.get("artist", "Unknown Artist")
            song_data["diff"] = song_info.get("level", {}).get(song_data["level"], 0)
            song_data["title"] = song_info.get("title", song_data["id"].split(".")[0])
        
        has_rsk_song_datas = [
            {
                "id": song_data["trackId"].replace("track.", ""),
                "level": song_data["difficultyClassName"],
                "rks": song_data["rks"],
            } for song_data in raw_data["levelsRks"]
        ]
        _has_rsk_song_datas = {f"{has_rsk_song_datas[i]['id']}@{has_rsk_song_datas[i]['level']}": i for i in range(len(has_rsk_song_datas))}
        for song_data in song_datas:
            if f"{song_data['id']}@{song_data['level']}" in _has_rsk_song_datas:
                has_rsk_song_datas[_has_rsk_song_datas[f"{song_data['id']}@{song_data['level']}"]].update(song_data)
        has_rsk_song_datas.sort(key=lambda x: x["rks"], reverse=True)
        
        player_info["rks"] = sum([song["rks"] for song in has_rsk_song_datas[:40]]) / 40
        
        return player_info, song_datas, has_rsk_song_datas
