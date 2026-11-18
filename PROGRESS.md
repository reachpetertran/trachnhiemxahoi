# Tiến độ dự án trachnhiemxahoi.com

Đọc file này đầu mỗi phiên. Cập nhật cuối mỗi phiên.

## Trạng thái (18/11/2026) – v0.1, giai đoạn 1
- Khung 3 trục: Tôi là ai / Tôi gặp chuyện gì / Gọi ai. Mẫu bài cố định: Tóm tắt 3 dòng → Luật nói gì → Bạn làm gì → Gọi ai → Đúng đến ngày → Sắp thay đổi → Nguồn.
- Nhóm đang có bài: công nhân & nghề nặng nhọc, độc hại, nguy hiểm; người Việt đi làm việc ở nước ngoài. Các nhóm khác hiện "Sắp có".
- 6 bài đã đăng: hop-dong-lao-dong, tien-luong-lam-them-gio, bao-hiem-xa-hoi, an-toan-ve-sinh-lao-dong, di-lam-viec-o-nuoc-ngoai, giu-bang-chung. Danh bạ /danh-ba/.
- 1 bài nháp nhạy cảm (công đoàn, đối thoại, đình công, công ước ILO) giữ ngoài repo – chờ Peter duyệt.

## Hạ tầng (18/11/2026)
- Cloudflare Pages project `trachnhiemxahoi` – **upload trực tiếp** (zip thư mục public/), chưa nối GitHub. Bản chạy: https://trachnhiemxahoi.pages.dev
- Lý do: Chrome đang đăng nhập GitHub tài khoản `thomastran1618`, không phải `reachpetertran` → chưa tạo repo. Khi Peter đăng nhập đúng tài khoản: tạo repo reachpetertran/trachnhiemxahoi, push, rồi nối Pages với Git (hoặc tiếp tục upload tay).
- Zone trachnhiemxahoi.com trên Cloudflare, gói Free ($0). Đã xóa 3 bản ghi đỗ của GoDaddy (2 A, 1 CNAME www); giữ `_domainconnect`, `_dmarc`.
- Nameserver GoDaddy đã đổi sang `christian.ns.cloudflare.com`, `clarissa.ns.cloudflare.com` (18/11/2026). Chờ zone active rồi thêm custom domain trachnhiemxahoi.com + www vào Pages.
- Đăng bản mới: `python3 _build/build.py` → zip public/ → Cloudflare Pages → Create deployment.

## Quyết định của Peter (18/11/2026)
- Phạm vi: tiếng Việt, đa quốc gia (gồm lao động Việt ở nước ngoài).
- Chủ đề nhạy cảm chính trị: chỉ dẫn luật VN + ILO, không bình luận; Peter duyệt từng bài trước khi đăng.
- Giai đoạn 1: khung + 5–8 bài lõi.
- Được phép đăng web, sửa DNS GoDaddy/Cloudflare. Mọi thao tác tốn tiền phải báo Peter.

## Nguyên tắc nội dung
- Nhãn "Đang đối chiếu" cho mục chỉ thấy ở nguồn thứ cấp hoặc chưa trích nguyên văn. Số điện thoại chưa xác minh thì không đăng.
- Nguồn: hồ sơ nghiên cứu 18/11/2026 + file findings đánh giá của Peter (trích nguyên văn điều luật).

## Việc tiếp theo
1. Đối chiếu văn bản gốc Peter tải từ thuvienphapluat (danh sách đã gửi 18/11/2026), gỡ các nhãn "Đang đối chiếu".
2. Theo dõi Quốc hội khóa XVI kỳ 2: luật sửa BLLĐ, Luật ATVSLĐ. Rà lương tối thiểu mỗi tháng 11–12.
3. Xác minh danh bạ còn thiếu: Công đoàn, BHXH/VssID, TGPL từng tỉnh, Đại sứ quán/Ban QLLĐ, NGO.
4. Bài tiếp: tai nạn lao động (bồi thường, trợ cấp), lao động thuê lại, lao động chưa thành niên, BHXH tự nguyện, quản lý tiền/vay app.
