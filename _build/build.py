#!/usr/bin/env python3
"""Bộ sinh trang tĩnh cho trachnhiemxahoi.com.

Nội dung:
  data/groups.yaml       Trục 1 – "Tôi là ai" (nhóm người đọc)
  data/situations.yaml   Trục 2 – "Tôi đang gặp chuyện gì"
  data/danhba.yaml       Trục 3 – "Gọi ai ngay" (danh bạ đã đối chiếu)
  content/bai/*.md       bài viết: YAML front matter + Markdown
                         status: published | draft  (draft KHÔNG được đưa ra public/)

Chạy:
  python3 _build/build.py            -> public/
  python3 _build/build.py --preview  -> preview/ (có cả bài nháp, mở file trực tiếp)
"""
import html, re, shutil, sys, datetime
from pathlib import Path
import markdown, yaml

ROOT = Path(__file__).resolve().parent.parent
PREVIEW = "--preview" in sys.argv
OUT = ROOT / ("preview" if PREVIEW else "public")
SITE = "https://trachnhiemxahoi.com"
NAME = "Trách Nhiệm Xã Hội"
TAGLINE = "Biết luật, biết nơi nhờ giúp – cho người lao động"
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)


def y(p):
    return yaml.safe_load((ROOT / p).read_text(encoding="utf-8"))


GROUPS = y("data/groups.yaml")["groups"]
GROUP = {g["code"]: g for g in GROUPS}
SITU = y("data/situations.yaml")["situations"]
DIR = y("data/danhba.yaml")


def md(t):
    return markdown.markdown(t, extensions=["tables", "md_in_html", "attr_list", "sane_lists"])


def load():
    out = []
    files = sorted((ROOT / "content/bai").glob("*.md"))
    if PREVIEW:  # bài nháp nhạy cảm nằm ở content/nhap/ (không đưa lên GitHub)
        files += sorted((ROOT / "content/nhap").glob("*.md"))
    for f in files:
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S)
        meta = yaml.safe_load(m.group(1))
        meta["body"] = m.group(2)
        if meta.get("status") == "published" or PREVIEW:
            out.append(meta)
    return sorted(out, key=lambda a: a.get("order", 99))


ARTS = load()
ART = {a["slug"]: a for a in ARTS}

NAV = [("nhom/", "Tôi là ai"), ("tinh-huong/", "Tôi gặp chuyện gì"), ("danh-ba/", "Gọi ai"),
       ("bai/", "Tất cả bài"), ("gioi-thieu/", "Giới thiệu")]


def page(path, title, body, desc=""):
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    r = "/" if path == "404.html" and not PREVIEW else "../" * depth
    idx = "index.html" if PREVIEW else ""
    body = body.replace("{{R}}", r).replace("{{I}}", idx)
    nav = "".join(f'<a href="{r}{h}{idx}"{" aria-current=page" if path.startswith(h) else ""}>{l}</a>' for h, l in NAV)
    full = f"{title} – {NAME}" if path else f"{NAME} – {TAGLINE}"
    canon = f"{SITE}/{path}" if path != "404.html" else SITE + "/"
    doc = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc or TAGLINE)}">
