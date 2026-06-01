from ..database import song_data as song_data_database
from ..database import player_data as player_data_database
from ..database import player_song_data as player_song_data_database
from .request import UserAPI
from ..config import Config

from ...common import utils
from ...common import config

import math
import time
import numpy
import packaging.version
from typing import Tuple, Any, List
from datetime import datetime
from datetime import timedelta

def calculate_level(xp: int) -> float:
    xp_ups = [100, 120, 140, 160, 180, 200, 220, 240, 300, 210]
    xp_ups += [220, 230, 240, 250, 260, 270, 280, 290, 300, 250]
    xp_ups += [260, 270, 280, 290, 300, 310, 320, 330, 340, 350]
    xp_ups += [360, 370, 380, 390, 400, 410, 420, 430, 440, 450]
    xp_ups += [460, 470, 480, 490, 500]
    level = 1
    for xp_up in xp_ups:
        xp -= xp_up
        level += 1
        if xp < 1: break
    if xp > 0:
        level += xp / 500
    return level

def calculate_xp(level: float) -> int:
    xp_ups = [100, 120, 140, 160, 180, 200, 220, 240, 300, 210]
    xp_ups += [220, 230, 240, 250, 260, 270, 280, 290, 300, 250]
    xp_ups += [260, 270, 280, 290, 300, 310, 320, 330, 340, 350]
    xp_ups += [360, 370, 380, 390, 400, 410, 420, 430, 440, 450]
    xp_ups += [460, 470, 480, 490, 500]
    if level < 1:
        return 0
    full_levels = int(level)
    extra_fraction = level - full_levels
    xp = 0
    for i in range(1, full_levels):
        if i - 1 < len(xp_ups):
            xp += xp_ups[i - 1]
        else:
            xp += 500
    if extra_fraction > 0:
        xp += extra_fraction * 500
    return int(round(xp))

def reverse_calculate_score(song_rating: float, rating_real: float, needSmall1010000=True) -> Tuple[int, bool]:
    diff = song_rating - rating_real
    
    bounds = [
        (2**31 - 1, 3.6),
        (1010000, 3.6),
        (1008000, 3.4),
        (1004000, 2.4),
        (1000000, 2.0),
        (980000, 1.0),
        (950000, 0.0),
        (900000, -1.0),
        (800000, -2.0),
        (700000, -3.0),
        (600000, -4.0),
        (500000, -5.0),
        (0, -9999),
        (-2**31, -9999)
    ]
        
    song_score = 0
    if diff > 3.6:
        song_score = 1145141
    elif song_rating <= 0.0:
        song_score = 0
    else:
        for index in range(1, len(bounds)):
            current_tier = bounds[index]
            next_tier = bounds[index - 1] 
            if current_tier[1] <= diff <= next_tier[1]:
                if next_tier[1] == current_tier[1]:
                    return current_tier[0]
                ratio = (diff - current_tier[1]) / (next_tier[1] - current_tier[1])
                score = current_tier[0] + ratio * (next_tier[0] - current_tier[0])
                song_score = math.ceil(score)
                break
    
    song_score = int(song_score)
    if needSmall1010000:
        song_score = min(1010000, int(song_score))
    song_is_cleared = song_rating > 6

    return song_score, song_is_cleared

def calculate_song_rating(song_score: int, rating_real: float, song_is_cleared: bool) -> Tuple[float, int]:
    next_rating_point = 0.001

    bounds = [
        (2**31 - 1, 3.6),
        (1010000, 3.6),
        (1008000, 3.4),
        (1004000, 2.4),
        (1000000, 2.0),
        (980000, 1.0),
        (950000, 0.0),
        (900000, -1.0),
        (800000, -2.0),
        (700000, -3.0),
        (600000, -4.0),
        (500000, -5.0),
        (0, -9999),
        (-2**31, -9999)
    ]
        
    song_rating = 0
    for index in range(len(bounds)):
        if song_score >= bounds[index][0]:
            if index == 0:
                song_rating = max(rating_real + bounds[index][1], 0)
            else:
                current_tier = bounds[index]
                next_tier = bounds[index - 1] 
                ratio = (song_score - current_tier[0]) / (next_tier[0] - current_tier[0])
                offset = current_tier[1] + ratio * (next_tier[1] - current_tier[1])
                song_rating = max(rating_real + offset, 0)
            break
    next_point_score = reverse_calculate_score(song_rating + next_rating_point, rating_real, False)[0]
        
    if song_rating < 0: song_rating = 0
        
    if not song_is_cleared:
        song_rating = min(6, song_rating)
        
    next_point_score -= song_score
    if next_point_score + song_score > 1010000: next_point_score = 1010000 - song_score
    
    return song_rating, next_point_score

