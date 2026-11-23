# TIẾN ĐỘ – trachnhiemxahoi.com

Đọc file này đầu mỗi phiên làm việc mới. Cập nhật cuối mỗi phiên.
Cập nhật gần nhất: 23/11/2026 (phiên 4).

## 1. Trạng thái hiện tại – v0.3, ĐANG CHẠY THẬT
- Trang chính: https://trachnhiemxahoi.com (đã chạy). www.trachnhiemxahoi.com: đã chạy. Bản dự phòng: https://trachnhiemxahoi-web.pages.dev
- Song ngữ: tiếng Việt ở `/`, tiếng Anh ở `/en/`. Mỗi trang có nút chuyển ngôn ngữ và thẻ hreflang.
- Logo: đã thiết kế, cùng họ huy hiệu với daynentang và kynanglamviec (mũ bảo hộ đặt trên sách mở; phía sau là nhà máy, ruộng bậc thang, máy bay).
- 8 bài đã đăng, có cả bản tiếng Việt và tiếng Anh. 1 bài nháp nhạy cảm chờ Peter duyệt.
- **Khung chương trình** (phiên 4): VI `/khung-chuong-trinh/`, EN `/en/curriculum/`, có trên menu và trang chủ. 6 phần, 19 bài (8 đã đăng, 11 "Sắp có") + Phần 7 các nhóm giai đoạn sau. Dữ liệu: `data/curriculum.yaml` (slug = bài đã đăng; t/t_en = bài dự kiến). Bài nháp nhạy cảm KHÔNG đưa vào khung.

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
| 8 | lao-dong-thue-lai | leased-workers | BLLĐ Đ52–58, 188; NĐ 145/2020 Đ21, 30, Phụ lục II (bảng 20 công việc nguyên văn, ĐÃ đối chiếu 23/11/2026 với toàn văn trên vanban.vcci.com.vn + bài TVPL Peter gửi); hộp Sắp thay đổi: dự thảo Bộ Nội vụ 7/2026 thay Phụ lục II (dòng 5 thêm "trưng bày và đóng gói sản phẩm") |

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
- 23/11/2026 (phiên 3): nối Pages với GitHub; Peter cấp quyền cho Claude mọi tác vụ của dự án (soạn và đăng). Vẫn giữ: chủ đề nhạy cảm chính trị phải để nháp chờ duyệt; khoản tốn tiền phải báo trước.

## 9. Việc tiếp theo (theo thứ tự)
0. Lưu ý kỹ thuật: thuvienphapluat.vn chặn công cụ đọc web và trình duyệt tự động (Cloudflare). Lấy toàn văn ở vanban.vcci.com.vn hoặc nhờ Peter gửi file.
1. Peter gửi số hiệu văn bản thay thế TT 02/2024, TT 29/2021, NĐ 12/2022 → cập nhật bài 2 và bài 5.
2. Peter duyệt bài nháp dai-dien-nguoi-lao-dong.
3. Xác minh danh bạ còn thiếu.
4. Bài tiếp theo: lao động chưa thành niên (BLLĐ Chương XI – cần TT 09/2020/TT-BLĐTBXH); BHXH tự nguyện (Luật BHXH 2024 – cần nghị định hướng dẫn mức hỗ trợ); quản lý tiền, tránh vay qua app; trợ cấp thôi việc, mất việc (BLLĐ Đ46, 47).
5. Định kỳ: theo dõi dự thảo sửa NĐ 145/2020 (Bộ Nội vụ, 7/2026) – khi ban hành, cập nhật bảng Phụ lục II bài 8; rà lương tối thiểu vào tháng 11–12; theo dõi luật sửa BLLĐ và Luật ATVSLĐ (Quốc hội khóa XVI); Nhật Bản 育成就労 từ 01/4/2027.
6. (Tùy chọn) Xóa Pages project cũ `trachnhiemxahoi`.