<link rel="canonical" href="{canon}">
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{r}assets/style.css">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc or TAGLINE)}">
</head><body>
<a class="skip" href="#main">Bỏ qua, tới nội dung</a>
<div class="sos"><div class="wrap"><span>Nguy hiểm ngay? Gọi <a href="tel:113">113</a> công an · <a href="tel:115">115</a> cấp cứu · <a href="tel:111">111</a> trẻ em, mua bán người</span><a href="{r}danh-ba/{idx}">Danh bạ hỗ trợ →</a></div></div>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{r}{idx}"><img class="logo" src="{r}assets/logo.svg" alt="" width="38" height="38"><span>{NAME}<small>{TAGLINE}</small></span></a>
<nav class="nav" aria-label="Chính">{nav}</nav></div></header>
<main id="main"><div class="wrap">{body}</div></main>
<footer><div class="wrap">
<p><b>{NAME}</b> – trang tự học miễn phí, phi lợi nhuận, không đăng nhập, không quảng cáo, không theo dõi. Người biên soạn: Liêm.</p>
<p>Thông tin trên trang để <b>tham khảo</b>, không thay thế tư vấn pháp lý cho từng vụ việc. Luật thay đổi thường xuyên: mỗi bài ghi rõ “đúng đến ngày”. Với vụ việc cụ thể, hãy liên hệ <a href="{r}danh-ba/{idx}">Trung tâm Trợ giúp pháp lý nhà nước</a>.</p>
<p>Học thêm miễn phí: <a href="https://kynanglamviec.com">Kỹ Năng Làm Việc</a> · <a href="https://tienganhcanban.com">Tiếng Anh Căn Bản</a> · <a href="https://daynentang.com">Dạy Nền Tảng</a> · <a href="https://tamhonkhoe.com">Tâm Hồn Khỏe</a></p>
<p>Nội dung tự viết: <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.vi">CC BY-NC-SA 4.0</a>. Văn bản pháp luật trích dẫn không thuộc đối tượng bảo hộ quyền tác giả.</p>
</div></footer></body></html>"""
    dest = OUT / (path if path.endswith(".html") else path + "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")


def link(slug):
    return f"{{{{R}}}}bai/{slug}/{{{{I}}}}"


def card(a):
    t = '<span class="tag chk">Nháp – chưa đăng</span>' if a.get("status") != "published" else ""
    return f'<li><a class="card" href="{link(a["slug"])}"><b>{e(a["title"])}</b>{t}<span class="muted small">{e(a["short"])}</span></a></li>'


def group_card(g):
    n = sum(1 for a in ARTS if g["code"] in a.get("groups", []))
    if g["status"] == "active":
        return f'<li><a class="card" href="{{{{R}}}}nhom/{g["code"]}/{{{{I}}}}"><b>{e(g["name"])}</b><span class="muted small">{e(g["short"])}</span><br><span class="tag ok">{n} bài</span></a></li>'
    return f'<li><div class="card soon"><b>{e(g["name"])}</b><br><span class="muted small">{e(g["short"])}</span><br><span class="tag">Sắp có</span></div></li>'


def visible_groups():
    return [g for g in GROUPS if g["status"] != "hidden"]


# ------------------------------------------------------------------ trang
def home():
    sit = "".join(f'<li><a href="{link(s["to"]) if s["to"] != "danh-ba" else "{{R}}danh-ba/{{I}}"}">{e(s["q"])}</a></li>' for s in SITU[:8])
    groups = "".join(group_card(g) for g in visible_groups())
    body = f"""<section class="hero">
