# TIẾN ĐỘ – trachnhiemxahoi.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.
Cập nhật gần nhất: 23/11/2026 (phiên 7).

## 1. Trạng thái hiện tại – v0.3, ĐANG CHẠY THẬT
- Trang chính: https://trachnhiemxahoi.com (đã chạy). www.trachnhiemxahoi.com: đã chạy. Bản dự phòng: https://trachnhiemxahoi-web.pages.dev
- Song ngữ: tiếng Việt ở `/`, tiếng Anh ở `/en/`. Mỗi trang có nút chuyển ngôn ngữ và thẻ hreflang.
- Logo: đã thiết kế, cùng họ huy hiệu với daynentang và kynanglamviec (mũ bảo hộ đặt trên sách mở; phía sau là nhà máy, ruộng bậc thang, máy bay).
- 19 bài đã đăng, có cả bản tiếng Việt và tiếng Anh. 1 bài nháp nhạy cảm chờ Peter duyệt.
- **Khung chương trình** (phiên 4): VI `/khung-chuong-trinh/`, EN `/en/curriculum/`, có trên menu và trang chủ. 6 phần, 19 bài – ĐỦ cả 6 phần (Phần 6 xong phiên 7) + Phần 7 các nhóm giai đoạn sau (8 nhóm, còn "Sắp có"). Dữ liệu: `data/curriculum.yaml` (slug = bài đã đăng; t/t_en = bài dự kiến). Bài nháp nhạy cảm KHÔNG đưa vào khung.

## 2. Hạ tầng
- Cloudflare: tài khoản Reach.petertran@gmail.com (account f9970afd818f540f45e8ef101099de6a), gói Free ($0).
- **Đăng bài TỰ ĐỘNG từ 23/11/2026:** Pages project `trachnhiemxahoi-web` nối với GitHub reachpetertran/trachnhiemxahoi, nhánh `main`, build command để trống, output `public`. Push lên `main` là Cloudflare tự đăng (khoảng 1 phút).
- Project cũ `trachnhiemxahoi` (upload trực tiếp) không còn gắn tên miền; để lại làm dự phòng, có thể xóa.
- Zone trachnhiemxahoi.com: Active từ 18/11/2026. Nameserver GoDaddy: christian.ns.cloudflare.com, clarissa.ns.cloudflare.com. Custom domain: trachnhiemxahoi.com và www → project trachnhiemxahoi-web.
- Đã xóa bản ghi đỗ của GoDaddy (2 A, 1 CNAME www); giữ `_domainconnect`, `_dmarc`.
- GitHub: https://github.com/reachpetertran/trachnhiemxahoi (public, nhánh `main`), đẩy lên 18/11/2026. Bài nháp nhạy cảm (`content/nhap/`) KHÔNG có trên GitHub (.gitignore).
- Phiên mới: gắn repo (add_repo reachpetertran/trachnhiemxahoi, quyền push), clone, sửa, `python3 _build/build.py`, commit cả `public/`, push → tự đăng.
- Bài nháp nằm ở máy của phiên cũ; bản đã gửi Peter: NHAP-dai-dien-nguoi-lao-dong.md. Phiên mới cần Peter gửi lại file này nếu làm tiếp.

