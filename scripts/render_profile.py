"""Generate original profile vector artwork using only Python's standard library."""
from pathlib import Path
from math import sin, cos
from html import escape

OUT = Path(__file__).resolve().parents[1] / "assets" / "profile"
INK, PAPER, SILVER, MUTED = "#0B0D10", "#F5F7FA", "#DCE3EC", "#B8C0CC"
LINE, GRID = "#687382", "#343B46"


def text(x, y, value, size=16, color=PAPER, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def line(x1, y1, x2, y2, color=GRID, extra=""):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" {extra}/>'


def svg(name, height, title, content, bg=INK):
    OUT.mkdir(parents=True, exist_ok=True)
    data = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Original schematic artwork for Mevin Benty's profile. Decorative motion, not live measurements.</desc>
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-opacity=".10"/></pattern>
<clipPath id="bounds"><rect width="1000" height="{height}"/></clipPath>
</defs>
<style>
text{{font-family:Arial,Helvetica,sans-serif}}
.mono{{font-family:'Courier New',monospace;letter-spacing:2px}}
.orbit{{transform-origin:750px 300px;animation:orbit 36s linear infinite}}
.reverse{{animation-direction:reverse;animation-duration:48s}}
.flow{{stroke-dasharray:5 14;animation:flow 12s linear infinite}}
.breathe{{animation:breathe 6s ease-in-out infinite}}
@keyframes orbit{{to{{transform:rotate(360deg)}}}}
@keyframes flow{{to{{stroke-dashoffset:-190}}}}
@keyframes breathe{{50%{{opacity:.35}}}}
@media(prefers-reduced-motion:reduce){{.orbit,.flow,.breathe{{animation:none!important}}}}
</style>
<g clip-path="url(#bounds)"><rect width="1000" height="{height}" fill="{bg}"/>{content}</g></svg>
'''
    (OUT / f"{name}.svg").write_text(data, encoding="utf-8")


def hero():
    p = ['<rect width="1000" height="650" fill="url(#grid)"/>']
    p += [text(40, 47, "MB / INDEPENDENT BUILDER", 14, SILVER, extra='class="mono"'), text(960, 47, "SOURCE OPEN ↗", 14, MUTED, extra='text-anchor="end" class="mono"'), line(40, 68, 960, 68)]
    p.append(f'<g fill="none" stroke="{LINE}" stroke-width="1">')
    for r in (100, 150, 200, 245):
        p.append(f'<circle cx="750" cy="300" r="{r}" opacity=".35"/>')
    for angle in range(0, 180, 20):
        p.append(f'<ellipse cx="750" cy="300" rx="240" ry="85" transform="rotate({angle} 750 300)" opacity=".45"/>')
    p.append(f'</g><g class="orbit" fill="none" stroke="{SILVER}"><ellipse cx="750" cy="300" rx="245" ry="91" transform="rotate(-30 750 300)"/><circle cx="995" cy="300" r="5" fill="{SILVER}"/></g>')
    p.append(f'<g class="orbit reverse" fill="none" stroke="{SILVER}" stroke-opacity=".5"><ellipse cx="750" cy="300" rx="182" ry="240"/><circle cx="750" cy="60" r="4" fill="{SILVER}"/></g>')
    p += [text(34, 233, "MEVIN", 164, PAPER, 900, 'letter-spacing="-11"'), text(40, 370, "BENTY", 164, PAPER, 900, 'letter-spacing="-11"')]
    p += [f'<rect x="43" y="404" width="62" height="5" fill="{SILVER}"/>', text(42, 463, "Software, from", 35), text(42, 506, "interface to engine.", 35)]
    p += [text(750, 308, "m/b", 38, SILVER, 700, 'text-anchor="middle"'), line(650, 542, 929, 542), text(650, 569, "AI × DESKTOP × WEB", 15, MUTED, extra='class="mono"')]
    p += [line(40, 604, 960, 604), text(40, 633, "EXPLORE THE SYSTEMS BELOW", 13, MUTED, extra='class="mono"'), text(960, 633, "↓", 22, SILVER, extra='text-anchor="end"')]
    svg("hero", 650, "Mevin Benty — software, from interface to engine", "".join(p))


def panel(name, number, title, subtitle, stack, art):
    bg, fg, secondary = INK, PAPER, MUTED
    accent = SILVER
    body = '<rect x="610" width="390" height="300" fill="url(#grid)"/>'
    body += line(610, 0, 610, 300, GRID)
    body += text(34, 43, f"{number} / SELECTED WORK", 13, secondary, extra='class="mono"')
    body += text(32, 122, title, 65, fg, 700, 'letter-spacing="-3"')
    body += text(35, 165, subtitle, 21, secondary)
    body += text(35, 252, stack, 13, secondary, extra='class="mono"')
    body += text(564, 254, "↗", 32, accent)
    svg(name, 300, f"{title} — {subtitle}", body + art, bg)


def projects():
    art = f'<g fill="none" stroke="{LINE}" stroke-width="1">'
    for i in range(12):
        x = 674 + i * 16
        art += f'<path d="M{x} 55Q{790-i*5} 150 {x} 247" opacity=".65"/>'
    for i in range(9):
        y = 63 + i * 22
        art += f'<path d="M674 {y}Q790 {150+(y-150)*.25} 850 {y}"/>'
    art += f'</g><path class="flow" d="M645 151H953" fill="none" stroke="{SILVER}" stroke-width="2"/>'
    for x, y in [(703, 103), (821, 103), (762, 151), (727, 207), (798, 207)]:
        art += f'<circle cx="{x}" cy="{y}" r="4" fill="{SILVER}"/>'
    art += text(645, 278, "DETECT → ALIGN → BLEND", 12, MUTED, extra='class="mono"')
    panel("reactor", "01", "ReactorX", "Local image processing.", "PYTHON / ONNX / GRADIO", art)

    art = f'<g fill="none" stroke="{LINE}">'
    for i in range(4):
        art += f'<rect x="{679+i*18}" y="{53+i*13}" width="205" height="150" rx="3"/>'
    art += f'</g><circle cx="817" cy="150" r="45" fill="{INK}"/><path d="M807 129L835 150L807 171Z" fill="{SILVER}"/>'
    for i in range(35):
        h = 5 + 20 * abs(sin(i * .47)) * abs(cos(i * .19))
        art += line(667+i*8, 253-h, 667+i*8, 253+h, SILVER, 'stroke-width="2"')
    panel("mediahub", "02", "MediaHub", "Your library. Your machine.", "PYQT6 / LIBVLC / SQLITE", art)

    art = f'<g fill="none" stroke="{LINE}">'
    for x, y in [(680, 64), (925, 65), (938, 231), (674, 235)]:
        art += f'<path d="M807 150Q{x} 150 {x} {y}"/><path class="flow" d="M807 150Q{x} 150 {x} {y}" stroke="{SILVER}"/>'
        art += f'<rect x="{x-17}" y="{y-17}" width="34" height="34" fill="{INK}"/>'
    art += f'<circle cx="807" cy="150" r="67"/><circle cx="807" cy="150" r="52" stroke="{SILVER}"/><circle class="breathe" cx="807" cy="150" r="34" fill="{SILVER}" stroke="none"/></g>'
    for x, y, label in [(680, 34, "MODEL"), (915, 34, "TOOLS"), (680, 279, "MEMORY"), (922, 279, "ACTION")]:
        art += text(x, y, label, 11, MUTED, extra='text-anchor="middle" class="mono"')
    panel("arc", "03", "ARC", "Models connected to tools.", "PYTHON / ROUTING / AUTOMATION", art)

    # Manuscript sheets connected by a writing / revision flow.
    art = ""
    for i, (x, y) in enumerate([(650, 62), (756, 90), (862, 118)]):
        art += f'<rect x="{x}" y="{y}" width="78" height="120" rx="2" fill="{INK}" stroke="{LINE}"/>'
        art += text(x + 12, y + 25, f"0{i+1}", 14, SILVER, extra='class="mono"')
        for row, width in enumerate([48, 42, 48, 32]):
            art += line(x + 12, y + 45 + row * 14, x + 12 + width, y + 45 + row * 14, LINE)
    art += f'<path class="flow" d="M728 120H746V148H756M834 148H851V176H862" fill="none" stroke="{SILVER}" stroke-width="2"/>'
    art += text(645, 278, "PLAN → WRITE → REFINE", 12, MUTED, extra='class="mono"')
    panel("story-teller", "04", "Story Teller", "Long-form fiction, chapter by chapter.", "PYTHON / FLASK / FAISS", art)


def contact():
    body = text(40, 45, "THE NEXT INTERESTING THING", 14, INK, extra='class="mono"')
    body += text(36, 124, "Let's build it.", 76, INK, 700, 'letter-spacing="-4"')
    body += text(42, 175, "mevinbenty507@gmail.com", 20, GRID)
    body += f'<path d="M830 143L931 42M835 42H931V138" fill="none" stroke="{INK}" stroke-width="8"/>'
    svg("contact", 210, "Let's build it — contact Mevin Benty", body, SILVER)


if __name__ == "__main__":
    hero()
    projects()
    contact()
    print("Generated six profile SVGs.")