<h1>Biết luật để tự bảo vệ mình</h1>
<p class="lead">Trang này viết cho người làm việc nặng nhọc, độc hại, nguy hiểm, cho công nhân và người Việt đi làm ở nước ngoài.
Bạn sẽ biết luật nói gì, cần làm gì từng bước, và gọi ai khi cần giúp. Hoàn toàn miễn phí.</p>
<p><a class="btn alt" href="{{{{R}}}}tinh-huong/{{{{I}}}}">Tôi đang gặp chuyện</a><a class="btn" href="{{{{R}}}}danh-ba/{{{{I}}}}">Gọi ai bây giờ?</a></p>
</section>
<h2>Bạn đang gặp chuyện gì?</h2>
<ul>{sit}</ul>
<p><a href="{{{{R}}}}tinh-huong/{{{{I}}}}">Xem tất cả tình huống →</a></p>
<h2>Bạn là ai?</h2>
<ul class="cards grid">{groups}</ul>
<h2>Cách đọc một bài</h2>
<p>Bài nào cũng đi theo cùng một thứ tự, để bạn đọc nhanh trên điện thoại:</p>
<ol><li><b>Tóm tắt 3 dòng</b> – điều quan trọng nhất.</li><li><b>Luật nói gì</b> – trích đúng điều, khoản, số hiệu văn bản.</li>
<li><b>Bạn làm gì</b> – từng bước cụ thể.</li><li><b>Gọi ai</b> – nơi hỗ trợ đã kiểm tra.</li><li><b>Đúng đến ngày</b> và <b>Sắp thay đổi</b>.</li></ol>
<p class="note">Nhãn <span class="tag ok">Đã đối chiếu</span> nghĩa là thông tin đã kiểm tra với văn bản gốc hoặc trang của cơ quan nhà nước.
Nhãn <span class="tag chk">Đang đối chiếu</span> nghĩa là mới thấy ở nguồn thứ cấp – bạn nên hỏi lại trước khi dựa vào.</p>"""
    page("", NAME, body)


def groups_index():
    body = "<h1>Tôi là ai?</h1><p class=lead>Chọn nhóm gần với bạn nhất. Hai nhóm đầu đã có bài; các nhóm khác đang được biên soạn.</p>"
    body += f'<ul class="cards grid">{"".join(group_card(g) for g in visible_groups())}</ul>'
    page("nhom/", "Tôi là ai", body)
    for g in GROUPS:
        if g["status"] != "active":
            continue
        arts = [a for a in ARTS if g["code"] in a.get("groups", [])]
        b = f'<p class="crumb"><a href="{{{{R}}}}nhom/{{{{I}}}}">Tôi là ai</a> ›</p><h1>{e(g["name"])}</h1><p class=lead>{e(g["short"])}</p>'
        b += f'<ul class="cards">{"".join(card(a) for a in arts)}</ul>'
        b += '<p class="note">Cần giúp ngay? Xem <a href="{{R}}danh-ba/{{I}}">danh bạ hỗ trợ</a>.</p>'
        page(f"nhom/{g['code']}/", g["name"], b, g["short"])


def situations():
    rows = "".join(f'<li><a class="card" href="{link(s["to"]) if s["to"] != "danh-ba" else "{{R}}danh-ba/{{I}}"}"><b>{e(s["q"])}</b></a></li>' for s in SITU)
    page("tinh-huong/", "Tôi đang gặp chuyện gì", f"<h1>Bạn đang gặp chuyện gì?</h1><p class=lead>Chọn tình huống gần nhất. Mỗi mục dẫn tới bài có luật, các bước làm và nơi hỗ trợ.</p><ul class='cards'>{rows}</ul>")


def directory():
    b = ['<h1>Gọi ai bây giờ?</h1><p class=lead>Danh bạ chỉ ghi những số đã kiểm tra nguồn. Số nào chưa kiểm tra được thì chưa đăng.</p>',
         f'<p class="meta">Tra cứu gần nhất: 18/11/2026.</p>']
    for s in DIR["sections"]:
        b.append(f"<h2>{e(s['title'])}</h2><div class='dir'>")
        for it in s["items"]:
            tag = '<span class="tag ok">Đã đối chiếu</span>' if it["status"] == "ok" else '<span class="tag chk">Đang đối chiếu</span>'
            ph = f'<p><a class="phone" href="tel:{it["phone"].replace("-", "")}">{e(it["phone"])}</a></p>' if it["phone"] else ""
            b.append(f'<div class="card"><h3>{e(it["name"])}</h3>{tag}{ph}<p>{e(it["what"])}</p><p class="small muted">{e(it["note"])} <a href="{e(it["src"])}" rel="noopener">Nguồn</a></p></div>')
        b.append("</div>")
    b.append("<h2>Đang kiểm tra, sẽ bổ sung</h2><ul>" + "".join(f"<li>{e(p)}</li>" for p in DIR["pending"]) + "</ul>")
    b.append('<p class="note">Bạn biết một số điện thoại hỗ trợ đang hoạt động tốt? Ghi lại tên, số, nơi bạn thấy số đó – trang sẽ kiểm tra trước khi đăng.</p>')
    page("danh-ba/", "Danh bạ hỗ trợ", "".join(b), "Số điện thoại hỗ trợ người lao động ở Việt Nam, Nhật Bản, Đài Loan, Hàn Quốc – đã kiểm tra nguồn.")


def articles():
    page("bai/", "Tất cả bài", f"<h1>Tất cả bài</h1><ul class='cards'>{''.join(card(a) for a in ARTS)}</ul>")
    for i, a in enumerate(ARTS):
        g = " · ".join(f'<a href="{{{{R}}}}nhom/{c}/{{{{I}}}}">{e(GROUP[c]["name"])}</a>' for c in a.get("groups", []) if GROUP[c]["status"] == "active")
        srcs = "".join(f'<li>{e(s["t"])}' + (f' – <a href="{e(s["u"])}" rel="noopener">mở</a>' if s.get("u") else "") + "</li>" for s in a.get("sources", []))
        draft = '<p class="danger"><b>BẢN NHÁP – chưa đăng công khai.</b> Bài có chủ đề nhạy cảm, chờ người biên soạn duyệt.</p>' if a.get("status") != "published" else ""
        prev = ARTS[i - 1] if i > 0 else None
        nxt = ARTS[i + 1] if i + 1 < len(ARTS) else None
        pn = '<div class="pn">' + (f'<a href="{link(prev["slug"])}">← {e(prev["title"])}</a>' if prev else "<span></span>") + (f'<a href="{link(nxt["slug"])}">{e(nxt["title"])} →</a>' if nxt else "") + "</div>"
        body = f"""<p class="crumb"><a href="{{{{R}}}}bai/{{{{I}}}}">Bài</a> › {g}</p>{draft}