## 3. Cấu trúc mã nguồn
```
data/groups.yaml        Trục 1 "Tôi là ai" – name/short (+ name_en/short_en); status active|soon|hidden
data/situations.yaml    Trục 2 "Tôi gặp chuyện gì" – q (+ q_en), to = slug bài tiếng Việt hoặc "danh-ba"
data/curriculum.yaml    Khung chương trình – modules (title, goals, lessons: slug | t/t_en)
data/danhba.yaml        Trục 3 "Gọi ai" – status ok|check; trường *_en; pending + pending_en
content/bai/*.md        bài tiếng Việt (front matter: slug, order, status, title, short, groups, checked, summary, sources, upcoming)
content/en/*.md         bài tiếng Anh, có thêm `pair:` = slug bài tiếng Việt tương ứng
content/nhap/           bài nháp nhạy cảm – .gitignore, KHÔNG đưa lên GitHub
_build/build.py         sinh public/ (song ngữ, sitemap, 404); --preview sinh preview/ có cả nháp
_build/art/logo_art.py  sinh logo.svg, logo-khong-chu.svg, logo-icon.svg, favicon.svg (chữ đã chuyển thành nét, font Inter Bold)
_build/static/          CSS, logo, PNG (logo-512/1024, logo-icon-512, apple-touch-icon), _headers, robots.txt
```
Đường dẫn: VI `bai/ nhom/ tinh-huong/ danh-ba/ khung-chuong-trinh/ gioi-thieu/` – EN `en/articles/ en/groups/ en/situations/ en/contacts/ en/curriculum/ en/about/`.

