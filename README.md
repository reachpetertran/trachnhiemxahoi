# trachnhiemxahoi.com

Mã nguồn website **Trách Nhiệm Xã Hội** – biết luật, biết nơi nhờ giúp, cho người lao động.

- Trang tĩnh (HTML/CSS), không đăng nhập, không cookie, không công cụ theo dõi, không tải mã hay phông chữ bên ngoài.
- Nội dung tự viết: CC BY-NC-SA 4.0. Văn bản pháp luật trích dẫn không thuộc đối tượng bảo hộ quyền tác giả.

## Cấu trúc
```
data/groups.yaml       Trục 1 – Tôi là ai (nhóm người đọc)
data/situations.yaml   Trục 2 – Tôi đang gặp chuyện gì
data/danhba.yaml       Trục 3 – Gọi ai (chỉ số đã đối chiếu nguồn)
content/bai/*.md       bài đã đăng (front matter: summary, sources, checked, upcoming)
content/nhap/          bài nháp nhạy cảm – KHÔNG đưa lên GitHub (.gitignore)
_build/build.py        sinh public/ ; --preview sinh preview/ có cả bài nháp
public/                Cloudflare Pages phục vụ thư mục này
```

## Build
```
pip install markdown pyyaml
python3 _build/build.py
```
Cloudflare Pages: build command để trống · output `public` · nhánh `main`.
