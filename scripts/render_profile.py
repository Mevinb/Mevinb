"""Generate original profile vector artwork using only Python's standard library."""
from pathlib import Path
from math import sin, cos
from html import escape

OUT = Path(__file__).resolve().parents[1] / "assets" / "profile"
INK, PAPER, LIME, MUTED = "#101310", "#eef0e7", "#c4f569", "#a4aca0"


def text(x, y, value, size=16, color=PAPER, weight=400, extra=""):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def line(x1, y1, x2, y2, color="#343c31", extra=""):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" {extra}/>'


def svg(name, height, title, content, bg=INK):
    OUT.mkdir(parents=True, exist_ok=True)
    data = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">Original schematic artwork for Mevin Benty's profile. Decorative motion, not live measurements.</desc>
<defs>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#89927f" stroke-opacity=".10"/></pattern>
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
    p += [text(40, 47, "MB / INDEPENDENT BUILDER", 14, LIME, extra='class="mono"'), text(960, 47, "SOURCE OPEN ↗", 14, MUTED, extra='text-anchor="end" class="mono"'), line(40, 68, 960, 68)]
    p.append('<g fill="none" stroke="#728064" stroke-width="1">')
    for r in (100, 150, 200, 245):
        p.append(f'<circle cx="750" cy="300" r="{r}" opacity=".35"/>')
    for angle in range(0, 180, 20):
        p.append(f'<ellipse cx="750" cy="300" rx="240" ry="85" transform="rotate({angle} 750 300)" opacity=".45"/>')
    p.append('</g><g class="orbit" fill="none" stroke="#c4f569"><ellipse cx="750" cy="300" rx="245" ry="91" transform="rotate(-30 750 300)"/><circle cx="995" cy="300" r="5" fill="#c4f569"/></g>')
    p.append('<g class="orbit reverse" fill="none" stroke="#c4f569" stroke-opacity=".5"><ellipse cx="750" cy="300" rx="182" ry="240"/><circle cx="750" cy="60" r="4" fill="#c4f569"/></g>')
    p += [text(34, 233, "MEVIN", 164, PAPER, 900, 'letter-spacing="-11"'), text(40, 370, "BENTY", 164, PAPER, 900, 'letter-spacing="-11"')]
    p += [f'<rect x="43" y="404" width="62" height="5" fill="{LIME}"/>', text(42, 463, "Software, from", 35), text(42, 506, "interface to engine.", 35)]
    p += [text(750, 308, "m/b", 38, LIME, 700, 'text-anchor="middle"'), line(650, 542, 929, 542), text(650, 569, "AI × DESKTOP × WEB", 15, MUTED, extra='class="mono"')]
    p += [line(40, 604, 960, 604), text(40, 633, "EXPLORE THE SYSTEMS BELOW", 13, MUTED, extra='class="mono"'), text(960, 633, "↓", 22, LIME, extra='text-anchor="end"')]
    svg("hero", 650, "Mevin Benty — software, from interface to engine", "".join(p))


def panel(name, number, title, subtitle, stack, art, light=False):
    bg, fg, secondary = (PAPER, INK, "#4c5844") if light else (INK, PAPER, MUTED)
    accent = "#465e28" if light else LIME
    body = '<rect x="610" width="390" height="300" fill="url(#grid)"/>'
    body += line(610, 0, 610, 300, "#bac3ae" if light else "#343c31")
    body += text(34, 43, f"{number} / SELECTED WORK", 13, secondary, extra='class="mono"')
    body += text(32, 122, title, 65, fg, 700, 'letter-spacing="-3"')
    body += text(35, 165, subtitle, 21, secondary)
    body += text(35, 252, stack, 13, secondary, extra='class="mono"')
    body += text(564, 254, "↗", 32, accent)
    svg(name, 300, f"{title} — {subtitle}", body + art, bg)


