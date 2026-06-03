from __future__ import annotations

from typing import List

from .request import UserAPI
from .model import ServerRegion

try:
    from ...common import utils
    from ...common import config
except ImportError:
    from common import utils
    from common import config


class Processor:
    def __init__(
        self,
        region: ServerRegion,
        user_profile: dict,
        proxies: dict | None = None,
        *,
        verify_ssl: bool = False,
    ) -> None:
        self.api = UserAPI(region=region, user_profile=user_profile, proxies=proxies, verify_ssl=verify_ssl)

    def get_best50(self) -> List[dict]:
        return self.api.get_best50()
