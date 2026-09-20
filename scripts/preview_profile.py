"""Local preview only. Requires the optional Python 'markdown' package."""
import argparse
from pathlib import Path
import markdown

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("output", type=Path)
parser.add_argument("--light", action="store_true")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
source = (root / "README.md").read_text().replace("<details>", '<details markdown="1">')
body = markdown.markdown(source, extensions=["extra", "toc"])
bg, fg, border, link = ("#ffffff", "#1f2328", "#d1d9e0", "#0969da") if args.light else ("#0d1117", "#d1d9e0", "#3d444d", "#c4f569")
args.output.write_text(f'''<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<base href="{root.as_uri()}/"><title>Mevin Benty — profile preview</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:{bg};color:{fg};font:16px/1.65 system-ui,sans-serif}}
main{{max-width:940px;margin:24px auto;padding:32px;border:1px solid {border};border-radius:6px}}
img{{max-width:100%;height:auto;vertical-align:middle}}a{{color:{link};text-decoration:none}}a:hover{{text-decoration:underline}}
h2{{font-size:24px;border-bottom:1px solid {border};padding-bottom:8px}}summary{{cursor:pointer}}
table{{border-collapse:collapse;display:block;overflow:auto}}td,th{{border:1px solid {border};padding:8px 14px;text-align:left}}
@media(max-width:600px){{main{{padding:16px;margin:0;border:0}}body{{font-size:14px}}}}
</style></head><body><main>{body}</main></body></html>''', encoding="utf-8")
print(args.output)
