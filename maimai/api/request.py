from __future__ import annotations

import re
import random
from abc import ABC, abstractmethod
from typing import List
import requests
import requests.cookies
from bs4 import BeautifulSoup

from .model import ServerRegion, ServerURL

class BaseAPI(ABC):
    def __init__(
        self,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        self.user_profile = user_profile
        self.proxies = proxies
        self.verify_ssl = verify_ssl
        self.requests = requests.Session()
    
    @abstractmethod
    def _build_headers(self) -> dict: ...

    @abstractmethod
    def get(self, endpoint: str, params: dict | None = None) -> str | dict: ...

    @abstractmethod
    def post(self, endpoint: str, data: dict | None = None) -> str | dict: ...
    
    @abstractmethod
    def get_best50(self) -> List[dict]: ...

class InternationalUtils:
    @staticmethod
    def parse_best50_page(content: str) -> List[dict]:
        soup = BeautifulSoup(content, "html.parser")
        songs = []
        current_category = None
        
        for div in soup.find_all("div", recursive=True):
            classes = div.get("class", [])
            
            if "screw_block" in classes:
                current_category = div.get_text(strip=True)
                continue
            
            if not any("score_back" in c for c in classes):
                continue
            
            song = {"category": current_category}
            
            diff_img = div.find("img", src=re.compile(r"diff_\w+\.png"))
            if diff_img:
                diff_match = re.search(r"diff_(\w+)\.png", diff_img["src"])
                if diff_match:
                    song["difficulty"] = diff_match.group(1).lower()
            
            kind_img = div.find("img", class_="music_kind_icon")
            if kind_img and "src" in kind_img.attrs:
                if "music_dx.png" in kind_img["src"]:
                    song["type"] = "DX"
                elif "music_standard.png" in kind_img["src"]:
                    song["type"] = "Standard"
            
            level_elem = div.find("div", class_="music_lv_block")
            if level_elem:
                song["level"] = level_elem.get_text(strip=True)
            
            name_elem = div.find("div", class_="music_name_block")
            if name_elem:
                song["song_name"] = name_elem.get_text(strip=True)
            
            score_elem = div.find("div", class_="music_score_block")
            if score_elem:
                score_text = score_elem.get_text(strip=True)
                match = re.search(r"([\d\.]+)%", score_text)
                if match:
                    song["score_percent"] = float(match.group(1))
                else:
                    song["score_percent"] = None

            rank_img = div.find("img", class_="ratingtarget_scorerank_img")
            if rank_img and "src" in rank_img.attrs:
                rank_match = re.search(r"music_icon_(\w+)\.png", rank_img["src"])
                if rank_match:
                    song["rank"] = rank_match.group(1).upper()

            songs.append(song)

        return songs

class InternationalAPI(BaseAPI):
    @staticmethod
    def check_cookie(user_profile: dict):
        if "_t" not in user_profile:
            raise ValueError("InternationalAPI requires '_t' in user_profile")
        if "userId" not in user_profile:
            raise ValueError("InternationalAPI requires 'userId' in user_profile")
    
    @staticmethod
    def require_cookie(method):
        def wrapper(self, *args, **kwargs):
            self.check_cookie(user_profile=self.user_profile)
            return method(self, *args, **kwargs)
        return wrapper

    def __init__(
        self,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        super().__init__(user_profile, proxies=proxies, verify_ssl=verify_ssl)
        self.base_url = ServerURL.INTERNATIONAL

    def _build_headers(self) -> dict:
        def build_user_agent(seed: int):
            rng = random.Random(seed)
            chrome_ver = f"{rng.randint(110,130)}.0.{rng.randint(1000,5000)}.{rng.randint(0,200)}"
            os_ver = f"{rng.randint(10,15)}.0"
            return f"Mozilla/5.0 (Windows NT {os_ver}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"

        try:
            self.check_cookie(user_profile=self.user_profile)
            return {
                "User-Agent": build_user_agent(self.user_profile.get("device", "undefined")),
                "Cookie": f"_t={self.user_profile['_t']}; userId={self.user_profile['userId']}"
            }
        except:
            return {"User-Agent": build_user_agent(self.user_profile.get("device", "undefined"))}

    def get(self, endpoint: str, params: dict | None = None) -> str:
        response = self.requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            params=params,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        )
        if "error" in response.headers.get("Location"):
            raise Exception
        
        return response.text

    def post(self, endpoint: str, data: dict | None = None) -> str:
        response = self.requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        )
        if "error" in response.headers.get("Location"):
            raise Exception
        
        return response.text

    @require_cookie
    def get_best50(self) -> List[dict]:
        content = self.get("maimai-mobile/home/ratingTargetMusic")
        return InternationalUtils.parse_best50_page(content=content)

class CNAPI(BaseAPI):
    def __init__(
        self,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        super().__init__(user_profile, proxies=proxies, verify_ssl=verify_ssl)
        self.base_url = ServerURL.CN
        raise NotImplementedError("CN region not yet implemented")

    def _build_headers(self) -> dict:
        return {}

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        return self.requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            params=params,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

    def post(self, endpoint: str, data: dict | None = None) -> dict:
        return self.requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

class JPAPI(BaseAPI):
    def __init__(
        self,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        super().__init__(user_profile, proxies=proxies, verify_ssl=verify_ssl)
        self.base_url = ServerURL.JP
        raise NotImplementedError("JP region not yet implemented")

    def _build_headers(self) -> dict:
        return {}

    def get(self, endpoint: str, params: dict | None = None) -> dict:
        return self.requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            params=params,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

    def post(self, endpoint: str, data: dict | None = None) -> dict:
        return self.requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

class UserAPI(BaseAPI):
    def __new__(cls, region: ServerRegion, user_profile: dict, proxies: dict | None = None, *, verify_ssl: bool = False):
        mapping = {
            ServerRegion.INTERNATIONAL: InternationalAPI,
            ServerRegion.CN: CNAPI,
            ServerRegion.JP: JPAPI,
        }
        if region not in mapping:
            raise ValueError(f"Invalid region: {region}")
        return mapping[region](user_profile, proxies=proxies, verify_ssl=verify_ssl)
