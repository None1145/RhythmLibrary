import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import rizline

def main(region: rizline.api.model.ServerRegion, user_profile: dict, platform: str, save_path: str):
    base_api = rizline.api.request.BaseAPI(region=region, user_profile=user_profile, verify_ssl=False)
    
    response = base_api.get("game/server_api/v1/dis", client=True).json()
    version = response["minimalVersion"]
    for config in response["configs"]:
        if config["version"] == version:
            break
    
    if region == rizline.api.model.ServerRegion.CN:
        base_api.base_url = "https://rizlineasset.pigeongames.net"
    elif region == rizline.api.model.ServerRegion.GLOBAL:
        base_api.base_url = "https://rizlineassetstore.pigeongames.cn"
    
    endpoints = {}
    def get(version: str) -> None:
        response = base_api.get(f"versions/{version}/patch_metadata", client=True)
        if response.status_code != 200:
            return
        patch_metadata = response.text.strip().split("\n")
        for metadata in patch_metadata[1:]:
            if platform not in metadata:
                continue
            endpoints[f"versions/{version}/{metadata}"] = metadata
        get(version=patch_metadata[0])
    get(version=config["resourceVersion"])
    
    for endpoint, path in endpoints.items():
        os.makedirs(os.path.dirname(os.path.join(save_path, path)), exist_ok=True)
        response = base_api.get(endpoint, client=True)
        with open(os.path.join(save_path, path), "wb") as f:
            f.write(response.content)

main(
    region=rizline.api.model.ServerRegion.CN,
    user_profile={
        "serverCode": "cn",
        "token": "",
        "phone": "",
        "device_id": ""
    },
    platform="Android",
    save_path=r""
)
