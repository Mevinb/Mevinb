# Profile artwork

An engineering folio: oversized type, an orbital masthead, four project
schematics, and a lime contact plate. Illustrations represent concepts, not
screenshots, performance measurements, or live status.

Edit copy and links in `README.md`. Edit artwork in `scripts/render_profile.py`,
then run `python3 scripts/render_profile.py`. Commit both the generator and
`assets/profile/*.svg`. Python's standard library is the only build dependency.

The SVGs use local font fallbacks and decorative CSS animations with a
reduced-motion query. Every diagram has a complete static state. GitHub or a
browser may suppress animation. There are no remote fonts, scripts, or embedded
HTML in the images. Native links wrap the project panels; native details elements
contain readable project descriptions and additional source links.

The previous README is preserved in `docs/previous-profile.md`, including the
local Spotify addition. The Spotify script is unchanged and its markers remain
in the new README. No credentials or new Spotify automation were added. The
displayed listening status is the existing placeholder, not verified live data.

The meme updater remains available through manual workflow dispatch. Its daily
and README-push triggers were retired to avoid automatic random changes. The
meme is inside the collapsed off-duty section.

Review images at full and narrow widths, light and dark surrounds, links,
expandable sections, and reduced motion. Inspect the final GitHub rendering
after publication: local previews cannot reproduce its caching and sanitization
exactly. No claim is made that nobody has ever used these techniques; the
composition and illustrations were created specifically for this profile.
