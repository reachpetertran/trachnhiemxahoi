#!/usr/bin/env python3
"""Sinh app/www/ từ public/ của website trachnhiemxahoi.com.

- Chép mọi trang, tài nguyên (bỏ sitemap, robots, _headers, 404).
- Đổi link thư mục `a/b/` thành `a/b/index.html` để chạy được khi mất mạng.
- Bỏ canonical, hreflang, og:*; bỏ thanh SOS, header, menu của web; chèn khung app.
- Chèn script nhỏ trong <head> áp cỡ chữ, nền đã lưu (tránh nháy màn hình).
- Sinh www/app/index.js: khung chương trình (Phần → bài), cặp VI/EN, chỉ mục tìm kiếm.
- Nếu có app/sach-data/ (dữ liệu sách, KHÔNG đưa lên GitHub) thì sinh trang sách www/sach/.

Chạy:  python3 app/build_www.py
"""
import html as H
import json
import re
import shutil
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "public"
APP = ROOT / "app"
WWW = APP / "www"
SHELL = APP / "shell"
BOOK = APP / "sach-data"          # out/app/ của sách – .gitignore
SKIP = {"sitemap.xml", "robots.txt", "_headers", "404.html"}


def front(p):
    t = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


# ---------- 1. Dữ liệu bài, khung chương trình ----------
vi = {}
for p in sorted((ROOT / "content/bai").glob("*.md")):
    f = front(p)
    if f.get("status") == "published":
        vi[f["slug"]] = f
en_by_pair = {}
for p in sorted((ROOT / "content/en").glob("*.md")):
    f = front(p)
    if f.get("status") == "published" and f.get("pair"):
        en_by_pair[f["pair"]] = f

cur = yaml.safe_load((ROOT / "data/curriculum.yaml").read_text(encoding="utf-8"))
modules = []
for i, m in enumerate(cur["modules"], 1):
    lessons = []
    for l in m.get("lessons", []):
        s = l.get("slug")
        if not s or s not in vi:
            continue                     # bài "Sắp có" không vào app
        e = en_by_pair.get(s)
        lessons.append({
            "vi": f"bai/{s}/index.html", "t": vi[s]["title"],
            "en": f"en/articles/{e['slug']}/index.html" if e else None,
            "t_en": e["title"] if e else None,
        })
    modules.append({"id": f"p{i}", "t": m["title"], "t_en": m.get("title_en", m["title"]),
                    "lessons": lessons})


# ---------- 2. Chép public/ ----------
if WWW.exists():
    shutil.rmtree(WWW)
shutil.copytree(PUB, WWW, ignore=lambda d, names: [n for n in names if n in SKIP])
(WWW / "app").mkdir(exist_ok=True)
for f in SHELL.iterdir():
    shutil.copy(f, WWW / "app" / f.name)

HEAD_JS = ("<script>try{var s=JSON.parse(localStorage.getItem('tnxh.v1')||'{}').set||{};"
           "var d=document.documentElement;d.dataset.fs=s.fs||'2';"
           "var t=s.theme||'auto';if(t==='auto')t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';"
           "d.dataset.theme=t;}catch(e){}</script>")


def fix_href(h):
    """Link nội bộ tương đối: thư mục → index.html."""
    if re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:)", h):
        return h
    path, _, frag = h.partition("#")
    if path == "" and frag:
        return h
    if path == "" or path.endswith("/") or path in (".", ".."):
        path = (path.rstrip("/") + "/" if path not in ("",) else "") + "index.html"
        path = path.replace("./index.html", "index.html")
    return path + ("#" + frag if frag else "")


def rel_prefix(p):
    depth = len(p.relative_to(WWW).parts) - 1
    return "../" * depth


