#!/usr/bin/env python3
"""Bộ sinh trang tĩnh song ngữ cho trachnhiemxahoi.com.

Nội dung:
  data/groups.yaml       Trục 1 – Tôi là ai (name/short + name_en/short_en)
  data/situations.yaml   Trục 2 – Tôi gặp chuyện gì (q + q_en, to = slug bài tiếng Việt hoặc "danh-ba")
  data/danhba.yaml       Trục 3 – Gọi ai (các trường *_en cho bản tiếng Anh)
  content/bai/*.md       bài tiếng Việt (status: published)
  content/en/*.md        bài tiếng Anh (pair: slug bài tiếng Việt tương ứng)
  content/nhap/          bài nháp nhạy cảm – KHÔNG đưa lên GitHub, chỉ build khi --preview

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
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s), quote=True)


def y(p):
    return yaml.safe_load((ROOT / p).read_text(encoding="utf-8"))


GROUPS = y("data/groups.yaml")["groups"]
SITU = y("data/situations.yaml")["situations"]
DIR = y("data/danhba.yaml")
CUR = y("data/curriculum.yaml")


def md(t):
    return markdown.markdown(t, extensions=["tables", "md_in_html", "attr_list", "sane_lists"])


def load(folder, drafts=None):
    files = sorted((ROOT / folder).glob("*.md"))
    if PREVIEW and drafts:
        files += sorted((ROOT / drafts).glob("*.md"))
    out = []
    for f in files:
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", f.read_text(encoding="utf-8"), re.S)
        meta = yaml.safe_load(m.group(1))
        meta["body"] = m.group(2)
        if meta.get("status") == "published" or PREVIEW:
            out.append(meta)
    return sorted(out, key=lambda a: a.get("order", 99))


# ------------------------------------------------------------------ ngôn ngữ
LANGS = {
    "vi": dict(
        code="vi", pre="", name="Trách Nhiệm Xã Hội", tag="Biết luật, biết nơi nhờ giúp – cho người lao động",
        p=dict(groups="nhom/", sit="tinh-huong/", dir="danh-ba/", arts="bai/", cur="khung-chuong-trinh/", about="gioi-thieu/"),
        nav=["Tôi là ai", "Tôi gặp chuyện gì", "Gọi ai", "Tất cả bài", "Khung chương trình", "Giới thiệu"],
        sos='Nguy hiểm ngay? Gọi <a href="tel:113">113</a> công an · <a href="tel:115">115</a> cấp cứu · <a href="tel:111">111</a> trẻ em, mua bán người',
        sos_link="Danh bạ hỗ trợ →", switch="English", skip="Bỏ qua, tới nội dung",
        foot1="– trang tự học miễn phí, phi lợi nhuận, không đăng nhập, không quảng cáo, không theo dõi. Người biên soạn: Liêm.",
        foot2='Thông tin trên trang để <b>tham khảo</b>, không thay thế tư vấn pháp lý cho từng vụ việc. Luật thay đổi thường xuyên: mỗi bài ghi rõ “đúng đến ngày”. Với vụ việc cụ thể, hãy liên hệ <a href="{dir}">Trung tâm Trợ giúp pháp lý nhà nước</a>.',
        foot3="Học thêm miễn phí:", foot4="Nội dung tự viết:", foot5="Văn bản pháp luật trích dẫn không thuộc đối tượng bảo hộ quyền tác giả.",
        lic="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.vi",
        n_arts="bài", soon="Sắp có", draft="Nháp – chưa đăng", checked="Đúng đến ngày", by="Biên soạn: Liêm",
        summary="Tóm tắt", upcoming="Sắp thay đổi", sources="Nguồn", open="mở",
        report="Thấy thông tin sai hoặc đã cũ? Hãy báo cho người biên soạn để sửa. Bài này không thay thế tư vấn pháp lý cho từng vụ việc.",
        crumb_arts="Bài", crumb_groups="Tôi là ai", need_help='Cần giúp ngay? Xem <a href="{dir}">danh bạ hỗ trợ</a>.',
        draft_box="<b>BẢN NHÁP – chưa đăng công khai.</b> Bài có chủ đề nhạy cảm, chờ người biên soạn duyệt.",
        ok="Đã đối chiếu", chk="Đang đối chiếu", src="Nguồn",
        t404="Không tìm thấy trang", m404='Trang bạn tìm không có. Về <a href="{home}">trang chủ</a> hoặc xem <a href="{dir}">danh bạ hỗ trợ</a>.',
    ),
    "en": dict(
        code="en", pre="en/", name="Trách Nhiệm Xã Hội", tag="Know the law, know where to get help – for workers",
        p=dict(groups="en/groups/", sit="en/situations/", dir="en/contacts/", arts="en/articles/", cur="en/curriculum/", about="en/about/"),
        nav=["Who I am", "What's happening", "Who to call", "All articles", "Curriculum", "About"],
        sos='In danger now? In Vietnam call <a href="tel:113">113</a> police · <a href="tel:115">115</a> ambulance · <a href="tel:111">111</a> children, trafficking',
        sos_link="Help contacts →", switch="Tiếng Việt", skip="Skip to content",
        foot1="– a free, non-profit self-study site. No login, no ads, no tracking. Compiled by Liêm.",
        foot2='This site is for <b>general information</b> and is not legal advice for any individual case. Laws change often: every article shows the date it was last checked. For a specific case, contact a <a href="{dir}">State Legal Aid Centre</a>.',
        foot3="Learn more for free:", foot4="Original content:", foot5="Quoted legal texts are not subject to copyright under Vietnamese law. English quotations of Vietnamese law are unofficial translations.",
        lic="https://creativecommons.org/licenses/by-nc-sa/4.0/",
        n_arts="articles", soon="Coming soon", draft="Draft – not published", checked="Checked on", by="Compiled by Liêm",
        summary="In short", upcoming="Coming changes", sources="Sources", open="open",
        report="Spotted something wrong or out of date? Please tell the editor. This article is not legal advice for any individual case.",
        crumb_arts="Articles", crumb_groups="Who I am", need_help='Need help now? See the <a href="{dir}">help contacts</a>.',
        draft_box="<b>DRAFT – not public.</b>",
        ok="Verified", chk="Being verified", src="Source",
        t404="Page not found", m404='This page does not exist. Go to the <a href="{home}">home page</a> or the <a href="{dir}">help contacts</a>.',
    ),
}
ART = {"vi": load("content/bai", "content/nhap"), "en": load("content/en")}
ART_BY = {k: {a["slug"]: a for a in v} for k, v in ART.items()}
EN_OF = {a["pair"]: a["slug"] for a in ART["en"] if a.get("pair")}
VI_OF = {v: k for k, v in EN_OF.items()}


def f(item, key, L):
    """Lấy trường theo ngôn ngữ: key_en cho tiếng Anh, có thì dùng."""
    return item.get(f"{key}_en", item.get(key)) if L["code"] == "en" else item.get(key)


def art_url(L, slug):
    return f'{{{{R}}}}{L["p"]["arts"]}{slug}/{{{{I}}}}'


def sit_target(L, s):
    if s["to"] == "danh-ba":
        return f'{{{{R}}}}{L["p"]["dir"]}{{{{I}}}}'
    slug = s["to"] if L["code"] == "vi" else EN_OF.get(s["to"])
    return art_url(L, slug) if slug else None


def page(L, path, title, body, alt, desc=""):
    depth = 0 if path in ("", "404.html") else path.strip("/").count("/") + 1
    r = "/" if path == "404.html" and not PREVIEW else "../" * depth
    idx = "index.html" if PREVIEW else ""
    nav = "".join(f'<a href="{r}{h}{idx}"{" aria-current=page" if path.startswith(h) and h else ""}>{l}</a>'
                  for h, l in zip(L["p"].values(), L["nav"]))
    home = r + L["pre"] + idx
    body = body.replace("{{R}}", r).replace("{{I}}", idx).replace("{dir}", r + L["p"]["dir"] + idx).replace("{home}", home)
    full = f"{title} – {L['name']}" if path not in ("", "en/") else f"{L['name']} – {L['tag']}"
    canon = f"{SITE}/{path}" if path != "404.html" else SITE + "/"
    other = "en" if L["code"] == "vi" else "vi"
    alt_html = f'<link rel="alternate" hreflang="{other}" href="{SITE}/{alt}">' if alt is not None else ""
    switch = f'<a class="lang" href="{r}{alt}{idx}" hreflang="{other}" lang="{other}">{L["switch"]}</a>' if alt is not None else ""
    lic = L["lic"]
    doc = f"""<!doctype html>
