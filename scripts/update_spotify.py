import os
import re
import sys
import json
import base64
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

README_PATH = Path(__file__).resolve().parents[1] / "README.md"

SPOTIFY_START = "<!-- SPOTIFY_START -->"
SPOTIFY_END = "<!-- SPOTIFY_END -->"

SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")


def refresh_access_token() -> str | None:
    body = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }).encode()
    b64 = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    req = Request(
        "https://accounts.spotify.com/api/token",
        data=body,
        headers={
            "Authorization": f"Basic {b64}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    try:
        with urlopen(req) as resp:
            data = json.load(resp)
            return data.get("access_token")
    except Exception:
        return None


def fetch_current_track(access_token: str) -> dict | None:
    req = Request(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    try:
        with urlopen(req) as resp:
            if resp.status == 204:
                return None
            return json.load(resp)
    except Exception:
        return None


def format_track_output(data: dict | None) -> str:
    if data is None:
        return (
            f'{SPOTIFY_START}\n'
            f'<div align="center">\n'
            f'  <sub><i>Nothing playing right now</i></sub>\n'
            f'</div>\n'
            f'{SPOTIFY_END}'
        )

    item = data.get("item", {})
    name = item.get("name", "Unknown")
    artists = ", ".join(a.get("name", "") for a in item.get("artists", []))
    album = item.get("album", {})
    album_name = album.get("name", "")
    album_art = (album.get("images") or [{}])[0].get("url", "")
    url = item.get("external_urls", {}).get("spotify", "https://open.spotify.com")
    progress_ms = data.get("progress_ms", 0)
    duration_ms = item.get("duration_ms", 0)
    progress_pct = (progress_ms / duration_ms * 100) if duration_ms else 0

    return (
        f'{SPOTIFY_START}\n'
        f'<div align="center">\n'
        f'  <a href="{url}">\n'
        f'    <img src="{album_art}" width="100" height="100" style="border-radius:12px" alt="Album art"/>\n'
        f'  </a>\n'
        f'  <br>\n'
        f'  <b>{name}</b> — <i>{artists}</i>\n'
        f'  <br>\n'
        f'  <sub>{album_name}</sub>\n'
        f'  <br>\n'
        f'  <img src="https://progress-bar.dev/{int(progress_pct)}/?title=&width=300&color=1db954"/>\n'
        f'</div>\n'
        f'{SPOTIFY_END}'
    )


def main() -> int:
    if not README_PATH.exists():
        print("README.md not found", file=sys.stderr)
        return 1

    missing = [k for k, v in [
        ("SPOTIFY_CLIENT_ID", SPOTIFY_CLIENT_ID),
        ("SPOTIFY_CLIENT_SECRET", SPOTIFY_CLIENT_SECRET),
        ("SPOTIFY_REFRESH_TOKEN", SPOTIFY_REFRESH_TOKEN),
    ] if not v]
    if missing:
        print(f"Missing env vars: {', '.join(missing)}", file=sys.stderr)
        return 1

    access_token = refresh_access_token()
    if not access_token:
        print("Failed to refresh access token", file=sys.stderr)
        return 1

    track_data = fetch_current_track(access_token)
    new_content = format_track_output(track_data)

    original = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(SPOTIFY_START) + r".*?" + re.escape(SPOTIFY_END),
        flags=re.DOTALL,
    )
    updated = pattern.sub(new_content, original)

    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        print("Updated README with current Spotify track")
    else:
        print("No changes applied.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