def calculate_song_ratings(song_score: numpy.ndarray | List[int], rating_real: numpy.ndarray | List[float], song_is_cleared: numpy.ndarray | List[bool]) -> Tuple[numpy.ndarray, numpy.ndarray]:
    song_score = numpy.array(song_score)
    rating_real = numpy.array(rating_real)
    song_is_cleared = numpy.array(song_is_cleared)
    
    song_rating = numpy.zeros_like(song_score, dtype=float)
    next_point_score = numpy.zeros_like(song_score, dtype=float)
    
    next_rating_point = 0.001
    
    xp = numpy.array([0, 500000, 600000, 700000, 800000, 900000, 950000, 980000, 1000000, 1004000, 1008000, 1010000])
    fp = numpy.array([-9999.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 2.4, 3.4, 3.6])
    
    offsets = numpy.interp(song_score, xp, fp)
    song_rating = numpy.maximum(rating_real + offsets, 0)
    
    target_offsets = (song_rating + next_rating_point) - rating_real
    next_point_score = numpy.interp(target_offsets, fp, xp)
    
    song_rating = numpy.maximum(song_rating, 0)
    song_rating = numpy.where(song_is_cleared, song_rating, numpy.minimum(song_rating, 6))

    next_point_score = next_point_score - song_score
    next_point_score = numpy.clip(next_point_score, 0, 1010000 - song_score)

    return song_rating, next_point_score

def calculate_completion_point(diff: float, rating: float, score: int, status: str) -> float:
    def calculate_completion_point_by_rating(diff, rating):
        rating_max = diff + 3.6
        return (rating / rating_max) * 0.925

    def calculate_completion_point_by_score(score):
        if score >= 1008000 and score <= 1008999:
            return (score - 1008000) / 1000 * 0.01
        elif score >= 1009000 and score <= 1009249:
            progress = (score - 1009000) / 1000
            return progress * 2 / 100 + 0.01
        elif score >= 1009250 and score <= 1009499:
            progress = (score - 1009250) / 1000
            return progress * 3 / 100 + 0.015
        elif score >= 1009500 and score <= 1009749:
            progress = (score - 1009500) / 1000
            return progress * 4 / 100 + 0.0225
        elif score >= 1009750 and score <= 1009899:
            progress = (score - 1009750) / 1000
            return progress * 5 / 100 + 0.0325
        elif score >= 1009900:
            progress = (score - 1009900) / 1000
            return progress * 10 / 100 + 0.04
        return 0
    
    def claculate_completion_point_by_status(status):
        if status == "FC":
            return 0.01
        elif status == "AP":
            return 0.02
        elif status == "APP":
            return 0.025
        return 0
    
    return min(calculate_completion_point_by_rating(diff, rating) + calculate_completion_point_by_score(score) + claculate_completion_point_by_status(status), 1)