<html lang="{L['code']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(full)}</title>
<meta name="description" content="{e(desc or L['tag'])}">
<link rel="canonical" href="{canon}">{alt_html}
<link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{r}assets/apple-touch-icon.png">
<link rel="stylesheet" href="{r}assets/style.css">
<meta property="og:title" content="{e(full)}"><meta property="og:description" content="{e(desc or L['tag'])}">
<meta property="og:image" content="{SITE}/assets/logo-1024.png">
</head><body>
<a class="skip" href="#main">{L['skip']}</a>
<div class="sos"><div class="wrap"><span>{L['sos']}</span><a href="{r}{L['p']['dir']}{idx}">{L['sos_link']}</a></div></div>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{home}"><img class="logo" src="{r}assets/logo-icon.svg" alt="" width="40" height="40"><span>{L['name']}<small>{L['tag']}</small></span></a>
<nav class="nav" aria-label="Menu">{nav}</nav>{switch}</div></header>
<main id="main"><div class="wrap">{body}</div></main>
<footer><div class="wrap">
<p><b>{L['name']}</b> {L['foot1']}</p>
<p>{L['foot2'].replace('{dir}', r + L['p']['dir'] + idx)}</p>
<p>{L['foot3']} <a href="https://kynanglamviec.com">Kỹ Năng Làm Việc</a> · <a href="https://tienganhcanban.com">Tiếng Anh Căn Bản</a> · <a href="https://daynentang.com">Dạy Nền Tảng</a> · <a href="https://tamhonkhoe.com">Tâm Hồn Khỏe</a></p>
<p>{L['foot4']} <a href="{lic}">CC BY-NC-SA 4.0</a>. {L['foot5']}</p>
</div></footer></body></html>"""
    dest = OUT / (path if path.endswith(".html") else path + "index.html")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")


def card(L, a):
    t = f'<span class="tag chk">{L["draft"]}</span>' if a.get("status") != "published" else ""
    return f'<li><a class="card" href="{art_url(L, a["slug"])}"><b>{e(a["title"])}</b>{t}<span class="muted small">{e(a["short"])}</span></a></li>'


def visible():
    return [g for g in GROUPS if g["status"] != "hidden"]


def group_card(L, g):
    key = "vi" if L["code"] == "vi" else "en"
    n = sum(1 for a in ART[key] if g["code"] in a.get("groups", []))
    name, short = f(g, "name", L), f(g, "short", L)
    if g["status"] == "active":
        return f'<li><a class="card" href="{{{{R}}}}{L["p"]["groups"]}{g["code"]}/{{{{I}}}}"><b>{e(name)}</b><span class="muted small">{e(short)}</span><br><span class="tag ok">{n} {L["n_arts"]}</span></a></li>'
    return f'<li><div class="card soon"><b>{e(name)}</b><br><span class="muted small">{e(short)}</span><br><span class="tag">{L["soon"]}</span></div></li>'


HOME = {
    "vi": dict(h1="Biết luật để tự bảo vệ mình",
               lead="Trang này viết cho người làm việc nặng nhọc, độc hại, nguy hiểm, cho công nhân và người Việt đi làm ở nước ngoài. Bạn sẽ biết luật nói gì, cần làm gì từng bước, và gọi ai khi cần giúp. Hoàn toàn miễn phí.",
               b1="Tôi đang gặp chuyện", cur="Muốn học từ đầu, theo thứ tự? Xem", b2="Gọi ai bây giờ?", h_sit="Bạn đang gặp chuyện gì?", all_sit="Xem tất cả tình huống →",
               h_grp="Bạn là ai?", h_how="Cách đọc một bài", how="""<p>Bài nào cũng đi theo cùng một thứ tự, để bạn đọc nhanh trên điện thoại:</p>
