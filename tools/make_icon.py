"""Builds icons/icon.svg: an eighth note filled with the app's color wheel (the 12 note
colors swept around its centre, C red at the top), on a black button.
Run: python3 tools/make_icon.py  (then tools/render_icons.sh for the PNGs)"""
import math, colorsys

HUES = [0, 28, 54, 88, 134, 168, 192, 218, 248, 276, 304, 334]   # app's chromatic map
SATS = [88, 92, 94, 82, 82, 84, 90, 90, 84, 86, 88, 88]
CX, CY = 335, 300   # centre of the color sweep: in the gap under the flag, so no seam on the note


def hsl(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return '#%02x%02x%02x' % (round(r * 255), round(g * 255), round(b * 255))


def hue_at(a):  # a = degrees clockwise from top; interpolate the 12 note hues
    s = a / 30.0
    i = int(math.floor(s)) % 12; j = (i + 1) % 12; t = s - math.floor(s)
    h0, h1 = HUES[i], HUES[j] + (360 if HUES[j] < HUES[i] else 0)
    return (h0 + (h1 - h0) * t) % 360, SATS[i] + (SATS[j] - SATS[i]) * t


def pt(a_deg, r):
    th = math.radians(a_deg)
    return CX + r * math.sin(th), CY - r * math.cos(th)


wedges = []
N = 180
for k in range(N):
    a0, a1 = k * 360 / N, (k + 1.15) * 360 / N
    h, s = hue_at((a0 + a1) / 2)
    x0, y0 = pt(a0, 400); x1, y1 = pt(a1, 400)
    wedges.append(f'<path d="M{CX} {CY} L{x0:.2f} {y0:.2f} L{x1:.2f} {y1:.2f}Z" fill="{hsl(h, s, 56)}"/>')
wedges = ''.join(wedges)

# Eighth note: tilted oval head, stem rising from its right side, one curled flag.
HEAD = '<ellipse cx="206" cy="366" rx="92" ry="64" transform="rotate(-24 206 366)"/>'
STEM = '<rect x="268" y="84" width="28" height="290" rx="6"/>'
FLAG = ('<path d="M282 84 C 290 150 404 172 404 270 C 404 314 388 346 366 372 '
        'C 380 334 388 300 372 262 C 354 222 318 206 282 200 Z"/>')
SHAPE = HEAD + STEM + FLAG

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <defs>
    <mask id="note"><g fill="#fff">{SHAPE}</g></mask>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="24"/></filter>
    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0.32"/><stop offset="0.55" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="512" height="512" fill="#000"/>
  <g mask="url(#note)" filter="url(#soft)" opacity="0.5">{wedges}</g>
  <g mask="url(#note)">{wedges}<rect width="512" height="512" fill="url(#sheen)"/></g>
</svg>
'''
open('icons/icon.svg', 'w').write(svg)
print('wrote icons/icon.svg')
