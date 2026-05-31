from __future__ import annotations

from . import api


def get_api_processor(
    user_profile: dict,
    *,
    client_version: int,
) -> api.processor.MobileProcessor:
    """
    获取 KALPA 的 API Processor（统一各子项目入口风格）。

    目前仅封装移动端（Mobile）接口；如后续补齐 PC 端，可在这里扩展。
    """

    return api.processor.MobileProcessor(client_version=client_version, user_profile=user_profile)


def get_user_info(user_profile: dict, *, client_version: int) -> dict:
    """获取用户信息（对外入口统一使用 get_xxx 命名）。"""

    return get_api_processor(user_profile=user_profile, client_version=client_version).get_user_info()