## 4. Bài đã đăng (VI ↔ EN)
| # | Tiếng Việt | English | Văn bản chính |
|---|---|---|---|
| 1 | hop-dong-lao-dong | employment-contracts | BLLĐ 45/2019 Đ14, 17, 18, 20, 25, 26, 35, 48, 113.3 |
| 2 | tien-luong-lam-them-gio | wages-and-overtime | NĐ 293/2025; BLLĐ Đ95, 97, 98, 107, 109, 111, 113; TT 11/2020 + 19/2023; TT 24/2022 |
| 3 | bao-hiem-xa-hoi | social-insurance | Luật BHXH 41/2024 Đ38–41, 64; Luật Việc làm 74/2025 Đ38, 39; BLLĐ Đ168.3 |
| 4 | an-toan-ve-sinh-lao-dong | safety-and-health | Luật ATVSLĐ 84/2015 Đ6, 21; TT 60/2025/TT-BYT (35 bệnh); Luật Hóa chất 69/2025 Đ25; QCVN 25:2015 |
| 5 | di-lam-viec-o-nuoc-ngoai | working-abroad | Luật 69/2020 Đ23; TT 21/2021 (Đài Loan 1.500 TWD/tháng); Luật PCMBN 53/2024; NĐ 162/2025 |
| 6 | giu-bang-chung | keep-evidence | BLLĐ Đ95.3, 188, 190; NĐ 129/2025; Luật TGPL 11/2017 Đ7 + Luật 05/2026 |
| 7 | tai-nan-lao-dong | work-accidents | Luật ATVSLĐ Đ34, 38–40, 45, 48, 49 (không bị Luật BHXH 2024 sửa); TT 60/2025-BYT |
| 8 | lao-dong-thue-lai | leased-workers | BLLĐ Đ52–58, 188; NĐ 145/2020 Đ21, 30, Phụ lục II (bảng 20 công việc nguyên văn, ĐÃ đối chiếu 23/11/2026 với toàn văn trên vanban.vcci.com.vn + bài TVPL Peter gửi); hộp Sắp thay đổi: dự thảo Bộ Nội vụ 7/2026 thay Phụ lục II (dòng 5 thêm "trưng bày và đóng gói sản phẩm"). Phiên 5: sửa chỗ "phải có giấy phép" – từ 01/7/2026 NQ 66.18/2026/NQ-CP thay giấy phép bằng ký quỹ + thông báo Sở Nội vụ (đến 28/02/2027), nhãn Đang đối chiếu |
| 9 | gio-lam-viec-nghi-ngoi | working-hours-and-leave | BLLĐ Đ99, 105, 106, 109–115 (nguyên văn); NĐ 145/2020 Đ64–67; NQ 28/2026/QH16 (24/11 nghỉ hưởng lương, hiệu lực 01/7/2026) |
| 10 | tro-cap-thoi-viec-mat-viec | severance-and-job-loss | BLLĐ Đ34, 36, 42, 43, 45–48 (nguyên văn); NĐ 145/2020 Đ8 (nguyên văn); ví dụ giả định |
| 11 | bhxh-tu-nguyen | voluntary-social-insurance | Luật BHXH 41/2024 Đ2.4, 31, 32, 36, 94–95, 98–99, 102–103 (nguyên văn, vcci.com.vn); NĐ 159/2025 Đ5 (50/40/30/20%, nguồn báo – Đang đối chiếu); NĐ 351/2025 (chuẩn nghèo nông thôn 2026: 1,5 tr; từ 2027: 2,2 tr) |
| 12 | bao-hiem-y-te | health-insurance | Luật BHYT 25/2008 sửa bởi 51/2024, Đ22 (nguyên văn, hethongphapluat.com); NĐ 188/2025; NĐ 161/2026 (lương cơ sở 2.530.000 từ 01/7/2026 → ngưỡng 379.500); ngoại trú trái tuyến 50% từ 01/7/2026 (Bộ Y tế); tỷ lệ 3%/1,5% Đang đối chiếu |
| 13 | hoa-chat | chemicals | Luật Hóa chất 69/2025 Đ14, 23, 25, 33, 36 (nguyên văn, hethongphapluat.com); 9 hình đồ GHS; SDS 16 mục (GHS); NĐ 26/2026 (biển báo, SDS tiếng Việt – Đang đối chiếu); TT 10/2020 |
| 14 | lao-dong-nu | women-workers | BLLĐ Đ37, 122, 136–142 (nguyên văn, bản JETRO); Đ139.1 sửa bởi Luật Dân số 113/2025 (Đang đối chiếu – nguồn báo); NĐ 145 Đ80; Luật BHXH Đ50, 51, 53, 58, 59; TT 10/2020 phụ lục (55 + 38 việc); NĐ 283/2026 Đ26 |
| 15 | phan-biet-doi-xu-quay-roi | discrimination-and-harassment | BLLĐ Đ3.8, 3.9, 8, 35.2, 118.2, 125; NĐ 145 Đ84–86; NĐ 283/2026 Đ7, 10, 11, 17; Luật 69/2020 Đ6.1đ. Có trích nguyên văn Đ3.8 (có cụm "chính kiến", "công đoàn") – đã báo Peter |
| 16 | truoc-khi-di-nuoc-ngoai | before-going-abroad | Luật 69/2020 Đ6, 7, 21, 23, 25, 44, 45, 56, 58, 59, 63, 65; NĐ 112/2021 Đ29, 30, PL II (ký quỹ: Đài Loan 12tr, Hàn 36tr, Nhật 0 – Đang đối chiếu sau NĐ 372/2025); NĐ 283 Đ49, 53; TT 09/2026; Luật 22/2026 (Sắp thay đổi) |
| 18 | quan-ly-tien-luong | managing-your-pay | BLLĐ Đ94.2, 95.3, 96.2, 97, 101, 102, 127.2 (nguyên văn, vcci); BLDS Đ471 (nguyên văn, caselaw); NĐ 399/2026 lương tối thiểu 2027 (Sắp thay đổi – Đang đối chiếu, nguồn lsvn); ví dụ ngân sách giả định |
| 19 | vay-qua-ung-dung-tin-dung-den | app-loans-and-loan-sharks | BLDS Đ468, 471 (nguyên văn); BLHS Đ201 (nguyên văn bản hợp nhất caselaw; Luật 86/2025 không sửa Đ201), Đ155, 170; Luật Đầu tư 143/2025 Đ6.1 cấm dịch vụ đòi nợ (Đang đối chiếu); Luật BVDLCN 91/2025 (Đang đối chiếu); NĐ 94/2025 + 382/2026 (P2P sandbox) |
| 17 | ve-nuoc | coming-home | Luật 69/2020 Đ6.2g, 23.3, 25.3, 46.8 (180 ngày), 60, 61, 67; NĐ 112 Đ31, 32; Luật BHXH Đ2.1g, 33.2 (22%, truy đóng); QĐ 34/2025/QĐ-TTg (mức hỗ trợ – Đang đối chiếu); NĐ 283 Đ49, 53 |

Bản tiếng Anh ghi rõ: trích dẫn luật là bản dịch không chính thức, văn bản tiếng Việt có giá trị.