<ol><li><b>Tóm tắt 3 dòng</b> – điều quan trọng nhất.</li><li><b>Luật nói gì</b> – trích đúng điều, khoản, số hiệu văn bản.</li>
<li><b>Bạn làm gì</b> – từng bước cụ thể.</li><li><b>Gọi ai</b> – nơi hỗ trợ đã kiểm tra.</li><li><b>Đúng đến ngày</b> và <b>Sắp thay đổi</b>.</li></ol>""",
               tags='Nhãn <span class="tag ok">Đã đối chiếu</span> nghĩa là thông tin đã kiểm tra với văn bản gốc hoặc trang của cơ quan nhà nước. Nhãn <span class="tag chk">Đang đối chiếu</span> nghĩa là chưa kiểm tra xong – bạn nên hỏi lại trước khi dựa vào.',
               logo_alt="Logo Trách Nhiệm Xã Hội"),
    "en": dict(h1="Know the law, protect yourself",
               lead="This site is for people in heavy, hazardous or dangerous jobs, for factory workers, and for Vietnamese people working abroad. You will learn what the law says, what to do step by step, and who to call for help. It is completely free. The English version helps auditors, NGOs, employers and anyone supporting Vietnamese workers.",
               b1="Something is happening to me", cur="Want to learn step by step, from the start? See the", b2="Who do I call?", h_sit="What is happening to you?", all_sit="See all situations →",
               h_grp="Who are you?", h_how="How each article is built", how="""<p>Every article follows the same order, so it is quick to read on a phone:</p>