def projects():
    art = '<g fill="none" stroke="#637653" stroke-width="1">'
    for i in range(12):
        x = 674 + i * 16
        art += f'<path d="M{x} 55Q{790-i*5} 150 {x} 247" opacity=".65"/>'
    for i in range(9):
        y = 63 + i * 22
        art += f'<path d="M674 {y}Q790 {150+(y-150)*.25} 850 {y}"/>'
    art += '</g><path class="flow" d="M645 151H953" fill="none" stroke="#c4f569" stroke-width="2"/>'
    for x, y in [(703, 103), (821, 103), (762, 151), (727, 207), (798, 207)]:
        art += f'<circle cx="{x}" cy="{y}" r="4" fill="#c4f569"/>'
    art += text(645, 278, "DETECT → ALIGN → BLEND", 12, MUTED, extra='class="mono"')
    panel("reactor", "01", "ReactorX", "Local image processing.", "PYTHON / ONNX / GRADIO", art)

    art = '<g fill="none" stroke="#89967c">'
    for i in range(4):
        art += f'<rect x="{679+i*18}" y="{53+i*13}" width="205" height="150" rx="3"/>'
    art += '</g><circle cx="817" cy="150" r="45" fill="#101310"/><path d="M807 129L835 150L807 171Z" fill="#c4f569"/>'
    for i in range(35):
        h = 5 + 20 * abs(sin(i * .47)) * abs(cos(i * .19))
        art += line(667+i*8, 253-h, 667+i*8, 253+h, "#465e28", 'stroke-width="2"')
    panel("mediahub", "02", "MediaHub", "Your library. Your machine.", "PYQT6 / LIBVLC / SQLITE", art, True)

    art = '<g fill="none" stroke="#637653">'
    for x, y in [(680, 64), (925, 65), (938, 231), (674, 235)]:
        art += f'<path d="M807 150Q{x} 150 {x} {y}"/><path class="flow" d="M807 150Q{x} 150 {x} {y}" stroke="#c4f569"/>'
        art += f'<rect x="{x-17}" y="{y-17}" width="34" height="34" fill="#101310"/>'
    art += '<circle cx="807" cy="150" r="67"/><circle cx="807" cy="150" r="52" stroke="#c4f569"/><circle class="breathe" cx="807" cy="150" r="34" fill="#c4f569" stroke="none"/></g>'
    for x, y, label in [(680, 34, "MODEL"), (915, 34, "TOOLS"), (680, 279, "MEMORY"), (922, 279, "ACTION")]:
        art += text(x, y, label, 11, MUTED, extra='text-anchor="middle" class="mono"')
    panel("arc", "03", "ARC", "Models connected to tools.", "PYTHON / ROUTING / AUTOMATION", art)

    art = '<g fill="none" stroke="#8c9c7d" stroke-width="2"><path d="M660 244C765 244 705 56 927 56"/><path d="M660 244C784 244 758 151 927 151"/><path d="M660 244H927"/></g>'
    art += '<path class="flow" d="M660 244C765 244 705 56 927 56" fill="none" stroke="#465e28" stroke-width="3"/>'
    for y, label in [(56, "A"), (151, "B"), (244, "C")]:
        art += f'<circle cx="927" cy="{y}" r="20" fill="#101310"/>' + text(927, y+6, label, 17, LIME, 700, 'text-anchor="middle"')
    art += '<circle cx="660" cy="244" r="7" fill="#465e28"/>'
    panel("pathwise", "04", "PATHWISE", "Different futures, made tangible.", "EXPO / REACT NATIVE / UI PROTOTYPE", art, True)


def contact():
    body = text(40, 45, "THE NEXT INTERESTING THING", 14, INK, extra='class="mono"')
    body += text(36, 124, "Let's build it.", 76, INK, 700, 'letter-spacing="-4"')
    body += text(42, 175, "mevinbenty507@gmail.com", 20, "#354427")
    body += '<path d="M830 143L931 42M835 42H931V138" fill="none" stroke="#101310" stroke-width="8"/>'
    svg("contact", 210, "Let's build it — contact Mevin Benty", body, LIME)


if __name__ == "__main__":
    hero()
    projects()
    contact()
    print("Generated six profile SVGs.")
