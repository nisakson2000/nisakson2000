#!/usr/bin/env python3
"""Generate the retro SVG assets for the profile README.

Edit the CONTENT section below, then run:  python3 scripts/build.py
Font: Press Start 2P (SIL Open Font License), subset + embedded as woff2.
"""
import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
FONT = base64.b64encode((ROOT / "scripts" / "ps2p.woff2").read_bytes()).decode()

# ── palette ────────────────────────────────────────────────────────────────
BG, BG2 = "#0b0820", "#160f3a"
PINK, CYAN, YEL, GRN, WHT, DIM = "#ff3caa", "#3ef0ff", "#ffd23f", "#39ff88", "#f4f1ff", "#6b5fa8"

# ── CONTENT ────────────────────────────────────────────────────────────────
NAME = "NICK ISAKSON"
SUBTITLE = "DATA CENTER TECH * SECURITY NERD * BUILDER"
BOOT = [
    "C:\\> LOAD NISAKSON2000.SAV",
    "READING SAVE FILE......... OK",
    "LAST SAVE: A WHILE AGO. WELCOME BACK.",
]
SHEET = [
    ("NAME", "NICK"),
    ("CLASS", "DATA CENTER TECH"),
    ("GUILD", "AMAZON"),
    ("ORIGIN", "WASHINGTON"),
    ("BACKSTORY", "CYBERSECURITY B.A.S."),
]
STATS = [  # label, 0-100
    ("HARDWARE", 85), ("LINUX", 75), ("SECURITY", 80),
    ("PYTHON", 55), ("KQL", 70), ("CAFFEINE", 100),
]
ACHIEVEMENTS = [  # title, subtitle, unlocked
    ("SECURITY+", "COMPTIA", True),
    ("CYSA+", "COMPTIA", True),
    ("B.A.S. CYBER", "COLUMBIA BASIN", True),
    ("DC TECH", "JOINED AMAZON", True),
    ("ARCH BTW", "DAILY-DRIVES LINUX", True),
    ("???", "COMING SOON...", False),
]

# 16x18 player sprite. K=outline H=hair S=skin E=eye G=headset T=shirt Y=badge P=pants M=mic
SPRITE = [
    "....KKKKKKKK....",
    "...KHHHHHHHHK...",
    "..KHHHHHHHHHHK..",
    "..KHHHSSSSHHHK..",
    ".GKHSSSSSSSSHKG.",
    ".GKSSESSSSESSKG.",
    ".GKSSSSSSSSSSKG.",
    ".MKSSSSKKSSSSK..",
    "..MMKSSSSSSKK...",
    "....KKKKKKKK....",
    "..KKTTTTTTTTKK..",
    ".KTTTTTTTTTTTTK.",
    ".KTTKTTTTYYTKTK.",
    ".KSKKTTTTYYTKSK.",
    ".KSKKTTTTTTTKSK.",
    "..K.KPPPPPPPK.K.",
    "....KPPK.KPPK...",
    "....KKKK.KKKK...",
]
SPRITE_COLORS = {"K": "#120a24", "H": "#5a3a22", "S": "#f2c49b", "E": "#120a24",
                 "G": "#3a3a4a", "M": "#3a3a4a", "T": "#2f6fdb", "Y": YEL, "P": "#2a2a44"}


