"""Sách "Quyền Làm Việc" → www/sach/ (gọi từ build_www.py khi có app/sach-data/manifest.json).

app/sach-data/ = thư mục out/app/ do build/app.py của mã sách xuất ra:
manifest.json, chapters/chNN.json, images/chNN.jpg, app.css. KHÔNG đưa lên GitHub công khai.
"""
import html as H
import json
import re
from pathlib import Path

from PIL import Image

E = H.escape

CSS = """
.sach-hd{border-radius:var(--r);padding:16px 16px 14px;color:#fff;margin:14px 0 10px}
.sach-hd small{display:block;font:700 .82rem var(--ui);opacity:.9;letter-spacing:.3px}
.sach-hd h1{color:#fff;margin:.2em 0 .1em}
.sach-hd p{margin:0;font:1rem/1.45 var(--ui);opacity:.95}
.sach-meta{font:.9rem/1.5 var(--ui);color:var(--muted);margin:8px 0}
.sach-meta b{color:var(--ink)}
.sach-fig{margin:12px 0}
.sach-fig img{width:100%;max-width:520px;display:block;margin:0 auto;border-radius:var(--r);height:auto}
.sach-fig figcaption{font:.85rem/1.4 var(--ui);color:var(--muted);text-align:center;margin-top:6px}
.sach-tabs{display:flex;gap:6px;margin:16px 0 4px;position:sticky;top:calc(var(--top-h) + var(--sat));background:var(--bg);padding:6px 0;z-index:5}
.sach-tabs button{flex:1;min-height:48px;border:2px solid var(--brand);background:var(--card);color:var(--brand);border-radius:999px;font:700 15px var(--ui);cursor:pointer}
.sach-tabs button[aria-selected="true"]{background:var(--brand);color:#fff}
html[data-theme="dark"] .sach-tabs button[aria-selected="true"]{color:#12161c}
.sach-l[hidden]{display:none}
.sach .nho{background:var(--warn-bg);border-left:5px solid #d39a1e;padding:10px 14px;margin:0 0 10px;border-radius:0 10px 10px 0}
.sach .nho p{margin:0}
.sach ul.check{list-style:none;padding:0}
.sach ul.check li{padding-left:34px;position:relative;margin-bottom:10px;cursor:pointer}
.sach ul.check li::before{content:"";position:absolute;left:0;top:5px;width:20px;height:20px;border:2px solid var(--brand);border-radius:5px}
.sach ul.check li.on::before{content:"✓";color:#fff;background:var(--ok);border-color:var(--ok);font:800 15px/20px var(--ui);text-align:center}
.sach ol.buoc li{margin-bottom:8px}
.sach .goi{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:4px 14px}
.sach .gia-dinh{border:2px dashed var(--muted);border-radius:10px;padding:12px 14px;margin:1em 0}
.sach .sap{background:var(--no-bg);border-left:5px solid var(--no);padding:10px 14px;border-radius:0 10px 10px 0;margin:1em 0}
.sach .nhan{font:700 12px var(--ui);background:var(--no);color:#fff;padding:1px 6px;border-radius:4px;white-space:nowrap}
html[data-theme="dark"] .sach .nhan{color:#12161c}
.sach ol.nguon{font-size:.85rem;color:var(--muted)}
.sach table{display:block;overflow-x:auto}
.sach-web{margin:22px 0 4px;display:flex;flex-wrap:wrap;gap:8px}
.sach-sos{list-style:none;padding:0}
.sach-sos li{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:10px 14px;margin:8px 0;font-family:var(--ui)}
.sach-sos a{font-size:1.3rem;font-weight:800;color:var(--no);text-decoration:none}
"""

PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8">{head}
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title} – Quyền Làm Việc</title>
<link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="../app/app.css"><link rel="stylesheet" href="sach.css">
</head><body data-page="sach/{name}.html" data-root="../">
<main id="main"><div class="wrap sach" lang="vi">
{body}
</div></main>
<script src="../app/index.js"></script><script src="../app/app.js"></script>
<script>document.querySelectorAll('.sach-tabs button').forEach(function(b){{b.onclick=function(){{
document.querySelectorAll('.sach-tabs button').forEach(function(x){{x.setAttribute('aria-selected',x===b)}});
document.querySelectorAll('.sach-l').forEach(function(l){{l.hidden=l.id!==b.dataset.t}});}}}});
document.querySelectorAll('.sach ul.check li').forEach(function(li){{li.onclick=function(){{li.classList.toggle('on')}}}});</script>
</body></html>
"""


def text_of(h):
    return H.unescape(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", h))).strip()


def build(src: Path, www: Path, head_js: str):
    m = json.loads((src / "manifest.json").read_text(encoding="utf-8"))
    out = www / "sach"
    (out / "img").mkdir(parents=True, exist_ok=True)
    (out / "sach.css").write_text(CSS, encoding="utf-8")

    nums = {k["so"] for k in m.get("khan_cap", [])}

    def tel(h):  # số đã xác minh (danh sách khẩn cấp của sách) → bấm gọi được
        def rep(mm):
            n = mm.group(2)
            return f'<{mm.group(1)}><a href="tel:{n.replace("-", "")}">{n}</a></{mm.group(1)}>' if n in nums else mm.group(0)
        return re.sub(r"<(strong|b)>([0-9][0-9-]{2,13})</\1>", rep, h)

    def web_to_app(h):  # link về trang web → bài tương ứng trong app (đọc offline)
        return re.sub(r'href="https://trachnhiemxahoi\.com/((?:bai|en/articles)/[^/"]+)/"', r'href="../\1/index.html"', h)

    chapters, search = [], []
    for c in m["chuong"]:
        d = json.loads((src / c["file"]).read_text(encoding="utf-8"))
        n = d["so"]
        name = f"ch{n:02d}"
        img = ""
        if d.get("tranh") and (src / d["tranh"]).exists():
            im = Image.open(src / d["tranh"]).convert("RGB")
            im.thumbnail((720, 1066))
            im.save(out / "img" / f"{name}.webp", "WEBP", quality=74, method=6)
            img = (f'<figure class="sach-fig"><img src="img/{name}.webp" width="{im.width}" height="{im.height}" alt="" loading="lazy">'
                   f'<figcaption>{E(d.get("tranh_chu_thich", ""))}<br><em>{E(d.get("tranh_nhan_ai", ""))}</em></figcaption></figure>')
        review = bool(d.get("can_chuyen_gia_duyet"))
        l1, l2 = tel(web_to_app(d["lop1_html"])), tel(web_to_app(d["lop2_html"]))
        app_bai = f'../bai/{d["slug"]}/index.html' if (www / "bai" / d["slug"] / "index.html").exists() else ""
        body = (f'<header class="sach-hd" style="background:{E(d["mau"])}"><small>{E(d["phan"])} · Chương {n}</small>'
                f'<h1>{E(d["tieu_de"])}</h1><p>{E(d.get("phu_de", ""))}</p></header>'
                f'<p class="sach-meta"><b>Dành cho:</b> {E(d.get("danh_cho", ""))}<br><b>Đọc xong:</b> {E(d.get("muc_tieu", ""))}'
                f'<br><b>Đúng đến ngày:</b> {E(d.get("dung_den", ""))}</p>{img}'
                '<div class="sach-tabs" role="tablist"><button type="button" role="tab" data-t="l1" aria-selected="true">Đọc nhanh</button>'
                '<button type="button" role="tab" data-t="l2" aria-selected="false">Cho người hỗ trợ</button></div>'
                f'<section class="sach-l" id="l1">{l1}</section><section class="sach-l" id="l2" hidden>{l2}</section>'
                '<div class="sach-web ab-ui">'
                + (f'<a class="ab-b" href="{app_bai}">Đọc bài cùng chủ đề trong app</a>' if app_bai else "")
                + f'<a class="ab-b" href="{E(d["url"])}">Xem bản mới nhất trên web ↗</a></div>'
                f'<p class="small muted">{E(m.get("mien_tru", ""))}</p>')
        (out / f"{name}.html").write_text(PAGE.format(head=head_js, title=E(d["tieu_de"]), name=name, body=body), encoding="utf-8")
        u = f"sach/{name}.html"
        chapters.append({"u": u, "n": n, "t": d["tieu_de"], "review": review})
        search.append({"u": u, "l": "vi", "t": f'Sách – Chương {n}. {d["tieu_de"]}',
                       "x": text_of(" ".join(d.get("ba_dieu_can_nho", [])) + " " + d["lop1_html"] + " " + d["lop2_html"])[:6000]})

    # Giới thiệu sách
    intro = (f'<header class="sach-hd" style="background:#1d3f6e"><small>Sách</small><h1>{E(m["ten_sach"])}</h1><p>{E(m.get("phu_de", ""))}</p></header>'
             f'<p class="sach-meta"><b>Tác giả:</b> {E(m.get("tac_gia", ""))}<br><b>Phiên bản:</b> {E(m.get("phien_ban", ""))}'
             f'<br><b>Đúng đến ngày:</b> {E(m.get("dung_den", ""))}</p>'
             f'<p>{E(m.get("mien_tru", ""))}</p><p class="note">{E(m.get("cong_khai_ai", ""))}</p>'
             f'<p>Giấy phép: <a href="{E(m.get("giay_phep_url", ""))}">{E(m.get("giay_phep", ""))}</a>. Văn bản pháp luật trích dẫn không thuộc đối tượng bảo hộ quyền tác giả.</p>'
             f'<p>Bản mới nhất của từng chủ đề: <a href="https://{E(m.get("website", ""))}">{E(m.get("website", ""))}</a></p>')
    (out / "gioi-thieu.html").write_text(PAGE.format(head=head_js, title="Giới thiệu sách", name="gioi-thieu", body=intro), encoding="utf-8")

    # Cần giúp ngay
    flags = {"VN": "Việt Nam", "TW": "Đài Loan", "JP": "Nhật Bản", "KR": "Hàn Quốc"}
    sos = ('<h1>Cần giúp ngay</h1><p>Bấm vào số để gọi. Chỉ ghi các số đã kiểm tra nguồn.</p><ul class="sach-sos">'
           + "".join(f'<li><a href="tel:{E(k["so"].replace("-", ""))}">{E(k["so"])}</a> · <b>{E(k["ten"])}</b>'
                     f' <span class="tag">{E(flags.get(k.get("nuoc", ""), k.get("nuoc", "")))}</span><br><span class="muted">{E(k.get("khi", ""))}</span></li>'
                     for k in m.get("khan_cap", []))
           + '</ul><p><a class="ab-b" href="../danh-ba/index.html">Danh bạ đầy đủ</a></p>')
    (out / "can-giup-ngay.html").write_text(PAGE.format(head=head_js, title="Cần giúp ngay", name="can-giup-ngay", body=sos), encoding="utf-8")

    by_n = {c["n"]: i for i, c in enumerate(chapters)}
    parts = [{"t": p["ten"], "c": p.get("mau"), "ch": [by_n[x] for x in p["chuong"] if x in by_n]} for p in m["phan"]]
    return {"title": m["ten_sach"], "author": m.get("tac_gia", ""), "checked": m.get("dung_den", ""),
            "parts": parts, "chapters": chapters,
            "front": [{"u": "sach/gioi-thieu.html", "t": "Giới thiệu sách"}, {"u": "sach/can-giup-ngay.html", "t": "Cần giúp ngay – số điện thoại"}],
            "back": [], "search": search}
