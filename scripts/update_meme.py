import os
import re
import sys
import json
from pathlib import Path
from urllib.request import urlopen

README_PATH = Path(__file__).resolve().parents[1] / "README.md"

FALLBACK_MEME = "https://api.memegen.link/images/buzz/it_works/now_fixed.png"

SECTION_TAGS = (
    ("<!-- MEME_SECTION_START -->", "<!-- MEME_SECTION_END -->", 700),
    ("<!-- FOOTER_MEME_START -->", "<!-- FOOTER_MEME_END -->", 300),
)


def fetch_random_meme_url() -> str:
    """Fetch a random meme image URL from meme-api.com with a simple fallback."""
    try:
        with urlopen("https://meme-api.com/gimme") as resp:
            data = json.load(resp)
            url = data.get("url")
            if isinstance(url, str) and url.startswith("http"):
                return url
    except Exception:
        pass
    return FALLBACK_MEME


def replace_between_tags(content: str, start_tag: str, end_tag: str, new_img_url: str, width: int) -> str:
    pattern = re.compile(
        re.escape(start_tag) + r".*?" + re.escape(end_tag),
        flags=re.DOTALL,
    )
    replacement = (
        f"{start_tag}\n"
        f"  <img src=\"{new_img_url}\" width=\"{width}\" alt=\"Random meme\"/>\n"
        f"{end_tag}"
    )
    return pattern.sub(replacement, content)


def main() -> int:
    if not README_PATH.exists():
        print("README.md not found", file=sys.stderr)
        return 1

    new_meme = fetch_random_meme_url()

    original = README_PATH.read_text(encoding="utf-8")
    updated = original
    for start, end, width in SECTION_TAGS:
        updated = replace_between_tags(updated, start, end, new_meme, width)

    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
        print(f"Updated README with meme: {new_meme}")
    else:
        print("No changes applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
