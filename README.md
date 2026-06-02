# RhythmLibrary

> A Python tool library for querying player data and score records from multiple mobile rhythm games. Supports authentication, cloud save decryption, rating computation (Best30/Best40/Best40+RKS), and scorecard image rendering.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](pyproject.toml)

---

## ✨ Features

- **Multi-game support** — Query player data from Phigros, Rotaeno, Rizline, and KALPA
- **QR-code authentication** — TapTap-based device code login (no password needed)
- **Binary decryption** — Decrypt game-specific encrypted save data (AES-CBC, custom binary formats)
- **Rating computation** — Calculate Best30, Best40, RKS, Completion Points using official formulas
- **Local databases** — Persist song metadata, player history, and per-song score history via SQLAlchemy
- **Scorecard rendering** — Generate shareable JPG/PNG scorecard images via Playwright (Chromium)
- **Friend data** — View followee/friend cloud saves (Rotaeno)

---

## 🎮 Supported Games

| Game | Module | Status | Key Features |
|------|--------|--------|-------------|
| **Phigros** | `phigros/` | ✅ Supported | TapTap auth, AES decrypted save, Best30 rating |
| **Rotaeno** | `rotaeno/` | ✅ Supported | Full cloud save parse, Best40, Completion Points, friend data, historical tracking |
| **Rizline** | `rizline/` | ✅ Supported | AES-CBC API, Best40 (RKS), asset downloader |
| **KALPA** | `kalpa/` | ✅ Supported | Mobile API user info retrieval |
| CHUNITHM | — | 🗂️ Planned | |
| MAIMAI DX | — | 🗂️ Planned | |
| Orzmic | — | 🗂️ Planned | |
| osu! | — | 🗂️ Planned | |

---

## 🏗️ Architecture

Each game module follows a consistent layered design:

```
rhythmlibrary/
├── common/                    # Shared utilities across all modules
│   ├── config.py              # DATA_DIR, TEMP_DIR paths
│   └── utils.py               # save_data, compress_image, render_html_to_jpg
│
├── {game}/
│   ├── __init__.py
│   ├── config.py              # Game-specific paths and constants
│   ├── processor.py           # 🎯 Public API entry points
│   │
│   ├── api/
│   │   ├── model.py           # Enums: ServerRegion, URL, secrets
│   │   ├── request.py         # Low-level HTTP client (REST / LeanCloud)
│   │   ├── processor.py       # Core logic: decrypt, parse, compute ratings
│   │   └── auth.py            # TapTap QR-code authentication flow
│   │
│   ├── database/
│   │   ├── song_data.py       # Song metadata DB (SQLAlchemy + SQLite)
│   │   ├── player_data.py     # Player history tracking (Rotaeno)
│   │   └── player_song_data.py# Per-song score history (Rotaeno)
│   │
│   ├── assets/
│   │   └── html/              # Tailwind/React HTML templates for rendering
│   │
│   └── saves/                 # Downloaded save data (cached locally)
│
├── downloader/
│   └── rizline_cli.py         # Rizline asset downloader CLI
│
├── common/
│   └── utils.py               # Shared: CompressImage, RenderHtmlToJpg
│
└── tests/                     # Integration tests (credential-gated)
```

### Layered Architecture in Detail

