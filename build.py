import random, io, zlib
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

F = 'C:/Users/maisa/Documents/SoraWebsite/fonts/'


def load(n, w):
    return instantiateVariableFont(TTFont(F + n), {'wght': w})


SORA = load('sora-latin-wght-normal.woff2', 800)
MONO = load('geist-mono-latin-wght-normal.woff2', 500)
MONOB = load('geist-mono-latin-wght-normal.woff2', 700)
INK = '#0e0e12'; RED = '#e11d33'; HOT = '#ff3a52'; SOLID = '#d4132b'
MUTED = '#9a9098'; LABEL = '#ff6b7d'; PANEL = '#16161c'; LINE = '#2a2a33'; WHITE = '#f4f1f2'


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


def pixels(x0, y0, w, h, cell, seed, left_fade=True, flick=True, gap=1):
    random.seed(seed); o = []; cols = w // cell; rows = h // cell
    for r in range(rows):
        for c in range(cols):
            p = c / max(cols - 1, 1)
            if not left_fade:
                p = 1 - p
            if random.random() < 0.08 + 0.72 * p ** 1.6:
                col = random.choices([RED, HOT, SOLID, '#7a1035', '#3a1a22', WHITE], [5, 3, 3, 3, 4, 1])[0]
                op = round(random.uniform(.3, 1), 2)
                cls = ' class="f%d"' % random.randint(1, 3) if flick and random.random() < .2 else ''
                o.append(f'<rect{cls} x="{x0 + c * cell}" y="{y0 + r * cell}" width="{cell - gap}" height="{cell - gap}" fill="{col}" opacity="{op}"/>')
    return ''.join(o)


FL = '@keyframes a{0%,100%{opacity:.15}50%{opacity:1}}.f1{animation:a 3s infinite}.f2{animation:a 4.3s .7s infinite}.f3{animation:a 5.1s 1.9s infinite}'

# BANNER
W, H = 1200, 320
b = f'<defs><linearGradient id="g"><stop offset="0" stop-color="{INK}" stop-opacity=".96"/><stop offset=".7" stop-color="{INK}" stop-opacity=".85"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient></defs>'
b += f'<rect width="{W}" height="{H}" fill="{INK}"/>' + pixels(0, 0, W, H, 20, 11)
b += f'<rect width="760" height="{H}" fill="url(#g)"/>'
t, _ = text(MONO, '// STUDIO  ·  AI TOOLS  ·  DESKTOP APPS', 56, 92, 17, LABEL, 3); b += t
t, wd = text(SORA, 'CYBER', 52, 200, 104, WHITE, -2); b += t
t, _ = text(SORA, 'SORA', 52 + wd + 10, 200, 104, RED, -2); b += t
t, _ = text(MONO, 'cybersora.pl', 56, 262, 19, MUTED, 1); b += t
b += f'<rect x="0" y="{H - 4}" width="{W}" height="4" fill="{RED}"/>'
save('banner-3.svg', svg(W, H, b, FL))

# SECTION HEADERS
for n, (num, lab) in {'who': ('01', 'WHO WE ARE'), 'what': ('02', 'WHAT WE BUILD'), 'vision': ('03', 'VISION'),
                      'stack': ('04', 'STACK'), 'beyond': ('05', 'BEYOND CODE')}.items():
    W2 = 1200; H2 = 56
    s = f'<rect width="{W2}" height="{H2}" fill="{INK}"/><rect width="6" height="{H2}" fill="{RED}"/>'
    t, w1 = text(MONO, num, 28, 36, 15, RED, 2); s += t
    t, w2 = text(SORA, lab, 28 + w1 + 18, 38, 26, WHITE, 1); s += t
    xs = int(28 + w1 + 18 + w2 + 24)
    s += pixels(xs, 12, W2 - xs, 32, 8, zlib.crc32(n.encode()) % 99)
    save(f'h-{n}.svg', svg(W2, H2, s, FL))


def panel(name, lines, H2, size=19):
    W2 = 1200
    s = f'<rect width="{W2}" height="{H2}" fill="{PANEL}"/><rect width="6" height="{H2}" fill="{LINE}"/>'
    y = 42
    for ln, col in lines:
        t, _ = text(MONO, ln, 32, y, size, col, 0); s += t; y += size + 14
    save(name, svg(W2, H2, s))


panel('p-who-2.svg', [('> cybersora is a software brand.', WHITE),
                    ('> we build desktop apps, local-first tools and AI assistants.', WHITE),
                    ('> shipped for real clients. not templates, not tutorials.', MUTED)], 142)
