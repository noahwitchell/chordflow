"""Builds icons/icon.svg: an eighth note filled with the app's color wheel (the 12 note
colors swept around its centre, C red at the top), on a black button.
Run: python3 tools/make_icon.py  (then tools/render_icons.sh for the PNGs)"""
import math, colorsys

HUES = [0, 28, 54, 88, 134, 168, 192, 218, 248, 276, 304, 334]   # app's chromatic map
SATS = [88, 92, 94, 82, 82, 84, 90, 90, 84, 86, 88, 88]


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))


def hue_at(a):  # a = degrees clockwise from top; interpolate the 12 note hues
    s = a / 30.0
    i = int(math.floor(s)) % 12; j = (i + 1) % 12; t = s - math.floor(s)
    h0, h1 = HUES[i], HUES[j] + (360 if HUES[j] < HUES[i] else 0)
    return (h0 + (h1 - h0) * t) % 360, SATS[i] + (SATS[j] - SATS[i]) * t


# ---- the note, drawn in its own units, then fitted to the square ----------------
# Head: a tilted oval. Stem: rises from the head's rightmost point (so it meets the head
# cleanly and hides its foot inside it). Flag: one smooth shape with the stem's top.
HX, HY, HRX, HRY, HROT = 0.0, 0.0, 90.0, 63.0, -22.0
STEM_W, STEM_H = 25.0, 300.0
def head_right():
    th = math.radians(HROT)
    best = max(((HRX * math.cos(t) * math.cos(th) - HRY * math.sin(t) * math.sin(th),
                 HRX * math.cos(t) * math.sin(th) + HRY * math.sin(t) * math.cos(th))
                for t in [i * math.pi / 1800 for i in range(3600)]), key=lambda p: p[0])
    return HX + best[0], HY + best[1]
xr, yj = head_right()
xr -= 0.5                     # stem's right edge sits on the head's outline
xl, yt = xr - STEM_W, yj - STEM_H
yb = yj + 1                   # foot of the stem, ends on the head outline
f = lambda dx, dy: f'{xr + dx:.1f} {yt + dy:.1f}'
STEMFLAG = (f'M{xl:.1f} {yb:.1f} L{xl:.1f} {yt:.1f} L{xr:.1f} {yt:.1f} '
            f'C{f(6, 58)} {f(112, 96)} {f(112, 196)} '      # outer edge swells out…
            f'C{f(112, 238)} {f(98, 268)} {f(78, 294)} '      # …and tapers to a point
            f'C{f(90, 252)} {f(86, 208)} {f(52, 178)} '       # inner edge curls back…
            f'C{f(34, 162)} {f(16, 152)} {f(0, 146)} '        # …into the stem
            f'L{xr:.1f} {yb:.1f} Z')
HEAD = f'<ellipse cx="{HX}" cy="{HY}" rx="{HRX}" ry="{HRY}" transform="rotate({HROT} {HX} {HY})"/>'

# fit: glyph bounds (head + flag), scaled so its height fills ~66% of the icon, centred
gx0, gx1 = HX - 86, xr + 113
gy0, gy1 = yt, HY + 70
SIZE = 0.66 * 512
k = SIZE / (gy1 - gy0)
tx, ty = 256 - k * (gx0 + gx1) / 2, 256 - k * (gy0 + gy1) / 2
FIT = f'translate({tx:.2f} {ty:.2f}) scale({k:.4f})'
CX, CY = tx + k * (xr + 46), ty + k * (yt + 252)   # colour sweep centre: the hollow under the flag

def pt(a_deg, r):
    th = math.radians(a_deg)
    return CX + r * math.sin(th), CY - r * math.cos(th)


wedges = []
N = 720
for i in range(N):
    a0, a1 = i * 360 / N, (i + 2.5) * 360 / N
    h, s = hue_at((a0 + a1) / 2)
    x0, y0 = pt(a0, 400); x1, y1 = pt(a1, 400)
    wedges.append(f'<path d="M{CX} {CY} L{x0:.2f} {y0:.2f} L{x1:.2f} {y1:.2f}Z" fill="{hsl(h, s, 56)}"/>')
wedges = ''.join(wedges)

SHAPE = f'<g transform="{FIT}">{HEAD}<path d="{STEMFLAG}"/></g>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <mask id="note"><g fill="#fff">{SHAPE}</g></mask>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="24"/></filter>
    <filter id="smooth"><feGaussianBlur stdDeviation="1.2"/></filter>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0.32"/><stop offset="0.55" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="#000"/>
  <g mask="url(#note)" filter="url(#soft)" opacity="0.5">{wedges}</g>
  <g mask="url(#note)"><g filter="url(#smooth)">{wedges}</g><rect width="512" height="512" fill="url(#sheen)"/></g>
</svg>
'''
open('icons/icon.svg', 'w').write(svg)
print('wrote icons/icon.svg')