<ol><li><b>In short</b> – the three most important points.</li><li><b>What the law says</b> – exact article, clause and document number.</li>
<li><b>What you can do</b> – concrete steps.</li><li><b>Who to call</b> – checked support contacts.</li><li><b>Checked on</b> and <b>Coming changes</b>.</li></ol>""",
               tags='The <span class="tag ok">Verified</span> label means we checked the information against the original legal text or a government page. <span class="tag chk">Being verified</span> means checking is not finished yet – please confirm before relying on it.',
               logo_alt="Trách Nhiệm Xã Hội logo"),
}


def home(L):
    H = HOME[L["code"]]
    sit = "".join(f'<li><a href="{t}">{e(f(s, "q", L))}</a></li>' for s in SITU[:8] if (t := sit_target(L, s)))
    body = f"""<section class="hero"><img class="hero-badge" src="{{{{R}}}}assets/logo.svg" alt="{H['logo_alt']}" width="190" height="203">
<h1>{H['h1']}</h1><p class="lead">{H['lead']}</p>
<p><a class="btn alt" href="{{{{R}}}}{L['p']['sit']}{{{{I}}}}">{H['b1']}</a><a class="btn" href="{{{{R}}}}{L['p']['dir']}{{{{I}}}}">{H['b2']}</a></p></section>
<p class="note">{H['cur']} <a href="{{{{R}}}}{L['p']['cur']}{{{{I}}}}">{L['nav'][4]} →</a></p>
<h2>{H['h_sit']}</h2><ul>{sit}</ul><p><a href="{{{{R}}}}{L['p']['sit']}{{{{I}}}}">{H['all_sit']}</a></p>
<h2>{H['h_grp']}</h2><ul class="cards grid">{"".join(group_card(L, g) for g in visible())}</ul>
<h2>{H['h_how']}</h2>{H['how']}<p class="note">{H['tags']}</p>"""
    page(L, L["pre"], L["name"], body, "en/" if L["code"] == "vi" else "")


def groups(L):
    key = L["code"]
    other = LANGS["en" if key == "vi" else "vi"]
    lead = ("Chọn nhóm gần với bạn nhất. Nhóm có số bài là nhóm đã có bài; các nhóm khác đang được biên soạn." if key == "vi"
            else "Choose the group closest to you. Groups showing a number of articles have articles; the others are being written.")
    page(L, L["p"]["groups"], L["nav"][0], f"<h1>{L['nav'][0]}</h1><p class=lead>{lead}</p><ul class='cards grid'>{''.join(group_card(L, g) for g in visible())}</ul>", other["p"]["groups"])
    for g in GROUPS:
        if g["status"] != "active":
            continue
        arts = [a for a in ART[key] if g["code"] in a.get("groups", [])]
        b = (f'<p class="crumb"><a href="{{{{R}}}}{L["p"]["groups"]}{{{{I}}}}">{L["crumb_groups"]}</a> ›</p><h1>{e(f(g, "name", L))}</h1>'
             f'<p class=lead>{e(f(g, "short", L))}</p><ul class="cards">{"".join(card(L, a) for a in arts)}</ul><p class="note">{L["need_help"]}</p>')
        page(L, f'{L["p"]["groups"]}{g["code"]}/', f(g, "name", L), b, f'{other["p"]["groups"]}{g["code"]}/', f(g, "short", L))


def situations(L):
    other = LANGS["en" if L["code"] == "vi" else "vi"]
    lead = ("Chọn tình huống gần nhất. Mỗi mục dẫn tới bài có luật, các bước làm và nơi hỗ trợ." if L["code"] == "vi"
            else "Choose the closest situation. Each one leads to an article with the law, the steps to take and where to get help.")
    rows = "".join(f'<li><a class="card" href="{t}"><b>{e(f(s, "q", L))}</b></a></li>' for s in SITU if (t := sit_target(L, s)))
    page(L, L["p"]["sit"], L["nav"][1], f"<h1>{L['nav'][1]}?</h1><p class=lead>{lead}</p><ul class='cards'>{rows}</ul>", other["p"]["sit"])


def directory(L):
    other = LANGS["en" if L["code"] == "vi" else "vi"]
    vi = L["code"] == "vi"
    b = [f"<h1>{'Gọi ai bây giờ?' if vi else 'Who do I call?'}</h1><p class=lead>"
         + ("Danh bạ chỉ ghi những số đã kiểm tra nguồn. Số nào chưa kiểm tra được thì chưa đăng." if vi
            else "We only list numbers whose source we have checked. Numbers we could not check are not published.")
         + f"</p><p class='meta'>{'Tra cứu gần nhất' if vi else 'Last checked'}: 18/11/2026.</p>"]
    for s in DIR["sections"]:
        b.append(f"<h2>{e(f(s, 'title', L))}</h2><div class='dir'>")
        for it in s["items"]:
            tag = f'<span class="tag ok">{L["ok"]}</span>' if it["status"] == "ok" else f'<span class="tag chk">{L["chk"]}</span>'
            ph = f'<p><a class="phone" href="tel:{it["phone"].replace("-", "")}">{e(it["phone"])}</a></p>' if it["phone"] else ""
            b.append(f'<div class="card"><h3>{e(f(it, "name", L))}</h3>{tag}{ph}<p>{e(f(it, "what", L))}</p>'
                     f'<p class="small muted">{e(f(it, "note", L))} <a href="{e(it["src"])}" rel="noopener">{L["src"]}</a></p></div>')
        b.append("</div>")
    pend = DIR["pending_en"] if not vi else DIR["pending"]
    b.append(f"<h2>{'Đang kiểm tra, sẽ bổ sung' if vi else 'Being checked, coming later'}</h2><ul>" + "".join(f"<li>{e(p)}</li>" for p in pend) + "</ul>")
    b.append('<p class="note">' + ("Bạn biết một số điện thoại hỗ trợ đang hoạt động tốt? Ghi lại tên, số, nơi bạn thấy số đó – trang sẽ kiểm tra trước khi đăng." if vi
             else "Know a support number that works well? Note the name, the number and where you found it – we will check it before publishing.") + "</p>")
    page(L, L["p"]["dir"], L["nav"][2], "".join(b), other["p"]["dir"],
         "Số điện thoại hỗ trợ người lao động ở Việt Nam, Nhật Bản, Đài Loan, Hàn Quốc – đã kiểm tra nguồn." if vi
         else "Help lines for Vietnamese workers in Vietnam, Japan, Taiwan and Korea – sources checked.")


def articles(L):
    key = L["code"]
    other = LANGS["en" if key == "vi" else "vi"]
    arts = ART[key]
    page(L, L["p"]["arts"], L["nav"][3], f"<h1>{L['nav'][3]}</h1><ul class='cards'>{''.join(card(L, a) for a in arts)}</ul>", other["p"]["arts"])
    for i, a in enumerate(arts):
        gl = " · ".join(f'<a href="{{{{R}}}}{L["p"]["groups"]}{c}/{{{{I}}}}">{e(f(g, "name", L))}</a>'
                        for c in a.get("groups", []) for g in GROUPS if g["code"] == c and g["status"] == "active")
        srcs = "".join(f'<li>{e(s["t"])}' + (f' – <a href="{e(s["u"])}" rel="noopener">{L["open"]}</a>' if s.get("u") else "") + "</li>" for s in a.get("sources", []))
        draft = f'<p class="danger">{L["draft_box"]}</p>' if a.get("status") != "published" else ""
        prev = arts[i - 1] if i > 0 else None
        nxt = arts[i + 1] if i + 1 < len(arts) else None
        pn = ('<div class="pn">' + (f'<a href="{art_url(L, prev["slug"])}">← {e(prev["title"])}</a>' if prev else "<span></span>")
              + (f'<a href="{art_url(L, nxt["slug"])}">{e(nxt["title"])} →</a>' if nxt else "") + "</div>")
        pair = EN_OF.get(a["slug"]) if key == "vi" else a.get("pair")
        alt = f'{other["p"]["arts"]}{pair}/' if pair and (pair in ART_BY["en" if key == "vi" else "vi"]) else None
        body = f"""<p class="crumb"><a href="{{{{R}}}}{L['p']['arts']}{{{{I}}}}">{L['crumb_arts']}</a> › {gl}</p>{draft}