panel('p-vision.svg', [('> software that runs on your machine and respects your data.', WHITE),
                       ('> one job per tool, done well. no telemetry, no fluff.', MUTED)], 100)
panel('p-beyond.svg', [('> music production, game design, terminal toys,', WHITE),
                       ('> and tools we wish already existed.', MUTED)], 100)


def card(name, title, desc, tag, pub=True):
    W2, H2 = 588, 150
    s = f'<rect width="{W2}" height="{H2}" fill="{PANEL}"/><rect width="{W2}" height="3" fill="{RED if pub else LINE}"/>'
    t, _ = text(SORA, title, 24, 58, 28, WHITE if pub else MUTED, 0); s += t
    for i, ln in enumerate(desc):
        t, _ = text(MONO, ln, 24, 92 + i * 22, 15, MUTED, 0); s += t
    label = 'PUBLIC' if pub else 'PRIVATE'
    _, tw = text(MONOB, label, 0, 0, 12, '#fff', 2)
    px = W2 - 24 - tw - 20
    s += f'<rect x="{px}" y="28" width="{tw + 20}" height="24" rx="12" fill="{RED if pub else "none"}" stroke="{RED if pub else LINE}"/>'
    t, _ = text(MONOB, label, px + 10, 45, 12, '#fff' if pub else MUTED, 2); s += t
    t, _ = text(MONO, tag, 24, H2 - 16, 13, LABEL if pub else '#6a626c', 1); s += t
    save(name, svg(W2, H2, s))


card('c-soraflux-2.svg', 'SoraFlux', ['Free local converter: video, audio,', 'image, GIF. No telemetry.'], 'TAURI 2 · RUST')
card('c-pycodemath.svg', 'Pycodemath', ['Exact math for AI agents. Token-', 'efficient, SymPy + NumPy.'], 'PYTHON · SYMPY · NUMPY')
card('c-site.svg', 'cybersora.pl', ['Our site: a terminal-style OS,', 'running in the browser.'], 'HTML · JAVASCRIPT')
card('c-somi.svg', 'SOMI', ['Personal AI assistant: voice,', 'terminal, offers radar.'], 'PYTHON · AI', pub=False)
card('c-salondesk.svg', 'SalonDesk', ['Desktop app for beauty salons,', 'used in a real salon.'], 'PYTHON · SQLITE', pub=False)
card('c-more.svg', '+ more', ['Games, licensing, security tools.', 'Not public yet.'], 'SOON', pub=False)

# STACK chips
items = ['RUST', 'PYTHON', 'JAVASCRIPT', 'TAURI', 'SQLITE', 'THREE.JS', 'NEXT.JS', 'HTML/CSS', 'GIT', 'DISCORD API']
W2 = 1200; x = 0; y = 0; pos = []
for it in items:
    _, tw = text(MONOB, it, 0, 0, 15, RED, 1); w = tw + 40
    if x + w > W2:
        x = 0; y += 52
    pos.append((x, y, w, it)); x += w + 12
H2 = y + 40
s = f'<rect width="{W2}" height="{H2}" fill="{INK}"/>'
for x, y, w, it in pos:
    s += f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="3" fill="{PANEL}" stroke="{LINE}"/><rect x="{x}" y="{y}" width="4" height="40" fill="{RED}"/>'
    t, _ = text(MONOB, it, x + 20, y + 26, 15, WHITE, 1); s += t
save('stack.svg', svg(W2, H2, s))

# FOOTER
W2, H2 = 1200, 110
s = f'<defs><linearGradient id="g2"><stop offset="0" stop-color="{INK}" stop-opacity=".97"/><stop offset=".6" stop-color="{INK}" stop-opacity=".9"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></linearGradient></defs>'
s += f'<rect width="{W2}" height="{H2}" fill="{INK}"/>' + pixels(0, 0, W2, H2, 16, 5, left_fade=False)
s += f'<rect width="{W2}" height="{H2}" fill="url(#g2)"/>'
t, _ = text(SORA, 'cybersora.pl', 40, 66, 36, WHITE, 0); s += t
t, _ = text(MONO, 'terminal-style site, free tools, contact', 40, 92, 15, MUTED, 1); s += t
s += f'<rect x="0" y="{H2 - 3}" width="{W2}" height="3" fill="{RED}"/>'
save('footer.svg', svg(W2, H2, s, FL))
