import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import phigros

user_profiles = [
    {
        "serverCode": "cn",
        "sessionToken": "",
        "objectID": ""
    },
    {
        "serverCode": "global",
        "sessionToken": "",
        "objectID": ""
    },
]


class TestProcessor:
    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_user_data(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        user_data = processor.get_user_data()
        assert "nickname" in user_data
        assert "sessionToken" in user_data

    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_summaries(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        summaries = processor.get_summaries()
        assert isinstance(summaries, list)
        assert len(summaries) > 0
        assert "summary" in summaries[0]
        assert "saveURL" in summaries[0]

    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_latest_summary(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        latest = processor.get_latest_summary()
        assert "saveURL" in latest
        assert "summary" in latest

    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_game_record(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        records = processor.get_game_record()
        assert isinstance(records, list)
        if len(records) > 0:
            r = records[0]
            assert "title" in r
            assert "score" in r
            assert "accuracy" in r
            assert "diff" in r
            assert "level" in r
            assert "rating" in r

    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_user(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        user = processor.get_user()
        assert "nickname" in user
        assert "avatar" in user

    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_user_info(self, user_profile):
        processor = phigros.api.processor.Processor(
            user_profile=user_profile, verify_ssl=False
        )
        info = processor.get_user_info()
        assert "nickname" in info
        assert "summary" in info


class TestBest30:
    @pytest.mark.parametrize("user_profile", user_profiles)
    def test_get_best30_data(self, user_profile):
        result = phigros.processor.get_best30(user_profile=user_profile, just_data=True)
        assert isinstance(result, dict)
        assert "user_info" in result
        assert "song_data" in result
        songs = result["song_data"]
        assert isinstance(songs, list)
        assert len(songs) <= 30
        if len(songs) > 0:
            assert "title" in songs[0]
            assert "rating" in songs[0]