<h1>{e(a["title"])}</h1>
<p class="meta">{L['checked']} {e(a["checked"])} · {L['by']}</p>
<div class="sum"><b>{L['summary']}</b><ul>{"".join(f"<li>{e(x)}</li>" for x in a["summary"])}</ul></div>
{md(a["body"])}
{f'<div class="change"><b>{L["upcoming"]}</b>{md(a["upcoming"])}</div>' if a.get("upcoming") else ""}
<h2>{L['sources']}</h2><ul class="src">{srcs}</ul>
<p class="small muted">{L['report']}</p>
{pn}"""
        page(L, f'{L["p"]["arts"]}{a["slug"]}/', a["title"], body, alt, a["short"])


def curriculum(L):
    vi = L["code"] == "vi"
    other = LANGS["en" if vi else "vi"]
    key = L["code"]
    done = total = 0
    parts = []
    for m in CUR["modules"]:
        items = []
        for ls in m["lessons"]:
            total += 1
            slug = ls.get("slug")
            if slug:
                assert slug in ART_BY["vi"], f"curriculum: không có bài {slug}"
                s2 = slug if vi else EN_OF.get(slug)
            if slug and s2 and s2 in ART_BY[key] and ART_BY[key][s2].get("status") == "published":
                done += 1
                a = ART_BY[key][s2]
                items.append(f'<li><a class="card" href="{art_url(L, s2)}"><b>{e(a["title"])}</b><span class="muted small">{e(a["short"])}</span></a></li>')
            else:
                t = f(ls, "t", L) if not slug else ART_BY["vi"][slug]["title"]
                items.append(f'<li><div class="card soon"><b>{e(t)}</b><span class="tag">{L["soon"]}</span></div></li>')
        goals = "".join(f"<li>{e(g)}</li>" for g in (m["goals_en"] if not vi else m["goals"]))
        parts.append(f'<h2>{e(f(m, "title", L))}</h2><div class="sum"><b>{"Học xong, bạn làm được" if vi else "When you finish, you can"}</b><ul>{goals}</ul></div><ul class="cards">{"".join(items)}</ul>')
    later = [g for g in visible() if g["status"] == "soon"]
    nmod = len(CUR["modules"])
    if later:
        parts.append(f'<h2>{f"Phần {nmod + 1}. Các nhóm người lao động khác (giai đoạn sau)" if vi else f"Part {nmod + 1}. Other groups of workers (later stage)"}</h2>'
                     f'<p>{"Mỗi nhóm sẽ có bộ bài riêng, viết theo cùng mẫu." if vi else "Each group will get its own set of lessons, in the same format."}</p>'
                     f'<ul class="cards grid">{"".join(group_card(L, g) for g in later)}</ul>')
    prog = (f"Đã đăng {done}/{total} bài trong Phần 1–{nmod}." if vi else f"{done} of {total} lessons in Parts 1–{nmod} are published.")
    how = ("<h2>Cách học mỗi bài</h2><ol><li>Đọc <b>Tóm tắt</b> trước.</li><li>Đọc <b>Luật nói gì</b>, đối chiếu với giấy tờ của bạn (hợp đồng, phiếu lương, sổ BHXH).</li>"
           "<li>Làm theo <b>Bạn làm gì</b>, từng bước.</li><li>Lưu số ở <b>Gọi ai</b> vào điện thoại.</li><li>Xem <b>Đúng đến ngày</b>: luật có thể đã đổi.</li></ol>") if vi else (
           "<h2>How to study each lesson</h2><ol><li>Read <b>In short</b> first.</li><li>Read <b>What the law says</b> and compare it with your own papers (contract, payslip, social insurance record).</li>"
           "<li>Follow <b>What you can do</b>, step by step.</li><li>Save the numbers in <b>Who to call</b> on your phone.</li><li>Check the <b>Checked on</b> date: the law may have changed.</li></ol>")
    body = (f"<h1>{L['nav'][4]}</h1><p class=lead>{e(CUR['intro'] if vi else CUR['intro_en'])}</p>"
            f'<p class="meta">{prog}</p>' + "".join(parts) + how)
    page(L, L["p"]["cur"], L["nav"][4], body, other["p"]["cur"],
         "Khung chương trình tự học luật lao động miễn phí cho người lao động: hợp đồng, tiền lương, bảo hiểm, an toàn, đi làm ở nước ngoài." if vi
         else "Free self-study curriculum on Vietnamese labour law for workers: contracts, pay, insurance, safety, working abroad.")


ABOUT = {
    "vi": """<h1>Giới thiệu</h1><img class="hero-badge" src="{{R}}assets/logo.svg" alt="Logo Trách Nhiệm Xã Hội" width="190" height="203">
