"""Usage examples for all supported rhythm game modules.

Each example uses the recommended import style and shows the available
output modes: raw data (just_data=True), HTML (just_html=True),
or rendered JPG image (default).
"""

from phigros.processor import get_best30
from rizline.processor import get_best40, get_data
from rotaeno.processor import get_best40 as rotaeno_get_best40
from rotaeno.processor import get_song, get_song_rtr, get_song_status

# ── Phigros ───────────────────────────────────────────────────────────────────

# Best30 (just_data=True returns a list of song dicts)
best30_data = get_best30(
    user_profile={
        "serverCode": "cn",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    just_data=True,
)

# Best30 (default returns a rendered JPG image path)
best30_image = get_best30(
    user_profile={
        "serverCode": "cn",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
)

# Best30 (just_html=True returns the HTML string)
best30_html = get_best30(
    user_profile={
        "serverCode": "cn",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    just_html=True,
)

# ── Rotaeno ───────────────────────────────────────────────────────────────────

# Best40 (just_data=True returns a list of song dicts)
best40_data = rotaeno_get_best40(
    user_profile={
        "serverCode": "global",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
        "locale": "en-US",
    },
    just_data=True,
)

# Single song detail (aggregated by difficulty, includes artist)
song_data = get_song(
    user_profile={
        "serverCode": "global",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    song_id="song_id_here",
)

# Filter by status (returns HTML)
ap_songs_html = get_song_status(
    user_profile={
        "serverCode": "global",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    song_status="AP",
    just_html=True,
)

# Filter by difficulty range + sort by score
songs_by_range = get_song_rtr(
    user_profile={
        "serverCode": "global",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    song_level_num_range=(12.5, 14.0),
    song_sort_type="score",
    just_data=True,
)

# ── Rizline ───────────────────────────────────────────────────────────────────

# Raw login data (player info + song records)
login_data = get_data(
    user_profile={
        "serverCode": "cn",
        "token": "your_token",
    },
)

# Best40 by RKS (just_data=True returns a list of song dicts)
best40_rzl = get_best40(
    user_profile={
        "serverCode": "cn",
        "token": "your_token",
    },
    just_data=True,
)

# ── KALPA ─────────────────────────────────────────────────────────────────────

from kalpa.processor import get_user_info

player_info = get_user_info(
    user_profile={
        "userid": "your_userid",
        "password": "your_password",
    },
    client_version=30209,
)
