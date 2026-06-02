from __future__ import annotations

import os
import time
import hashlib

import curlify
import requests

from .model import ServerRegion, ServerSecret, ServerURL

_original_send = requests.Session.send


def _send_with_curl(self, request, **kwargs):
    print("[CURL]", curlify.to_curl(request))
    return _original_send(self, request, **kwargs)


# 默认不污染全局 requests 行为；需要时可设置环境变量启用：
#   RHYTHMLIBRARY_DEBUG_CURL=1
if os.getenv("RHYTHMLIBRARY_DEBUG_CURL") == "1":
    requests.Session.send = _send_with_curl

class BaseAPI:
    def __init__(
        self,
        region: ServerRegion,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        self.region = region
        self.user_profile = user_profile
        self.proxies = proxies
        self.verify_ssl = verify_ssl
        
        self.requests = requests.Session()

        if self.region == ServerRegion.CN:
            self.base_url = ServerURL.CN
            self.secret = ServerSecret.CN
        elif self.region == ServerRegion.GLOBAL:
            self.base_url = ServerURL.GLOBAL
            self.secret = ServerSecret.GLOBAL
        else:
            raise ValueError("Invalid region")

    def _build_headers(self) -> dict:
        timestamp = str(int(time.time() * 1000))
        sign_raw = f"{timestamp}{self.secret['key']}".encode("utf-8")
        sign = hashlib.md5(sign_raw).hexdigest()
        
        return {
            "X-LC-Sign": f"{sign},{timestamp}",
            "X-LC-Session": self.user_profile.get("sessionToken", ""),
            "X-LC-Id": self.secret["id"],
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: dict = None) -> dict:
        return self.requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            params=params,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

    def post(self, endpoint: str, data: dict = None) -> dict:
        return self.requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

    def put(self, endpoint: str, data: dict = None) -> dict:
        return self.requests.put(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        ).json()

class UserAPI(BaseAPI):
    def get_user_data(self) -> dict:
        return self.get("/1.1/users/me")
    
    def get_summaries(self) -> dict:
        return self.get("/1.1/classes/_GameSave")