## 5. Đối chiếu văn bản gốc (phiên 2, 18/11/2026)
- Nguồn: thư mục trên máy Peter `Desktop\DATA\00 Peter DATA\Danh mục văn bản pháp luật\File Full` (Peter cấp quyền đọc cho phiên 2).
- Đã gỡ nhãn "Đang đối chiếu" sau khi đối chiếu nguyên văn: BLLĐ Đ107 (40 giờ/tháng), Đ113.1 (14/16 ngày phép), Đ188, Đ190; Luật ATVSLĐ Đ6; Luật BHXH Đ40–41 (0,03%/ngày); Luật Việc làm Đ38 (12/24, 12/36 tháng, hạn nộp hồ sơ 3 tháng); TT 24/2022 Đ4; NĐ 293/2025; Luật TGPL Đ7; Luật 05/2026.
- Văn bản thay thế đã cập nhật vào bài:
  - TT 15/2016 + 02/2023 (BYT) → **TT 60/2025/TT-BYT**, hiệu lực 15/02/2026, vẫn 35 bệnh.
  - NĐ 191/2013 → **NĐ 105/2026/NĐ-CP** (tài chính công đoàn), hiệu lực 16/5/2026. Chỉ ảnh hưởng bài nháp.
  - Luật Dạy nghề 76/2006 → (Luật GDNN 74/2014 →) **Luật GDNN 124/2025/QH15**, hiệu lực 01/01/2026. Chưa dùng trong bài.
- Ghi chú khác với ý kiến của Peter: **Luật TGPL 11/2017/QH14 vẫn còn hiệu lực.** Luật 05/2026/QH16 chỉ là luật SỬA ĐỔI, hiệu lực 01/01/2027, không thay thế luật cũ. Bài vẫn dẫn 11/2017 kèm luật sửa đổi.
- CHƯA có văn bản thay thế trong thư mục (cần Peter gửi số hiệu):
  - TT 02/2024/TT-BLĐTBXH (mức trần giá dịch vụ môi giới XKLĐ). Bài 5 đã bỏ bảng "0 đồng", gắn hộp "đang đối chiếu văn bản thay thế".
  - TT 29/2021/TT-BLĐTBXH (phân loại điều kiện lao động; TT 24/2022 dẫn chiếu). Bài 2 gắn nhãn "Đang đối chiếu văn bản thay thế".
  - NĐ 12/2022/NĐ-CP (xử phạt lao động). Chưa dùng trong bài.
- Nhãn "Đang đối chiếu" còn lại: phí môi giới XKLĐ; điều kiện TT 24/2022; chế độ 育成就労 Nhật (khóa A1 100 giờ); số Hàn Quốc 1577-0071, 1350; Cục QLLĐNN thuộc Bộ Nội vụ (NĐ 25/2025 chưa có trong thư mục).

## 6. Nháp chờ Peter duyệt (chủ đề nhạy cảm chính trị)
- `content/nhap/dai-dien-nguoi-lao-dong.md`: Luật Công đoàn 50/2024 + 97/2025, đối thoại Đ63–64, đình công Chương XIV, công ước ILO (VN chưa phê chuẩn C87). Khi duyệt: cập nhật kinh phí công đoàn theo NĐ 105/2026; trích nguyên văn Chương XIII, XIV.
- Nhóm nhạy cảm cao (người nghiện, người bán dâm, lao động trong trại giam): không có trong mã nguồn công khai.

## 7. Danh bạ
- Đã đối chiếu: 113, 114, 115; 111 (trẻ em + mua bán người); TGPL nhà nước; Sở Nội vụ/UBND xã; Đài Loan 1955; Nhật OTIT 0120-250-168, 0570-013904, 0570-001706.
- Đang đối chiếu: Hàn Quốc 1577-0071, 1350.
- Chưa đăng: đường dây Công đoàn, tổng đài BHXH/VssID, TGPL từng tỉnh, Đại sứ quán/Ban QLLĐ ở nước ngoài, các NGO.