<h1>{e(a["title"])}</h1>
<p class="meta">Đúng đến ngày {e(a["checked"])} · Biên soạn: Liêm</p>
<div class="sum"><b>Tóm tắt</b><ul>{"".join(f"<li>{e(x)}</li>" for x in a["summary"])}</ul></div>
{md(a["body"])}
{f'<div class="change"><b>Sắp thay đổi</b>{md(a["upcoming"])}</div>' if a.get("upcoming") else ""}
<h2>Nguồn</h2><ul class="src">{srcs}</ul>
<p class="small muted">Thấy thông tin sai hoặc đã cũ? Hãy báo cho người biên soạn để sửa. Bài này không thay thế tư vấn pháp lý cho từng vụ việc.</p>
{pn}"""
        page(f"bai/{a['slug']}/", a["title"], body, a["short"])


def about():
    b = """<h1>Giới thiệu</h1>
<p class=lead><b>Trách Nhiệm Xã Hội</b> là trang tự học miễn phí, giúp người lao động biết luật để tự bảo vệ mình, biết nơi nhờ giúp, và có thêm kỹ năng tổ chức cuộc sống.</p>
<h2>Viết cho ai</h2>
<p>Giai đoạn đầu: công nhân, người làm nghề nặng nhọc, độc hại, nguy hiểm, và người Việt đi làm việc ở nước ngoài.
Sau đó: nông dân, lao động tự do, và những người dễ bị tổn thương khác – trẻ em phải đi làm, người bị lừa bán, phụ nữ bị bạo hành, người khuyết tật, người có vấn đề sức khỏe tâm thần, trẻ không nơi nương tựa.</p>
<h2>Nguyên tắc biên soạn</h2>
<ul><li>Chỉ dùng nguồn gốc: văn bản pháp luật chính thức, trang của cơ quan nhà nước, ILO, IOM, tiêu chuẩn gốc, nghiên cứu có bình duyệt.</li>
<li>Mỗi điều luật ghi số hiệu văn bản, số điều, và ngày tra cứu.</li>
<li>Không chắc thì ghi rõ “đang đối chiếu”. Số điện thoại chưa kiểm tra thì không đăng.</li>
<li>Viết trung lập: trình bày luật và cách làm, không bình luận chính trị.</li>
<li>Không thu thập dữ liệu người đọc: không đăng nhập, không cookie, không công cụ theo dõi.</li></ul>
<h2>Người biên soạn</h2>
<p>Liêm – đánh giá viên trách nhiệm xã hội và an toàn, sức khỏe nghề nghiệp nhiều năm làm việc tại nhà máy ở Việt Nam và khu vực. Các tình huống trong bài được viết chung, không nêu tên doanh nghiệp hay người lao động nào.</p>
<h2>Các trang học miễn phí khác của Liêm</h2>
<ul><li><a href="https://kynanglamviec.com">Kỹ Năng Làm Việc</a> – kỹ năng đi làm, từ người mới tới quản lý.</li>
<li><a href="https://tienganhcanban.com">Tiếng Anh Căn Bản</a> – tự học tiếng Anh.</li>
<li><a href="https://daynentang.com">Dạy Nền Tảng</a> – nền tảng học tập cho mọi lứa tuổi.</li>
<li><a href="https://tamhonkhoe.com">Tâm Hồn Khỏe</a> – chăm sóc tinh thần.</li></ul>"""
    page("gioi-thieu/", "Giới thiệu", b)


def extras():
    page("404.html", "Không tìm thấy trang", '<h1>Không tìm thấy trang</h1><p>Trang bạn tìm không có. Về <a href="{{R}}{{I}}">trang chủ</a> hoặc xem <a href="{{R}}danh-ba/{{I}}">danh bạ hỗ trợ</a>.</p>')
    urls = ["", "nhom/", "tinh-huong/", "danh-ba/", "bai/", "gioi-thieu/"] + [f"nhom/{g['code']}/" for g in GROUPS if g["status"] == "active"] + [f"bai/{a['slug']}/" for a in ARTS]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "_build/static", OUT)
    for f in (home, groups_index, situations, directory, articles, about, extras):
        f()
    leaked = [a["slug"] for a in ARTS if a.get("status") != "published"] if not PREVIEW else []
    assert not leaked, f"Bài nháp lọt ra public: {leaked}"
    print(f"OK -> {OUT.name}/ : {len(ARTS)} bài")


main()