<p class=lead><b>Trách Nhiệm Xã Hội</b> là trang tự học miễn phí, giúp người lao động biết luật để tự bảo vệ mình, biết nơi nhờ giúp, và có thêm kỹ năng tổ chức cuộc sống.</p>
<h2>Viết cho ai</h2>
<p>Giai đoạn đầu: công nhân, người làm nghề nặng nhọc, độc hại, nguy hiểm, và người Việt đi làm việc ở nước ngoài. Đã có bài cho nông dân, ngư dân, lao động tự do và trẻ em đi làm.
Sau đó: những người dễ bị tổn thương khác – người bị lừa bán, phụ nữ bị bạo hành, người khuyết tật, người có vấn đề sức khỏe tâm thần, trẻ không nơi nương tựa.</p>
<h2>Nguyên tắc biên soạn</h2>
<ul><li>Chỉ dùng nguồn gốc: văn bản pháp luật chính thức, trang của cơ quan nhà nước, ILO, IOM, tiêu chuẩn gốc, nghiên cứu có bình duyệt.</li>
<li>Mỗi điều luật ghi số hiệu văn bản, số điều, và ngày tra cứu.</li>
<li>Không chắc thì ghi rõ “đang đối chiếu”. Số điện thoại chưa kiểm tra thì không đăng.</li>
<li>Viết trung lập: trình bày luật và cách làm, không bình luận chính trị.</li>
<li>Không thu thập dữ liệu người đọc: không đăng nhập, không cookie, không công cụ theo dõi.</li></ul>
<h2>Logo</h2><p>Mũ bảo hộ đặt trên quyển sách mở: <b>biết luật để tự bảo vệ mình</b>. Phía sau là nhà máy, ruộng đồng và chiếc máy bay – công nhân, nông dân và người Việt đi làm xa.</p>
<h2>Người biên soạn</h2>
<p>Liêm – đánh giá viên trách nhiệm xã hội và an toàn, sức khỏe nghề nghiệp nhiều năm làm việc tại nhà máy ở Việt Nam và khu vực. Các tình huống trong bài được viết chung, không nêu tên doanh nghiệp hay người lao động nào.</p>
<h2>Các trang học miễn phí khác của Liêm</h2>
<ul><li><a href="https://kynanglamviec.com">Kỹ Năng Làm Việc</a> – kỹ năng đi làm, từ người mới tới quản lý.</li>
<li><a href="https://tienganhcanban.com">Tiếng Anh Căn Bản</a> – tự học tiếng Anh.</li>
<li><a href="https://daynentang.com">Dạy Nền Tảng</a> – nền tảng học tập cho mọi lứa tuổi.</li>
<li><a href="https://tamhonkhoe.com">Tâm Hồn Khỏe</a> – chăm sóc tinh thần.</li></ul>""",
    "en": """<h1>About</h1><img class="hero-badge" src="{{R}}assets/logo.svg" alt="Trách Nhiệm Xã Hội logo" width="190" height="203">