## 8. Quyết định của Peter
- 18/11/2026: tiếng Việt, đa quốc gia; chủ đề nhạy cảm chỉ dẫn luật VN + ILO, Peter duyệt từng bài; giai đoạn 1 = khung + 5–8 bài lõi; được đăng web, sửa DNS; mọi khoản tốn tiền phải báo trước.
- 18/11/2026 (phiên 2): web song ngữ Việt – Anh như các dự án khác; Claude thiết kế logo; Claude được chạy luôn sau khi dựng xong.
- 23/11/2026 (phiên 4): Peter yêu cầu có khung chương trình sẵn trên web; song ngữ Anh–Việt cho TẤT CẢ bài (bài mới luôn viết cả 2 bản).
- 23/11/2026 (phiên 5): Peter yêu cầu soạn và đăng nốt Phần 1, Phần 2 của khung chương trình → đã đăng bài 9–12.
- 23/11/2026 (phiên 6): Peter yêu cầu soạn và đăng Phần 3, 4, 5 → đã đăng bài 13–17; sửa hộp phí môi giới bài 5 (TT 09/2026).
- 23/11/2026 (phiên 7): Peter yêu cầu soạn và đăng Phần 6, 7 → chọn CHỈ Phần 6 phiên này (bài 18–19). **Phần 7 để phiên sau.** Peter quyết định: bài nhóm "Người bị lừa, bị mua bán, bị ép làm việc" được ĐĂNG LUÔN (không cần để nháp), chỉ dẫn Luật PCMBN 53/2024 + đường dây 111, không bình luận.
- 23/11/2026 (phiên 3): nối Pages với GitHub; Peter cấp quyền cho Claude mọi tác vụ của dự án (soạn và đăng). Vẫn giữ: chủ đề nhạy cảm chính trị phải để nháp chờ duyệt; khoản tốn tiền phải báo trước.