# ── helpers ────────────────────────────────────────────────────────────────
def svg(w, h, body, extra_defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
<style>
@font-face{{font-family:'PS2P';src:url(data:font/woff2;base64,{FONT}) format('woff2');}}
text{{font-family:'PS2P',monospace;}}
</style>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".28"/></pattern>
<radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".65"/></radialGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{extra_defs}
</defs>
{body}
</svg>'''


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def blink(dur="1s", begin="0s"):
    return (f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" '
            f'dur="{dur}" begin="{begin}" repeatCount="indefinite"/>')


def screen(w, h, inner):
    """CRT screen: bezel, background, content, scanlines, vignette."""
    return f'''<rect width="{w}" height="{h}" rx="18" fill="#1d1733"/>
<rect x="8" y="8" width="{w-16}" height="{h-16}" rx="12" fill="{BG}"/>
<g>{inner}</g>
<rect x="8" y="8" width="{w-16}" height="{h-16}" rx="12" fill="url(#scan)"/>
<rect x="8" y="8" width="{w-16}" height="{h-16}" rx="12" fill="url(#vig)"/>'''


def pixel_star(x, y, s, color):
    pts = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    return "".join(f'<rect x="{x+px*s}" y="{y+py*s}" width="{s}" height="{s}" fill="{color}"/>' for px, py in pts)


def trophy(x, y, s, color):
    rows = ["K.KKKKK.K", "KKYYYYYKK", "K.YYYYY.K", "...YYY...", "....Y....", "...YYY...", "..KKKKK.."]
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == ".":
                continue
            fill = color if ch == "Y" else ("#120a24" if color == DIM else "#b8860b")
            out.append(f'<rect x="{x+c*s}" y="{y+r*s}" width="{s}" height="{s}" fill="{fill}"/>')
    return "".join(out)


# ── assets ─────────────────────────────────────────────────────────────────
def header():
    W, H = 840, 330
    T = 6.0  # total intro length (s)
    parts, defs = [], []
    y, start = 52, 0.3
    for i, line in enumerate(BOOT):
        lw = len(line) * 14 + 4
        end = start + len(line) * 0.035
        defs.append(f'<clipPath id="c{i}"><rect x="40" y="{y-16}" width="{lw}" height="22">'
                    f'<animate attributeName="width" values="0;0;{lw}" keyTimes="0;{start/T:.3f};{end/T:.3f}" '
                    f'dur="{T}s" fill="freeze"/></rect></clipPath>')
        color = GRN if i < 2 else CYAN
        parts.append(f'<text x="40" y="{y}" font-size="14" fill="{color}" clip-path="url(#c{i})">{esc(line)}</text>')
        y += 28
        start = end + 0.25
    t0 = start / T
    fade = (f'<animate attributeName="opacity" values="0;0;1" keyTimes="0;{t0:.3f};{min(t0+0.05,1):.3f}" '
            f'dur="{T}s" fill="freeze"/>')
    tw = len(NAME) * 48
    parts.append(f'''<g>{fade}
<text x="{W/2+4}" y="{205+4}" font-size="48" text-anchor="middle" fill="{CYAN}">{NAME}</text>
<text x="{W/2}" y="205" font-size="48" text-anchor="middle" fill="{PINK}" filter="url(#glow)">{NAME}</text>
<rect x="{(W-tw)/2}" y="222" width="{tw}" height="4" fill="{YEL}"/>
<text x="{W/2}" y="254" font-size="14" text-anchor="middle" fill="{WHT}">{esc(SUBTITLE)}</text>
<g>{blink("1.1s")}
<polygon points="{W/2-118},281 {W/2-118},297 {W/2-106},289" fill="{YEL}"/>
<text x="{W/2+8}" y="297" font-size="16" text-anchor="middle" fill="{YEL}">PRESS START</text></g>
</g>''')
    return svg(W, H, screen(W, H, "\n".join(parts)), "\n".join(defs))


def banner(text, color=YEL):
    W, H = 840, 64
    tw = len(text) * 24
    l, r = (W - tw) / 2 - 50, (W + tw) / 2 + 26
    body = f'''<rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="{BG2}"/>
<rect x="0" y="0" width="{W}" height="{H}" rx="10" fill="url(#scan)"/>
<rect x="0" y="{H-6}" width="{W}" height="6" rx="3" fill="{PINK}" opacity=".85"/>
<g>{blink("1.4s")}{pixel_star(l, 20, 8, CYAN)}{pixel_star(r, 20, 8, CYAN)}</g>
<text x="{W/2+3}" y="{H/2+15}" font-size="24" text-anchor="middle" fill="{PINK}">{esc(text)}</text>
<text x="{W/2}" y="{H/2+12}" font-size="24" text-anchor="middle" fill="{color}">{esc(text)}</text>'''
    return svg(W, H, body)


def player():
    W, H = 840, 384
    s = 9
    sx, sy = 70, 92
    px = []
    for r, row in enumerate(SPRITE):
        for c, ch in enumerate(row):
            if ch != ".":
                px.append(f'<rect x="{sx+c*s}" y="{sy+r*s}" width="{s}" height="{s}" fill="{SPRITE_COLORS[ch]}"/>')
    sprite = (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -6;0 0" '
              f'keyTimes="0;.5;1" calcMode="discrete" dur=".9s" repeatCount="indefinite"/>{"".join(px)}</g>')
    hearts = "".join(
        f'<text x="{58+i*28}" y="320" font-size="20" fill="{PINK if i < 4 else DIM}">&#9829;</text>' for i in range(6))
    left = f'''<rect x="40" y="40" width="210" height="300" rx="6" fill="{BG2}" stroke="{CYAN}" stroke-width="3"/>
<text x="145" y="72" font-size="14" text-anchor="middle" fill="{YEL}">PLAYER 1</text>
<rect x="64" y="262" width="162" height="8" fill="#000" opacity=".35"/>
{sprite}
<text x="145" y="296" font-size="10" text-anchor="middle" fill="{WHT}">HP</text>
{hearts}'''
    lines = []
    y = 66
    for k, v in SHEET:
        lines.append(f'<text x="280" y="{y}" font-size="14" fill="{CYAN}">{esc(k)}</text>'
                     f'<text x="440" y="{y}" font-size="14" fill="{WHT}">{esc(v)}</text>')
        y += 26
    lines.append(f'<text x="280" y="{y}" font-size="14" fill="{CYAN}">STATUS</text>'
                 f'<text x="440" y="{y}" font-size="14" fill="{GRN}">RESPAWNING<tspan>{blink(".8s")}_</tspan></text>')
    y += 34
    bars = []
    bx, bw = 420, 360
    for i, (k, v) in enumerate(STATS):
        col, row = i % 2, i // 2
        x = 280 + col * 265
        yy = y + row * 36
        w = 140 * v / 100
        segs = "".join(f'<rect x="{x+100+j*14}" y="{yy-12}" width="2" height="14" fill="{BG}"/>' for j in range(1, 10))
        fill = YEL if v >= 100 else PINK
        bars.append(f'''<text x="{x}" y="{yy}" font-size="10" fill="{WHT}">{k}</text>
<rect x="{x+100}" y="{yy-12}" width="140" height="14" fill="#000" stroke="{DIM}" stroke-width="2"/>
<rect x="{x+100}" y="{yy-12}" width="{w}" height="14" fill="{fill}"><animate attributeName="width" from="0" to="{w}" dur="1.6s" begin="{.2+i*.15:.2f}s" fill="freeze"/></rect>{segs}''')
    # XP bar
    xy = y + 3 * 36 + 8
    xp = f'''<text x="280" y="{xy}" font-size="10" fill="{YEL}">XP</text>
<rect x="310" y="{xy-12}" width="475" height="14" fill="#000" stroke="{DIM}" stroke-width="2"/>
<rect x="310" y="{xy-12}" width="90" height="14" fill="{GRN}"><animate attributeName="width" values="20;90;90" keyTimes="0;.6;1" dur="3s" repeatCount="indefinite"/></rect>
<text x="547" y="{xy+22}" font-size="9" text-anchor="middle" fill="{DIM}">LEVELING BACK UP. SIDE QUESTS LOADING...</text>'''
    return svg(W, H, screen(W, H, left + "\n".join(lines) + "".join(bars) + xp))


def achievements():
    W, H = 840, 290
    cards = []
    cw, ch, gap = 244, 104, 20
    for i, (title, sub, ok) in enumerate(ACHIEVEMENTS):
        col, row = i % 3, i // 3
        x = 38 + col * (cw + gap)
        y = 30 + row * (ch + gap)
        border = YEL if ok else DIM
        tc = WHT if ok else DIM
        tag = (f'<text x="{x+cw-12}" y="{y+ch-12}" font-size="8" text-anchor="end" fill="{GRN}">UNLOCKED</text>' if ok
               else f'<text x="{x+cw-12}" y="{y+ch-12}" font-size="8" text-anchor="end" fill="{PINK}">LOCKED<tspan>{blink()}_</tspan></text>')
        cards.append(f'''<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="6" fill="{BG2}" stroke="{border}" stroke-width="3"/>
{trophy(x+16, y+22, 6, YEL if ok else DIM)}
<text x="{x+84}" y="{y+42}" font-size="12" fill="{tc}">{esc(title)}</text>
<text x="{x+84}" y="{y+62}" font-size="8" fill="{CYAN if ok else DIM}">{esc(sub)}</text>
{tag}''')
    return svg(W, H, screen(W, H, "\n".join(cards)))


def footer():
    W, H = 840, 200
    n = 10
    digits = "".join(
        f'<text x="{W/2+126}" y="118" font-size="28" text-anchor="middle" fill="{PINK}" opacity="0">{9-i}'
        f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0;{1/n:.3f};{1/n:.3f};1" '
        f'begin="{i}s" dur="{n}s" repeatCount="indefinite"/></text>' for i in range(n))
    body = f'''<text x="{W/2}" y="66" font-size="28" text-anchor="middle" fill="{YEL}" filter="url(#glow)">THANKS FOR PLAYING!</text>
<text x="{W/2-20}" y="118" font-size="28" text-anchor="middle" fill="{CYAN}">CONTINUE?</text>
{digits}
<g>{blink("1.2s")}<text x="{W/2}" y="164" font-size="14" text-anchor="middle" fill="{WHT}">INSERT COIN</text></g>'''
    return svg(W, H, screen(W, H, body))


def main():
    OUT.mkdir(exist_ok=True)
    files = {
        "header.svg": header(),
        "player.svg": player(),
        "achievements.svg": achievements(),
        "footer.svg": footer(),
        "banner-player.svg": banner("PLAYER SELECT"),
        "banner-quests.svg": banner("QUEST LOG"),
        "banner-inventory.svg": banner("INVENTORY"),
        "banner-achievements.svg": banner("ACHIEVEMENTS"),
        "banner-arcade.svg": banner("ARCADE"),
    }
    for name, content in files.items():
        (OUT / name).write_text(content)
        print(f"wrote assets/{name} ({len(content)//1024} KB)")


if __name__ == "__main__":
    main()
