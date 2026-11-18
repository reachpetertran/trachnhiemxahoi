#!/usr/bin/env python3
"""Sinh logo trachnhiemxahoi.com (cùng họ huy hiệu với daynentang, kynanglamviec).

Chạy: python3 _build/art/logo_art.py  -> _build/static/assets/logo*.svg, favicon.svg
Chữ được đổi thành đường nét (Inter Bold) để hiển thị giống nhau trên mọi máy.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

OUT = Path(__file__).resolve().parent.parent / "static/assets"
FONT = TTFont("/usr/share/fonts/opentype/inter/Inter-Bold.otf")
GS, CMAP = FONT.getGlyphSet(), FONT.getBestCmap()

NAVY, NAVY2, DEEP, INK = "#16324f", "#1f4673", "#0d2136", "#081625"
SUN1, SUN2, GOLD, CREAM = "#f39a45", "#e0701b", "#f6b04a", "#fffdf8"
HAT, HAT2 = "#f7c948", "#fde68a"
FIELD, FIELD2 = "#2f7d4a", "#5cae4f"


def text_path(txt, size, cx, baseline, fill, spacing=0.0):
    """Đường nét chữ, căn giữa tại cx."""
    upm = FONT["head"].unitsPerEm
    s = size / upm
    # dựng glyph (có dấu tiếng Việt: dùng ký tự đã dựng sẵn trong font)
    glyphs = [CMAP.get(ord(ch)) for ch in txt]
    widths = [FONT["hmtx"][g][0] * s + spacing * size if g else size * 0.3 for g in glyphs]
    x = cx - (sum(widths) - spacing * size) / 2
    pen = SVGPathPen(GS)
    for g, w in zip(glyphs, widths):
        if g:
            GS[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        x += w
    return f'<path fill="{fill}" d="{pen.getCommands()}"/>'


def person(x, y, k, hat="helmet", extra=""):
    """Người đứng, đội mũ bảo hộ hoặc nón lá."""
    head = (f'<path d="M-6.5 -33 Q0 -41 6.5 -33 L8 -32 H-8Z" fill="{CREAM}"/><rect x="-7.5" y="-33" width="15" height="2" fill="{SUN2}"/>'
            if hat == "helmet" else f'<path d="M-10 -31 L0 -40 L10 -31Z" fill="{GOLD}"/>')
    return (f'<g transform="translate({x} {y}) scale({k})" fill="{INK}">'
            f'<circle cx="0" cy="-30" r="4.3"/>'
            f'<path d="M-4.5 -25 Q0 -27.5 4.5 -25 L5.5 -12 L-5 -12Z"/>'
            f'<path d="M-2.5 -13 L-6 -1 M2.5 -13 L5.5 -1" stroke="{INK}" stroke-width="4" stroke-linecap="round" fill="none"/>'
            f'<path d="M-3.5 -23 L-8 -15 M3.5 -23 L8 -16" stroke="{INK}" stroke-width="3" stroke-linecap="round" fill="none"/>'
            f'{extra}{head}</g>')


def scene():
    p = []
    p.append(f'<rect width="400" height="440" fill="{NAVY}"/>')
    p.append(f'<circle cx="200" cy="170" r="92" fill="url(#tsun)"/>')
    # đồi xa
    p.append(f'<path d="M20 300 L100 222 L150 252 L205 196 L262 246 L310 212 L390 300Z" fill="{NAVY2}"/>')
    # máy bay – người đi làm việc ở nước ngoài
    p.append(f'<g transform="translate(296 106) rotate(-14)" fill="{DEEP}"><path d="M-22 0 Q-22 -3 -16 -3 H14 Q22 -3 24 0 Q22 3 14 3 H-16 Q-22 3 -22 0Z"/>'
             f'<path d="M-2 -2 L-12 -16 H-6 L8 -2Z M-2 2 L-12 16 H-6 L8 2Z M-18 -2 L-23 -10 H-19 L-12 -2Z"/></g>')
    p.append(f'<path d="M244 128 q-24 6 -46 4" fill="none" stroke="{CREAM}" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 6" opacity=".8"/>')
    # nhà máy mái răng cưa + ống khói (bên trái)
    p.append(f'<path d="M52 312 V252 L78 236 V252 L104 236 V252 L130 236 V252 L148 242 V312Z" fill="{DEEP}"/>')
    p.append(f'<rect x="60" y="196" width="12" height="58" fill="{DEEP}"/><rect x="60" y="204" width="12" height="4" fill="{SUN2}"/>')
    for cx, cy, r in [(70, 186, 6), (78, 176, 7.5), (88, 166, 9)]:
        p.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{CREAM}" opacity=".55"/>')
    for i in range(4):
        for j in range(2):
            p.append(f'<rect x="{62 + i * 20}" y="{264 + j * 16}" width="10" height="8" fill="{GOLD}"/>')
    # ruộng bậc thang (bên phải)
    p.append(f'<path d="M252 312 Q300 270 372 268 V312Z" fill="{FIELD}"/>')
    p.append(f'<path d="M262 312 Q312 284 372 284 V312Z" fill="{FIELD2}"/>')
    p.append(f'<path d="M282 312 Q322 298 372 298" fill="none" stroke="{FIELD}" stroke-width="3"/>')
    # mặt đất
    p.append(f'<path d="M0 306 Q200 292 400 306 L400 440 L0 440Z" fill="#102a44"/>')
    # biểu tượng giữa: quyển sách mở + mũ bảo hộ (biết luật để tự bảo vệ)
    p.append(f'<g transform="translate(200 300)">'
             f'<path d="M-62 -6 Q-30 -20 0 -8 Q30 -20 62 -6 V16 Q30 4 0 16 Q-30 4 -62 16Z" fill="{CREAM}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
             f'<path d="M0 -8 V16" stroke="{INK}" stroke-width="3"/>'
             f'<path d="M-50 0 Q-28 -9 -10 -2 M-50 8 Q-28 -1 -10 6 M10 -2 Q28 -9 50 0 M10 6 Q28 -1 50 8" stroke="{NAVY2}" stroke-width="2" fill="none" stroke-linecap="round"/>'
             f'<g transform="translate(0 -14)">'
             f'<path d="M-40 0 Q-40 -44 0 -46 Q40 -44 40 0Z" fill="{HAT}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<path d="M-8 -45 Q0 -47 8 -45 V-6 H-8Z" fill="{SUN2}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
             f'<path d="M-50 0 H50 Q52 6 46 7 H-46 Q-52 6 -50 0Z" fill="{HAT}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
             f'<path d="M-28 -24 Q-26 -36 -14 -40" stroke="{CREAM}" stroke-width="4" fill="none" stroke-linecap="round" opacity=".7"/>'
             f'</g></g>')
    # người lao động
    p.append(person(98, 318, 0.95))
    p.append(person(122, 320, 0.85))
    p.append(person(300, 316, 0.9, hat="nonla"))
    p.append(person(330, 320, 0.85, extra=f'<rect x="7" y="-18" width="9" height="11" rx="1.5"/><path d="M9.5 -18 v-2 h4 v2" stroke="{INK}" stroke-width="1.3" fill="none"/>'))
    return "".join(p)


DEFS = (f'<defs><clipPath id="tc"><path d="M48 392 V186 A152 152 0 0 1 352 186 V392 Z"/></clipPath>'
        f'<linearGradient id="tsun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SUN1}"/><stop offset="1" stop-color="{SUN2}"/></linearGradient></defs>')


def badge(with_text=True):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 428" role="img" aria-label="Trách Nhiệm Xã Hội">',
         '<title>Trách Nhiệm Xã Hội – trachnhiemxahoi.com</title>', DEFS,
         f'<path d="M36 400 V186 A164 164 0 0 1 364 186 V400 Z" fill="{NAVY}"/>',
         f'<g clip-path="url(#tc)">{scene()}</g>',
         f'<path d="M48 392 V186 A152 152 0 0 1 352 186 V392 Z" fill="none" stroke="{CREAM}" stroke-width="4"/>']
    if with_text:
        s.append(f'<path d="M14 322 H386 L374 352 L386 382 H14 L26 352Z" fill="{CREAM}" stroke="{NAVY}" stroke-width="6"/>')
        s.append(text_path("TRÁCH NHIỆM XÃ HỘI", 27, 200, 362, NAVY, spacing=0.04))
        s.append(f'<rect x="27" y="392" width="346" height="30" fill="{NAVY}"/>')
        s.append(text_path("EST. 2026 · TRACHNHIEMXAHOI.COM", 13.5, 200, 412, GOLD, spacing=0.09))
    s.append("</svg>")
    return "".join(s)


def icon():
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="Trách Nhiệm Xã Hội">'
            f'<defs><clipPath id="ti"><rect width="64" height="64" rx="13"/></clipPath>'
            f'<linearGradient id="tis" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SUN1}"/><stop offset="1" stop-color="{SUN2}"/></linearGradient></defs>'
            f'<g clip-path="url(#ti)"><rect width="64" height="64" fill="{NAVY}"/><circle cx="32" cy="25" r="17" fill="url(#tis)"/>'
            f'<rect y="48" width="64" height="16" fill="#102a44"/>'
            f'<path d="M10 48 Q21 43 32 47 Q43 43 54 48 V56 Q43 52 32 56 Q21 52 10 56Z" fill="{CREAM}" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M32 47 V56" stroke="{INK}" stroke-width="1.5"/>'
            f'<path d="M17 44 Q17 26 32 25 Q47 26 47 44Z" fill="{HAT}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
            f'<path d="M29 25.5 Q32 25 35 25.5 V40 H29Z" fill="{SUN2}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
            f'<path d="M13 44 H51 Q52 47 49 47.5 H15 Q12 47 13 44Z" fill="{HAT}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
            f'</g></svg>')


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "logo.svg").write_text(badge(True), encoding="utf-8")
    (OUT / "logo-khong-chu.svg").write_text(badge(False), encoding="utf-8")
    (OUT / "logo-icon.svg").write_text(icon(), encoding="utf-8")
    (OUT / "favicon.svg").write_text(icon(), encoding="utf-8")
    print("OK", OUT)
