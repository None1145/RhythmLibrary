import json
import base64
import requests
import Crypto.Cipher.AES
import Crypto.Util.Padding

from .model import ServerRegion, ServerSecret, ServerURL

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
        
        if region == ServerRegion.CN:
            self.base_url = ServerURL.CN
            self.identity = "phone"
        elif region == ServerRegion.GLOBAL:
            self.base_url = ServerURL.GLOBAL
            self.identity = "email"
        else:
            raise ValueError("Invalid region")
    
    def _build_headers(self, client: bool = False) -> dict:
        token = self.user_profile.get("token", None)
        identity = self.user_profile.get("identity", None)
        if not client and token is None:
            raise ValueError("Token not found")
        elif not client and identity is None:
            raise ValueError("Identity not found")
        
        headers = {
            "User-Agent": "UnityPlayer/2022.3.62f2 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
            "game_id": "pigeongames.rizline",
            "channel_id": "11",
            "i18n": self.user_profile.get("locale", "zh-CN"),
            "device_id": self.user_profile["device_id"],
            "Content-Type": "application/json"
        }
        
        if not client:
            headers["token"] = token
            headers[self.identity] = identity
        
        return headers
    
    def get(self, endpoint: str, params: dict = None, client: bool = False) -> requests.Response:
        return requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(client=client),
            params=params,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        )
    
    def post(self, endpoint: str, data: dict = None, client: bool = False) -> requests.Response:
        return requests.post(
            f"{self.base_url}/{endpoint}",
            headers=self._build_headers(client=client),
            json=data,
            allow_redirects=True,
            proxies=self.proxies,
            timeout=10,
            verify=self.verify_ssl,
        )
    
    def _decode(self, response: requests.Response | str) -> str | None:
        if isinstance(response, requests.Response):
            response = response.text
        
        try:
            cipher = Crypto.Cipher.AES.new(ServerSecret.AES["key"], Crypto.Cipher.AES.MODE_CBC, ServerSecret.AES["iv"])
            decrypted = cipher.decrypt(base64.b64decode(response))
            decrypted = Crypto.Util.Padding.unpad(decrypted, Crypto.Cipher.AES.block_size)
            return decrypted.decode()
        except:
            return None
    
    def decode(self, response: requests.Response | str) -> dict | None:
        content = self._decode(response=response)
        try:
            return json.loads(content)
        except:
            return content

class ClientAPI(BaseAPI):
    def _check_identity(self, identity: str) -> bool:
        if self.identity == "phone" and "@" in identity:
            return False
        elif self.identity == "email" and "@" not in identity:
            return False
        return True
    
    def _check_verify_code(self, verify_code: int | str) -> bool:
        try:
            return 99999 < int(verify_code) and int(verify_code) < 1000000
        except: ...
        return False
    
    def check_identity(self, identity: str) -> bool:
        assert self._check_identity(identity=identity), "Invalid identity"
        
        response = self.post(endpoint=f"account/check_{self.identity}", data={self.identity: identity}, client=True)
        if response.status_code != 200:
            return False
        
        return response.json().get("code", 0) == 1
    
    def verify_identity(self, identity: str) -> bool:
        assert self._check_identity(identity=identity), "Invalid identity"
        
        if self.identity == "phone":
            endpoint = f"account/send_verify_code"
        elif self.identity == "email":
            endpoint = f"account/send_email"
        
        response = self.post(endpoint=endpoint, data={self.identity: identity, "transaction": "login"}, client=True)
        return response.status_code == 200
    
    def login(self, identity: str, verify_code: int | str) -> str | None:
        assert self._check_identity(identity=identity), "Invalid identity"
        assert self._check_verify_code(verify_code=verify_code), "Invalid verify code"
        
        response = self.post(endpoint=f"account/login", data={self.identity: identity, "code": str(verify_code)}, client=True)
        return response.headers.get("set_token", None)

class UserAPI(ClientAPI):
    def get_login_data(self):
        return self.decode(response=self.post("game/rn_login", data={}))
    
    def get_user_info(self):
        return self.decode(response=self.post("game/fetch_user_info", data={}))
