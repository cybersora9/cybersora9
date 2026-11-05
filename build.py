"""Builds the profile README graphics (assets/*.svg). Text is drawn as paths, so GitHub needs no fonts.

v5 (05.11.2026): personal profile ("I", not "we"), black cat brand, Start-style panels
(#17171d, 20 px radius, no side bars), falling-code strips instead of pixels.
"""
import random, io, zlib, re, base64
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

F = 'C:/Users/maisa/Documents/SoraWebsite/fonts/'
DOC = 'C:/Users/maisa/Documents/'
V = '5'  # bump to bust GitHub's image cache


def load(n, w):
    return instantiateVariableFont(TTFont(F + n), {'wght': w})


SORA = load('sora-latin-wght-normal.woff2', 700)
MONO = load('geist-mono-latin-wght-normal.woff2', 500)
MONOB = load('geist-mono-latin-wght-normal.woff2', 700)
INK = '#0e0e12'; RED = '#e11d33'; HOT = '#ff3a52'; DARK = '#8f1726'; BONE = '#f6f2f3'
MUTED = '#9a9098'; PANEL = '#17171d'; LINE = '#2c2c36'; BOX = '#1e1e26'


def text(font, s, x, y, size, fill, track=0, anchor='start'):
    gs = font.getGlyphSet(); cmap = font.getBestCmap(); upm = font['head'].unitsPerEm; sc = size / upm
    adv = []; names = []
    for ch in s:
        g = cmap.get(ord(ch)) or cmap.get(32)
        names.append(g); adv.append(font['hmtx'][g][0] * sc + track)
    total = sum(adv) - track
    cx = x - (total if anchor == 'end' else total / 2 if anchor == 'middle' else 0)
    d = []
    for g, a in zip(names, adv):
        pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        d.append(pen.getCommands()); cx += a
    return f'<path fill="{fill}" d="{" ".join(d)}"/>', total


