import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import rizline

user_profiles = [
    {
        "serverCode": "cn",
        "token": "",
        "phone": "",
        "device_id": ""
    }
]

class TestRequest:
    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_login_data(self, user_profile):
        user_api = rizline.api.request.UserAPI(region=rizline.api.model.ServerRegion(user_profile["serverCode"]), user_profile=user_profile, verify_ssl=False)
        assert "username" in user_api.get_login_data()