search = []
pages = sorted(WWW.rglob("*.html"))
for p in pages:
    rel = p.relative_to(WWW).as_posix()
    if rel.startswith("app/"):
        continue
    s = p.read_text(encoding="utf-8")
    lang = "en" if rel.startswith("en/") else "vi"
    pre = rel_prefix(p)

    # cặp ngôn ngữ (từ nút .lang của web, trước khi bỏ header)
    m = re.search(r'<a class="lang" href="([^"]*)"', s)
    alt = fix_href(m.group(1)) if m else ""

    s = re.sub(r'<link rel="canonical"[^>]*>', "", s)
    s = re.sub(r'<link rel="alternate"[^>]*>', "", s)
    s = re.sub(r'<meta property="og:[^>]*>\n?', "", s)
    s = re.sub(r'<a class="skip"[^>]*>.*?</a>\n?', "", s)
    s = re.sub(r'<div class="sos">.*?</div></div>\n?', "", s, flags=re.S)
    s = re.sub(r'<header class="top">.*?</header>\n?', "", s, flags=re.S)
    # footer: bỏ dòng liên kết các trang khác (mở web, không cần trong app) – giữ lời miễn trừ, giấy phép
    s = re.sub(r"<p>(Học thêm miễn phí|Learn more for free|More free learning)[^\n]*</p>\n?", "", s)

    s = re.sub(r'href="([^"]*)"', lambda mm: f'href="{fix_href(mm.group(1))}"', s)
    s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + HEAD_JS, 1)
    s = s.replace('content="width=device-width,initial-scale=1"', 'content="width=device-width,initial-scale=1,viewport-fit=cover"')
    s = s.replace('<link rel="stylesheet" href="' + pre + 'assets/style.css">',
                  f'<link rel="stylesheet" href="{pre}assets/style.css">'
                  f'<link rel="stylesheet" href="{pre}app/app.css">')
    s = s.replace("<body>", f'<body data-lang="{lang}" data-page="{rel}" data-alt="{alt}" data-root="{pre}">', 1)
    s = s.replace("</body>", f'<script src="{pre}app/index.js"></script><script src="{pre}app/app.js"></script></body>')
    p.write_text(s, encoding="utf-8")

    # chỉ mục tìm kiếm
    if not re.match(r"^(bai/[^/]+/|en/articles/[^/]+/|danh-ba/|en/contacts/|gioi-thieu/|en/about/)index\.html$", rel) or rel in ("bai/index.html",):
        continue
    main = re.search(r"<main[^>]*>(.*?)</main>", s, re.S)
    body = main.group(1) if main else ""
    body = re.sub(r'<p class="(crumb|meta)">.*?</p>', "", body, flags=re.S)
    body = re.sub(r'<div class="pn">.*?</div>', "", body, flags=re.S)
    title = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S)
    title = re.sub("<[^>]+>", "", title.group(1)) if title else rel
    text = H.unescape(re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", body))).strip()
    search.append({"u": rel, "l": lang, "t": H.unescape(title), "x": text[:6000]})


# ---------- 3. Trang riêng của app: Của tôi, Tìm, Sách ----------
APP_PAGE = """<!doctype html>
<html lang="vi"><head><meta charset="utf-8">{head}
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Trách Nhiệm Xã Hội</title>
<link rel="stylesheet" href="../assets/style.css"><link rel="stylesheet" href="app.css">
</head><body data-page="app/{name}.html" data-root="../">
<main id="main"><div class="wrap"></div></main>
<script src="index.js"></script><script src="app.js"></script></body></html>
"""
for name in ("toi", "tim", "sach"):
    (WWW / f"app/{name}.html").write_text(APP_PAGE.format(head=HEAD_JS, name=name), encoding="utf-8")

# ---------- 4. Sách (nếu có dữ liệu) ----------
book = None
if (BOOK / "manifest.json").exists():
    import build_book                                   # app/build_book.py
    book = build_book.build(BOOK, WWW, HEAD_JS)
    search.extend(book.pop("search", []))

idx = {"modules": modules, "search": search, "book": book}
(WWW / "app/index.js").write_text(
    "window.TNXH=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";",
    encoding="utf-8")

n_less = sum(len(m["lessons"]) for m in modules)
print(f"www/: {len(pages)} trang web, {len(modules)} phần, {n_less} bài, sách: {'có' if book else 'chưa có'}")
