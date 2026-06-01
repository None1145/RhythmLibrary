from . import api

def get_api_processor(user_profile: dict) -> api.processor.Processor:
    if user_profile["serverCode"] == "cn": region = api.model.ServerRegion.CN
    elif user_profile["serverCode"] == "global": region = api.model.ServerRegion.GLOBAL
    return api.processor.Processor(region=region, user_profile=user_profile)

def get_data(user_profile: dict) -> dict:
    data = get_api_processor(user_profile).get_data()
    return data
