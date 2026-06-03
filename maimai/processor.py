from . import api
try:
    from ..common import utils
except ImportError:
    from common import utils

import json
import string

class SafeTemplate(string.Template):
    delimiter = "$$"

def get_api_processor(user_profile: dict) -> api.processor.Processor:
    server_code = user_profile.get("serverCode", user_profile.get("server", None))
    if server_code == "cn":
        region = api.model.ServerRegion.CN
    elif server_code == "international":
        region = api.model.ServerRegion.INTERNATIONAL
    elif server_code == "jp":
        region = api.model.ServerRegion.JP
    else:
        raise ValueError("Invalid region")
    return api.processor.Processor(region=region, user_profile=user_profile)
