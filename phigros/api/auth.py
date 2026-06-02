from __future__ import annotations

import json
import random
import time
import base64
import hmac
import tempfile
from urllib.parse import urlparse

import requests

from .model import AuthServerURL, ServerRegion, ServerSecret, ServerURL


class TapTapLogin:
    def __init__(self, region: ServerRegion, device_id: str | None = None, *, verify_ssl: bool = False) -> None:
        self.device_id = device_id
        self.verify_ssl = verify_ssl
        if device_id is None:
            raise ValueError("Device ID cannot be None")
        if region == ServerRegion.CN:
            self.app_key = ServerSecret.CN["key"]
            self.app_id = ServerSecret.CN["id"]
            self.cloud_server_address = ServerURL.CN
            self.code_url = AuthServerURL.CN["code"]
            self.token_url = AuthServerURL.CN["token"]
            self.account_url = AuthServerURL.CN["account"]
        elif region == ServerRegion.GLOBAL:
            self.app_key = ServerSecret.GLOBAL["key"]
            self.app_id = ServerSecret.GLOBAL["id"]
            self.cloud_server_address = ServerURL.GLOBAL
            self.code_url = AuthServerURL.GLOBAL["code"]
            self.token_url = AuthServerURL.GLOBAL["token"]
            self.account_url = AuthServerURL.GLOBAL["account"]
        else:
            raise ValueError("Invalid region")

        self.account_host = urlparse(self.account_url).hostname

    def _mac_sign(self, token: dict, method: str, path: str) -> str:
        ts = int(time.time())
        nonce = random.randint(0, 2**32 - 1)
        input_str = f"{ts}\n{nonce}\n{method}\n{path}\n{self.account_host}\n443\n\n"
        mac = hmac.new(token["mac_key"].encode(), input_str.encode(), "sha1")
        mac_base64 = base64.b64encode(mac.digest()).decode()
        return f"MAC id=\"{token['kid']}\",ts=\"{ts}\",nonce=\"{nonce}\",mac=\"{mac_base64}\""

    @staticmethod
    def _md5hash(text: str) -> str:
        from hashlib import md5
        return md5(text.encode()).hexdigest()

    def sign_headers(self, headers: dict, add_app_key: bool = False) -> None:
        ts = int(time.time() * 1000)
        raw = f"{ts}{self.app_key}" if add_app_key else str(ts)
        headers["X-LC-Sign"] = f"{self._md5hash(raw)},{ts}"

    def get_qrcode(self) -> dict:
        from qrcode import make

        device_id = self.device_id
        response = requests.post(
            self.code_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "TapTapAndroidSDK/3.16.5",
            },
            data=(
                f"client_id={self.app_id}"
                f"&response_type=device_code"
                f"&scope=basic_info"
                f"&version=1.2.0"
                f"&platform=unity"
                f"&info=%7b%22device_id%22%3a%22{device_id}%22%7d"
            ),
            verify=self.verify_ssl,
            timeout=10,
        )
        data = response.json()["data"]
        with tempfile.NamedTemporaryFile(mode="w+t", delete=False, suffix=".png") as tmp:
            make(data["qrcode_url"]).save(tmp.name, format="PNG")
            return {
                "device_code": data["device_code"],
                "qrcode_url": data["qrcode_url"],
                "interval": data["interval"],
                "device_id": device_id,
                "image": tmp.name,
            }

    def check_login(self, qrcode_data: dict) -> dict:
        device_id = qrcode_data["device_id"]
        response = requests.post(
            self.token_url,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "TapTapAndroidSDK/3.16.5",
            },
            data=(
                f"grant_type=device_token"
                f"&client_id={self.app_id}"
                f"&secret_type=hmac-sha-1"
                f"&code={qrcode_data['device_code']}"
                f"&version=1.0"
                f"&platform=unity"
                f"&info=%7b%22device_id%22%3a%22{device_id}%22%7d"
            ),
            verify=self.verify_ssl,
            timeout=10,
        )
        return response.json()

    def get_account_info(self, token: dict) -> dict:
        parsed = urlparse(self.account_url)
        path = f"{parsed.path}?client_id={self.app_id}"
        url = f"{self.account_url}?client_id={self.app_id}"
        response = requests.get(
            url,
            headers={
                "User-Agent": "TapTapAndroidSDK/3.16.5",
                "Authorization": self._mac_sign(token, "GET", path),
            },
            verify=self.verify_ssl,
            timeout=10,
        )
        return response.json()

    def get_objectid_and_sessiontoken(self, qrcode_data: dict | None = None, show_qrcode: bool = True) -> dict:
        from qrcode import make

        if qrcode_data is None:
            qrcode_data = self.get_qrcode()

        if show_qrcode:
            make(qrcode_data["qrcode_url"]).show()

        wait_time = qrcode_data["interval"]
        elapsed = 0.0
        while True:
            t0 = time.time()
            login_info = self.check_login(qrcode_data)
            if login_info.get("data") is not None and login_info["data"].get("kid") is not None:
                break
            time.sleep(wait_time)
            elapsed += time.time() - t0
            if elapsed > 120:
                raise TimeoutError("QR code expired")

        token = login_info["data"]
        account_data = self.get_account_info(token).get("data", {})

        response = requests.post(
            f"{self.cloud_server_address}/1.1/users",
            headers={
                "Content-Type": "application/json",
                "X-LC-Id": self.app_id,
                "X-LC-Key": self.app_key,
            },
            data=json.dumps({
                "authData": {
                    "taptap": {
                        "kid": token["kid"],
                        "access_token": token["kid"],
                        "token_type": "mac",
                        "mac_key": token["mac_key"],
                        "mac_algorithm": "hmac-sha-1",
                        "openid": account_data["openid"],
                        "unionid": account_data["unionid"],
                    }
                }
            }),
            verify=self.verify_ssl,
            timeout=10,
        )
        userdata = response.json()
        userdata["sessionToken"]
        userdata["objectId"]
        return {"sessionToken": userdata["sessionToken"], "objectID": userdata["objectId"]}
