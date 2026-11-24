/* Khung app Trách Nhiệm Xã Hội: thanh trên, tab, cài đặt, tiến độ, ghi chú, tìm kiếm, sách.
   Mọi dữ liệu chỉ lưu trên máy (localStorage, khóa tnxh.v1). Không gửi đi đâu. */
(function () {
  "use strict";
  var KEY = "tnxh.v1", D = window.TNXH || { modules: [], search: [], book: null };
  var B = document.body, ROOT = B.dataset.root || "", PAGE = B.dataset.page || "";
  var ROOTURL = new URL(ROOT || "./", location.href).href;

  // ---------- lưu trữ ----------
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  var S = load();
  ["set", "done", "saved", "notes", "days", "pos"].forEach(function (k) { if (!S[k] || typeof S[k] !== "object") S[k] = {}; });
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

  // ngôn ngữ: trang web tự mang ngôn ngữ; trang của app dùng ngôn ngữ đã lưu
  var LANG = B.dataset.lang || S.set.lang || "vi";
  if (B.dataset.lang && S.set.lang !== LANG) { S.set.lang = LANG; save(); }
  var EN = LANG === "en";
  document.documentElement.lang = LANG;

  // mở app lần đầu trong phiên: về đúng trang chủ ngôn ngữ đã chọn
  try {
    if (!sessionStorage.getItem("tnxh.s")) {
      sessionStorage.setItem("tnxh.s", "1");
      if (PAGE === "index.html" && S.set.lang === "en") { location.replace(ROOT + "en/index.html"); return; }
    }
  } catch (e) {}

  var T = EN ? {
    name: "Quyền Làm Việc", home: "Home", learn: "Learn", book: "Book", call: "Contacts", me: "Me",
    search: "Search", settings: "Reading settings", size: "Text size", bg: "Background", auto: "Device", light: "Light",
    dark: "Dark", lang: "Language", close: "Close", part: "Part", lesson: "Lesson", of: "of", done: "Mark as finished",
    isdone: "Finished ✓", savebtn: "Save", saved: "Saved ★", note: "My note (only on this phone)", prev: "Previous",
    next: "Next", cont: "Continue", resume: "Pick up where you left off", learning: "Courses in progress",
    week: "This week", weekdays: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"], daysw: function (n) { return n + (n === 1 ? " day" : " days") + " with learning this week"; },
    savedl: "Saved", notesl: "My notes", none: "Nothing yet.", wipe: "Delete all my data on this phone",
    wipe2: "Tap again to delete everything", wiped: "Deleted.", about: "About", privacy: "Everything you mark, save or write stays on this phone only. Nothing is sent anywhere.",
    q: "Type a word, e.g. overtime, contract…", nores: "No results.", start: "Start", chapter: "Chapter",
    booknotice: "The book is in Vietnamese only for now. An English translation is not available yet.",
    nobook: "The book is not in this version of the app yet.", review: "This chapter is waiting for expert review.",
    lessons: "lessons", chapters: "chapters", noen: "This page has no English version yet – opening the English home page."
  } : {
    name: "Quyền Làm Việc", home: "Trang chủ", learn: "Học", book: "Sách", call: "Gọi ai", me: "Của tôi",
    search: "Tìm", settings: "Cài đặt đọc", size: "Cỡ chữ", bg: "Màu nền", auto: "Theo máy", light: "Sáng",
    dark: "Tối", lang: "Ngôn ngữ", close: "Đóng", part: "Phần", lesson: "Bài", of: "trên", done: "Đánh dấu đã học xong",
    isdone: "Đã học xong ✓", savebtn: "Lưu bài", saved: "Đã lưu ★", note: "Ghi chú của tôi (chỉ lưu trên máy này)", prev: "Bài trước",
    next: "Bài tiếp theo", cont: "Học tiếp", resume: "Đọc tiếp chỗ đang dở", learning: "Khóa đang học",
    week: "Tuần này", weekdays: ["T2", "T3", "T4", "T5", "T6", "T7", "CN"], daysw: function (n) { return n + " ngày có học trong tuần này"; },
    savedl: "Bài đã lưu", notesl: "Ghi chú của tôi", none: "Chưa có.", wipe: "Xóa mọi dữ liệu của tôi trên máy này",
    wipe2: "Bấm lần nữa để xóa hết", wiped: "Đã xóa.", about: "Giới thiệu", privacy: "Mọi thứ bạn đánh dấu, lưu, ghi chú chỉ nằm trên điện thoại này. Không gửi đi đâu.",
    q: "Gõ từ cần tìm, ví dụ: tang ca, hop dong…", nores: "Không tìm thấy.", start: "Bắt đầu", chapter: "Chương",
    booknotice: "", nobook: "Sách chưa có trong bản app này.", review: "Chương này đang chờ chuyên gia đọc duyệt.",
    lessons: "bài", chapters: "chương", noen: ""
  };

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function el(html) { var d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
  function href(u) { return ROOT + u; }                       // đường dẫn từ gốc www → tương đối trang hiện tại
  function keyOf(abs) {                                         // link tuyệt đối → khóa từ gốc www
    if (abs.indexOf(ROOTURL) !== 0) return null;
    var k = abs.slice(ROOTURL.length).split("#")[0].split("?")[0];
    if (k === "" || /\/$/.test(k)) k += "index.html";
    return k;
  }
  function today(d) { d = d || new Date(); return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); }

  // ---------- chỉ mục bài: khóa chung = url tiếng Việt ----------
  var SEQ = [], BYURL = {};
  D.modules.forEach(function (m, mi) {
    m.lessons.forEach(function (l, li) {
      var it = { m: m, mi: mi, li: li, key: l.vi, vi: l.vi, en: l.en, t: l.t, t_en: l.t_en, n: m.lessons.length };
      it.seq = SEQ.length; SEQ.push(it); BYURL[l.vi] = it; if (l.en) BYURL[l.en] = it;
    });
  });
  var BK = D.book, CH = {};
  if (BK) BK.chapters.forEach(function (c, i) { c.i = i; CH[c.u] = c; });
  function urlOf(it) { return EN && it.en ? it.en : it.vi; }
  function titleOf(it) { return EN && it.t_en ? it.t_en : it.t; }
  function mTitle(m) { return EN ? m.t_en : m.t; }
  function mDone(m) { return m.lessons.filter(function (l) { return S.done[l.vi]; }).length; }
  function mNext(m) { for (var i = 0; i < m.lessons.length; i++) if (!S.done[m.lessons[i].vi]) return BYURL[m.lessons[i].vi]; return BYURL[m.lessons[0].vi]; }
  function bar(a, b) { return '<div class="ab-bar" role="progressbar" aria-valuemin="0" aria-valuemax="' + b + '" aria-valuenow="' + a + '"><i style="width:' + (b ? Math.round(100 * a / b) : 0) + '%"></i></div>'; }

  // ---------- biểu tượng ----------
  var I = {
    home: '<path d="M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
    learn: '<path d="M4 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H4zM20 5h-4a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h5z"/>',
    book: '<path d="M6 3h11a1 1 0 0 1 1 1v15H7a2 2 0 0 0 0 4h11M6 3a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2"/><path d="M9 7h6"/>',
    call: '<path d="M5 3h3l2 5-2.5 1.5a11 11 0 0 0 7 7L16 14l5 2v3a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2"/>',
    me: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>'
  };
  function ico(n) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + I[n] + "</svg>"; }

  // ---------- thanh trên + tab ----------
  var tabs = EN ? [["home", "en/index.html"], ["learn", "en/curriculum/index.html"], ["book", "app/sach.html"], ["call", "en/contacts/index.html"], ["me", "app/toi.html"]]
                : [["home", "index.html"], ["learn", "khung-chuong-trinh/index.html"], ["book", "app/sach.html"], ["call", "danh-ba/index.html"], ["me", "app/toi.html"]];
  var cur = "home";
  if (/^(en\/)?(khung-chuong-trinh|curriculum|bai|articles|en\/articles)/.test(PAGE) || /^en\/(curriculum|articles)/.test(PAGE)) cur = "learn";
  if (/^(app\/sach|sach\/)/.test(PAGE)) cur = "book";
  if (/^(en\/)?(danh-ba|contacts)/.test(PAGE)) cur = "call";
  if (/^app\/(toi|tim)/.test(PAGE)) cur = "me";
  if (/^(en\/)?(nhom|groups|tinh-huong|situations|gioi-thieu|about)/.test(PAGE) || PAGE === "index.html" || PAGE === "en/index.html") cur = "home";

  var top = el('<header class="ab-top"><div class="ab-top-in">' +
    '<a class="ab-brand" href="' + href(tabs[0][1]) + '"><img src="' + ROOT + 'assets/logo-icon.svg" alt="">' + esc(T.name) + '</a>' +
    '<a class="ab-btn" href="' + href("app/tim.html") + '" aria-label="' + T.search + '">' + ico("search") + '</a>' +
    '<button class="ab-btn" type="button" id="ab-aa" aria-label="' + T.settings + '">Aa</button>' +
    '<a class="ab-btn ab-sos" href="' + href(EN ? "en/contacts/index.html" : "danh-ba/index.html") + '">SOS</a>' +
    "</div></header>");
  var nav = '<nav class="ab-tabs" aria-label="' + (EN ? "Main" : "Chính") + '">';
  tabs.forEach(function (t) { nav += '<a class="ab-tab" href="' + href(t[1]) + '"' + (t[0] === cur ? ' aria-current="page"' : "") + ">" + ico(t[0]) + "<span>" + T[t[0]] + "</span></a>"; });
  B.insertBefore(top, B.firstChild);
  B.appendChild(el(nav + "</nav>"));

  // ---------- bảng cài đặt "Aa" ----------
  function seg(name, opts, val) {
    return '<div class="ab-seg" data-k="' + name + '">' + opts.map(function (o) { return '<button type="button" data-v="' + o[0] + '" aria-pressed="' + (String(val) === o[0]) + '">' + o[1] + "</button>"; }).join("") + "</div>";
  }
  var sheet = el('<div class="ab-sheet" role="dialog" aria-modal="true" aria-label="' + T.settings + '"><div class="ab-panel">' +
    "<h3>" + T.settings + "</h3>" +
    '<div class="ab-row"><b>' + T.size + "</b>" + seg("fs", [["1", "A−"], ["2", "A"], ["3", "A+"], ["4", "A++"]], S.set.fs || "2") + "</div>" +
    '<div class="ab-row"><b>' + T.bg + "</b>" + seg("theme", [["auto", T.auto], ["light", T.light], ["dark", T.dark]], S.set.theme || "auto") + "</div>" +
    '<div class="ab-row"><b>' + T.lang + "</b>" + seg("lang", [["vi", "Tiếng Việt"], ["en", "English"]], LANG) + "</div>" +
    '<button type="button" class="ab-b pri ab-close">' + T.close + "</button></div></div>");
  B.appendChild(sheet);
  document.getElementById("ab-aa").onclick = function () { sheet.classList.add("open"); };
  sheet.onclick = function (e) { if (e.target === sheet || e.target.classList.contains("ab-close")) sheet.classList.remove("open"); };
  function applyTheme() {
    var t = S.set.theme || "auto";
    if (t === "auto") t = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    document.documentElement.dataset.theme = t;
    document.documentElement.dataset.fs = S.set.fs || "2";
  }
  sheet.addEventListener("click", function (e) {
    var b = e.target.closest("button[data-v]"); if (!b) return;
    var k = b.parentNode.dataset.k, v = b.dataset.v;
    b.parentNode.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
    if (k === "lang") { if (v !== LANG) switchLang(v); return; }
    S.set[k] = v; save(); applyTheme();
  });
  function switchLang(v) {
    S.set.lang = v; save();
    var alt = B.dataset.alt;
    if (B.dataset.lang && alt) { location.href = alt; return; }       // trang web có bản ngôn ngữ kia
    if (PAGE.indexOf("app/") === 0 || PAGE.indexOf("sach/") === 0) { location.reload(); return; }
    location.href = href(v === "en" ? "en/index.html" : "index.html");
  }

  // ---------- ✓ cạnh link bài đã học xong ----------
  function markLinks(root) {
    (root || document).querySelectorAll("main a[href]").forEach(function (a) {
      if (a.closest(".ab-crs,.ab-pn,.ab-card,.ab-tabs") || a.dataset.ck) return;
      var k = keyOf(a.href), it = k && (BYURL[k] || CH[k]);
      if (!it) return;
      a.dataset.ck = 1;
      if (S.done[it.key || k]) (a.querySelector("b") || a).insertAdjacentHTML("beforeend", ' <span class="ab-done" aria-label="' + T.isdone + '">✓</span>');
    });
  }

  var main = document.querySelector("main .wrap") || document.querySelector("main");

  // ---------- trang bài học ----------
  function lessonPage(it) {
    var key = it.key, h1 = main.querySelector("h1");
    S.days[today()] = 1;
    S.last = { u: urlOf(it), k: key, y: 0 }; save();
    var crs = el('<a class="ab-crs ab-ui" href="' + href(EN ? "en/curriculum/index.html" : "khung-chuong-trinh/index.html") + '"><b>' + esc(mTitle(it.m)) + "</b> · " +
      T.lesson + " " + (it.li + 1) + " " + T.of + " " + it.n + bar(mDone(it.m), it.n) + "</a>");
    main.insertBefore(crs, main.firstChild);
    var acts = el('<div class="ab-ui"><div class="ab-acts">' +
      '<button type="button" class="ab-b" id="ab-done"></button>' +
      '<button type="button" class="ab-b" id="ab-save"></button></div>' +
      '<div class="ab-note"><label for="ab-nt"><b>' + T.note + '</b></label><textarea id="ab-nt"></textarea></div>' +
      '<div class="ab-pn"></div></div>');
    var pn = main.querySelector(".pn");
    if (pn) pn.parentNode.insertBefore(acts, pn); else main.appendChild(acts);
    var bd = acts.querySelector("#ab-done"), bs = acts.querySelector("#ab-save"), nt = acts.querySelector("#ab-nt");
    function paint() {
      bd.textContent = S.done[key] ? T.isdone : T.done; bd.classList.toggle("on", !!S.done[key]);
      bs.textContent = S.saved[key] ? T.saved : T.savebtn; bs.classList.toggle("on", !!S.saved[key]);
      crs.querySelector(".ab-bar i").style.width = Math.round(100 * mDone(it.m) / it.n) + "%";
    }
    bd.onclick = function () { if (S.done[key]) delete S.done[key]; else S.done[key] = Date.now(); save(); paint(); };
    bs.onclick = function () { if (S.saved[key]) delete S.saved[key]; else S.saved[key] = Date.now(); save(); paint(); };
    nt.value = S.notes[key] || "";
    nt.oninput = function () { if (nt.value.trim()) S.notes[key] = nt.value; else delete S.notes[key]; save(); };
    var pv = SEQ[it.seq - 1], nx = SEQ[it.seq + 1], box = acts.querySelector(".ab-pn");
    if (pv) box.insertAdjacentHTML("beforeend", '<a href="' + href(urlOf(pv)) + '"><small>← ' + T.prev + "</small>" + esc(titleOf(pv)) + "</a>");
    if (nx) box.insertAdjacentHTML("beforeend", '<a class="nx" href="' + href(urlOf(nx)) + '"><small>' + T.next + " →</small>" + esc(titleOf(nx)) + "</a>");
    paint();
    trackScroll(key);
  }

  // nhớ vị trí cuộn cho "Đọc tiếp"
  function trackScroll(key) {
    var y0 = S.pos[key];
    try { if (sessionStorage.getItem("tnxh.resume") === key && y0) { sessionStorage.removeItem("tnxh.resume"); setTimeout(function () { scrollTo(0, y0); }, 30); } } catch (e) {}
    var tm;
    addEventListener("scroll", function () {
      clearTimeout(tm);
      tm = setTimeout(function () { S.pos[key] = Math.round(scrollY); if (S.last) S.last.y = S.pos[key]; save(); }, 400);
    }, { passive: true });
  }
  function resumeLink(cls) {
    if (!S.last) return "";
    var it = BYURL[S.last.k], c = CH[S.last.k], u, t;
    if (it) { u = urlOf(it); t = titleOf(it); } else if (c) { u = c.u; t = T.chapter + " " + c.n + ". " + c.t; } else return "";
    return '<a class="' + (cls || "ab-b pri") + '" data-resume="' + esc(S.last.k) + '" href="' + href(u) + '">' + T.resume + "</a><p>" + esc(t) + "</p>";
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-resume]");
    if (a) try { sessionStorage.setItem("tnxh.resume", a.dataset.resume); } catch (x) {}
  });

  function learningCards() {
    var out = "";
    D.modules.forEach(function (m) {
      var d = mDone(m); if (!d || d === m.lessons.length) return;
      out += '<div class="ab-card"><h3>' + esc(mTitle(m)) + "</h3>" + bar(d, m.lessons.length) +
        "<p class=\"meta\">" + d + "/" + m.lessons.length + " " + T.lessons + '</p><a class="ab-b" href="' + href(urlOf(mNext(m))) + '">' + T.cont + "</a></div>";
    });
    if (BK) {
      var bd = BK.chapters.filter(function (c) { return S.done[c.u]; }).length;
      if (bd && bd < BK.chapters.length) out += '<div class="ab-card"><h3>' + esc(BK.title) + "</h3>" + bar(bd, BK.chapters.length) +
        '<p class="meta">' + bd + "/" + BK.chapters.length + " " + T.chapters + "</p></div>";
    }
    return out;
  }

  // ---------- trang chủ ----------
  function homePage() {
    var r = resumeLink(), l = learningCards();
    if (!r && !l) return;
    var box = el('<div class="ab-home ab-ui">' + (r ? '<div class="ab-card">' + r + "</div>" : "") +
      (l ? "<h2 style=\"margin:.6em 0 0\">" + T.learning + "</h2>" + l : "") + "</div>");
    var hero = main.querySelector(".hero");
    if (hero) hero.parentNode.insertBefore(box, hero.nextSibling); else main.insertBefore(box, main.firstChild);
  }

  // ---------- khung chương trình: thanh tiến độ từng phần ----------
  function curriculumPage() {
    var h2s = [].slice.call(main.querySelectorAll("h2"));
    D.modules.forEach(function (m) {
      var h = h2s.filter(function (x) { return x.textContent.trim() === mTitle(m).trim(); })[0];
      if (!h || !m.lessons.length) return;
      var d = mDone(m);
      h.insertAdjacentElement("afterend", el('<div class="ab-ui">' + bar(d, m.lessons.length) + '<p class="meta">' + d + "/" + m.lessons.length + " " + T.lessons +
        ' · <a href="' + href(urlOf(mNext(m))) + '"><b>' + (d ? T.cont : T.start) + " →</b></a></p></div>"));
    });
  }

  // ---------- trang của app ----------
  function weekBox() {
    var now = new Date(), wd = (now.getDay() + 6) % 7, mon = new Date(now); mon.setDate(now.getDate() - wd);
    var cells = "", n = 0;
    for (var i = 0; i < 7; i++) { var d = new Date(mon); d.setDate(mon.getDate() + i); var y = !!S.days[today(d)]; if (y) n++; cells += '<span class="' + (y ? "y" : "") + '"><i></i>' + T.weekdays[i] + "</span>"; }
    return '<div class="ab-card"><h3>' + T.week + '</h3><div class="ab-week">' + cells + '</div><p class="meta">' + T.daysw(n) + "</p></div>";
  }
  function itemLink(k) {
    var it = BYURL[k], c = CH[k];
    if (it) return '<a href="' + href(urlOf(it)) + '">' + esc(titleOf(it)) + "</a>";
    if (c) return '<a href="' + href(c.u) + '">' + T.chapter + " " + c.n + ". " + esc(c.t) + "</a>";
    return null;
  }
  function mePage() {
    var r = resumeLink(), l = learningCards();
    var sv = Object.keys(S.saved).sort(function (a, b) { return S.saved[b] - S.saved[a]; }).map(itemLink).filter(Boolean);
    var nt = Object.keys(S.notes).map(function (k) { var a = itemLink(k); return a ? a + '<p class="meta">' + esc(S.notes[k]).slice(0, 160) + "</p>" : null; }).filter(Boolean);
    main.innerHTML = '<div class="ab-ui"><h1>' + T.me + "</h1>" +
      '<div class="ab-home">' + (r ? '<div class="ab-card">' + r + "</div>" : "") + weekBox() + "</div>" +
      "<h2>" + T.learning + "</h2>" + (l ? '<div class="ab-home">' + l + "</div>" : "<p>" + T.none + "</p>") +
      "<h2>" + T.savedl + "</h2>" + (sv.length ? '<ul class="ab-list"><li>' + sv.join("</li><li>") + "</li></ul>" : "<p>" + T.none + "</p>") +
      "<h2>" + T.notesl + "</h2>" + (nt.length ? '<ul class="ab-list"><li>' + nt.join("</li><li>") + "</li></ul>" : "<p>" + T.none + "</p>") +
      "<h2>" + T.settings + '</h2><p><button type="button" class="ab-b" onclick="document.getElementById(\'ab-aa\').click()">Aa · ' + T.size + " · " + T.bg + " · " + T.lang + "</button></p>" +
      '<p class="note">' + T.privacy + "</p>" +
      '<p><button type="button" class="ab-b warn" id="ab-wipe">' + T.wipe + "</button></p>" +
      '<p><a href="' + href(EN ? "en/about/index.html" : "gioi-thieu/index.html") + '">' + T.about + "</a></p></div>";
    var w = document.getElementById("ab-wipe"), armed = false;
    w.onclick = function () {
      if (!armed) { armed = true; w.classList.add("arm"); w.textContent = T.wipe2; setTimeout(function () { armed = false; w.classList.remove("arm"); w.textContent = T.wipe; }, 5000); return; }
      try { localStorage.removeItem(KEY); } catch (e) {}
      S = { set: {}, done: {}, saved: {}, notes: {}, days: {}, pos: {} };
      w.textContent = T.wiped; setTimeout(function () { location.reload(); }, 600);
    };
    document.title = T.me + " – " + T.name;
  }

  function norm(s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d"); }
  function searchPage() {
    main.innerHTML = '<div class="ab-ui"><h1>' + T.search + '</h1><input class="ab-search" type="search" id="ab-q" autocomplete="off" placeholder="' + esc(T.q) + '"><div id="ab-r" class="ab-res"></div></div>';
    var q = document.getElementById("ab-q"), out = document.getElementById("ab-r");
    var docs = D.search.filter(function (d) { return d.l === LANG || (EN && d.l === "vi" && false); });
    docs.forEach(function (d) { d.nt = norm(d.t); d.nx = norm(d.x); });
    function run() {
      var words = norm(q.value).split(/\s+/).filter(function (w) { return w.length > 1; });
      if (!words.length) { out.innerHTML = ""; return; }
      var res = [];
      docs.forEach(function (d) {
        var sc = 0;
        for (var i = 0; i < words.length; i++) { var w = words[i], a = d.nt.indexOf(w) >= 0, b = d.nx.indexOf(w) >= 0; if (!a && !b) return; sc += (a ? 5 : 0) + (b ? 1 : 0); }
        res.push([sc, d]);
      });
      res.sort(function (a, b) { return b[0] - a[0]; });
      out.innerHTML = res.length ? '<ul class="ab-list">' + res.slice(0, 40).map(function (r) {
        var d = r[1], p = d.nx.indexOf(words[0]), snip = p >= 0 ? d.x.substr(Math.max(0, p - 60), 180) : d.x.substr(0, 150);
        return '<li><a href="' + href(d.u) + '">' + esc(d.t) + "</a><p>…" + esc(snip) + "…</p></li>";
      }).join("") + "</ul>" : "<p>" + T.nores + "</p>";
      markLinks(out);
    }
    q.oninput = run;
    setTimeout(function () { q.focus(); }, 50);
    document.title = T.search + " – " + T.name;
  }

  function bookPage() {
    document.title = T.book + " – " + T.name;
    if (!BK) { main.innerHTML = '<div class="ab-ui"><h1>' + T.book + '</h1><p class="ab-tr">' + T.nobook + "</p></div>"; return; }
    var done = BK.chapters.filter(function (c) { return S.done[c.u]; }).length;
    var h = '<div class="ab-ui" lang="vi"><h1>' + esc(BK.title) + "</h1>" + (EN ? '<p class="ab-tr" lang="en">' + T.booknotice + "</p>" : "") +
      '<p class="meta">' + esc(BK.author) + " · " + BK.chapters.length + " chương" + (BK.checked ? " · Đúng đến ngày " + esc(BK.checked) : "") + "</p>" +
      bar(done, BK.chapters.length) + '<p class="meta">' + done + "/" + BK.chapters.length + " chương đã đọc xong</p>";
    var last = S.last && CH[S.last.k] ? resumeLink() : "";
    if (last) h += '<div class="ab-card">' + last + "</div>";
    (BK.front || []).forEach(function (f) { h += '<p><a href="' + href(f.u) + '">' + esc(f.t) + "</a></p>"; });
    BK.parts.forEach(function (p) {
      h += "<h2>" + esc(p.t) + '</h2><ul class="ab-list">';
      p.ch.forEach(function (i) { var c = BK.chapters[i]; h += '<li><a href="' + href(c.u) + '">Chương ' + c.n + ". " + esc(c.t) + "</a>" + (c.review ? ' <span class="tag chk">chờ duyệt</span>' : "") + "</li>"; });
      h += "</ul>";
    });
    (BK.back || []).forEach(function (f) { h += '<p><a href="' + href(f.u) + '">' + esc(f.t) + "</a></p>"; });
    main.innerHTML = h + "</div>";
    markLinks(main);
  }

  function chapterPage(c) {
    S.days[today()] = 1; S.last = { u: c.u, k: c.u, y: 0 }; save();
    var done = BK.chapters.filter(function (x) { return S.done[x.u]; }).length;
    main.insertBefore(el('<a class="ab-crs ab-ui" href="' + href("app/sach.html") + '"><b>' + esc(BK.title) + "</b> · Chương " + c.n + " trên " + BK.chapters.length + bar(done, BK.chapters.length) + "</a>"), main.firstChild);
    if (EN) main.insertBefore(el('<p class="ab-tr ab-ui" lang="en">' + T.booknotice + "</p>"), main.children[1]);
    if (c.review) main.insertBefore(el('<p class="ab-tr ab-ui">' + T.review + "</p>"), main.children[1]);
    var it = { key: c.u };
    var acts = el('<div class="ab-ui"><div class="ab-acts"><button type="button" class="ab-b" id="ab-done"></button><button type="button" class="ab-b" id="ab-save"></button></div>' +
      '<div class="ab-note"><label for="ab-nt"><b>' + T.note + '</b></label><textarea id="ab-nt"></textarea></div><div class="ab-pn"></div></div>');
    main.appendChild(acts);
    var key = it.key, bd = acts.querySelector("#ab-done"), bs = acts.querySelector("#ab-save"), nt = acts.querySelector("#ab-nt");
    function paint() {
      bd.textContent = S.done[key] ? T.isdone : T.done; bd.classList.toggle("on", !!S.done[key]);
      bs.textContent = S.saved[key] ? T.saved : T.savebtn; bs.classList.toggle("on", !!S.saved[key]);
    }
    bd.onclick = function () { if (S.done[key]) delete S.done[key]; else S.done[key] = Date.now(); save(); paint(); };
    bs.onclick = function () { if (S.saved[key]) delete S.saved[key]; else S.saved[key] = Date.now(); save(); paint(); };
    nt.value = S.notes[key] || "";
    nt.oninput = function () { if (nt.value.trim()) S.notes[key] = nt.value; else delete S.notes[key]; save(); };
    var pv = BK.chapters[c.i - 1], nx = BK.chapters[c.i + 1], box = acts.querySelector(".ab-pn");
    if (pv) box.insertAdjacentHTML("beforeend", '<a href="' + href(pv.u) + '"><small>← Chương trước</small>' + esc(pv.t) + "</a>");
    if (nx) box.insertAdjacentHTML("beforeend", '<a class="nx" href="' + href(nx.u) + '"><small>Chương tiếp →</small>' + esc(nx.t) + "</a>");
    paint(); trackScroll(key);
  }

  // ---------- điều phối ----------
  if (main) {
    if (PAGE === "app/toi.html") mePage();
    else if (PAGE === "app/tim.html") searchPage();
    else if (PAGE === "app/sach.html") bookPage();
    else if (CH[PAGE]) chapterPage(CH[PAGE]);
    else if (BYURL[PAGE]) lessonPage(BYURL[PAGE]);
    else if (PAGE === "index.html" || PAGE === "en/index.html") homePage();
    else if (PAGE === "khung-chuong-trinh/index.html" || PAGE === "en/curriculum/index.html") curriculumPage();
    markLinks();
  }

  // trang không có bản tiếng Anh: nút ngôn ngữ về trang chủ (đã xử lý trong switchLang)
  matchMedia("(prefers-color-scheme: dark)").addEventListener && matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);
})();