def svg(w, h, body, css=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<style>{css}</style>{body}</svg>')


def save(n, s):
    io.open('assets/' + n, 'w', encoding='utf-8', newline='\n').write(s)


FL = '@keyframes a{0%,100%{opacity:.25}50%{opacity:1}}.f1{animation:a 3s infinite}.f2{animation:a 4.3s .7s infinite}.f3{animation:a 5.1s 1.9s infinite}'
CODE = '0123456789ABCDEF{}[]<>/$#%;:*+='


def codestrip(x0, y, w, seed, size=14, step=17):
    """A row of code glyphs that gets denser and redder to the right (falling-code motif, no pixels)."""
    random.seed(seed); o = []; n = int(w // step)
    for i in range(n):
        p = i / max(n - 1, 1)
        if random.random() > 0.15 + 0.7 * p ** 1.4:
            continue
        col = random.choices([DARK, RED, HOT, BONE], [6, 3, 1, .4])[0]
        yy = y + random.choice([-9, 0, 0, 9])
        t, _ = text(MONO, random.choice(CODE), x0 + i * step, yy, size, col)
        op = round(.25 + .75 * p * random.uniform(.6, 1), 2)
        cls = ' class="f%d"' % random.randint(1, 3) if random.random() < .18 else ''
        o.append(f'<g{cls} opacity="{op}">{t}</g>')
    return ''.join(o)


def rpanel(w, h, fill=PANEL):
    return f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="{fill}" stroke="{LINE}"/>'


# SECTION HEADERS: number + title, then a code strip. No side bar.
for n, (num, lab) in {'who': ('01', 'WHO I AM'), 'what': ('02', 'WHAT I BUILD'), 'how': ('03', 'HOW I WORK'),
                      'stack': ('04', 'STACK'), 'art': ('05', 'BEYOND CODE')}.items():
    W2 = 1200; H2 = 64
    s = ''
    t, w1 = text(MONOB, num, 4, 42, 18, RED, 2); s += t
    t, w2 = text(SORA, lab, 4 + w1 + 18, 44, 32, BONE, 1); s += t
    xs = int(4 + w1 + 18 + w2 + 36)
    s += codestrip(xs, 40, W2 - xs, zlib.crc32(n.encode()) % 99)
    save(f'h-{n}-{V}.svg', svg(W2, H2, s, FL))


def panel(name, lines, size=24):
    W2 = 1200; gap = 16; H2 = 52 + len(lines) * (size + gap)
    s = rpanel(W2, H2)
    y = 40 + size
    for ln, col in lines:
        if ln.startswith('>'):
            t, _ = text(MONOB, '>', 36, y, size, RED); s += t
            ln = ln[1:]
        t, _ = text(MONO, ln, 36 + size * .6, y, size, col); s += t; y += size + gap
    save(name, svg(W2, H2, s))


panel(f'p-who-{V}.svg', [
    ("> hi, I'm blackcat. my artist name: deadsora.", BONE),
    ('> artist first. art is where it all started,', BONE),
    ('  then code came along and stuck.', BONE),
    ('> I think it up, design it and code it myself:', BONE),
    ('  desktop apps, websites, AI tools.', BONE),
    ('> cybersora is the brand I build under.', MUTED)])
panel(f'p-how-{V}.svg', [
    ('> AI is my team: code, tests, graphics, research,', BONE),
    ('  automations, even my own agents.', BONE),
    ('> I check its work: pytest, Playwright, and', BONE),
    ('  screenshots I actually look at.', BONE),
    ('> local-first. your data stays on your machine.', MUTED)])
panel(f'p-art-{V}.svg', [
    ('> deadsora is my other face, my artist name.', BONE),
    ('> logos, banners, post templates, graphics.', BONE),
    ('> emotions, cats and art. code is art too.', BONE),
    ('> my art on Instagram: @deadsora', MUTED)])


def mark(path, x, y, size, uid):
    """Official product mark (own SVG file) nested as <svg>; ids prefixed to avoid clashes."""
    raw = io.open(DOC + path, encoding='utf-8').read()
    vb = re.search(r'viewBox="([^"]+)"', raw).group(1)
    inner = re.sub(r'^.*?<svg[^>]*>|</svg>\s*$', '', raw, flags=re.S)
    inner = re.sub(r'<!--.*?-->|<title>.*?</title>', '', inner, flags=re.S)
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{uid}{m.group(1)}"', inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{uid}{m.group(1)})', inner)
    inner = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{uid}{m.group(1)}"', inner)
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="{vb}">{inner}</svg>'


def card(name, title, desc, tag, pub=True, ver=None, logo=None, logo_bg=None):
    W2, H2 = 588, 210
    s = rpanel(W2, H2)
    uid = name.split('.')[0].replace('-', '') + '_'
    if logo_bg:  # marks that are not tiles get a round krew plate (Meshuga)
        s += f'<circle cx="62" cy="62" r="34" fill="{logo_bg}"/>' + mark(logo, 34, 34, 56, uid)
    else:
        s += f'<g><clipPath id="{uid}c"><rect x="28" y="28" width="68" height="68" rx="16"/></clipPath>' \
             f'<g clip-path="url(#{uid}c)">{mark(logo, 28, 28, 68, uid)}</g></g>'
    t, _ = text(SORA, title, 116, 74, 32, BONE, 0); s += t
    for i, ln in enumerate(desc):
        t, _ = text(MONO, ln, 28, 138 + i * 28, 19, MUTED, 0); s += t
    label = 'PUBLIC' if pub else 'PRIVATE'
    _, tw = text(MONOB, label, 0, 0, 13, '#fff', 2)
    px = W2 - 28 - tw - 24
    s += f'<rect x="{px}" y="30" width="{tw + 24}" height="28" rx="14" fill="{RED if pub else BOX}" stroke="{RED if pub else LINE}"/>'
    t, _ = text(MONOB, label, px + 12, 49, 13, '#fff' if pub else MUTED, 2); s += t
    t, _ = text(MONO, tag, W2 - 28, 88, 14, HOT if pub else MUTED, 1, 'end'); s += t
    if ver:
        t, _ = text(MONOB, ver, W2 - 28, H2 - 22, 16, BONE, 1, 'end'); s += t
    save(name, svg(W2, H2, s))


P = 'cybersora-assets/logo/produkty/'
card(f'c-pycodemath-{V}.svg', 'Pycodemath', ['Checks the math in your code.', 'On PyPI. MCP server for AI.'], 'PYTHON · SYMPY', ver='v0.5.1', logo=P + 'pycodemath/pycodemath-kafelek-krew.svg')
card(f'c-salondesk-{V}.svg', 'SalonDesk', ['Desktop app for a beauty salon,', 'used in a real salon.'], 'PYTHON · SQLITE', pub=False, logo='SalonDesk/assets/znak/salondesk-kafelek-krew.svg')
card(f'c-site-{V}.svg', 'cybersora.pl', ['My site: a desktop OS in the', 'browser, with an AI chatbot.'], 'HTML · JAVASCRIPT', ver='LIVE', logo='cybersora-assets/ikony/ikona-krew.svg')
card(f'c-meshuga-{V}.svg', 'Meshuga', ['The AI chatbot of cybersora,', 'on the site and on Discord.'], 'PYTHON · AI', pub=False, logo='cybersora-assets/logo/kot-awatar/meshuga.svg', logo_bg=RED)
card(f'c-reader-{V}.svg', 'SoraEbookReader', ['E-book reader for Windows.', 'Coming soon.'], 'TAURI · JS', pub=False, ver='SOON', logo=P + 'soraczytnik/soraczytnik-kafelek-krew.svg')
card(f'c-soraflux-{V}.svg', 'SoraFlux', ['Local video, audio, image and', 'GIF converter.'], 'TAURI 2 · RUST', pub=False, ver='v1.4.1', logo=P + 'soraflux/soraflux-kafelek-krew.svg')

# STACK chips (rounded, no side bar)
items = ['PYTHON', 'RUST', 'JAVASCRIPT', 'HTML/CSS', 'TAURI', 'SQLITE', 'SYMPY', 'NUMPY', 'PYTEST', 'PLAYWRIGHT',
         'MCP', 'AI AGENTS', 'GIT', 'LINUX', 'ADOBE']
W2 = 1200; x = 0; y = 0; pos = []
for it in items:
    _, tw = text(MONOB, it, 0, 0, 18, RED, 1); w = tw + 44
    if x + w > W2:
        x = 0; y += 60
    pos.append((x, y, w, it)); x += w + 12
H2 = y + 48
s = ''
for x, y, w, it in pos:
    s += f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="47" rx="23.5" fill="{PANEL}" stroke="{LINE}"/>'
    t, _ = text(MONOB, it, x + 22, y + 31, 18, BONE, 1); s += t
save(f'stack-{V}.svg', svg(W2, H2, s))

# STATS: numbers measured 05.11.2026 (PyPI, pytest --collect-only, GitHub contributions)
W2, H2 = 1200, 128
items = [('3082', 'PYCODEMATH TESTS'), ('88', 'PYCODEMATH COMMANDS'), ('568', 'CONTRIBUTIONS, LAST YEAR'), ('1', 'REAL SALON ON SALONDESK')]
s = ''
cw = 288; gap = 16
for i, (n, lab) in enumerate(items):
    x = i * (cw + gap)
    s += f'<rect x="{x + .5}" y=".5" width="{cw - 1}" height="{H2 - 1}" rx="20" fill="{PANEL}" stroke="{LINE}"/>'
    t, _ = text(SORA, n, x + 28, 70, 48, BONE, 0); s += t
    t, _ = text(MONOB, lab, x + 28, 102, 13, HOT, 1.5); s += t
save(f'stats-{V}.svg', svg(W2, H2, s))


def button(name, label, sub, primary):
    W2, H2 = 588, 96
    s = (f'<rect width="{W2}" height="{H2}" rx="20" fill="{RED}"/>' if primary else
         f'<rect x="1" y="1" width="{W2 - 2}" height="{H2 - 2}" rx="19" fill="{PANEL}" stroke="{RED}" stroke-width="2"/>')
    t, _ = text(SORA, label, 28, 46, 28, '#fff' if primary else BONE, 0); s += t
    t, _ = text(MONO, sub, 28, 74, 15, '#ffd5da' if primary else MUTED, 1); s += t
    t, _ = text(SORA, '>', W2 - 28, 60, 34, '#fff' if primary else RED, 0, 'end'); s += t
    save(name, svg(W2, H2, s))


button(f'b-pypi-{V}.svg', 'Pycodemath on PyPI', 'pip install pycodemath', True)
button(f'b-site-{V}.svg', 'Visit cybersora.pl', 'SITE  ·  CONTACT  ·  MESHUGA', False)

# FOOTER: contact + the cat avatar (raster, embedded)
im = Image.open(DOC + 'cybersora-assets/logo/kot-awatar/FB-awatar-1080.png').convert('RGBA').resize((192, 192), Image.LANCZOS)
from PIL import ImageDraw
m = Image.new('L', (768, 768), 0); ImageDraw.Draw(m).ellipse((4, 4, 764, 764), fill=255)
im.putalpha(Image.composite(im.getchannel('A'), Image.new('L', (192, 192), 0), m.resize((192, 192), Image.LANCZOS)))
buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
cat = base64.b64encode(buf.getvalue()).decode()
W2, H2 = 1200, 160
s = rpanel(W2, H2)
t, wc = text(SORA, 'cyber', 36, 78, 40, BONE, 0); s += t
t, _ = text(SORA, 'sora', 36 + wc, 78, 40, RED, 0); s += t
t, _ = text(MONO, 'cybersora.pl  ·  cybersora@zohomail.eu  ·  IG @deadsora', 36, 116, 18, MUTED, 0); s += t
s += codestrip(700, 84, 300, 7, 16, 19)
s += f'<image x="{W2 - 36 - 112}" y="24" width="112" height="112" href="data:image/png;base64,{cat}"/>'
save(f'footer-{V}.svg', svg(W2, H2, s, FL))