def calculate_completion_points(diff: numpy.ndarray | List[float], rating: numpy.ndarray | List[float], score: numpy.ndarray | List[int], status: numpy.ndarray | List[str]) -> numpy.ndarray:
    diff = numpy.asanyarray(diff, dtype=float)
    rating = numpy.asanyarray(rating, dtype=float)
    score = numpy.asanyarray(score, dtype=float)
    status = numpy.asanyarray(status)

    rating_max = diff + 3.6
    pt_rating = (rating / rating_max) * 0.925

    conds_score = [
        (score >= 1008000) & (score <= 1008999),
        (score >= 1009000) & (score <= 1009249),
        (score >= 1009250) & (score <= 1009499),
        (score >= 1009500) & (score <= 1009749),
        (score >= 1009750) & (score <= 1009899),
        (score >= 1009900)
    ]
    
    funcs_score = [
        (score - 1008000) / 1000 * 0.01,
        ((score - 1009000) / 1000) * 2 / 100 + 0.01,
        ((score - 1009250) / 1000) * 3 / 100 + 0.015,
        ((score - 1009500) / 1000) * 4 / 100 + 0.0225,
        ((score - 1009750) / 1000) * 5 / 100 + 0.0325,
        ((score - 1009900) / 1000) * 10 / 100 + 0.04
    ]
    
    pt_score = numpy.select(conds_score, funcs_score, default=0.0)

    conds_status = [
        status == "FC",
        status == "AP",
        status == "APP"
    ]
    funcs_status = [0.01, 0.02, 0.025]
    
    pt_status = numpy.select(conds_status, funcs_status, default=0.0)

    total_points = pt_rating + pt_score + pt_status
    return numpy.minimum(total_points, 1.0)

def find_keys_in_any_dict(any_dict: dict, keys: list, default: Any = None) -> Any:
    for key in keys:
        if key in any_dict:
            return any_dict[key]
    if default is not None: return default
    raise KeyError(f"{keys} not in {list(any_dict.keys())}")