1. **`api/request.py`** — REST client wrapping the game's backend (LeanCloud for Phigros/Rotaeno, custom for Rizline/KALPA). Handles MD5-signed headers, AES-CBC decryption, and session management.
2. **`api/processor.py`** — The core processing layer: decrypts binary save data, parses game records, and computes rating metrics.
3. **`database/`** — SQLite-backed song metadata and player history storage (upsert + append-only history).
4. **`processor.py`** (top-level) — Public API: single-function entry points like `get_best30()`, `get_best40()`, `get_song()`.
5. **`assets/html/`** — HTML/CSS templates rendered via Playwright headless Chromium into shareable scorecard images.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [Playwright Chromium](https://playwright.dev/python/) (for image rendering)

### Installation

```bash
# Clone the repository
git clone https://github.com/None1145/RhythmLibrary.git
cd RhythmLibrary

# Install dependencies
pip install -r requirements.txt

# Install Playwright Chromium browser
playwright install chromium
```

See [`example.py`](example.py) for complete usage examples across all supported games.

---

## 📦 Module Details

### 🔴 Phigros

| Public API | Description |
|-----------|-------------|
| `get_api_processor(user_profile)` | Create a `Processor`. `user_profile` requires `"serverCode"` (`"cn"` or `"global"`), `"objectID"`, and `"sessionToken"` |
| `get_best30(user_profile, just_data, just_html)` | Fetch Best30 data. `just_data=True` → list of dicts, `just_html=True` → HTML string, default → rendered JPG image path |

**Usage:**
```python
from phigros.processor import get_best30

# just_data=True returns raw data as a list
data = get_best30(
    user_profile={
        "serverCode": "cn",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    },
    just_data=True
)

# Default returns a rendered JPG image path
image_path = get_best30(
    user_profile={
        "serverCode": "cn",
        "objectID": "your_object_id",
        "sessionToken": "your_session_token",
    }
)
```

**Implementation details:**
- **Authentication** — TapTap device-code QR login. Scans QR code, exchanges for TapTap token (MAC-signed), creates a LeanCloud user, and returns `sessionToken` + `objectID`
- **Save decryption** — Downloads encrypted zip from LeanCloud, AES-256-CBC decrypts the inner file (hardcoded key/IV), then parses the custom binary format with `ByteReader`
- **Best30 selection** — All scores sorted by rating descending; top 3 slots prioritize All Perfect (AP) clears
- **Rating formula** — `(((acc × 100 − 55) / 45)²) × difficulty`
- **Summary decoding** — The `summary` field in save data is base64-encoded; decoded payload contains rks, challenge score, and per-difficulty Clear/FC/AP counts
- **SafeTemplate** — Uses `string.Template` subclass with `$$` delimiter to avoid conflicts with JavaScript template literals in the HTML template
- **Auto-caching** — Downloaded saves and user data are automatically saved to `common.config.DATA_DIR/phigros/{objectID}/`

### 🔵 Rotaeno

| Public API | Description |
|-----------|-------------|
| `get_api_processor(user_profile)` | Create a `Processor`. `user_profile` must contain `"serverCode"` (`"cn"` / `"global"` / `"friend_cn"` / `"friend_global"`) |
| `get_best40(user_profile, just_data, just_html)` | Fetch Best40 data (top 40 by `ratingMix` descending) |
| `get_song(user_profile, song_id, just_data, just_html)` | Query a single song's detailed data (aggregated by difficulty, includes artist) |
| `get_song_status(user_profile, song_status, just_data, just_html)` | Filter songs by status: `"CLEAR"` / `"NOTCLEAR"` / `"FAVORITE"` / `"NOTFAVORITE"`, or a specific status like `"AP"` / `"FC"` / `"APP"` |
| `get_song_rtr(user_profile, song_level_num_range, song_sort_type, just_data, just_html)` | Filter songs by difficulty range + sort order. Default range `(12.5, 1145)`, supports `"rating"` / `"score"` / `"level"` sorting |

**Usage:**
```python
from rotaeno.processor import get_best40, get_song, get_song_status, get_song_rtr

# Best40 data
data = get_best40(
    user_profile={"serverCode": "global", "objectID": "...", "sessionToken": "...", "locale": "en-US"},
    just_data=True
)

# Single song info
song = get_song(
    user_profile={"serverCode": "global", "objectID": "...", "sessionToken": "..."},
    song_id="song_xxx"
)

# Filter by status (returns HTML)
html = get_song_status(
    user_profile={"serverCode": "global", "objectID": "...", "sessionToken": "..."},
    song_status="AP",
    just_html=True
)
```

**Implementation details:**
- **Authentication** — TapTap device-code QR login + XDSDK Union Token exchange for dual-layer auth
- **Cloud save parsing** — Fetches JSON from LeanCloud `CloudSave` class, extracts player info (nickname, avatar, background, character, level, play time, collectibles, etc.)
- **Rating algorithm** — Vectorized piecewise linear interpolation via NumPy (`calculate_song_ratings()`). Overall Rating = `(top10_sum × 0.6 / 10) + (next10_sum × 0.2 / 10) + (20-40_sum × 0.2 / 20)`
- **Completion Points** — Computed from rating ratio + score bonuses + FC/AP/APP status bonuses
- **Player level** — Calculated from XP via a bracket lookup table (`calculate_level()` / `calculate_xp()`)
- **Version compatibility** — ~300 song rating change entries in `_CHANGE_SONGS` for v2.23.0, auto-applied based on the player's save version; `_REMOVED_SONGS` handles delisted songs
- **Difficulty conflict** — `IV_Alpha` and `IV` share the same tier; only the higher rating is counted
- **Friend mode** — `friend_cn` / `friend_global` regions use pre-configured friend credentials to query followee cloud saves via the `GetAllFolloweeSocialData` cloud function
- **Local databases** — `player_data.py` tracks player history (`player_latest` upsert + `player_history` append-only with timestamps), `player_song_data.py` tracks per-song score history (WAL mode)

### 🟢 Rizline

| Public API | Description |
|-----------|-------------|
| `get_api_processor(user_profile)` | Create a `Processor`. `user_profile` must contain `"serverCode"` (`"cn"` or `"global"`) |
| `get_data(user_profile)` | Fetch raw login data (`player_info` + `song_datas`) |
| `get_best40(user_profile, just_data, just_html)` | Fetch Best40 data (top 40 by RKS descending) |

**Usage:**
```python
from rizline.processor import get_data, get_best40

# Raw login data
data = get_data(
    user_profile={"serverCode": "cn", "token": "..."}
)

# Best40
best40 = get_best40(
    user_profile={"serverCode": "cn", "token": "..."},
    just_data=True
)
```

**Implementation details:**
- **Authentication** — Phone verification code flow (`check_identity` → `send_verify_code` → `login_with_code`)
- **API encryption** — Response body decrypted with AES-CBC (hardcoded hex key/IV) via `BaseAPI._decode()`
- **RKS calculation** — `Processor.get_data()` parses `raw_data` into `player_info` (name, coin, dot, avatar, bio, background, RKS) and `song_datas` (each with id, level, score, completion rate, FC flag, clear flag). RKS = average of top 40 song RKS values
- **Layered API** — `BaseAPI` (generic REST + AES decode) → `ClientAPI` (identity verification / login) → `UserAPI` (data retrieval)
- **Device identification** — Request headers include Unity User-Agent, `game_id`, `device_id`, and `locale`
- **Asset downloader** — `downloader/rizline_cli.py` is a standalone CLI for fetching `patch_metadata` and bulk-downloading game assets from the server

### 🟣 KALPA

| Public API | Description |
|-----------|-------------|
| `get_api_processor(user_profile, *, client_version)` | Create a `MobileProcessor`. Requires `client_version` (e.g. `30209`) |
| `get_user_info(user_profile, *, client_version)` | Fetch player info |

**Usage:**
```python
from kalpa.processor import get_user_info

info = get_user_info(
    user_profile={"userid": "...", "password": "..."},
    client_version=30209
)
```

**Implementation details:**
- **Authentication** — Username/password login (`userid` + `password`)
- **Custom headers** — Uses `Custom-UserToken` and `Custom-ClientVersion` in request headers
- **Response decoding** — Some endpoints return gzip + base64 encoded data requiring decompression
- **Server types** — Supports `MOBILE` and `PC` server types (currently only Mobile interface is implemented; PC is a placeholder)
- **Endpoint** — Shares the same LeanCloud host as Rotaeno (`rotaeno.leancloud.indie.xd.com`)

---

## 🖼️ Scorecard Image Rendering

HTML templates are rendered to JPEG/PNG images using Playwright headless Chromium:

```python
from common.utils import render_html_to_jpg

# Render a Best30/Best40 HTML template to an image
image_path = render_html_to_jpg((1920, 1080), html_content, "output.html")
# Returns: "temp/output.jpg"
```

**Templates:**
- **Phigros:** `phigros/assets/html/best30.html` — Tailwind CSS + Orbitron/Exo 2 fonts
- **Rotaeno:** `rotaeno/assets/html/b40.html`, `song.html`, `song_rtr.html`, `song_status.html`
- **Rizline:** `rizline/assets/html/b40.html`

Image output is automatically compressed (WebP → JPEG fallback) to stay under 9.5 MB.

---

## 🧪 Testing

```bash
pytest
```

Tests are integration-level and require real session credentials to pass — they are structured as validation placeholders. See `tests/` for:
- `test_phigros.py` — Phigros data processing tests
- `test_rizline.py` — Rizline login data test
- `test_rotaeno.py` — Rotaeno cloud save and rating tests (some marked `@skip("COMPLEX")`)

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `RHYTHMLIBRARY_DEBUG_CURL` | Set to print HTTP request curl commands for debugging |

### Game Regions

Each game module supports region-specific server endpoints:

| Game | Regions |
|------|---------|
| Phigros | `"cn"`, `"global"` |
| Rotaeno | `"cn"`, `"global"`, `"friend_cn"`, `"friend_global"` |
| Rizline | `"cn"`, `"global"` |
| KALPA | N/A — uses `client_version` instead |

---

## 📁 Data Storage

| Path | Purpose |
|------|---------|
| `data/` | Raw save data dumps (`.msgpack`, `.bin`) |
| `temp/` | Temporary rendered images |
| `{module}/saves/` | Per-module save data cache |
| `{module}/database/*.db` | SQLite databases for song metadata and player history |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit Issues and Pull Requests.

### Development Setup

```bash
pip install -r requirements-dev.txt
pre-commit install  # Enforces black, isort, flake8
```

### Code Style

- **Black** with line length 100
- **isort** with black profile
- **Flake8** (E203, W503 ignored)

---

## ⚠️ Disclaimer

This project is for **learning and research purposes only**. Please comply with the service terms of each game and do not abuse the API. Users need to obtain legitimate authentication information on their own.

- This tool does not modify game data or manipulate game clients
- All data is fetched through official game APIs with user-provided authentication
- No warranty is provided — use at your own risk

---

## 📄 License

[GNU General Public License v3.0](LICENSE)

---

*Made with ❤️ for the rhythm game community.*
