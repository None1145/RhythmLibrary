from .request import UserAPI
from ..database import song_data as song_data_database

try:
    from ...common import utils
    from ...common import config as common_config
except ImportError:
    from common import utils
    from common import config as common_config

import io
import time
import struct
import base64
import zipfile
import datetime
import Crypto.Cipher.AES
import Crypto.Util.Padding

class ByteReader:
    def __init__(self, data: bytes):
        self.data = data
        self.position = 0
    
    def get_byte(self):
        val = self.data[self.position]
        self.position += 1
        return val

    def get_bytes(self, n):
        val = self.data[self.position:self.position + n]
        self.position += n
        return val

    def get_int(self):
        val = struct.unpack_from("<i", self.data, self.position)[0]
        self.position += 4
        return val

    def get_float(self):
        val = struct.unpack_from("<f", self.data, self.position)[0]
        self.position += 4
        return val

    def get_varint(self):
        result = 0
        shift = 0

        while True:
            b = self.get_byte()
            result |= (b & 0x7F) << shift

            if not (b & 0x80):
                break

            shift += 7

        return result
    
    def get_string(self):
        length = self.get_varint()
        data = self.get_bytes(length)
        return data.decode("utf-8")

    def get_short(self):
        val = struct.unpack_from("<h", self.data, self.position)[0]
        self.position += 2
        return val

class Processor(UserAPI):
    def get_user_data(self) -> dict:
        user_data = super().get_user_data()
        save_dir = common_config.DATA_DIR / "phigros" / self.user_profile["objectID"] / "user_data"
        utils.save_data_to_file(user_data, save_dir / str(time.time()))

        return user_data
    
    def _get_summaries(self) -> dict:
        summaries = super().get_summaries()
        save_dir = common_config.DATA_DIR / "phigros" / self.user_profile["objectID"] / "summaries"
        utils.save_data_to_file(summaries, save_dir / str(time.time()))

        return summaries
    
    def _get_game_record(self, summary: dict) -> list[dict]:
        reader = self.get_byte_reader(summary=summary, key="gameRecord")
        
        song_datas = []
        level_map = ["EZ", "HD", "IN", "AT"]

        songs_num = reader.get_varint()

        for _ in range(songs_num):
            song_id = reader.get_string()

            length = reader.get_byte()

            value_bytes = reader.get_bytes(length)

            pos = 0

            flag = value_bytes[pos]
            pos += 1

            full_combo = value_bytes[pos]
            pos += 1

            song_info = song_data_database.song_data.get_song(song_id)

            for song_level in range(4):
                if (flag & (1 << song_level)) == 0:
                    continue

                score = int.from_bytes(value_bytes[pos:pos+4], "little", signed=True)
                pos += 4

                acc = struct.unpack_from("<f", value_bytes, pos)[0]
                pos += 4

                status = "FC" if (full_combo & (1 << song_level)) != 0 else "NONE"
                if score >= 1000000:
                    status = "AP"

                song_datas.append({
                    "title": song_info["title"],
                    "score": score,
                    "accuracy": acc,
                    "status": status,
                    "diff": song_info["levels"][level_map[song_level]],
                    "level": level_map[song_level],
                    "id": song_id,
                    "rating": ((((acc / 100) - 55) / 45) ** 2) * song_info["levels"][level_map[song_level]]
                })

        return song_datas

    def _get_user(self, summary: dict) -> dict:
        reader = self.get_byte_reader(summary=summary, key="user")
        _ = reader.get_byte()
        
        return {
            "nickname": self.get_display_name(),
            "intro": reader.get_string(),
            "avatar": reader.get_string(),
            "background": reader.get_string(),
        }

    def get_byte_reader(self, summary: dict, key: str) -> ByteReader:
        def decode(data: bytes, key: str) -> bytes:
            with zipfile.ZipFile(io.BytesIO(data)) as zip:
                with zip.open(key) as file:
                    first_byte = file.read(1)
                    if key == "gameRecord" and first_byte != b"\x01":
                        raise ValueError("Invalid game record file format")
                    encoded_data = file.read()
            key = base64.b64decode("6Jaa0qVAJZuXkZCLiOa/Ax5tIZVu+taKUN1V1nqwkks=")
            iv = base64.b64decode("Kk/wisgNYwcAV8WVGMgyUw==")
            return Crypto.Util.Padding.unpad(Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, iv).decrypt(encoded_data), Crypto.Cipher.AES.block_size)
        
        data = self.requests.get(
            summary["saveURL"],
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).content
        save_dir = common_config.DATA_DIR / "phigros" / self.user_profile["objectID"] / "game_save"
        utils.save_data_to_file(data, save_dir / str(datetime.datetime.strptime(summary["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()))

        return ByteReader(decode(data, key))
    
    def get_display_name(self) -> str:
        user_data = self.get_user_data()
        return user_data.get("nickname", "GUEST")

    def get_summaries(self) -> dict:
        results = self._get_summaries()["results"]
        
        datas = []
        for result in results:
            reader = ByteReader(base64.b64decode(result["summary"]))
            summary = {
                "saveVersion": reader.get_byte(),
                "challenge": reader.get_short(),
                "rks": reader.get_float(),
                "gameVersion": reader.get_varint(),
                "avatar": reader.get_string(),
                # Clear | Full Combo | All Perfect
                "EZ": [reader.get_short(), reader.get_short(), reader.get_short()],
                "HD": [reader.get_short(), reader.get_short(), reader.get_short()],
                "IN": [reader.get_short(), reader.get_short(), reader.get_short()],
                "AT": [reader.get_short(), reader.get_short(), reader.get_short()]
            }
            
            datas.append({
                "createdAt": result["createdAt"],
                "updatedAt": result["updatedAt"],
                "saveURL": result["gameFile"]["url"],
                "saveKey": result["gameFile"]["key"],
                "summary": summary
            })
        
        return datas
    
    def get_latest_summary(self) -> dict:
        summaries = self.get_summaries()
        latest_summary = summaries[0]

        for summary in summaries:
            if datetime.datetime.strptime(summary["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ") > datetime.datetime.strptime(latest_summary["updatedAt"], "%Y-%m-%dT%H:%M:%S.%fZ"):
                latest_summary = summary
        
        return latest_summary
    
    def get_game_record(self, summary: dict = None) -> list[dict]:
        if summary is None:
            summary = self.get_latest_summary()
        return self._get_game_record(summary=summary)

    def get_user(self, summary: dict = None) -> dict:
        if summary is None:
            summary = self.get_latest_summary()
        return self._get_user(summary=summary)
    
    def get_user_info(self, summary: dict = None) -> dict:
        if summary is None:
            summary = self.get_latest_summary()
        user_info = self._get_user(summary=summary)
        user_info["summary"] = summary["summary"]
        return user_info