class Processor(UserAPI):
    def get_cloud_save(self, get_object_id: bool = False) -> dict:
        def format_duration_en(td: timedelta):
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            parts = []
            if hours >= 0:
                parts.append(f"{hours} hour{'s' if hours not in [0, 1] else ''}")
            if minutes >= 0:
                parts.append(f"{minutes} minute{'s' if minutes not in [0, 1] else ''}")
            if seconds >= 0 or not parts:
                parts.append(f"{seconds} second{'s' if seconds not in [0, 1] else ''}")
            return " ".join(parts)
        
        if self.user_profile["serverCode"].startswith("friend_"):
            followee_data = self.get_followee_data(short_id=self.user_profile["shortID"], raw_data=self.follow_user(short_id=self.user_profile["shortID"]))
            self.unfollow_user(short_id=self.user_profile["shortID"])
            raw_data = self.followee_data_to_cloud_save_raw_data_format(followee_data=followee_data)
            
            object_id = f"{self.user_profile['serverCode']}_{self.user_profile['shortID']}"
        else:
            raw_data = super().get_cloud_save(get_object_id=get_object_id)
            
            if get_object_id:
                object_id = self.object_id
            else:
                object_id = self.user_profile["objectID"]
        cloud_save = raw_data["results"][0]["cloudSave"]
            
        save_dir = config.DATA_DIR / "rotaeno" / object_id / "cloud_save"
        save_dir.mkdir(parents=True, exist_ok=True)
        utils.save_data_to_file(raw_data, save_dir / str(time.time()))
        
        player_version = cloud_save.get("ClientVersion", Config.GAME_VERSION_NAME)
        player_version = packaging.version.Version(player_version)
        
        user_data = cloud_save["data"]["data"]
        player_favorite_song_ids = user_data.get("FavoriteSong", {"songIds": []})["songIds"]
        player_song_records = user_data["songs"]["songs"]
        player_display_name = user_data["profile"]["DisplayName"]
        player_avatar = user_data["badges"]["EquippedBadgeId"] if "boss" not in user_data["badges"]["EquippedBadgeId"] else user_data["badges"]["EquippedBadgeId"] + "-4"
        player_background = user_data["collectable-background"]["EquippedBackgroundId"].replace("background_", "")
        player_character = user_data["collectable-character"]["EquippedCharacterId"].replace("character_", "") if user_data["collectable-character"]["EquippedCharacterId"] is not None else "ilot"
        if user_data["collectable-character"].get("chars", None) is not None:
            if user_data["collectable-character"]["chars"].get(player_character, {"equipForm": None}) is not None:
                player_character += f"_{user_data['collectable-character']['chars'][player_character]['equipForm']}"
        player_total_play_time = [float(time) for time in cloud_save["TotalPlayTime"].replace("-", "").split(":")]
        player_total_play_time_delta = timedelta(hours=player_total_play_time[0], minutes=player_total_play_time[1], seconds=player_total_play_time[2])
        player_total_play_time = format_duration_en(player_total_play_time_delta)
        player_play_records = user_data["playRecords"]
        player_exp = user_data["PlayerLevel"]["AccumXp"]
        player_level = calculate_level(player_exp)
        try: 
            player_collectible_avatars = {i.replace("badge_", ""): user_data["missions"]["missions"]["data"][i]["completed"] for i in user_data["missions"]["missions"]["data"] if "badge_" in i}
            player_collectible_characters = {i.replace("character_", ""): user_data["missions"]["missions"]["data"][i]["completed"] for i in user_data["missions"]["missions"]["data"] if "character_" in i}
            player_collectible_backgrounds = {i.replace("background_", ""): user_data["collectables"]["Saves"][i]["Amount"] != 0 for i in user_data["collectables"]["Saves"] if "background_" in i and "background_cg" not in i}
            player_collectible_cgs = {i.replace("background_cg-", ""): user_data["collectables"]["Saves"][i]["Amount"] != 0 for i in user_data["collectables"]["Saves"] if "background_" in i and "background_cg" in i}
        except KeyError:
            player_collectible_avatars = {}
            player_collectible_characters = {}
            player_collectible_backgrounds = {}
            player_collectible_cgs = {}
        player_collectibles = {
            "avatar": player_collectible_avatars,
            "character": player_collectible_characters,
            "background": player_collectible_backgrounds,
            "cg": player_collectible_cgs
        }
        
        level_map = {"I": 0, "II": 1, "III": 2, "IV": 3, "IV_Alpha": 4}
        batch_scores = []
        batch_ratings_real = []
        batch_is_cleared = []
        batch_status = []
        batch_metadata = []
        for song_id, record in player_song_records.items():
            for level, level_index in level_map.items():
                if level not in record["levels"]:
                    continue
                try:
                    song_data = song_data_database.song_data.get_song(song_id)
                    rating_real = song_data["levels"][level]["num"]
                    if song_id in Config.REMOVED_SONGS:
                        if Config.REMOVED_SONGS[song_id] <= player_version:
                            rating_real = 0
                    if song_id in Config.CHANGE_SONGS:
                        if Config.CHANGE_SONGS[song_id]["version"] > player_version:
                            rating_real = Config.CHANGE_SONGS[song_id]["rating"].get(level, rating_real)
                    song_score = int(record["levels"][level]["Score"])
                    is_cleared = record["levels"][level]["IsCleared"]
                    song_status = record["levels"][level]["Flag"]

                    batch_scores.append(song_score)
                    batch_ratings_real.append(rating_real)
                    batch_is_cleared.append(is_cleared)
                    batch_status.append(song_status)
                    batch_metadata.append((song_id, level, record, song_data, level_index))
                except:
                    continue
        _song_ratings, song_next_score = calculate_song_ratings(batch_scores, batch_ratings_real, batch_is_cleared)
        song_completion_points = calculate_completion_points(batch_ratings_real, song_ratings, batch_scores, batch_status)
        
        song_ratings = {}
        for i, (song_id, level, record, song_info, level_index) in enumerate(batch_metadata):
            if song_id not in song_ratings:
                song_ratings[song_id] = {}
            song_ratings[song_id][level] = {
                "songRatingMix": _song_ratings[i],
                "songRating": _song_ratings[i],
                "songScore": batch_scores[i],
                "songName": song_info["title"],
                "songStatus": record["levels"][level]["Flag"],
                "songNextPointScore": song_next_score[i],
                "songIsCleared": batch_is_cleared[i],
                "songLevelNum": batch_ratings_real[i],
                "songLevelName": level,
                "songRecord": record,
                "songInfo": song_info
            }
            if song_id in Config.REMOVED_SONGS and player_version >= Config.REMOVED_SONGS[song_id]:
                song_completion_points[i] = 0
            song_ratings[song_id][level]["songCompletionPoint"] = song_completion_points[i]
        
        for song_id, levels in song_ratings.items():
            if "IV_Alpha" in levels and "IV" in levels:
                if levels["IV_Alpha"]["ratingMix"] >= levels["IV"]["ratingMix"]:
                    levels["IV"]["ratingMix"] = 0
                else:
                    levels["IV_Alpha"]["ratingMix"] = 0
                song_ratings[song_id] = levels

        all_ratings = []
        for levels in song_ratings.values():
            for data in levels.values():
                all_ratings.append(data["ratingMix"])
        all_ratings.sort(reverse=True)
        
        rating = (sum(all_ratings[:10]) * 0.6 / 10) + (sum(all_ratings[10:20]) * 0.2 / 10) + (sum(all_ratings[20:40]) * 0.2 / 20)
        completion_point = 0
        weight_map = {
            "I": 0.7,
            "II": 0.8,
            "III": 0.9,
            "IV": 1.0
        }
        for _, levels in song_ratings.items():
            regular_cps = []
            for lvl_name, weight in weight_map.items():
                if lvl_name in levels:
                    single_cp = levels[lvl_name].get("songCompletionPoint", 0)
                    regular_cps.append(single_cp * weight)
            cp_regular = max(regular_cps) if regular_cps else 0.0
            cp_iva = 0.0
            if "IV_Alpha" in levels:
                cp_iva = levels["IV_Alpha"].get("songCompletionPoint", 0) * 1.0
            cp_song = cp_regular + cp_iva
            completion_point += cp_song
        
        player_info = {
            "displayName": player_display_name,
            "rating": rating,
            "exp": player_exp,
            "level": player_level,
            "avatar": player_avatar,
            "background": player_background,
            "character": player_character,
            "completion": completion_point,
            "totalPlayTime": player_total_play_time,
            "favoriteSongIDs": player_favorite_song_ids,
            "collectibles": player_collectibles,
            "playRecords": player_play_records
        }

        song_datas = []
        for song_id, song_levels in song_ratings.items():
            for song_level, song_data in song_levels.items():
                song_data["id"] = song_id
                song_data["level"] = song_level
                song_datas.append(song_data)
        
        timestamp = datetime.now()
        
        player = player_data_database.Player(
            object_id=object_id,
            name=player_info["displayName"],
            rating=player_info["rating"],
            completion=player_info["completion"],
            exp=player_info["exp"],
            level=player_info["level"],
            all_perfect_plus=player_info["playRecords"]["TotalApp"],
            all_perfect=player_info["playRecords"]["TotalAp"],
            full_combo=player_info["playRecords"]["TotalFc"],
            miss=player_info["playRecords"]["Miss"],
            good=player_info["playRecords"]["Good"],
            perfect=player_info["playRecords"]["Perfect"],
            perfect_plus=player_info["playRecords"]["PerfectPlus"],
            play_record=player_info["playRecords"]
        )
        player_data_database.player_data.add_player(player=player, timestamp=timestamp)
        
        for song_data in song_datas:
            player_song_score = player_song_data_database.PlayerSongScore(
                object_id=object_id,
                difficulty=song_data["level"],
                score=song_data["score"],
                rating=song_data["ratingMix"]
            )
            
            player_song_data_database.player_song_score_manager.get_song_data(song_data["id"]).add_score(player_song_score)
        
        return {
            "playerInfo": player_info,
            "songDatas": song_datas
        }
    
    def get_user_data(self) -> dict:
        if self.user_profile["serverCode"].startswith("friend_"):
            followee_data = self.get_followee_data(short_id=self.user_profile["shortID"], raw_data=self.follow_user(short_id=self.user_profile["shortID"]))
            self.unfollow_user(short_id=self.user_profile["shortID"])
            raw_data = self.followee_data_to_user_data_raw_data_format(followee_data=followee_data)
            
            object_id = f"{self.user_profile['serverCode']}_{self.user_profile['shortID']}"
        else:
            raw_data = super().get_user_data()
            
            object_id = self.user_profile["objectID"]
        user_data = raw_data
        if user_data.get("privateSocialData", None) is None:
            raise ValueError("privateSocialData not found in user data, cannot process user data")
        save_dir = config.DATA_DIR / "rotaeno" / object_id / "user_data"
        save_dir.mkdir(parents=True, exist_ok=True)
        utils.save_data_to_file(raw_data, save_dir / str(time.time()))
        
        i = 0
        ii = 0
        iii = 0
        iv = 0
        iv_alpha = 0
        playStats = {"i": {}, "ii": {}, "iii": {}, "iv": {}, "iv_alpha": {}, "all": {}}
        for x in user_data["privateSocialData"]["UserData"]["SongRecords"]:
            i += find_keys_in_any_dict(user_data["privateSocialData"]["UserData"]["SongRecords"][x]["Levels"], ["I", "I"])["Score"]
            ii += find_keys_in_any_dict(user_data["privateSocialData"]["UserData"]["SongRecords"][x]["Levels"], ["Ii", "II"])["Score"]
            iii += find_keys_in_any_dict(user_data["privateSocialData"]["UserData"]["SongRecords"][x]["Levels"], ["Iii", "III"])["Score"]
            iv += find_keys_in_any_dict(user_data["privateSocialData"]["UserData"]["SongRecords"][x]["Levels"], ["Iv", "IV"])["Score"]
            iv_alpha += find_keys_in_any_dict(user_data["privateSocialData"]["UserData"]["SongRecords"][x]["Levels"], ["IV_Alpha"], default={"Score": 0})["Score"]
        playStats["i"]["scores"] = i
        playStats["ii"]["scores"] = ii
        playStats["iii"]["scores"] = iii
        playStats["iv"]["scores"] = iv
        playStats["iv_alpha"]["scores"] = iv_alpha
        playStats["all"]["scores"] = i + ii + iii + iv + iv_alpha
        
        return {
            "updateAt": user_data["updatedAt"],
            "friendCap": user_data["privateSocialData"]["FriendCap"],
            "avatar": user_data["privateSocialData"]["UserData"]["BadgeId"] if "boss" not in user_data["privateSocialData"]["UserData"]["BadgeId"] else user_data["privateSocialData"]["UserData"]["BadgeId"] + "-4",
            "background": user_data["privateSocialData"]["UserData"]["BackgroundId"].replace("background_", ""),
            "character": user_data["privateSocialData"]["UserData"]["CharacterId"].replace("character_", "") if user_data["privateSocialData"]["UserData"]["CharacterId"] is not None else "ilot",
            "showRating": user_data["privateSocialData"]["UserData"]["ShowRating"],
            "showCompletion": user_data["privateSocialData"]["UserData"]["ShowCompletion"],
            "exp": user_data["privateSocialData"]["UserData"]["Exp"],
            "level": calculate_level(user_data["privateSocialData"]["UserData"]["Exp"]),
            "displayName": user_data["privateSocialData"]["UserData"]["DisplayName"],
            "rating": user_data["privateSocialData"]["UserData"]["Rating"],
            "completion": user_data["privateSocialData"]["UserData"]["CompletionPoint"],
            "createdAt": user_data["createdAt"].split("T")[0],
            "emailVerified": user_data["emailVerified"],
            "mobilePhoneVerified": user_data["mobilePhoneVerified"],
            "playStats": playStats,
            "shortID": user_data["shortId"].lower(),
            "userID": user_data["authData"]["xdg"]["detail"]["userId"]
        }
    
    def get_followee_data(self, short_id: str = None) -> dict | list[dict]:
        def processing_followee_data(user_data):
            i = 0
            ii = 0
            iii = 0
            iv = 0
            iv_alpha = 0
                
            scoresKey = "scores" if "scores" in user_data else "songScores"
            for x in user_data[scoresKey]:
                    i += find_keys_in_any_dict(user_data[scoresKey][x], ["i", "I"], default=0)
                    ii += find_keys_in_any_dict(user_data[scoresKey][x], ["ii", "II"], default=0)
                    iii += find_keys_in_any_dict(user_data[scoresKey][x], ["iii", "III"], default=0)
                    iv += find_keys_in_any_dict(user_data[scoresKey][x], ["iv", "IV"], default=0)
                    iv_alpha += find_keys_in_any_dict(user_data[scoresKey][x], ["iv_alpha", "IV_Alpha"], default=0)
            user_data["playStats"]["i"] = user_data["playStats"].get("i", {})
            user_data["playStats"]["ii"] = user_data["playStats"].get("ii", {})
            user_data["playStats"]["iii"] = user_data["playStats"].get("iii", {})
            user_data["playStats"]["iv"] = user_data["playStats"].get("iv", {})
            user_data["playStats"]["iv_alpha"] = user_data["playStats"].get("iv_alpha", {})
            user_data["playStats"]["i"]["scores"] = i
            user_data["playStats"]["ii"]["scores"] = ii
            user_data["playStats"]["iii"]["scores"] = iii
            user_data["playStats"]["iv"]["scores"] = iv
            user_data["playStats"]["iv_alpha"]["scores"] = iv_alpha
            user_data["playStats"]["all"]["scores"] = i + ii + iii + iv + iv_alpha
            
            score_datas = user_data[scoresKey]
            for song_id, song_data in score_datas.items():
                score_datas[song_id] = {
                    "I": find_keys_in_any_dict(song_data, ["i", "I"], default=0),
                    "II": find_keys_in_any_dict(song_data, ["ii", "II"], default=0),
                    "III": find_keys_in_any_dict(song_data, ["iii", "III"], default=0),
                    "IV": find_keys_in_any_dict(song_data, ["iv", "IV"], default=0),
                    "IV_Alpha": find_keys_in_any_dict(song_data, ["iv_alpha", "IV_Alpha"], default=0)
                }
                    
            return {
                "shortID": user_data["shortId"].lower(),
                "rating": user_data["rating"],
                "displayName": user_data["displayName"],
                "playStats": user_data["playStats"],
                "isFriend": user_data["isTwoWayFriend"],
                "background": user_data["backgroundId"],
                "character": user_data["characterId"],
                "avatar": user_data["badgeId"],
                "exp": user_data["exp"],
                "level": calculate_level(user_data["exp"]),
                "songs": score_datas
            }
        
        raw_data = super().get_followee_data()
        follow_data = raw_data["result"]["socialDatas"]
        
        object_id = self.user_profile["objectID"]
        save_dir = config.DATA_DIR / "rotaeno" / object_id / "followee_data"
        save_dir.mkdir(parents=True, exist_ok=True)
        utils.save_data_to_file(raw_data, save_dir / str(time.time()))
        
        if short_id is not None:
            for user_data in follow_data:
                if user_data["shortId"].lower() == short_id.lower():
                    return processing_followee_data(user_data)
            raise ValueError(f"Followee with short ID `{short_id}` not found")

        return [processing_followee_data(user_data) for user_data in follow_data]

    def followee_data_to_cloud_save_raw_data_format(self, short_id: str = None, followee_data: dict = None) -> dict:
        if followee_data is None:
            followee_data = self.get_followee_data(short_id=short_id)
        
        followee_data_cloud_save_raw_data_format = {
            "results": [
                {
                    "cloudSave": {
                        "data": {
                            "data": {
                                "FavoriteSong": {"songIds": []},
                                "songs": {
                                    "songs": {
                                        song_id: {
                                            "levels": {
                                                level_name: {
                                                    "Score": song_data[level_name],
                                                    "Flag": "APP" if song_data[level_name] >= 1010000 else "NONE",
                                                    "IsCleared": True
                                                } for level_name in song_data
                                            }
                                        } for song_id, song_data in followee_data["songScores"].items()
                                    }
                                },
                                "profile": {
                                    "DisplayName": followee_data["playerDisplayName"]
                                },
                                "badges": {
                                    "EquippedBadgeId": followee_data["playerAvatar"]
                                },
                                "collectable-background": {
                                    "EquippedBackgroundId": followee_data["playerBackground"]
                                },
                                "collectable-character": {
                                    "EquippedCharacterId": followee_data["playerCharacter"]
                                },
                                "playRecords": {
                                    "TotalPlayCount": 0,
                                    "PlayCountI": 0,
                                    "PlayCountIi": 0,
                                    "PlayCountIii": 0,
                                    "PlayCountIv": 0,
                                    "TotalFc": 0,
                                    "TotalAp": 0,
                                    "TotalApp": 0,
                                    "TotalEx": 0,
                                    "TotalExPlus": 0,
                                    "Tap": 0,
                                    "Slide": 0,
                                    "Flick": 0,
                                    "Catch": 0,
                                    "Rotate": 0,
                                    "Early": 0,
                                    "Late": 0,
                                    "Good": 0,
                                    "Miss": 0,
                                    "Perfect": 0,
                                    "PerfectPlus": 0
                                },
                                "PlayerLevel": {
                                    "AccumXp": calculate_xp(followee_data["playerLevel"])
                                }
                            }
                        },
                        "TotalPlayTime": "0:0:0",
                        "ClientVersion": Config.GAME_VERSION_NAME
                    }
                }
            ]
        }
        
        return followee_data_cloud_save_raw_data_format
    
    def followee_data_to_user_data_raw_data_format(self, short_id: str = None, followee_data: dict = None) -> dict:
        if followee_data is None:
            followee_data = self.get_followee_data(short_id=short_id)
        
        followee_data_user_data_raw_data_format = {
            "sessionToken": "",
            "updatedAt": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "loginRecord": {},
            "privateSocialData": {
                "FriendCap": 1 if followee_data["isFriend"] else 0,
                "UserData": {
                    "BadgeId": followee_data["playerAvatar"],
                    "BackgroundId": followee_data["playerBackground"],
                    "CharacterId": followee_data["playerCharacter"],
                    "Rating": followee_data["playerRating"],
                    "ShowRating": True,
                    "ShowCompletion": False,
                    "CompletionPoint": 0,
                    "Exp": calculate_xp(followee_data["playerLevel"]),
                    "DisplayName": followee_data["playerDisplayName"],
                    "SongRecords": {
                        songID: {
                            "Levels": {
                                levelName: {
                                    "Score": songData[levelName],
                                    "Flag": "APP" if songData[levelName] >= 1010000 else "NONE",
                                    "IsCleared": True
                                } for levelName in songData
                            }
                        } for songID, songData in followee_data["songScores"].items()
                    }
                }
            },
            "objectId": "",
            "username": "",
            "shortId": followee_data["shortID"],
            "createdAt": "1970-01-01T00:0:01.000Z",
            "emailVerified": False,
            "banReason": "",
            "mirrorGemAmount": 0,
            "mirrorInventoryItemSids": [],
            "mirrorFreeGemAmount": 0,
            "mirrorPaidGemAmount": 0,
            "authData": {"xdg": {"detail": {"userId": ""}, "id": "", "access_token": ""}},
            "banUntilTime": {},
            "mobilePhoneVerified": False
        }
        
        return followee_data_user_data_raw_data_format
    
    def follow_user(self, short_id: str) -> dict:
        followee_data_raw_data_format = {
            "result": {
                "socialDatas": [super().follow_user(short_id=short_id)["result"]]
            }
        }
        return followee_data_raw_data_format
    
    def unfollow_user(self, short_id: str) -> dict:
        return super().unfollow_user(short_id=short_id)