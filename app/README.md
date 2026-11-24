# App Android – Trách Nhiệm Xã Hội

Bọc trang tĩnh `public/` thành app bằng Capacitor 8. Nội dung đóng gói sẵn, đọc được khi mất mạng.
Không tài khoản, không quảng cáo, không theo dõi; tiến độ, bài đã lưu, ghi chú chỉ nằm trên máy (localStorage `tnxh.v1`, tắt sao lưu đám mây).

```
app/build_www.py      public/ → app/www/ (đổi link, bỏ header web, chèn khung app, sinh app/index.js)
app/build_book.py     sách "Quyền Làm Việc" → www/sach/ (chỉ chạy khi có app/sach-data/)
app/shell/            app.css, app.js – thanh trên, 5 tab, cài đặt Aa, tiến độ, ghi chú, tìm kiếm, sách
app/capacitor.config.json   appId com.trachnhiemxahoi.app (KHÔNG đổi được sau lần tải lên Play đầu tiên)
app/android/          dự án Android (targetSdk 36, minSdk 24)
```

## Build
```
cd app && npm ci
python3 build_www.py && npx cap sync android
cd android && ./gradlew assembleDebug      # cần ANDROID_HOME / local.properties
```
Đẩy nhánh `app` → GitHub Actions build APK bản thử (artifact). **Bản Actions không có sách**:
dữ liệu sách (`app/sach-data/` = out/app/ của mã sách) không đưa lên kho công khai; APK có sách build tại máy.

## Chưa lên cửa hàng
Sách trong app: chờ hỏi NXB và Luật 17/2026/QH16 Đ10.2.g (hiệu lực 01/3/2027). Xem PROGRESS.md.
