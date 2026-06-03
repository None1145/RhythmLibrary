import fake_useragent
import requests
import requests.cookies

from .model import AuthServerURL

class International:
    @staticmethod
    def clal(clal: str) -> dict:
        headers = {
            "User-Agent": fake_useragent.UserAgent(
                os=["windows", "macos", "android", "ios"]
            ).random
        }
        cookiejar = requests.cookies.RequestsCookieJar()

        response = requests.get(
            AuthServerURL.INTERNATIONAL["mobile"],
            headers=headers,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        response = requests.get(
            response.headers.get("Location"),
            headers={"Cookie": f"clal={clal}"},
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException

        response = requests.get(
            response.headers.get("Location"),
            headers=headers,
            cookies=cookiejar,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        return {"_t": cookiejar["_t"], "userId": cookiejar["userId"]}

    @staticmethod
    def sega(sid: str, password: str) -> dict:
        headers = {
            "User-Agent": fake_useragent.UserAgent(
                os=["windows", "macos", "android", "ios"]
            ).random
        }
        cookiejar = requests.cookies.RequestsCookieJar()

        response = requests.get(
            AuthServerURL.INTERNATIONAL["mobile"],
            headers=headers,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        response = requests.get(
            response.headers.get("Location"),
            cookies=cookiejar,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 200:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        response = requests.post(
            AuthServerURL.INTERNATIONAL["sega_login"],
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "retention": "1",
                "sid": sid,
                "password": password
            },
            cookies=cookiejar,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        response = requests.get(
            response.headers.get("Location"),
            headers=headers,
            cookies=cookiejar,
            allow_redirects=False,
            verify=False
        )
        if response.status_code != 302:
            raise requests.RequestException
        cookiejar.update(response.cookies)

        return {"_t": cookiejar["_t"], "userId": cookiejar["userId"]}