<p class=lead><b>Trách Nhiệm Xã Hội</b> (“Social Responsibility”) is a free self-study site that helps workers know the law so they can protect themselves, know where to get help, and build practical life skills.</p>
<h2>Who it is for</h2>
<p>First: factory workers, people in heavy, hazardous or dangerous jobs, and Vietnamese people working abroad under contract. Articles for farmers, fishers, informal workers and working children are now available.
Later: other vulnerable groups – people who were deceived or trafficked, women facing violence, people with disabilities, people with mental health conditions, and children without care.</p>
<p>The main audience is Vietnamese. The English version supports social auditors, NGOs, brands, employers and anyone who works with Vietnamese workers.</p>
<h2>How we write</h2>
<ul><li>Primary sources only: official legal texts, government pages, ILO, IOM, original standards and peer-reviewed research.</li>
<li>Every legal point shows the document number, the article and the date checked.</li>
<li>If we are not sure, we say “being verified”. Phone numbers we could not check are not published.</li>
<li>Neutral writing: we explain the law and practical steps, without political commentary.</li>
<li>English quotations of Vietnamese law are unofficial translations; the Vietnamese text prevails.</li>
<li>No data collection: no login, no cookies, no tracking.</li></ul>
<h2>The logo</h2><p>A safety helmet resting on an open book: <b>knowing the law protects you</b>. Behind it are a factory, rice fields and an aeroplane – factory workers, farmers and Vietnamese people working far from home.</p>
<h2>The editor</h2>
<p>Liêm – a social compliance and occupational health and safety auditor with many years of factory audits in Vietnam and the region. Examples in the articles are general and never name any company or worker.</p>
<h2>Other free sites by Liêm</h2>
<ul><li><a href="https://kynanglamviec.com">Kỹ Năng Làm Việc</a> – work skills, from first job to manager.</li>
<li><a href="https://tienganhcanban.com">Tiếng Anh Căn Bản</a> – English self-study.</li>
<li><a href="https://daynentang.com">Dạy Nền Tảng</a> – foundation learning for all ages.</li>
<li><a href="https://tamhonkhoe.com">Tâm Hồn Khỏe</a> – mental and spiritual well-being.</li></ul>""",
}


def about(L):
    other = LANGS["en" if L["code"] == "vi" else "vi"]
    page(L, L["p"]["about"], L["nav"][5], ABOUT[L["code"]], other["p"]["about"])


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "_build/static", OUT)
    for L in LANGS.values():
        for fn in (home, groups, situations, directory, articles, curriculum, about):
            fn(L)
    V = LANGS["vi"]
    page(V, "404.html", V["t404"], f"<h1>{V['t404']}</h1><p>{V['m404']}</p><p lang='en'>{LANGS['en']['m404'].replace('{home}', '/en/').replace('{dir}', '/en/contacts/')}</p>", None)
    urls = []
    for L in LANGS.values():
        urls += [L["pre"]] + list(L["p"].values()) + [f'{L["p"]["groups"]}{g["code"]}/' for g in GROUPS if g["status"] == "active"]
        urls += [f'{L["p"]["arts"]}{a["slug"]}/' for a in ART[L["code"]]]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                    + "".join(f"<url><loc>{SITE}/{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    if not PREVIEW:
        leaked = [a["slug"] for k in ART for a in ART[k] if a.get("status") != "published"]
        assert not leaked, f"Bài nháp lọt ra public: {leaked}"
    print(f"OK -> {OUT.name}/ : {len(ART['vi'])} bài VI, {len(ART['en'])} bài EN")


main()