## 9. Việc tiếp theo (theo thứ tự)
000. (Phiên 7) **NĐ 399/2026/NĐ-CP** lương tối thiểu, hiệu lực 01/01/2027, THAY NĐ 293/2025: vùng I 5.700.000, II 5.080.000, III 4.450.000, IV 4.040.000; giờ 27.400/24.400/21.400/19.400 (nguồn lsvn.vn, vov.vn – chưa đối chiếu toàn văn). CẦN cập nhật bài 2 (tien-luong-lam-them-gio) và các bài dẫn NĐ 293 trước 01/01/2027. **Luật Đầu tư 143/2025/QH15** (hiệu lực 01/3/2026) đã thay Luật Đầu tư 2020.
00. (Phiên 6) Đã xác minh: **NĐ 283/2026/NĐ-CP** (15/7/2026, hiệu lực 10/9/2026) THAY NĐ 12/2022 (Đ66.4) – bản PDF có chữ ký số tại storage-vnportal.vnpt.vn (qnm-ubnd). Mức phạt trong NĐ là mức cá nhân, tổ chức x2 (Đ7), trừ Đ49 (doanh nghiệp đưa đi nước ngoài) là mức tổ chức. **TT 09/2026/TT-BNV** (hiệu lực 30/6/2026) thay phụ lục mức trần môi giới của TT 02/2024 – bài 5 đã sửa hộp, chưa có Phụ lục X. **Luật 22/2026/QH16** sửa Luật 69/2020, hiệu lực 01/3/2027 – cần toàn văn. **QĐ 34/2025/QĐ-TTg** thay QĐ 40/2021 (Quỹ HTVLNN). Lương cơ sở/mức tham chiếu 2.530.000 đ.
0a. (Phiên 6) Nguồn kỹ thuật mới: caselaw.vn đọc được toàn văn bằng curl (NĐ 145/2020, Luật 69/2020, NĐ 112/2021, TT 10/2020); vcci.com.vn/van-ban-phap-luat/41-2024-qh15 (Luật BHXH); hethongphapluat.com/luat-hoa-chat-2025.html; BLLĐ bản gốc song ngữ JETRO PDF.
0b. (Phiên 6) Còn Đang đối chiếu: Đ139.1 BLLĐ sau Luật Dân số (nguyên văn từ VBHN 18/VBHN-VPQH); chồng nghỉ 10 ngày khi sinh con thứ hai; NĐ 26/2026 (biển báo, SDS tiếng Việt); PL II NĐ 112 sau NĐ 372/2025; QĐ 34/2025 mức hỗ trợ và mức đóng 100.000 đ.
0. Lưu ý kỹ thuật: thuvienphapluat.vn chặn công cụ đọc web và trình duyệt tự động (Cloudflare). Lấy toàn văn ở vanban.vcci.com.vn hoặc nhờ Peter gửi file.
1. Peter gửi số hiệu văn bản thay thế TT 02/2024, TT 29/2021, NĐ 12/2022 → cập nhật bài 2 và bài 5. (Phiên 5 thấy tin: NĐ 283/2026/NĐ-CP xử phạt lĩnh vực lao động, BHXH áp dụng từ 10/9/2026 – có thể là văn bản thay NĐ 12/2022, CHƯA xác minh.)
1a. (Phiên 5) Việc cần đối chiếu nguyên văn để gỡ nhãn: NĐ 159/2025 Đ5 (tỷ lệ hỗ trợ BHXH tự nguyện); tỷ lệ đóng BHYT 3%/1,5% (Luật BHYT Đ13 + NĐ 188/2025); NQ 66.18/2026/NQ-CP phần cho thuê lại lao động (bài 8).
1b. (Phiên 5) Ngày 01/01/2027: cập nhật bài 11 – mức đóng BHXH tự nguyện thấp nhất 484.000 đ khi BHXH VN thông báo; số tiền hỗ trợ tăng theo. Theo dõi dự thảo nghị định tăng mức đóng BHYT (4,5% → 5,1%).
1c. (Phiên 5) Lưu ý: BLLĐ Đ139 (thai sản) đã được sửa bởi Luật Dân số 2025 từ 01/7/2026 (con thứ hai 7 tháng) – khi viết bài Lao động nữ (Phần 3) phải dùng bản sửa. Khi Quốc hội thông qua luật sửa BLLĐ (24/11, có thể thêm 27/7; dự kiến hiệu lực 01/3/2027): cập nhật bài 9.
2. Peter duyệt bài nháp dai-dien-nguoi-lao-dong.
3. Xác minh danh bạ còn thiếu.
4. Bài tiếp theo: Phần 1–6 ĐÃ XONG (phiên 7). Tiếp: Phần 7 – mỗi nhóm 1 bài lõi song ngữ (nông dân/ngư dân, lao động tự do, trẻ em đi làm, mua bán người – đăng luôn theo QĐ phiên 7, phụ nữ bị bạo hành, khuyết tật, sức khỏe tâm thần, trẻ khó khăn); khi đăng đổi status nhóm trong groups.yaml từ soon → active. Ngoài khung: lao động chưa thành niên (BLLĐ Chương XI – cần TT 09/2020/TT-BLĐTBXH).
4a. Nguồn kỹ thuật (phiên 5): shell của phiên đọc được vanban.vcci.com.vn và vcci.com.vn/van-ban-phap-luat/... bằng curl (lấy toàn văn, trích nguyên văn được); vbpl.vn, thuvienphapluat.vn, datafiles.chinhphu.vn bị chặn (403).
5. Định kỳ: theo dõi dự thảo sửa NĐ 145/2020 (Bộ Nội vụ, 7/2026) – khi ban hành, cập nhật bảng Phụ lục II bài 8; rà lương tối thiểu vào tháng 11–12; theo dõi luật sửa BLLĐ và Luật ATVSLĐ (Quốc hội khóa XVI); Nhật Bản 育成就労 từ 01/4/2027.
6. (Tùy chọn) Xóa Pages project cũ `trachnhiemxahoi`.
